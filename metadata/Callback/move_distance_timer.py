# This callback is associated with the move_distance state node.

# parameters
distance = gd.params['distance']
max_vel = abs(gd.params['max_vel'])
distance_error = abs(gd.params['distance_error'])
kp = abs(gd.params['kp'])

# get odometry messages
odom_position = gd.shared.odom_position
init_odom_position = gd.shared.init_odom_position

# get current distance
current_distance = gd.shared.current_distance

# if there is no odometry feedback, skip current iteration
if odom_position is not None:

    # instanciate twist message
    vel_msg = Twist()

    # if robot has not translated the desired distance keep publishing command velocity
    # else publish zero command velocity and trigger transition through the exit port
    current_error = abs(distance) - current_distance
    if current_error > distance_error and current_error > 0:
        # calculate a velocity in linear proportion to the distance to be translated
        vel = abs(kp * current_error)

        # add upper limit to the velocity
        if vel > max_vel:
            vel = max_vel

        # move forward (positive velocity) when the distance to be covered is positive and vise versa  
        if distance > 0:
            vel_msg.linear.x = vel
        else:
            vel_msg.linear.x = -vel
        
        # publish command velocity
        gd.oport['cmd_vel'].send(vel_msg)
        
        # calculate and update the current distance to goal
        gd.shared.current_distance = sqrt( (odom_position.x - init_odom_position.x)**2 + (odom_position.y - init_odom_position.y)**2 )
        
    else:
        # log
        logger.info('Goal reached')

        # publish zero command velocity to stop the robot
        vel_msg.linear.x = 0
        gd.oport['cmd_vel'].send(vel_msg)
        
        # transition throught exit port
        gd.oport['exit'].send()
