# Let pending actions and physics settle before evaluating the final state.
# Each Done is a full simulator step (rendered and captured as a video frame),
# so keep this count small; the wall-clock waits still give physics time to settle.
for _ in range(10):
    action_queue.extend([{'action': 'Done'}])
    time.sleep(0.25)
while action_queue and actions_thread.is_alive():
    time.sleep(0.1)
task_over = True
actions_thread.join()

objects = c.last_event.metadata['objects']
gcr = goal_completion_ratio(ground_truth, objects)
if not ground_truth:
    print('No ground-truth goals supplied; task completion cannot be evaluated.')
tc = int(bool(ground_truth) and gcr == 1.0)
exec_rate = success_exec / total_exec if total_exec else 0.0

# Resource use: 1.0 at the ground-truth number of sequential stages, falling
# linearly to 0 at the maximum the task allows, clamped to [0, 1]. A plan that
# uses fewer stages than the ground truth cannot score better than 1.0.
max_trans += 1
no_trans_gt += 1
if max_trans <= no_trans_gt:
    ru = float(no_trans <= no_trans_gt)
else:
    ru = max(0.0, min(1.0, (max_trans - no_trans) / (max_trans - no_trans_gt)))
sr = int(tc == 1 and ru == 1)
print(f'SR:{sr}, TC:{tc}, GCR:{gcr}, Exec:{exec_rate}, RU:{ru}')

try:
    generate_video()
finally:
    c.stop()
    cv2.destroyAllWindows()
