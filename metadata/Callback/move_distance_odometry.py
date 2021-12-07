# This callback is associated with the move_distance state node.

# capture the first odometry message
if gd.shared.init_odom_position is None:
    gd.shared.init_odom_position = msg.pose.pose.position

# capture pose part of the odometry message to a shared variable
gd.shared.odom_position = msg.pose.pose.position