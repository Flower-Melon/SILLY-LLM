import ast
from contextlib import redirect_stdout
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
        expected = {'FloorPlan6': 3, 'FloorPlan15': 6, 'FloorPlan21': 6,
                    'FloorPlan201': 5, 'FloorPlan209': 5, 'FloorPlan303': 6, 'FloorPlan414': 5}
        for path in (ROOT / 'data/final_test').glob('*.json'):
            tasks = json.loads(path.read_text(encoding='utf-8'))
            self.assertEqual(len(tasks), expected[path.stem])
            for task in tasks:
                self.assertEqual(set(task), {'task', 'robot list', 'object_states', 'trans', 'max_trans'})
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

    def test_planning_outputs_assemble_into_executable_python(self):
        decomposition = '```python\ndef task():\n    pass\n```'
        code = '```python\n# 中文注释\ndef task(robot):\n    pass\n\ntask(robots[0])\n```'
        replies = [completion(text) for _ in range(3)
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
                                    run_llm.main(['--floor-plan', '6'])
                self.assertEqual(post.call_count, 9)
                self.assertIn('Assign robot1.', post.call_args_list[2].kwargs['json']['messages'][1]['content'])
            folders = list((root / 'logs').iterdir())
            self.assertEqual(len(folders), 3)
            with patch.object(execute_plan, 'ROOT', root):
                for output in folders:
                    metadata = json.loads((output / 'task.json').read_text(encoding='utf-8'))
                    self.assertEqual(metadata['model'], 'deepseek-flash')
                    self.assertEqual(metadata['floor_plan'], 6)
                    self.assertNotIn('api_key', metadata)
                    executable = execute_plan.compile_aithor_exec_file(output.name)
                    source = Path(executable).read_text(encoding='utf-8')
                    ast.parse(source)
                    self.assertIn('# 中文注释', source)
                    self.assertNotIn('```', source)
                    self.assertTrue((output / 'allocated_plan.txt').is_file())
                    self.assertFalse((output / 'llm_config.json').exists())

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

    def test_coalition_navigation_waits_for_the_remaining_robot(self):
        path = ROOT / 'data/aithor_connect/aithor_connect.py'
        function = next(node for node in ast.parse(path.read_text(encoding='utf-8')).body
                        if isinstance(node, ast.FunctionDef) and node.name == 'GoToObject')
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
                     'reachable_positions': [(1, 0, 0), (1, 0, 1)], 're': re, 'np': np, 'math': math,
                     'time': SimpleNamespace(sleep=advance),
                     'closest_node': lambda *args: [(1, 0, 0), (1, 0, 1)],
                     'distance_pts': lambda a, b: math.hypot(a[0] - b[0], a[2] - b[2])}
        exec(compile(ast.Module(body=[function], type_ignores=[]), str(path), 'exec'), namespace)
        with redirect_stdout(io.StringIO()):
            namespace['GoToObject']([{'name': 'robot1'}, {'name': 'robot2'}], 'Apple')
        self.assertEqual(events[1].metadata['agent']['position']['x'], 1)
        self.assertTrue(all(action['agent_id'] == 1 for action in queue
                            if action['action'] == 'ObjectNavExpertAction'))

    def test_throw_example_accepts_coalition_and_receptacle(self):
        path = ROOT / 'data/aithor_connect/aithor_connect.py'
        function = next(node for node in ast.parse(path.read_text(encoding='utf-8')).body
                        if isinstance(node, ast.FunctionDef) and node.name == 'ThrowObject')
        events = [SimpleNamespace(metadata={'inventoryObjects': []}),
                  SimpleNamespace(metadata={'inventoryObjects': [{'objectId': 'Fork|1|0|0'}]})]
        controller = SimpleNamespace(last_event=SimpleNamespace(events=events,
                                      metadata={'objects': [{'objectId': 'Fork|1|0|0'}]}))
        queue = []
        navigate = Mock()
        namespace = {'c': controller, 'action_queue': queue, 're': re,
                     'GoToObject': navigate, 'time': SimpleNamespace(sleep=lambda _: None)}
        exec(compile(ast.Module(body=[function], type_ignores=[]), str(path), 'exec'), namespace)
        team = [{'name': 'robot1'}, {'name': 'robot2'}]
        namespace['ThrowObject'](team, 'Fork', 'GarbageCan')
        navigate.assert_called_once_with(team[1], 'GarbageCan')
        self.assertEqual(queue[0], {'action': 'ThrowObject', 'objectId': 'Fork|1|0|0', 'agent_id': 1})


if __name__ == '__main__':
    unittest.main()
