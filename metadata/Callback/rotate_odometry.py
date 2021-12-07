# This callback is associated with the rotate state node.

# capture the first odometry message
if gd.shared.init_odom_yaw is None:
    init_odom_orient = msg.pose.pose.orientation
    # convert the orientation from quaternion to euler
    init_odom_orient_euler = transformations.euler_from_quaternion([init_odom_orient.x, init_odom_orient.y, init_odom_orient.z, init_odom_orient.w])
    # get the yaw, add pi to limit the angle to positive values
    gd.shared.init_odom_yaw = init_odom_orient_euler[2]

# capture pose part of the odometry message to a shared variable
gd.shared.odom_orient = msg.pose.pose.orientation
