# This callback is associated with the go_to state node.

# parameters
x_position = gd.params['x_position']
y_position = gd.params['y_position']
yaw_angle = gd.params['yaw_angle']

# log
logger.info(f'Moving to (x, y, theta): ({x_position}, {y_position}, {yaw_angle})')

# prepare the input data
yaw_angle_rad = radians(yaw_angle)
yaw_angle_quaternion = transformations.quaternion_from_euler(0, 0, yaw_angle_rad)

# construct the message
message = MoveBaseGoal()
# set frame id and stamp
message.target_pose.header.frame_id = 'map'
message.target_pose.header.stamp = rospy.Time.now()
# set x and y positions
position = message.target_pose.pose.position
position.x = float(x_position)
position.y = float(y_position)
# set angle
quaternion = message.target_pose.pose.orientation
quaternion.x = yaw_angle_quaternion[0]
quaternion.y = yaw_angle_quaternion[1]
quaternion.z = yaw_angle_quaternion[2]
quaternion.w = yaw_angle_quaternion[3]

# publish the goal message through the out port 'goal' at 'action' action client
gd.oport['goal@action'].send(message)
