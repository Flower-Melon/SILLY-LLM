import ast
from contextlib import redirect_stderr, redirect_stdout
import copy
import io
import json
from pathlib import Path
import shutil
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import Mock, patch

import requests
import numpy as np
import math
import re

from scripts import execute_plan, run_llm


ROOT = Path(__file__).resolve().parents[1]


def completion(content, finish_reason='stop'):
    response = requests.Response()
    response.status_code = 200
    response._content = json.dumps({'choices': [{
        'finish_reason': finish_reason,
        'message': {'content': content, 'reasoning_content': 'Do not execute reasoning.'},
    }]}).encode('utf-8')
    return response


class ReproductionTests(unittest.TestCase):
    def test_all_36_tasks_are_complete_standard_json(self):
        count = 0
        expected = {'elemental': 6, 'simple': 8, 'compound': 14, 'complex': 8}
        for path in (ROOT / 'data/final_test').glob('*.json'):
            tasks = json.loads(path.read_text(encoding='utf-8'))
            self.assertEqual(len(tasks), expected[path.stem])
            for task in tasks:
                self.assertEqual(set(task), {'task', 'floor_plan', 'robot list', 'object_states',
                                             'trans', 'max_trans'})
                self.assertIn(task['floor_plan'], [6, 15, 21, 201, 209, 303, 414])
                self.assertIsInstance(task['trans'], int)
                self.assertIsInstance(task['max_trans'], int)
                self.assertTrue(all(1 <= robot <= 28 for robot in task['robot list']))
                for goal in task['object_states']:
                    self.assertEqual(set(goal), {'name', 'contains', 'state'})
                    self.assertEqual(goal['name'], goal['name'].strip().rstrip(','))
                    self.assertIn(goal['state'], [None, 'SLICED', 'BROKEN', 'OFF', 'ON',
                                                'HOT', 'COOKED', 'OPENED', 'CLOSED', 'PICKED'])
                count += 1
        self.assertEqual(count, 36)

    def test_fixed_key_and_direct_connection(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'key.txt'
            path.write_text(' test-key\n', encoding='utf-8-sig')
            with patch.object(run_llm, 'API_KEY_FILE', path):
                with run_llm.create_session() as session:
                    self.assertEqual(session.headers['Authorization'], 'Bearer test-key')
                    self.assertFalse(session.trust_env)

    def test_native_deepseek_request(self):
        session = Mock()
        session.post.return_value = completion(' OK ')
        messages = [{'role': 'user', 'content': 'hello'}]
        self.assertEqual(run_llm.ask_deepseek(session, messages), 'OK')
        session.post.assert_called_once_with(
            'https://api.deepseek.com/chat/completions',
            json={'model': 'deepseek-flash', 'messages': messages, 'max_tokens': 8192,
                  'temperature': 0, 'stream': False, 'thinking': {'type': 'disabled'}},
            timeout=(15, 180))

    def test_truncated_and_empty_plans_are_not_used(self):
        for answer, reason in [('partial', 'length'), ('', 'stop'), (None, 'stop')]:
            with self.subTest(answer=answer, reason=reason):
                session = Mock()
                session.post.return_value = completion(answer, reason)
                with self.assertRaises(RuntimeError):
                    run_llm.ask_deepseek(session, [{'role': 'user', 'content': 'hello'}])

    def test_task_robot_names_do_not_leak_between_tasks(self):
        original = copy.deepcopy(run_llm.robots)
        first = run_llm.task_robots([1, 2])
        second = run_llm.task_robots([2, 1])
        self.assertEqual([robot['name'] for robot in first], ['robot1', 'robot2'])
        self.assertEqual([robot['name'] for robot in second], ['robot1', 'robot2'])
        self.assertEqual(run_llm.robots, original)
        self.assertTrue(all('mass_capacity' in robot and 'mass' not in robot
                            for robot in run_llm.robots))

    def test_api_check_does_not_launch_unity(self):
        with requests.Session() as session:
            with patch.object(session, 'post', return_value=completion('OK')) as post:
                with patch.object(run_llm, 'create_session', return_value=session):
                    with patch.object(run_llm, 'get_ai2_thor_objects') as simulator:
                        with redirect_stdout(io.StringIO()) as output:
                            run_llm.main(['--check-api'])
        simulator.assert_not_called()
        self.assertEqual(post.call_count, 1)
        self.assertEqual(post.call_args.kwargs['json']['max_tokens'], 128)
        self.assertIn('API check succeeded: OK', output.getvalue())

    def test_level_argument_is_required(self):
        with redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit):
                run_llm.main([])

    def test_evaluation_parsing_and_averaging(self):
        scores = execute_plan.parse_evaluation('SR:1, TC:1, GCR:1.0, Exec:0.5, RU:0.0\n')
        self.assertEqual(scores, {'SR': 1.0, 'TC': 1.0, 'GCR': 1.0, 'Exec': 0.5, 'RU': 0.0})
        self.assertIsNone(execute_plan.parse_evaluation('no scores here'))
        failed = {metric: 0.0 for metric in execute_plan.METRICS}
        average = execute_plan.average_scores([scores, failed])
        self.assertEqual(average['Exec'], 0.25)
        self.assertEqual(average['SR'], 0.5)
        self.assertEqual(execute_plan.average_scores([])['GCR'], 0.0)

    def test_execute_plan_detects_level_task_folders(self):
        with tempfile.TemporaryDirectory() as folder:
            level = Path(folder)
            for name in ('b_plans', 'a_plans'):
                (level / name).mkdir()
                (level / name / 'task.json').write_text('{}', encoding='utf-8')
            (level / 'not_a_task').mkdir()
            found = execute_plan.find_task_folders(level)
            self.assertEqual([path.name for path in found], ['a_plans', 'b_plans'])

    def test_execute_plan_retries_a_timed_out_task(self):
        with tempfile.TemporaryDirectory() as folder:
            task_folder = Path(folder)
            counter = task_folder / 'attempts.txt'
            script = task_folder / 'child.py'
            script.write_text(
                'import time\n'
                'from pathlib import Path\n'
                f'folder = Path({str(task_folder)!r})\n'
                'count_file = folder / "attempts.txt"\n'
                'count = int(count_file.read_text()) + 1 if count_file.exists() else 1\n'
                'count_file.write_text(str(count))\n'
                'if count == 1:\n'
                '    time.sleep(60)\n'
                'else:\n'
                '    (folder / "evaluation.txt").write_text('
                '"SR:1, TC:1, GCR:1.0, Exec:1.0, RU:1.0\\n")\n',
                encoding='utf-8')
            with patch.object(execute_plan, 'compile_aithor_exec_file', return_value=str(script)):
                with redirect_stdout(io.StringIO()):
                    status, scores, attempts = execute_plan.execute_folder_task(
                        'dummy_folder', task_folder, timeout=2, retries=1)
            self.assertEqual(attempts, 2)
            self.assertEqual(status, 'ok')
            self.assertEqual(scores['SR'], 1.0)
            self.assertEqual(counter.read_text(), '2')

    def test_frame_recording_dedupes_frames_and_scores_first(self):
        import cv2
        import subprocess
        import sys
        with tempfile.TemporaryDirectory() as folder:
            run_dir = Path(folder)
            saved_stdout, saved_stderr = sys.stdout, sys.stderr
            try:
                namespace = {'__file__': str(run_dir / 'executable_plan.py'),
                             '__name__': '__main__', 'np': np, 'cv2': cv2}
                exec(execute_plan.FRAME_RECORDING, namespace)
                frame = np.zeros((64, 64, 3), dtype=np.uint8)
                changed = frame.copy()
                changed[0, 0] = (255, 255, 255)
                for index in range(5):
                    namespace['cv2'].imwrite(str(run_dir / 'agent_1' / ('img_%05d.png' % index)), frame)
                for index in range(5):
                    namespace['cv2'].imwrite(str(run_dir / 'agent_1' / ('img_%05d.png' % (100 + index))), changed)
                order = []
                writer = namespace['_video_writers']['agent_1']
                original_finish = writer.finish

                def spy_finish():
                    order.append((run_dir / 'evaluation.txt').is_file())
                    original_finish()

                writer.finish = spy_finish
                namespace.update(sr=1, tc=1, gcr=1.0, exec_rate=1.0, ru=1.0)
                namespace['generate_video']()
            finally:
                sys.stdout, sys.stderr = saved_stdout, saved_stderr
            self.assertEqual(order, [True])  # evaluation.txt exists before video finalize
            self.assertEqual((run_dir / 'evaluation.txt').read_text(encoding='utf-8').strip(),
                             'SR:1, TC:1, GCR:1.0, Exec:1.0, RU:1.0')
            probe = subprocess.run(
                ['ffprobe', '-v', 'error', '-select_streams', 'v:0',
                 '-show_entries', 'stream=nb_frames', '-of', 'default=nw=1:nk=1',
                 str(run_dir / 'video_agent_1.mp4')], capture_output=True, text=True)
            self.assertEqual(probe.stdout.strip(), '2')  # 5 identical + 5 identical -> 2 unique frames

    def test_planning_outputs_assemble_into_executable_python(self):
        decomposition = '```python\ndef task():\n    pass\n```'
        code = '```python\n# 中文注释\ndef task(robot):\n    pass\n\ntask(robots[0])\n```'
        replies = [completion(text) for _ in range(8)
                   for text in (decomposition, '# Assign robot1.', code)]
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            shutil.copytree(ROOT / 'data', root / 'data')
            with requests.Session() as session:
                with patch.object(session, 'post', side_effect=replies) as post:
                    with patch.object(run_llm, 'create_session', return_value=session):
                        with patch.object(run_llm, 'ROOT', root):
                            with patch.object(run_llm, 'get_ai2_thor_objects',
                                              return_value=[{'name': 'Tomato', 'mass': 0.1}]):
                                with redirect_stdout(io.StringIO()):
                                    run_llm.main(['--level', 'simple'])
                self.assertEqual(post.call_count, 24)
                self.assertIn('Assign robot1.', post.call_args_list[2].kwargs['json']['messages'][1]['content'])
            folders = list((root / 'logs' / 'simple').iterdir())
            self.assertEqual(len(folders), 8)
            floor_plans = set()
            with patch.object(execute_plan, 'ROOT', root):
                for output in folders:
                    metadata = json.loads((output / 'task.json').read_text(encoding='utf-8'))
                    self.assertEqual(metadata['model'], 'deepseek-flash')
                    self.assertEqual(metadata['level'], 'simple')
                    self.assertIn(metadata['floor_plan'], [6, 15, 21, 201, 209, 303, 414])
                    floor_plans.add(metadata['floor_plan'])
                    self.assertNotIn('api_key', metadata)
                    executable = execute_plan.compile_aithor_exec_file(f'simple/{output.name}')
                    source = Path(executable).read_text(encoding='utf-8')
                    ast.parse(source)
                    self.assertIn('# 中文注释', source)
                    self.assertNotIn('```', source)
                    self.assertTrue((output / 'allocated_plan.txt').is_file())
                    self.assertFalse((output / 'llm_config.json').exists())
            self.assertIn(6, floor_plans)

    def test_goal_counting_handles_duplicates_multiple_contents_and_broken(self):
        path = ROOT / 'data/aithor_connect/imports_aux_fn.py'
        tree = ast.parse(path.read_text(encoding='utf-8'))
        functions = [node for node in tree.body if isinstance(node, ast.FunctionDef)
                     and node.name in ('goal_satisfied', 'goal_completion_ratio')]
        namespace = {}
        exec(compile(ast.Module(body=functions, type_ignores=[]), str(path), 'exec'), namespace)
        ratio = namespace['goal_completion_ratio']
        objects = [{'name': 'TomatoSliced_1', 'isSliced': True},
                   {'name': 'TomatoSliced_2', 'isSliced': True},
                   {'name': 'Vase_1', 'isBroken': True},
                   {'name': 'Drawer_1', 'receptacleObjectIds': ['Watch|1', 'KeyChain|2']}]
        goals = [{'name': 'Tomato', 'state': 'SLICED', 'contains': []},
                 {'name': 'Vase', 'state': 'BROKEN', 'contains': []},
                 {'name': 'Drawer', 'state': None, 'contains': ['Watch', 'KeyChain']}]
        self.assertEqual(ratio(goals, objects), 1.0)
        objects[-1]['receptacleObjectIds'] = ['Watch|1']
        self.assertAlmostEqual(ratio(goals, objects), 2 / 3)
        self.assertEqual(ratio([], objects), 0.0)

    def test_execution_counter_accepts_empty_segments(self):
        self.assertEqual(execute_plan.append_trans_ctr('task(robots[0])\n\n'), 1)
        self.assertEqual(execute_plan.append_trans_ctr('\n\n'), 0)

    def test_execution_counter_counts_sequential_stages(self):
        # A single threaded chain is one stage like a single direct call.
        thread_chain = ('import threading\n'
                        'def go():\n    task(robots[0])\n'
                        't = threading.Thread(target=go)\n'
                        't.start()\n'
                        't.join()\n')
        self.assertEqual(execute_plan.append_trans_ctr(thread_chain), 1)
        # The same robot doing two steps is one stage (no utilization transition).
        self.assertEqual(execute_plan.append_trans_ctr('first(robots[0])\nsecond(robots[0])\n'), 1)
        # Two different robots taking over are two stages.
        self.assertEqual(execute_plan.append_trans_ctr('first(robots[0])\nsecond(robots[1])\n'), 2)
        # The same robot split over two sequential thread bursts is still one stage.
        same_robot_bursts = ('a = threading.Thread(target=f, args=([robots[0]],))\n'
                             'a.start()\n'
                             'a.join()\n'
                             'b = threading.Thread(target=g, args=([robots[0]],))\n'
                             'b.start()\n'
                             'b.join()\n')
        self.assertEqual(execute_plan.append_trans_ctr(same_robot_bursts), 1)
        # Two threads started before any join run concurrently: one stage.
        parallel = ('a = threading.Thread(target=f)\n'
                    'b = threading.Thread(target=g)\n'
                    'a.start()\n'
                    'b.start()\n'
                    'a.join()\n'
                    'b.join()\n')
        self.assertEqual(execute_plan.append_trans_ctr(parallel), 1)
        # A second burst after the joins is a new stage.
        two_bursts = ('a = threading.Thread(target=f)\n'
                      'a.start()\n'
                      'a.join()\n'
                      'b = threading.Thread(target=g)\n'
                      'b.start()\n'
                      'b.join()\n')
        self.assertEqual(execute_plan.append_trans_ctr(two_bursts), 2)

    def test_coalition_navigation_waits_for_the_remaining_robot(self):
        path = ROOT / 'data/aithor_connect/aithor_connect.py'
        functions = [node for node in ast.parse(path.read_text(encoding='utf-8')).body
                     if isinstance(node, ast.FunctionDef) and node.name in ('coerce_robots', 'GoToObject')]
        events = [SimpleNamespace(metadata={'agent': {'position': {'x': x, 'y': 0, 'z': z},
                                                      'rotation': {'y': 0}, 'cameraHorizon': 0}})
                  for x, z in [(1, 0), (3, 1)]]
        controller = SimpleNamespace(last_event=SimpleNamespace(events=events, metadata={'objects': [
            {'objectId': 'Apple|1|0|0', 'axisAlignedBoundingBox': {'center': {'x': 1, 'y': 0, 'z': 0}}},
        ]}))
        queue = []

        def advance(_):
            position = events[1].metadata['agent']['position']
            position['x'] = max(1, position['x'] - 1)

        namespace = {'c': controller, 'recp_id': None, 'action_queue': queue,
                     'sim_error_count': 0,
                     'reachable_positions': [(1, 0, 0), (1, 0, 1)], 're': re, 'np': np, 'math': math,
                     'time': SimpleNamespace(sleep=advance),
                     'closest_node': lambda *args: [(1, 0, 0), (1, 0, 1)],
                     'distance_pts': lambda a, b: math.hypot(a[0] - b[0], a[2] - b[2])}
        exec(compile(ast.Module(body=functions, type_ignores=[]), str(path), 'exec'), namespace)
        with redirect_stdout(io.StringIO()):
            namespace['GoToObject']([{'name': 'robot1'}, {'name': 'robot2'}], 'Apple')
        self.assertEqual(events[1].metadata['agent']['position']['x'], 1)
        self.assertTrue(all(action['agent_id'] == 1 for action in queue
                            if action['action'] == 'ObjectNavExpertAction'))

    def test_navigation_aborts_when_simulator_stops_responding(self):
        path = ROOT / 'data/aithor_connect/aithor_connect.py'
        functions = [node for node in ast.parse(path.read_text(encoding='utf-8')).body
                     if isinstance(node, ast.FunctionDef) and node.name in ('coerce_robots', 'GoToObject')]
        controller = SimpleNamespace(last_event=SimpleNamespace(events=[
            SimpleNamespace(metadata={'agent': {'position': {'x': 0, 'y': 0, 'z': 0},
                                                 'rotation': {'y': 0}, 'cameraHorizon': 0}})],
            metadata={'objects': [
                {'objectId': 'Apple|1|0|0',
                 'axisAlignedBoundingBox': {'center': {'x': 1, 'y': 0, 'z': 0}}}]}))
        queue = []
        namespace = {'c': controller, 'recp_id': None, 'action_queue': queue,
                     'sim_error_count': 10,
                     'reachable_positions': [(1, 0, 0)], 're': re, 'np': np, 'math': math,
                     'time': SimpleNamespace(sleep=lambda _: None),
                     'closest_node': lambda *args: [(1, 0, 0)],
                     'distance_pts': lambda a, b: math.hypot(a[0] - b[0], a[2] - b[2])}
        exec(compile(ast.Module(body=functions, type_ignores=[]), str(path), 'exec'), namespace)
        with redirect_stdout(io.StringIO()) as output:
            namespace['GoToObject']([{'name': 'robot1'}], 'Apple')
        self.assertEqual(queue, [])
        self.assertIn('abandoning navigation', output.getvalue())

    def test_navigation_teleports_the_robot_when_it_is_stuck(self):
        path = ROOT / 'data/aithor_connect/aithor_connect.py'
        functions = [node for node in ast.parse(path.read_text(encoding='utf-8')).body
                     if isinstance(node, ast.FunctionDef) and node.name in ('coerce_robots', 'GoToObject')]
        events = [SimpleNamespace(metadata={'agent': {'position': {'x': 0, 'y': 0, 'z': 0},
                                                      'rotation': {'y': 0}, 'cameraHorizon': 0}})]
        controller = SimpleNamespace(last_event=SimpleNamespace(events=events, metadata={'objects': [
            {'objectId': 'Apple|1|0|0',
             'axisAlignedBoundingBox': {'center': {'x': 1, 'y': 0, 'z': 0}}}]}))
        queue = []

        def advance(_):
            # Simulate the executor applying a queued teleport.
            teleports = [action for action in queue if action['action'] == 'Teleport']
            if teleports:
                position = teleports[-1]['position']
                events[0].metadata['agent']['position'].update(position)

        namespace = {'c': controller, 'recp_id': None, 'action_queue': queue,
                     'sim_error_count': 0, 'reachable_positions': [(1, 0, 0)],
                     're': re, 'np': np, 'math': math,
                     'time': SimpleNamespace(sleep=advance),
                     'closest_node': lambda *args: [(1, 0, 0)],
                     'distance_pts': lambda a, b: math.hypot(a[0] - b[0], a[2] - b[2])}
        exec(compile(ast.Module(body=functions, type_ignores=[]), str(path), 'exec'), namespace)
        with redirect_stdout(io.StringIO()) as output:
            namespace['GoToObject']([{'name': 'robot1'}], 'Apple')
        teleports = [action for action in queue if action['action'] == 'Teleport']
        self.assertEqual(len(teleports), 1)
        self.assertEqual(teleports[0]['agent_id'], 0)
        self.assertEqual((teleports[0]['position']['x'], teleports[0]['position']['z']), (1, 0))
        self.assertIn('teleporting', output.getvalue())

    def test_navigation_relocates_an_idle_blocker(self):
        path = ROOT / 'data/aithor_connect/aithor_connect.py'
        functions = [node for node in ast.parse(path.read_text(encoding='utf-8')).body
                     if isinstance(node, ast.FunctionDef) and node.name in ('coerce_robots', 'GoToObject')]
        events = [
            SimpleNamespace(metadata={'agent': {'position': {'x': 0, 'y': 0, 'z': 0},
                                                 'rotation': {'y': 0}, 'cameraHorizon': 0}}),
            SimpleNamespace(metadata={'agent': {'position': {'x': 0.5, 'y': 0, 'z': 0},
                                                 'rotation': {'y': 0}, 'cameraHorizon': 0}}),
        ]
        controller = SimpleNamespace(last_event=SimpleNamespace(events=events, metadata={'objects': [
            {'objectId': 'Apple|1|0|0',
             'axisAlignedBoundingBox': {'center': {'x': 1, 'y': 0, 'z': 0}}}]}))
        queue = []

        def advance(_):
            # Once the blocker is teleported away, pretend the acting robot
            # walks the remaining distance.
            if any(action['action'] == 'Teleport' and action['agent_id'] == 1 for action in queue):
                events[0].metadata['agent']['position'].update(x=1, z=0)

        namespace = {'c': controller, 'recp_id': None, 'action_queue': queue,
                     'sim_error_count': 0, 'reachable_positions': [(1, 0, 0), (10, 0, 0)],
                     're': re, 'np': np, 'math': math,
                     'time': SimpleNamespace(sleep=advance),
                     'closest_node': lambda *args: [(1, 0, 0)],
                     'distance_pts': lambda a, b: math.hypot(a[0] - b[0], a[2] - b[2])}
        exec(compile(ast.Module(body=functions, type_ignores=[]), str(path), 'exec'), namespace)
        with redirect_stdout(io.StringIO()) as output:
            namespace['GoToObject']([{'name': 'robot1'}], 'Apple')
        blocker = [action for action in queue
                   if action['action'] == 'Teleport' and action['agent_id'] == 1]
        acting = [action for action in queue
                  if action['action'] == 'Teleport' and action['agent_id'] == 0]
        self.assertEqual(len(blocker), 1)
        self.assertEqual(len(acting), 0)  # the acting robot was not teleported
        self.assertEqual(blocker[0]['position']['x'], 10)
        self.assertIn('teleporting it away', output.getvalue())

    def test_open_close_skip_when_already_in_target_state(self):
        path = ROOT / 'data/aithor_connect/aithor_connect.py'
        tree = ast.parse(path.read_text(encoding='utf-8'))
        functions = [node for node in tree.body if isinstance(node, ast.FunctionDef)
                     and node.name in ('coerce_robots', 'OpenObject', 'CloseObject')]

        def run(function_name, is_open):
            queue = []
            navigate = Mock()
            controller = SimpleNamespace(last_event=SimpleNamespace(metadata={'objects': [
                {'objectId': 'Blinds|1', 'isOpen': is_open}]}))
            namespace = {'c': controller, 'action_queue': queue, 're': re, 'recp_id': None,
                         'GoToObject': navigate, 'time': SimpleNamespace(sleep=lambda _: None)}
            exec(compile(ast.Module(body=functions, type_ignores=[]), str(path), 'exec'),
                 namespace)
            with redirect_stdout(io.StringIO()) as output:
                namespace[function_name]({'name': 'robot1'}, 'Blinds')
            return navigate, queue, output.getvalue()

        navigate, queue, output = run('CloseObject', False)
        self.assertFalse(navigate.called)
        self.assertEqual(queue, [])
        self.assertIn('already closed', output)

        navigate, queue, output = run('OpenObject', True)
        self.assertFalse(navigate.called)
        self.assertEqual(queue, [])
        self.assertIn('already open', output)

        navigate, queue, _ = run('CloseObject', True)
        navigate.assert_called_once_with({'name': 'robot1'}, 'Blinds|1')
        self.assertEqual(queue[0]['action'], 'CloseObject')

    def test_coerce_robots_accepts_name_strings(self):
        path = ROOT / 'data/aithor_connect/aithor_connect.py'
        functions = [node for node in ast.parse(path.read_text(encoding='utf-8')).body
                     if isinstance(node, ast.FunctionDef) and node.name == 'coerce_robots']
        first = {'name': 'robot1', 'skills': [], 'mass_capacity': 100}
        second = {'name': 'robot2', 'skills': [], 'mass_capacity': 100}
        namespace = {'robots': [first, second]}
        exec(compile(ast.Module(body=functions, type_ignores=[]), str(path), 'exec'), namespace)
        coerce = namespace['coerce_robots']
        self.assertIs(coerce('robot2'), second)
        self.assertEqual(coerce(['robot1', 'robot2']), [first, second])
        self.assertIs(coerce(first), first)
        self.assertEqual(coerce('robot99'), 'robot99')

    def test_pickup_accepts_a_robot_name_string(self):
        path = ROOT / 'data/aithor_connect/aithor_connect.py'
        tree = ast.parse(path.read_text(encoding='utf-8'))
        functions = [node for node in tree.body if isinstance(node, ast.FunctionDef)
                     and node.name in ('coerce_robots', 'PickupObject')]
        queue = []
        controller = SimpleNamespace(last_event=SimpleNamespace(metadata={'objects': [
            {'objectId': 'Apple|1', 'axisAlignedBoundingBox': {'center': {'x': 1, 'y': 1, 'z': 1}}}]}))
        namespace = {'c': controller, 'action_queue': queue, 're': re,
                     'robots': [{'name': 'robot1', 'skills': [], 'mass_capacity': 100}],
                     'time': SimpleNamespace(sleep=lambda _: None)}
        exec(compile(ast.Module(body=functions, type_ignores=[]), str(path), 'exec'), namespace)
        with redirect_stdout(io.StringIO()):
            namespace['PickupObject']('robot1', 'Apple')  # a name string, not the dict
        self.assertEqual(queue[0], {'action': 'PickupObject', 'objectId': 'Apple|1', 'agent_id': 0})

    def test_throw_example_accepts_coalition_and_receptacle(self):
        path = ROOT / 'data/aithor_connect/aithor_connect.py'
        functions = [node for node in ast.parse(path.read_text(encoding='utf-8')).body
                     if isinstance(node, ast.FunctionDef) and node.name in ('coerce_robots', 'ThrowObject')]
        events = [SimpleNamespace(metadata={'inventoryObjects': []}),
                  SimpleNamespace(metadata={'inventoryObjects': [{'objectId': 'Fork|1|0|0'}]})]
        controller = SimpleNamespace(last_event=SimpleNamespace(events=events,
                                      metadata={'objects': [{'objectId': 'Fork|1|0|0'}]}))
        queue = []
        navigate = Mock()
        namespace = {'c': controller, 'action_queue': queue, 're': re,
                     'GoToObject': navigate, 'time': SimpleNamespace(sleep=lambda _: None)}
        exec(compile(ast.Module(body=functions, type_ignores=[]), str(path), 'exec'), namespace)
        team = [{'name': 'robot1'}, {'name': 'robot2'}]
        namespace['ThrowObject'](team, 'Fork', 'GarbageCan')
        navigate.assert_called_once_with(team[1], 'GarbageCan')
        self.assertEqual(queue[0], {'action': 'ThrowObject', 'objectId': 'Fork|1|0|0', 'agent_id': 1})


if __name__ == '__main__':
    unittest.main()
