# Let pending actions and physics settle before evaluating the final state.
for _ in range(25):
    action_queue.extend([{'action': 'Done'}] * 3)
    time.sleep(0.1)
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

# Retain the original resource-use formula and sequential-block estimate.
max_trans += 1
no_trans_gt += 1
if max_trans == no_trans_gt:
    ru = float(no_trans == no_trans_gt)
else:
    ru = (max_trans - no_trans) / (max_trans - no_trans_gt)
sr = int(tc == 1 and ru == 1)
print(f'SR:{sr}, TC:{tc}, GCR:{gcr}, Exec:{exec_rate}, RU:{ru}')

try:
    generate_video()
finally:
    c.stop()
    cv2.destroyAllWindows()
