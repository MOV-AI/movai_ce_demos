# This callback is associated with the align_to_cart node.

# receive the tf message and store the TF information of the goal of the align process
# the information is gathered only once and only if we have the initial odometry
if not gd.shared.receive_tf and gd.shared.init_odom is not None:  # and gd.shared.begin:
    # parameter
    camera = gd.params['camera']
    # set the step value to be 0.
    # the step represents the steps in the align procedure (0, 1, 2, 3)
    gd.shared.step = 0
    gd.shared.is_printed = False

    gd.shared.success = False
    gd.shared.wait = True
    gd.shared.executing = True

    # save the TF message to shared variable to be used in other callbacks
    gd.shared.tf = msg

    # retrieve the x, y and the yaw from the goal TF
    dist_x_tag = msg.position.x
    dist_y_tag = msg.position.y
    ori = msg.orientation
    euler = euler_from_quaternion([ori.x, ori.y, ori.z, ori.w])
    yaw_tag = euler[2]

    # based on the camera used and the position of the goal TF,
    # calculate the first rotation, traslation and the second rotation,
    # to be executed by the robot to reach the goal TF
    if camera == 'back':
        gd.shared.rot1 = -math.asin(
            dist_y_tag / math.sqrt(math.pow(dist_x_tag, 2) + math.pow(dist_y_tag, 2))
        )
        gd.shared.lin1 = math.sqrt(math.pow(dist_x_tag, 2) + math.pow(dist_y_tag, 2))
        gd.shared.rot2 = yaw_tag
    elif camera == 'front':
        gd.shared.rot1 = math.asin(
            dist_y_tag / math.sqrt(math.pow(dist_x_tag, 2) + math.pow(dist_y_tag, 2))
        )
        gd.shared.lin1 = math.sqrt(math.pow(dist_x_tag, 2) + math.pow(dist_y_tag, 2))
        gd.shared.rot2 = yaw_tag
    else:
        logger.error('Invalid camera parameter')

    # retrieve the x, y and the yaw from the odometry message
    gd.shared.odom_x0 = gd.shared.odom.position.x
    gd.shared.odom_y0 = gd.shared.odom.position.y
    ori_odom = gd.shared.odom.orientation
    euler_odom = euler_from_quaternion([ori_odom.x, ori_odom.y, ori_odom.z, ori_odom.w])
    gd.shared.odom_yaw0 = euler_odom[2]

    gd.shared.receive_tf = True
