

total_exec = 0
success_exec = 0
sim_error_count = 0

# server_timeout caps how long one action may hang inside Unity before the
# bridge gives up (ai2thor defaults to 100s; a stuck action such as closing
# the FloorPlan303 blinds would otherwise stall the whole run for 100 seconds).
c = Controller( height=1000, width=1000, server_timeout=20)
c.reset("FloorPlan" + str(floor_no)) 
no_robot = len(robots)

# initialize n agents into the scene
multi_agent_event = c.step(dict(action='Initialize', agentMode="default", snapGrid=False, gridSize=0.5, rotateStepDegrees=20, visibilityDistance=100, fieldOfView=90, agentCount=no_robot))

# add a top view camera
event = c.step(action="GetMapViewCameraProperties")
event = c.step(action="AddThirdPartyCamera", **event.metadata["actionReturn"])

# get reachabel positions
reachable_positions_ = c.step(action="GetReachablePositions").metadata["actionReturn"]
reachable_positions = positions_tuple = [(p["x"], p["y"], p["z"]) for p in reachable_positions_]

# Randomize positions of the agents, keeping at least 1 m between robots so
# that they do not spawn blocking each other's collision volume.
spawn_positions = []
for i in range (no_robot):
    for _ in range(50):
        init_pos = random.choice(reachable_positions_)
        if all(distance_pts([init_pos['x'], init_pos['y'], init_pos['z']],
                            [p['x'], p['y'], p['z']]) >= 1.0 for p in spawn_positions):
            break
    spawn_positions.append(init_pos)
    c.step(dict(action="Teleport", position=init_pos, agentId=i))
    
objs = list([obj["objectId"] for obj in c.last_event.metadata["objects"]])
# print (objs)
    
# x = c.step(dict(action="RemoveFromScene", objectId='Lettuce|+01.11|+00.83|-01.43'))
#c.step({"action":"InitialRandomSpawn", "excludedReceptacles":["Microwave", "Pan", "Chair", "Plate", "Fridge", "Cabinet", "Drawer", "GarbageCan"]})
# c.step({"action":"InitialRandomSpawn", "excludedReceptacles":["Cabinet", "Drawer", "GarbageCan"]})

action_queue = []

task_over = False

recp_id = None

for i in range (no_robot):
    multi_agent_event = c.step(action="LookDown", degrees=35, agentId=i)
    # c.step(action="LookUp", degrees=30, 'agent_id':i)

def exec_actions():
    global total_exec, success_exec, sim_error_count
    # delete if current output already exist
    cur_path = os.path.dirname(__file__) + "/*/"
    for x in glob(cur_path, recursive = True):
        shutil.rmtree (x)
    
    # create new folders to save the images from the agents
    for i in range(no_robot):
        folder_name = "agent_" + str(i+1)
        folder_path = os.path.dirname(__file__) + "/" + folder_name
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
    
    # create folder to store the top view images
    folder_name = "top_view"
    folder_path = os.path.dirname(__file__) + "/" + folder_name
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    
    img_counter = 0
    
    while not task_over or action_queue:
        if len(action_queue) > 0:
            try:
                act = action_queue[0]
                if act['action'] == 'ObjectNavExpertAction':
                    multi_agent_event = c.step(dict(action=act['action'], position=act['position'], agentId=act['agent_id']))
                    next_action = multi_agent_event.metadata['actionReturn']

                    if next_action != None:
                        multi_agent_event = c.step(action=next_action, agentId=act['agent_id'], forceAction=True)
                
                elif act['action'] == 'MoveAhead':
                    multi_agent_event = c.step(action="MoveAhead", agentId=act['agent_id'])
                    
                elif act['action'] == 'MoveBack':
                    multi_agent_event = c.step(action="MoveBack", agentId=act['agent_id'])
                        
                elif act['action'] == 'Teleport':
                    multi_agent_event = c.step(dict(action="Teleport", position=act['position'], agentId=act['agent_id'], forceAction=True))

                elif act['action'] == 'RotateLeft':
                    multi_agent_event = c.step(action="RotateLeft", degrees=act['degrees'], agentId=act['agent_id'])
                    
                elif act['action'] == 'RotateRight':
                    multi_agent_event = c.step(action="RotateRight", degrees=act['degrees'], agentId=act['agent_id'])
                    
                elif act['action'] == 'PickupObject':
                    total_exec += 1
                    multi_agent_event = c.step(action="PickupObject", objectId=act['objectId'], agentId=act['agent_id'], forceAction=True)
                    if multi_agent_event.metadata['errorMessage'] != "":
                        print (multi_agent_event.metadata['errorMessage'])
                    else:
                        success_exec += 1
 
                elif act['action'] == 'PutObject':
                    total_exec += 1
                    multi_agent_event = c.step(action="PutObject", objectId=act['objectId'], agentId=act['agent_id'], forceAction=True)
                    if multi_agent_event.metadata['errorMessage'] != "":
                        print (multi_agent_event.metadata['errorMessage'])
                    else:
                        success_exec += 1
 
                elif act['action'] == 'ToggleObjectOn':
                    total_exec += 1
                    multi_agent_event = c.step(action="ToggleObjectOn", objectId=act['objectId'], agentId=act['agent_id'], forceAction=True)
                    if multi_agent_event.metadata['errorMessage'] != "":
                        print (multi_agent_event.metadata['errorMessage'])
                    else:
                        success_exec += 1
                
                elif act['action'] == 'ToggleObjectOff':
                    total_exec += 1
                    multi_agent_event = c.step(action="ToggleObjectOff", objectId=act['objectId'], agentId=act['agent_id'], forceAction=True)
                    if multi_agent_event.metadata['errorMessage'] != "":
                        print (multi_agent_event.metadata['errorMessage'])
                    else:
                        success_exec += 1
                    
                elif act['action'] == 'OpenObject':
                    total_exec += 1
                    multi_agent_event = c.step(action="OpenObject", objectId=act['objectId'], agentId=act['agent_id'], forceAction=True)
                    if multi_agent_event.metadata['errorMessage'] != "":
                        print (multi_agent_event.metadata['errorMessage'])
                    else:
                        success_exec += 1
 
                    
                elif act['action'] == 'CloseObject':
                    total_exec += 1
                    multi_agent_event = c.step(action="CloseObject", objectId=act['objectId'], agentId=act['agent_id'], forceAction=True)
                    if multi_agent_event.metadata['errorMessage'] != "":
                        print (multi_agent_event.metadata['errorMessage'])
                    else:
                        success_exec += 1
                        
                elif act['action'] == 'SliceObject':
                    total_exec += 1
                    multi_agent_event = c.step(action="SliceObject", objectId=act['objectId'], agentId=act['agent_id'], forceAction=True)
                    if multi_agent_event.metadata['errorMessage'] != "":
                        print (multi_agent_event.metadata['errorMessage'])
                    else:
                        success_exec += 1
                        
                elif act['action'] == 'ThrowObject':
                    total_exec += 1
                    multi_agent_event = c.step(action="ThrowObject", moveMagnitude=7, agentId=act['agent_id'], forceAction=True)
                    if multi_agent_event.metadata['errorMessage'] != "":
                        print (multi_agent_event.metadata['errorMessage'])
                    else:
                        success_exec += 1
                        
                elif act['action'] == 'BreakObject':
                    total_exec += 1
                    multi_agent_event = c.step(action="BreakObject", objectId=act['objectId'], agentId=act['agent_id'], forceAction=True)
                    if multi_agent_event.metadata['errorMessage'] != "":
                        print (multi_agent_event.metadata['errorMessage'])
                    else:
                        success_exec += 1

                elif act['action'] == 'CleanObject':
                    total_exec += 1
                    multi_agent_event = c.step(action='CleanObject', objectId=act['objectId'],
                                               agentId=act['agent_id'], forceAction=True)
                    if multi_agent_event.metadata['errorMessage']:
                        print(multi_agent_event.metadata['errorMessage'])
                    else:
                        success_exec += 1
 
                
                elif act['action'] == 'Done':
                    multi_agent_event = c.step(action="Done")
                    
                    
            except Exception as e:
                print (e)
                sim_error_count += 1
                
            if act['action'] != 'Done':
                for i,e in enumerate(multi_agent_event.events):
                    cv2.imshow('agent%s' % i, e.cv2img)
                    f_name = os.path.dirname(__file__) + "/agent_" + str(i+1) + "/img_" + str(img_counter).zfill(5) + ".png"
                    cv2.imwrite(f_name, e.cv2img)
                top_view_rgb = cv2.cvtColor(c.last_event.events[0].third_party_camera_frames[-1], cv2.COLOR_BGR2RGB)
                cv2.imshow('Top View', top_view_rgb)
                f_name = os.path.dirname(__file__) + "/top_view/img_" + str(img_counter).zfill(5) + ".png"
                cv2.imwrite(f_name, top_view_rgb)
                if cv2.waitKey(25) & 0xFF == ord('q'):
                    break

            img_counter += 1
            action_queue.pop(0)
        else:
            time.sleep(0.01)
       
actions_thread = threading.Thread(target=exec_actions)
actions_thread.start()

def coerce_robots(value):
    """Accept a robot dict, a robot name string like 'robot1', or a list of
    either; return the matching robot dict(s). Generated code occasionally
    passes robots[0]['name'] instead of the robot dict."""
    if isinstance(value, str):
        return next((r for r in robots if r['name'] == value), value)
    if isinstance(value, list):
        return [coerce_robots(item) for item in value]
    return value


def GoToObject(robots, dest_obj):
    global recp_id

    robots = coerce_robots(robots)
    
    # check if robots is a list
    
    if not isinstance(robots, list):
        # convert robot to a list
        robots = [robots]
    no_agents = len (robots)
    # robots distance to the goal 
    dist_goals = [10.0] * len(robots)
    prev_dist_goals = [10.0] * len(robots)
    count_since_update = [0] * len(robots)
    clost_node_location = [0] * len(robots)
    
    # list of objects in the scene and their centers
    objs = list([obj["objectId"] for obj in c.last_event.metadata["objects"]])
    objs_center = list([obj["axisAlignedBoundingBox"]["center"] for obj in c.last_event.metadata["objects"]])
    if "|" in dest_obj:
        # obj alredy given
        dest_obj_id = dest_obj
        pos_arr = dest_obj_id.split("|")
        dest_obj_center = {'x': float(pos_arr[1]), 'y': float(pos_arr[2]), 'z': float(pos_arr[3])}
    else:
        for idx, obj in enumerate(objs):
            
            match = re.match(dest_obj, obj)
            if match is not None:
                dest_obj_id = obj
                dest_obj_center = objs_center[idx]
                if dest_obj_center != {'x': 0.0, 'y': 0.0, 'z': 0.0}:
                    break # find the first instance
        
    print ("Going to ", dest_obj_id, dest_obj_center)
        
    dest_obj_pos = [dest_obj_center['x'], dest_obj_center['y'], dest_obj_center['z']] 
    
    # closest reachable position for each robot
    # all robots cannot reach the same spot 
    # differt close points needs to be found for each robot
    crp = closest_node(dest_obj_pos, reachable_positions, no_agents, clost_node_location)
    
    goal_thresh = 0.25
    others_seen = {}
    relocated_agents = set()
    # at least one robot is far away from the goal
    
    while any(d > goal_thresh for d in dist_goals):
        if sim_error_count >= 10:
            # The simulator stopped responding (e.g. an action hung until the
            # server timeout); navigation can never succeed, so give up instead
            # of spinning forever and let the run finish and report results.
            print ("Simulator stopped responding; abandoning navigation to", dest_obj)
            return
        for ia, robot in enumerate(robots):
            robot_name = robot['name']
            agent_id = int(robot_name[5:]) - 1
            
            # get the pose of robot        
            metadata = c.last_event.events[agent_id].metadata
            location = {
                "x": metadata["agent"]["position"]["x"],
                "y": metadata["agent"]["position"]["y"],
                "z": metadata["agent"]["position"]["z"],
                "rotation": metadata["agent"]["rotation"]["y"],
                "horizon": metadata["agent"]["cameraHorizon"]}

            # Track the other agents' positions so that long-stationary robots
            # (idle blockers) can be told apart from robots that are working.
            for other_id in range(len(c.last_event.events)):
                if other_id == agent_id:
                    continue
                other_pos = c.last_event.events[other_id].metadata["agent"]["position"]
                other_key = (round(other_pos["x"], 2), round(other_pos["z"], 2))
                last_key, still = others_seen.get(other_id, (None, 0))
                others_seen[other_id] = (other_key, still + 1 if other_key == last_key else 0)

            prev_dist_goals[ia] = dist_goals[ia] # store the previous distance to goal
            dist_goals[ia] = distance_pts([location['x'], location['y'], location['z']], crp[ia])
            if dist_goals[ia] <= goal_thresh:
                continue
            
            dist_del = abs(dist_goals[ia] - prev_dist_goals[ia])
            # print (ia, "Dist to Goal: ", dist_goals[ia], dist_del, clost_node_location[ia])
            if dist_del < 0.2:
                # robot did not move 
                count_since_update[ia] += 1
            else:
                # robot moving 
                count_since_update[ia] = 0
                
            if count_since_update[ia] < 8:
                action_queue.append({'action':'ObjectNavExpertAction', 'position':dict(x=crp[ia][0], y=crp[ia][1], z=crp[ia][2]), 'agent_id':agent_id})
            else:    
                #updating goal
                clost_node_location[ia] += 1
                count_since_update[ia] = 0
                crp = closest_node(dest_obj_pos, reachable_positions, no_agents, clost_node_location)
                if clost_node_location[ia] % 3 == 0:
                    # No progress after several candidate goals: the robot is
                    # most likely blocked by another robot's collision volume.
                    # First move long-stationary robots near the acting robot or
                    # its goal out of the way; only if there is no such blocker,
                    # teleport the acting robot to the candidate goal.
                    relocated = False
                    away_spots = []
                    for other_id, (key, still) in others_seen.items():
                        if still < 10 or other_id in relocated_agents:
                            continue
                        other_pos = c.last_event.events[other_id].metadata["agent"]["position"]
                        near_robot = distance_pts([other_pos["x"], other_pos["y"], other_pos["z"]],
                                                  [location['x'], location['y'], location['z']]) < 1.2
                        near_goal = distance_pts([other_pos["x"], other_pos["y"], other_pos["z"]],
                                                 dest_obj_pos) < 1.2
                        if not (near_robot or near_goal):
                            continue
                        candidates = sorted(reachable_positions,
                                            key=lambda p: -distance_pts(list(p), dest_obj_pos))
                        away = next((p for p in candidates
                                     if distance_pts(list(p), [location['x'], location['y'], location['z']]) > 2.0
                                     and all(distance_pts(list(p), list(s)) > 1.0 for s in away_spots)), None)
                        if away is None:
                            continue
                        print ("Blocked by robot" + str(other_id + 1) + "; teleporting it away from the goal")
                        action_queue.append({'action':'Teleport', 'position':dict(x=away[0], y=away[1], z=away[2]), 'agent_id':other_id})
                        away_spots.append(away)
                        relocated_agents.add(other_id)
                        others_seen[other_id] = (None, 0)
                        relocated = True
                    if relocated:
                        # Retry the closest goal position now that the way is clear.
                        clost_node_location[ia] = 0
                        crp = closest_node(dest_obj_pos, reachable_positions, no_agents, clost_node_location)
                    else:
                        print ("Navigation stalled; teleporting", robot_name, "to", crp[ia])
                        action_queue.append({'action':'Teleport', 'position':dict(x=crp[ia][0], y=crp[ia][1], z=crp[ia][2]), 'agent_id':agent_id})
    
            time.sleep(0.5)

    # align the robot once goal is reached
    # compute angle between robot heading and object
    metadata = c.last_event.events[agent_id].metadata
    robot_location = {
        "x": metadata["agent"]["position"]["x"],
        "y": metadata["agent"]["position"]["y"],
        "z": metadata["agent"]["position"]["z"],
        "rotation": metadata["agent"]["rotation"]["y"],
        "horizon": metadata["agent"]["cameraHorizon"]}
    
    robot_object_vec = [dest_obj_pos[0] -robot_location['x'], dest_obj_pos[2]-robot_location['z']]
    y_axis = [0, 1]
    unit_y = y_axis / np.linalg.norm(y_axis)
    unit_vector = robot_object_vec / np.linalg.norm(robot_object_vec)
    
    angle = math.atan2(np.linalg.det([unit_vector,unit_y]),np.dot(unit_vector,unit_y))
    angle = 360*angle/(2*np.pi)
    angle = (angle + 360) % 360
    rot_angle = angle - robot_location['rotation']
    
    if rot_angle > 0:
        action_queue.append({'action':'RotateRight', 'degrees':abs(rot_angle), 'agent_id':agent_id})
    else:
        action_queue.append({'action':'RotateLeft', 'degrees':abs(rot_angle), 'agent_id':agent_id})
        
    print ("Reached: ", dest_obj)
    if dest_obj == "Cabinet" or dest_obj == "Fridge" or dest_obj == "CounterTop":
        recp_id = dest_obj_id
    
def PickupObject(robots, pick_obj):
    robots = coerce_robots(robots)
    if not isinstance(robots, list):
        # convert robot to a list
        robots = [robots]
    no_agents = len (robots)
    # robots distance to the goal 
    for idx in range(no_agents):
        robot = robots[idx]
        print ("PIcking: ", pick_obj)
        robot_name = robot['name']
        agent_id = int(robot_name[5:]) - 1
        # list of objects in the scene and their centers
        objs = list([obj["objectId"] for obj in c.last_event.metadata["objects"]])
        objs_center = list([obj["axisAlignedBoundingBox"]["center"] for obj in c.last_event.metadata["objects"]])
        
        for idx, obj in enumerate(objs):
            match = re.match(pick_obj, obj)
            if match is not None:
                pick_obj_id = obj
                dest_obj_center = objs_center[idx]
                if dest_obj_center != {'x': 0.0, 'y': 0.0, 'z': 0.0}:
                    break # find the first instance
        # GoToObject(robot, pick_obj_id)
        # time.sleep(1)
        print ("Picking Up ", pick_obj_id, dest_obj_center)
        action_queue.append({'action':'PickupObject', 'objectId':pick_obj_id, 'agent_id':agent_id})
        time.sleep(1)
    
def PutObject(robot, put_obj, recp):
    robot = coerce_robots(robot)
    robot_name = robot['name']
    agent_id = int(robot_name[5:]) - 1
    objs = [obj["objectId"] for obj in c.last_event.metadata["objects"]]
    objs_center = list([obj["axisAlignedBoundingBox"]["center"] for obj in c.last_event.metadata["objects"]])
    objs_dists = list([obj["distance"] for obj in c.last_event.metadata["objects"]])

    metadata = c.last_event.events[agent_id].metadata
    robot_location = [metadata["agent"]["position"]["x"], metadata["agent"]["position"]["y"], metadata["agent"]["position"]["z"]]
    dist_to_recp = 9999999 # distance b/w robot and the recp obj
    for idx, obj in enumerate(objs):
        match = re.match(recp, obj)
        if match is not None:
            dist = objs_dists[idx]
            if dist < dist_to_recp:
                recp_obj_id = obj
                dest_obj_center = objs_center[idx]
                dist_to_recp = dist
                
    
    global recp_id         
    # if recp_id is not None:
    #     recp_obj_id = recp_id
    # GoToObject(robot, recp_obj_id)
    # time.sleep(1)
    action_queue.append({'action':'PutObject', 'objectId':recp_obj_id, 'agent_id':agent_id})
    time.sleep(1)
         
def SwitchOn(robot, sw_obj):
    robot = coerce_robots(robot)
    print ("Switching On: ", sw_obj)
    robot_name = robot['name']
    agent_id = int(robot_name[5:]) - 1
    objs = list(set([obj["objectId"] for obj in c.last_event.metadata["objects"]]))
    
    # turn on all stove burner
    if sw_obj == "StoveKnob":
        for obj in objs:
            match = re.match(sw_obj, obj)
            if match is not None:
                sw_obj_id = obj
                GoToObject(robot, sw_obj_id)
                # time.sleep(1)
                action_queue.append({'action':'ToggleObjectOn', 'objectId':sw_obj_id, 'agent_id':agent_id})
                time.sleep(0.1)
    
    # all objects apart from Stove Burner
    else:
        for obj in objs:
            match = re.match(sw_obj, obj)
            if match is not None:
                sw_obj_id = obj
                break # find the first instance
        GoToObject(robot, sw_obj_id)
        time.sleep(1)
        action_queue.append({'action':'ToggleObjectOn', 'objectId':sw_obj_id, 'agent_id':agent_id})
        time.sleep(1)            
        
def SwitchOff(robot, sw_obj):
    robot = coerce_robots(robot)
    print ("Switching Off: ", sw_obj)
    robot_name = robot['name']
    agent_id = int(robot_name[5:]) - 1
    objs = list(set([obj["objectId"] for obj in c.last_event.metadata["objects"]]))
    
    # turn on all stove burner
    if sw_obj == "StoveKnob":
        for obj in objs:
            match = re.match(sw_obj, obj)
            if match is not None:
                sw_obj_id = obj
                action_queue.append({'action':'ToggleObjectOff', 'objectId':sw_obj_id, 'agent_id':agent_id})
                time.sleep(0.1)
    
    # all objects apart from Stove Burner
    else:
        for obj in objs:
            match = re.match(sw_obj, obj)
            if match is not None:
                sw_obj_id = obj
                break # find the first instance
        GoToObject(robot, sw_obj_id)
        time.sleep(1)
        action_queue.append({'action':'ToggleObjectOff', 'objectId':sw_obj_id, 'agent_id':agent_id})
        time.sleep(1)      
    
def OpenObject(robot, sw_obj):
    robot = coerce_robots(robot)
    robot_name = robot['name']
    agent_id = int(robot_name[5:]) - 1
    objs = list(set([obj["objectId"] for obj in c.last_event.metadata["objects"]]))
    
    for obj in objs:
        match = re.match(sw_obj, obj)
        if match is not None:
            sw_obj_id = obj
            break # find the first instance
        
    global recp_id
    if recp_id is not None:
        sw_obj_id = recp_id

    current = next((obj for obj in c.last_event.metadata["objects"]
                    if obj["objectId"] == sw_obj_id), None)
    if current is not None and current.get("isOpen") is True:
        # Already open: replaying the animation is a pointless no-op, and on
        # some objects (e.g. the FloorPlan303 blinds) it hangs this AI2-THOR
        # build until the server timeout kills the whole simulator.
        print ("OpenObject skipped: ", sw_obj_id, "is already open")
        if recp_id is not None:
            recp_id = None
        return

    GoToObject(robot, sw_obj_id)
    time.sleep(1)
    action_queue.append({'action':'OpenObject', 'objectId':sw_obj_id, 'agent_id':agent_id})
    time.sleep(1)
    
def CloseObject(robot, sw_obj):
    robot = coerce_robots(robot)
    robot_name = robot['name']
    agent_id = int(robot_name[5:]) - 1
    objs = list(set([obj["objectId"] for obj in c.last_event.metadata["objects"]]))
    
    for obj in objs:
        match = re.match(sw_obj, obj)
        if match is not None:
            sw_obj_id = obj
            break # find the first instance
        
    global recp_id
    if recp_id is not None:
        sw_obj_id = recp_id

    current = next((obj for obj in c.last_event.metadata["objects"]
                    if obj["objectId"] == sw_obj_id), None)
    if current is not None and current.get("isOpen") is False:
        # Already closed: replaying the animation is a pointless no-op, and on
        # some objects (e.g. the FloorPlan303 blinds) it hangs this AI2-THOR
        # build until the server timeout kills the whole simulator.
        print ("CloseObject skipped: ", sw_obj_id, "is already closed")
        if recp_id is not None:
            recp_id = None
        return

    GoToObject(robot, sw_obj_id)
    time.sleep(1)

    action_queue.append({'action':'CloseObject', 'objectId':sw_obj_id, 'agent_id':agent_id})

    if recp_id is not None:
        recp_id = None
    time.sleep(1)
    
def BreakObject(robot, sw_obj):
    robot = coerce_robots(robot)
    robot_name = robot['name']
    agent_id = int(robot_name[5:]) - 1
    objs = list(set([obj["objectId"] for obj in c.last_event.metadata["objects"]]))
    
    for obj in objs:
        match = re.match(sw_obj, obj)
        if match is not None:
            sw_obj_id = obj
            break # find the first instance
    GoToObject(robot, sw_obj_id)
    time.sleep(1)
    action_queue.append({'action':'BreakObject', 'objectId':sw_obj_id, 'agent_id':agent_id}) 
    time.sleep(1)
    
def SliceObject(robot, sw_obj):
    robot = coerce_robots(robot)
    print ("Slicing: ", sw_obj)
    robot_name = robot['name']
    agent_id = int(robot_name[5:]) - 1
    objs = list(set([obj["objectId"] for obj in c.last_event.metadata["objects"]]))
    
    for obj in objs:
        match = re.match(sw_obj, obj)
        if match is not None:
            sw_obj_id = obj
            break # find the first instance
    GoToObject(robot, sw_obj_id)
    time.sleep(1)
    action_queue.append({'action':'SliceObject', 'objectId':sw_obj_id, 'agent_id':agent_id})      
    time.sleep(1)
    
def CleanObject(robot, sw_obj):
    robot = coerce_robots(robot)
    robot_name = robot['name']
    agent_id = int(robot_name[5:]) - 1
    objs = list(set([obj["objectId"] for obj in c.last_event.metadata["objects"]]))

    for obj in objs:
        match = re.match(sw_obj, obj)
        if match is not None:
            sw_obj_id = obj
            break # find the first instance
    GoToObject(robot, sw_obj_id)
    time.sleep(1)
    action_queue.append({'action':'CleanObject', 'objectId':sw_obj_id, 'agent_id':agent_id}) 
    time.sleep(1)
    
def ThrowObject(robot, sw_obj, recp=None):
    robot = coerce_robots(robot)
    if isinstance(robot, list):
        # A coalition's held object belongs to one simulator agent.
        holders = [member for member in robot
                   if any(re.match(sw_obj, obj['objectId'])
                          for obj in c.last_event.events[int(member['name'][5:]) - 1]
                          .metadata.get('inventoryObjects', []))]
        robot = holders[0] if holders else robot[0]
    if recp is not None:
        GoToObject(robot, recp)
    robot_name = robot['name']
    agent_id = int(robot_name[5:]) - 1
    objs = list(set([obj["objectId"] for obj in c.last_event.metadata["objects"]]))

    for obj in objs:
        match = re.match(sw_obj, obj)
        if match is not None:
            sw_obj_id = obj
            break # find the first instance
    
    action_queue.append({'action':'ThrowObject', 'objectId':sw_obj_id, 'agent_id':agent_id}) 
    time.sleep(1)
