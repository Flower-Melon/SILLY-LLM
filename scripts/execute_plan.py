"""Assemble and execute generated plans in AI2-THOR.

``--command`` accepts both layouts produced under ``logs/``:

* a difficulty level directory (for example ``simple``, written by
  ``scripts/run_llm.py``) — every task folder inside it is executed and the
  SR/TC/GCR/Exec/RU metrics are averaged and saved to
  ``logs/<level>/evaluation_summary_<stamp>.txt``;
* a single task folder (for example ``simple/Slice_the_tomato_plans_...`` or an
  older first-level folder) — only that task is executed.

An execution that exceeds ``--timeout`` seconds is killed together with its
AI2-THOR process and retried up to ``--retries`` times: robot spawn positions
are randomized per run, so a retry escapes the deadlock where an idle robot
blocks the acting robot's path.

Frames are no longer written to disk as ``img_*.png``. Every camera view is
streamed straight into one ffmpeg process and saved as ``video_<view>.mp4``;
consecutive identical frames are skipped, so the static settle phase costs no
video time. The full terminal output is mirrored to ``run_log.txt`` and the
final evaluation scores are written to ``evaluation.txt`` inside the generated
folder - before the video encoders are closed, so a timeout kill during
finalization cannot lose a completed evaluation.
"""

import argparse
import ast
from datetime import datetime
import json
import os
from pathlib import Path
import re
import signal
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]

# Injected right after the helper imports, so simulator startup and the whole
# run are mirrored to run_log.txt. The frame loop in
# data/aithor_connect/aithor_connect.py still calls cv2.imwrite for every
# captured frame; the replacement below pipes those frames into one ffmpeg
# process per view instead of writing img_*.png files. It also shadows
# generate_video() (called by data/aithor_connect/end_thread.py), so the old
# PNG-glob encoder is never used, and records the final evaluation to a file.
FRAME_RECORDING = r'''
# --- streaming frame recording (replaces the PNG pipeline) ----------------
import atexit as _record_atexit
import os as _record_os
import shutil as _record_shutil
import subprocess as _record_subprocess
import sys as _record_sys

_RUN_DIR = _record_os.path.dirname(_record_os.path.realpath(__file__))

# Terminal output is only shown once; mirror it into the run folder so the
# progress messages can be inspected after the run.
_record_log = open(_record_os.path.join(_RUN_DIR, 'run_log.txt'), 'w',
                   buffering=1, encoding='utf-8', errors='replace')


class _TeeStream(object):
    def __init__(self, stream, log_file):
        self._stream = stream
        self._log = log_file

    def write(self, data):
        self._stream.write(data)
        self._log.write(data)
        return len(data)

    def flush(self):
        self._stream.flush()
        self._log.flush()

    def isatty(self):
        try:
            return self._stream.isatty()
        except Exception:
            return False

    def fileno(self):
        return self._stream.fileno()


_record_sys.stdout = _TeeStream(_record_sys.stdout, _record_log)
_record_sys.stderr = _TeeStream(_record_sys.stderr, _record_log)
_record_atexit.register(_record_log.flush)


class _VideoWriter(object):
    """One ffmpeg process per camera view, fed through stdin."""

    FRAME_RATE = 5

    def __init__(self, view):
        self._view = view
        self._output = _record_os.path.join(_RUN_DIR, 'video_%s.mp4' % view)
        self._process = None
        self._size = None
        self._last_frame = None
        self._disabled = _record_shutil.which('ffmpeg') is None
        if self._disabled:
            print('ffmpeg is not installed; skipping video generation.')

    def write(self, frame):
        if self._disabled or frame is None:
            return
        if frame.ndim != 3 or frame.shape[2] != 3:
            print('Unexpected frame for %s: shape %r; frame skipped.'
                  % (self._view, frame.shape))
            return
        frame = np.ascontiguousarray(frame.astype(np.uint8, copy=False))
        height, width = frame.shape[:2]
        if self._process is not None and (width, height) != self._size:
            print('Frame size changed for %s (%dx%d -> %dx%d); frame skipped.'
                  % (self._view, self._size[0], self._size[1], width, height))
            return
        data = frame.tobytes()
        if data == self._last_frame:
            return  # identical to the previous frame (e.g. the settle phase)
        if self._process is None:
            self._size = (width, height)
            self._process = _record_subprocess.Popen(
                ['ffmpeg', '-y', '-loglevel', 'error',
                 '-f', 'rawvideo', '-pix_fmt', 'bgr24',
                 '-s', '%dx%d' % (width, height),
                 '-r', str(self.FRAME_RATE),
                 '-i', '-', '-pix_fmt', 'yuv420p', self._output],
                stdin=_record_subprocess.PIPE)
        self._last_frame = data
        self._process.stdin.write(data)

    def finish(self):
        process, self._process = self._process, None
        if process is None:
            return
        try:
            process.stdin.close()
            process.wait(timeout=60)
        except _record_subprocess.TimeoutExpired:
            process.kill()
            process.wait()
        print('Video written: %s' % self._output)


_video_writers = {}


def _record_frame(path, frame):
    """Replacement for cv2.imwrite: stream the frame into the view's video."""
    view = _record_os.path.basename(_record_os.path.dirname(path))
    if view not in _video_writers:
        _video_writers[view] = _VideoWriter(view)
    _video_writers[view].write(frame)
    return True


cv2.imwrite = _record_frame


def generate_video():
    """Replaces the PNG-frame encoder in imports_aux_fn.py.

    Writes the final scores to evaluation.txt first - a timeout kill during
    video finalization must not lose a completed evaluation - then closes the
    live encoders and removes the empty frame folders left by exec_actions().
    """
    scores = {name: globals().get(name)
              for name in ('sr', 'tc', 'gcr', 'exec_rate', 'ru')}
    if all(value is not None for value in scores.values()):
        line = 'SR:{sr}, TC:{tc}, GCR:{gcr}, Exec:{exec_rate}, RU:{ru}'.format(**scores)
        with open(_record_os.path.join(_RUN_DIR, 'evaluation.txt'), 'w',
                  encoding='utf-8') as handle:
            handle.write(line + '\n')
    for writer in _video_writers.values():
        writer.finish()
    for view in _video_writers:
        try:
            _record_os.rmdir(_record_os.path.join(_RUN_DIR, view))
        except OSError:
            pass
    _record_log.flush()
'''


def append_trans_ctr(code):
    """Count the sequential execution stages of a generated plan.

    A stage is a top-level call of a task chain, or one burst of thread starts
    whose threads run concurrently. Consecutive stages that use the same set of
    robots are merged: they contain no transition in robot utilization, which
    is what the ground-truth convention ``trans + 1`` counts.
    """
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return 0

    def event_key(call):
        indices = {sub.slice.value for sub in ast.walk(call)
                   if isinstance(sub, ast.Subscript) and isinstance(sub.value, ast.Name)
                   and sub.value.id == "robots"
                   and isinstance(sub.slice, ast.Constant) and isinstance(sub.slice.value, int)}
        if indices:
            return frozenset(indices)
        for keyword in call.keywords:
            if keyword.arg == "target" and isinstance(keyword.value, ast.Name):
                return frozenset([keyword.value.id])
        name = call.func
        name = name.attr if isinstance(name, ast.Attribute) else getattr(name, "id", None)
        return frozenset([name]) if name else frozenset()

    thread_keys = {}
    events = []
    burst = None
    for statement in tree.body:
        if isinstance(statement, ast.Assign) and isinstance(statement.value, ast.Call):
            call = statement.value
            func = call.func
            fname = func.attr if isinstance(func, ast.Attribute) else getattr(func, "id", "")
            if fname == "Thread":
                for target in statement.targets:
                    if isinstance(target, ast.Name):
                        thread_keys[target.id] = event_key(call)
        elif isinstance(statement, ast.Expr) and isinstance(statement.value, ast.Call):
            call = statement.value
            func = call.func
            attr = func.attr if isinstance(func, ast.Attribute) else None
            if attr == "start":
                if burst is None:
                    burst = set()
                if isinstance(func.value, ast.Name) and func.value.id in thread_keys:
                    burst |= thread_keys[func.value.id]
                elif isinstance(func.value, ast.Call):
                    burst |= event_key(func.value)
                elif isinstance(func.value, ast.Name):
                    burst.add(func.value.id)
            elif attr == "join":
                if burst is not None:
                    events.append(frozenset(burst))
                    burst = None
            elif isinstance(func, ast.Name) and func.id not in ("print", "sleep"):
                events.append(event_key(call))
    if burst is not None:
        events.append(frozenset(burst))

    stages = 0
    previous = None
    for event in events:
        if event and event == previous:
            continue
        stages += 1
        previous = event
    return stages


METRICS = ("SR", "TC", "GCR", "Exec", "RU")
EVALUATION_LINE = re.compile(
    r"SR:(?P<SR>-?[\d.]+),\s*TC:(?P<TC>-?[\d.]+),\s*GCR:(?P<GCR>-?[\d.]+),"
    r"\s*Exec:(?P<Exec>-?[\d.]+),\s*RU:(?P<RU>-?[\d.]+)")


def parse_evaluation(text):
    """Extract the SR/TC/GCR/Exec/RU line written by the recording block."""
    match = EVALUATION_LINE.search(text)
    if match is None:
        return None
    return {metric: float(value) for metric, value in match.groupdict().items()}


def read_evaluation(folder):
    path = folder / "evaluation.txt"
    if not path.is_file():
        return None
    return parse_evaluation(path.read_text(encoding="utf-8"))


def average_scores(rows):
    """Mean of SR/TC/GCR/Exec/RU over the rows; a failed task contributes zeros."""
    if not rows:
        return {metric: 0.0 for metric in METRICS}
    return {metric: sum(row[metric] for row in rows) / len(rows) for metric in METRICS}


def find_task_folders(folder):
    return sorted((child for child in folder.iterdir()
                   if child.is_dir() and (child / "task.json").is_file()),
                  key=lambda path: path.name)


def compile_aithor_exec_file(command):
    folder = ROOT / "logs" / command
    metadata = json.loads((folder / "task.json").read_text(encoding="utf-8"))
    templates = ROOT / "data/aithor_connect"
    code = (folder / "code_plan.py").read_text(encoding="utf-8")
    parts = [
        (templates / "imports_aux_fn.py").read_text(encoding="utf-8"),
        FRAME_RECORDING,
        f"robots = {metadata['robots']!r}\nfloor_no = {metadata['floor_plan']!r}\n"
        f"ground_truth = {metadata['ground_truth']!r}\n"
        f"no_trans_gt = {metadata['trans']!r}\nmax_trans = {metadata['max_trans']!r}\n",
        (templates / "aithor_connect.py").read_text(encoding="utf-8"),
        code,
        f"no_trans = {append_trans_ctr(code)}",
        (templates / "end_thread.py").read_text(encoding="utf-8"),
    ]
    executable = folder / "executable_plan.py"
    executable.write_text("\n\n".join(parts) + "\n", encoding="utf-8")
    return str(executable)


def run_executable(executable, timeout):
    """Run the assembled script; kill it and its AI2-THOR child on timeout.

    Returns (returncode, timed_out); returncode is None when the timeout fired.
    """
    process = subprocess.Popen([sys.executable, executable], start_new_session=True)
    try:
        return process.wait(timeout=timeout or None), False
    except KeyboardInterrupt:
        os.killpg(process.pid, signal.SIGTERM)
        process.wait()
        raise
    except subprocess.TimeoutExpired:
        os.killpg(process.pid, signal.SIGTERM)
        try:
            process.wait(timeout=30)
        except subprocess.TimeoutExpired:
            os.killpg(process.pid, signal.SIGKILL)
            process.wait()
        return None, True


def execute_folder_task(relative, folder, timeout, retries):
    """Execute one task folder, retrying after a timeout.

    Robot spawn positions are randomized per run, so a retry usually escapes the
    deadlock where an idle robot blocks the acting robot's path.
    Returns (status, scores, attempts); scores is None when the task failed.
    """
    evaluation_path = folder / "evaluation.txt"
    attempts = retries + 1
    for attempt in range(1, attempts + 1):
        if evaluation_path.is_file():
            evaluation_path.unlink()  # stale scores from an earlier run
        executable = compile_aithor_exec_file(relative)
        code, timed_out = run_executable(executable, timeout)
        scores = read_evaluation(folder)
        if timed_out:
            if scores is not None:  # evaluation finished, the process hung afterwards
                return "ok (timed out after evaluation)", scores, attempt
            if attempt < attempts:
                print(f"!! {relative} exceeded {timeout}s without finishing; "
                      f"retrying (attempt {attempt + 1}/{attempts})")
            continue
        if scores is None:
            return (f"failed (exit {code})" if code else "failed (no evaluation)"), None, attempt
        if code == 0:
            return "ok", scores, attempt
        return f"exit {code} (evaluated)", scores, attempt
    return f"timeout after {attempts} attempts", None, attempts


def run_single(command, timeout, retries):
    folder = ROOT / "logs" / command
    status, scores, attempt = execute_folder_task(command, folder, timeout, retries)
    print(f"{command}: {status}" + (f" (attempt {attempt})" if attempt > 1 else "")
          + ("" if scores is None else
             "  " + ", ".join(f"{metric}:{scores[metric]:g}" for metric in METRICS)))
    if scores is None:
        sys.exit(1)


def render_summary(command, rows, average):
    failures = sum(1 for row in rows if not row["status"].startswith("ok"))
    lines = [f"==================== logs/{command} summary ====================",
             f"{'Task folder':<44} {'Status':<24} " + " ".join(f"{m:>6}" for m in METRICS)]
    for row in rows:
        lines.append(f"{row['folder'][:44]:<44} {row['status'][:24]:<24} "
                     + " ".join(f"{row[metric]:>6.3f}" for metric in METRICS))
    lines.append(f"{'Average':<44} {'%d tasks, %d failed' % (len(rows), failures):<24} "
                 + " ".join(f"{average[metric]:>6.3f}" for metric in METRICS))
    lines.append("=" * 62)
    return "\n".join(lines)


def run_level(command, task_folders, timeout, retries):
    rows = []
    for index, folder in enumerate(task_folders, 1):
        relative = str(Path(command) / folder.name)
        print(f"\n=== [{index}/{len(task_folders)}] Executing {relative} ===")
        status, scores, attempt = execute_folder_task(relative, folder, timeout, retries)
        task_name = json.loads((folder / "task.json").read_text(encoding="utf-8"))["task"]
        row = {"task": task_name, "folder": folder.name, "status": status, "attempts": attempt}
        row.update({metric: (scores or {}).get(metric, 0.0) for metric in METRICS})
        rows.append(row)
        print(f"    {task_name}: {status}"
              + (f" (attempt {attempt})" if attempt > 1 else "")
              + ("" if scores is None else
                 "  " + ", ".join(f"{metric}:{row[metric]:g}" for metric in METRICS)))

    summary = render_summary(command, rows, average_scores(rows))
    print("\n" + summary)
    stamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S-%f")
    summary_path = ROOT / "logs" / command / f"evaluation_summary_{stamp}.txt"
    summary_path.write_text(summary + "\n", encoding="utf-8")
    print(f"Saved summary: {summary_path}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--command", required=True,
                        help="Difficulty level directory under logs/ (executes every task in it "
                             "and averages the metrics) or a single task folder under logs/.")
    parser.add_argument("--timeout", type=int, default=600,
                        help="Seconds a single task attempt may run before it is killed and "
                             "retried (default: 600; 0 disables). Note that genuinely slow tasks "
                             "may exceed this and be retried; raise it for long levels.")
    parser.add_argument("--retries", type=int, default=3,
                        help="Retries per task after a timeout (default: 3; spawn positions are "
                             "randomized per run, so a retry usually escapes a deadlock).")
    args = parser.parse_args()
    target = ROOT / "logs" / args.command
    if not target.is_dir():
        parser.error(f"logs/{args.command} is not a directory.")
    timeout = args.timeout or None
    if (target / "task.json").is_file():
        run_single(args.command, timeout, args.retries)
        return
    task_folders = find_task_folders(target)
    if not task_folders:
        parser.error(f"logs/{args.command} contains no task folders (no task.json found).")
    run_level(args.command, task_folders, timeout, args.retries)


if __name__ == "__main__":
    main()
