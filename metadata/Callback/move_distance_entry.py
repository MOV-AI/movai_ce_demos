# This callback is associated with the move_distance state node.

# parameters
distance = gd.params['distance']

# log
if distance > 0:
    logger.info(f'Moving forward for {distance}m')
elif distance < 0:
    logger.info(f'Moving backward for {distance}m')

# set default shared variables
gd.shared.init_odom_position = None
gd.shared.odom_position = None
gd.shared.current_distance = 0.0