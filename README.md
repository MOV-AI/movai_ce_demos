# movai-ce-demos

This repository will provide you the following:
- A set of MOV.AI flows, nodes, callbacks and their corresponding ROS packages (package.xml)
- The repository will provide MOV.AI flows to be run in combination with the Ignition simulator and rviz will create a set of robot actions.
- The flows and the corresponding functionalities are described below.
- This package depends on ros packages with licenses such as 3-Clause BSD License which are being installed from APT. They are not modified and should bring their own licenses on installation.

## Release Status
| Package         | Noetic |
| :---:           | :---:  |
| movai_ce_demos      | [![Deploy - To Nexus On Github Release](https://github.com/MOV-AI/movai_ce_demos/actions/workflows/DeployOnGitRelease.yml/badge.svg)](https://github.com/MOV-AI/movai_ce_demos/actions/workflows/DeployOnGitRelease.yml)

## Deploy Status (branch → main)
| Package         | Noetic |
| :---:           | :---:  |
| movai_ce_demos      | [![Deploy - On branch main/release Push](https://github.com/MOV-AI/movai_ce_demos/actions/workflows/DeployOnMergeMain.yml/badge.svg)](https://github.com/MOV-AI/movai_ce_demos/actions/workflows/DeployOnMergeMain.yml)

## Continuous Integration Status

| Package         | Noetic |
| :---:           | :---:  |
| movai_ce_demos  | [![CI - On main/dev/release branches](https://github.com/MOV-AI/movai_ce_demos/actions/workflows/TestOnPR.yml/badge.svg)](https://github.com/MOV-AI/movai_ce_demos/actions/workflows/TestOnPR.yml)


## Flows and functionalities

| Robot         | Flow | Functionality |
| :---:           | :---:  | :---:  |
| Tugbot | [tugbot_simple_navigation](https://github.com/MOV-AI/movai_ce_demos/blob/main/metadata/Flow/tugbot_simple_navigation.json) | Robot repeats a pattern of 2m forward and 90° CW with odometry feedback |
| " | [tugbot_mapping](https://github.com/MOV-AI/movai_ce_demos/blob/main/metadata/Flow/tugbot_mapping.json) | Map a new world using gmapping and ekf_localization |
| " | [tugbot_autonomous_navigation](https://github.com/MOV-AI/movai_ce_demos/blob/main/metadata/Flow/tugbot_autonomous_navigation.json) | Localize the robot using amcl and autonomously navigate using move_base, global and local planners |
| " | [tugbot_pick_and_drop](https://github.com/MOV-AI/movai_ce_demos/blob/main/metadata/Flow/tugbot_pick_and_drop.json) | Cart pick and drop operation with help of autonomous navigation and apriltag_ros |
| Husky | [husky_simple_navigation](https://github.com/MOV-AI/movai_ce_demos/blob/main/metadata/Flow/husky_simple_navigation.json) | Robot repeats a pattern of 2m forward and 90° CW with odometry feedback |
| " | [husky_mapping](https://github.com/MOV-AI/movai_ce_demos/blob/main/metadata/Flow/husky_mapping.json) | Map a new world using gmapping and ekf_localization |
| " | [husky_autonomous_navigation](https://github.com/MOV-AI/movai_ce_demos/blob/main/metadata/Flow/husky_autonomous_navigation.json) | Localize the robot using amcl and autonomously navigate using move_base, global and local planners |
| Panda arm | [panda_hello_world](https://github.com/MOV-AI/movai_ce_demos/blob/main/metadata/Flow/panda_hello_world.json) | Panda arm rotates the joint1 counter-clockwise and then clockwise repeatedly |
| N/A | [visualize_map](https://github.com/MOV-AI/movai_ce_demos/blob/main/metadata/Flow/visualize_map.json) |  Visualize map in rviz by publishing in map topic |
