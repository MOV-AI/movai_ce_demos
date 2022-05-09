# This callback is associated with the align_to_cart node.
# This is the main loop for the align_to_cart cart node

# This function aligns the robot with the cart tag (back camera points to tag).
# The robot moves backwards. The manoeuvres consist of changes in position and
# orientation.The function receives inputs from odometry (current position and
# attitude measurements).
# The procedure consists in the following 4 steps:
# - Step 1: at P1 (initial position) and perform rotatation. Point back camera
#           to a location some distance in front of tag.
# - Step 2: translation from P1 to P2 (point in front of tag).
# - Step 3: rotatation at P2. Point to tag.
# - Step 4: translation from P2 to P3 (point in front of tag, closer to it than
#           P2).
# This callback is associated with the align_to_cart node.

# The function uses target angles and points determined from the transforms
# computed at odometry initialization.

# parameters
camera = gd.params['camera']

# initialization for linear and angular velocity
vel_lin = 0.0
vel_ang = 0.0

# proced the align process if,
# we have recieved the goal TF information as well as the initial odom
if gd.shared.receive_tf == True and gd.shared.init_odom is not None:
    # set the execution status if not set
    # a true value means that the align is currently on going
    if not gd.shared.executing:
        gd.shared.executing = True
    # if the tf_gen has been called, then send command to stop it,
    # to save resource and set the staus to False
    if gd.shared.source_status:
        gd.oport['enable_tf_generator'].send(False)
        gd.shared.source_status = False

    # instanciate the velocity messge to be published
    vel_msg = Twist()

    # set the direction of robot motion based on,
    # the camera selected. backwards is -1 and forwardsis +1
    if camera == 'back':
        direction = -1
    elif camera == 'front':
        direction = +1
    else:
        logger.error(
            'Please set the correct value for the camera paramter (back/front)'
        )

    # Rotation: point to tag
    # Location P1: starting point
    if gd.shared.step == 0:
        # log once
        if not gd.shared.is_printed:
            logger.debug('Aligning to cart tag corrected')
            gd.shared.is_printed = True

        # convert attitude from quaternion to Euler angles (pitch, yaw, roll)
        ori = gd.shared.odom.orientation
        euler_odom = tf.transformations.euler_from_quaternion(
            [ori.x, ori.y, ori.z, ori.w]
        )
        # get current yaw angle [rad]
        odom_y = euler_odom[2]

        # get smallest angle difference to alignment angle
        # (in one of the intervals [0,2pi] or [0,2pi])
        if gd.shared.odom_yaw0 < 0 and odom_y > 2:
            odom_y = odom_y - 2 * math.pi
        if gd.shared.odom_yaw0 > 0 and odom_y < -2:
            odom_y = odom_y + 2 * math.pi

        # Orientation misalignment: determine rotation angle [rad].
        # Get difference between current yaw and final yaw (tag).
        # gd.shared.rot1: rotation target at P2 [rad]
        # gd.shared.odom_yaw0: initial yaw angle of the robot at P1 [rad]
        prsc1 = gd.shared.rot1 - (odom_y - gd.shared.odom_yaw0)

        # rotation => linear velocity is 0
        vel_lin = 0.0
        # set angular velocity for rotation
        if abs(prsc1) > gd.shared.min_rot:
            vel_ang = gd.shared.rot1_w * prsc1
        else:
            vel_ang = 0.0
            # move on to next step
            gd.shared.step = 1
            gd.shared.is_printed = False

    # Move to point in front of tag
    elif gd.shared.step == 1:
        if gd.shared.is_printed:
            logger.debug('Linear movement to cart tag corrected')
            gd.shared.is_printed = True

        # get current robot position
        odom_x = gd.shared.odom.position.x
        odom_y = gd.shared.odom.position.y

        # Get robot distance to P2.
        # gd.shared.lin1: distance between points P1 and P2 [m]
        # gd.shared.odom_x0, gd.shared.odom_y0: robot position at initialization (P1) [m]
        prsc2 = gd.shared.lin1 - math.sqrt(
            pow(odom_x - gd.shared.odom_x0, 2) + pow(odom_y - gd.shared.odom_y0, 2)
        )

        # translation => angular velocity is 0
        vel_ang = 0.0
        # set linear velocity [m/s]
        if abs(prsc2) > gd.shared.min_lin1:
            vel_lin = gd.shared.move_vel1 * prsc2 * direction
        else:
            vel_lin = 0.0
            # go to next step
            gd.shared.step = 2
            gd.shared.is_printed = False

    # Rotate to align with tag
    elif gd.shared.step == 2:
        if not gd.shared.is_printed:
            logger.debug('Rotate to match cart')
            gd.shared.is_printed = True

        # get current robot attitude
        ori = gd.shared.odom.orientation
        euler_odom = tf.transformations.euler_from_quaternion(
            [ori.x, ori.y, ori.z, ori.w]
        )
        odom_y = euler_odom[2]

        if gd.shared.odom_yaw0 < 0 and odom_y > 2:
            odom_y = odom_y - 2 * math.pi
        if gd.shared.odom_yaw0 > 0 and odom_y < -2:
            odom_y = odom_y + 2 * math.pi

        # Get rotation angle to perform in Step 3.
        # nav.rot2: tag yaw angle [rad]
        # nav.odom_yaw0: initial yaw angle at P1 [rad]
        prsc3 = gd.shared.rot2 - (odom_y - gd.shared.odom_yaw0)

        # rotation => linear velocity is 0
        vel_lin = 0.0
        # set angular velocity [rad/s]
        if abs(prsc3) > gd.shared.min_rot:
            vel_ang = gd.shared.rot2_w * prsc3
        else:
            vel_ang = 0.0
            # go to next step
            gd.shared.step = 3
            gd.shared.is_printed = False
            # Re-initialization for next step: reference for location is now P2
            gd.shared.odom_x0 = gd.shared.odom.position.x
            gd.shared.odom_y0 = gd.shared.odom.position.y

    # Move a bit in a straight line towards final point in front of tag.
    # Final distance to tag (P3) is received as parameter.
    elif gd.shared.step == 3:
        if not gd.shared.is_printed:
            logger.debug('Final movement to attach')
            # is this to be replaced by response?
            # gd.oport['back_cam'].send(False)
            gd.shared.is_printed = True

        ori = gd.shared.odom.orientation
        euler_odom = tf.transformations.euler_from_quaternion(
            [ori.x, ori.y, ori.z, ori.w]
        )
        gd.shared.odom_yaw0 = euler_odom[2]

        # get current position of the robot
        odom_x = gd.shared.odom.position.x
        odom_y = gd.shared.odom.position.y

        # Get current distance from P2 [m].
        # odom0 is now odometry in P2.
        current_dist = math.sqrt(
            pow(odom_x - gd.shared.odom_x0, 2) + pow(odom_y - gd.shared.odom_y0, 2)
        )

        # translation => angular velocity is 0
        vel_ang = 0.0
        # set linear velocity [m/s]
        if (
            abs(current_dist) < gd.shared.move_back_dist
            and not gd.shared.inductive_switch
        ):
            vel_lin = gd.shared.final_speed * direction
        else:
            vel_lin = 0.0
            # finalize actions
            gd.shared.is_printed = False
            gd.shared.wait = False
            gd.shared.success = True
            # flag ending
            gd.shared.begin = False
            gd.shared.executing = False
            gd.iport['timeout_timer'].unregister()

    # set output values for linear velocity and angular velocity
    # linear motion along x axis (forward)
    vel_msg.linear.x = vel_lin
    if abs(vel_msg.linear.x) > gd.shared.max_vel_lin:
        vel_msg.linear.x = gd.shared.max_vel_lin * direction
    # angular velocity for rotation along the z axis
    vel_msg.angular.z = vel_ang
    if abs(vel_msg.angular.z) > gd.shared.max_vel_ang:
        vel_msg.angular.z = gd.shared.max_vel_ang * sign(vel_msg.angular.z)

    # send output message
    gd.oport['cmd_vel_pub'].send(vel_msg)

    # transition to the success port if align is success
    if gd.shared.success == True:
        gd.oport['success'].send()
