# This callback is associated with the align_to_cart node.

# save the initial odometry message if not set
if gd.shared.init_odom is None:
    gd.shared.init_odom = msg.pose.pose
# save the current odometry message
gd.shared.odom = msg.pose.pose