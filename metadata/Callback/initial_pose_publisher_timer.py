# This callback is associated with the initial_pose_publisher state node.

# parameters
position = gd.params['position']
orientation = gd.params['orientation']
frame_id = gd.params['frame_id']

# create message
message = PoseWithCovarianceStamped()

# populate the message with parameter data
message.header.frame_id = frame_id

message.pose.pose.position.x = position[0]
message.pose.pose.position.y = position[1]
message.pose.pose.position.z = position[2]

message.pose.pose.orientation.x = orientation[0]
message.pose.pose.orientation.y = orientation[1]
message.pose.pose.orientation.z = orientation[2]
message.pose.pose.orientation.w = orientation[3]

# send message
gd.oport['initialpose'].send(message)

# exit the node
gd.oport['end'].send()
