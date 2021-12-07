# This callback is associated with the tf_gen node.

# parameters
distance = gd.params['distance']
shift = gd.params['shift']
generated_tf_frame = gd.params['generated_tf_frame']

# get tag id with confirmation from the tag detections of the apriltag_ros
tag_frame = gd.shared.tag_frame

# make a new Pose message to be published as the generated TF
pub_msg = Pose()
# update the position
pub_msg.position.x = shift
pub_msg.position.y = 0.0
pub_msg.position.z = distance
# update the orientation
pub_msg.orientation.x = gd.shared.rotation[0]
pub_msg.orientation.y = gd.shared.rotation[1]
pub_msg.orientation.z = gd.shared.rotation[2]
pub_msg.orientation.w = gd.shared.rotation[3]

# publish the TF message
# the child is the name given as the generated_tf_frame parameter and the parent is the original TF published by apriltag_ros node
gd.oport['generated_tf'].send(pub_msg, child=generated_tf_frame, parent=tag_frame)
