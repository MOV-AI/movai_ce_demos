# This callback is associated with the rotate state node.

# parameters
target_deg = gd.params['angle']
max_vel = abs(gd.params['max_vel'])
rotation_error = abs(gd.params['rotation_error'])
kp = abs(gd.params['kp'])

# rotate error to radian
rotation_error_rad = math.radians(rotation_error)

# get odometry messages
odom_orient = gd.shared.odom_orient
init_odom_yaw = gd.shared.init_odom_yaw

# get current angle rotated by the robot (rad)
already_rotated = gd.shared.already_rotated

# if there is no odometry feedback, skip current iteration
if odom_orient is not None:

    # instanciate twist message
    vel_msg = Twist()

    # get angle to perform rotation or current error [rad]
    target_rad = math.radians(target_deg)
    current_error = target_rad - gd.shared.already_rotated

    # publish velocity if the error is more than the parameter value
    # stop if the robot reaches the acceptable error tolerance or if the error value overshoots, due to manual intervention
    overshoot_or_man_control = (
        True
        if current_error / abs(current_error) != target_rad / abs(target_rad)
        else False
    )
    if abs(current_error) > rotation_error_rad and not overshoot_or_man_control:
        # calculate angular velocity to be published [rad/s]
        vel_ang = abs(kp * current_error)

        # upper limit to angular velocity
        if vel_ang > max_vel:
            vel_ang = max_vel

        # move counter clockwise (positive velocity) when the angle to be covered is positive and vise versa
        if target_deg > 0:
            vel_msg.angular.z = vel_ang
        else:
            vel_msg.angular.z = -vel_ang

        # publish command velocity
        gd.oport['cmd_vel'].send(vel_msg)

        # calculate and update the current angle to goal
        # convert the orientation from quaternion to euler
        odom_orient_euler = transformations.euler_from_quaternion(
            [odom_orient.x, odom_orient.y, odom_orient.z, odom_orient.w]
        )
        # get the yaw, add pi to limit the angle to positive values
        odom_yaw = odom_orient_euler[2]

        # get angle already rotated by the robot
        already_rotated = odom_yaw - init_odom_yaw

        # keep angle (difference to target) within values [0,2pi] if target angle is > 0
        if target_deg > 0 and already_rotated < -rotation_error_rad:
            already_rotated += 2 * math.pi
        # keep angle between [-2pi,0] if target < 0
        if target_deg < 0 and already_rotated > rotation_error_rad:
            already_rotated -= 2 * math.pi

        # update shared variable
        gd.shared.already_rotated = already_rotated
    else:
        # log
        logger.info('Goal reached')

        # publish zero command velocity to stop the robot
        vel_msg.angular.z = 0
        gd.oport['cmd_vel'].send(vel_msg)

        # transition throught exit port
        gd.oport['exit'].send()
