# This callback is associated with the rotate state node.

# parameters
angle = gd.params['angle']

# log
if angle > 0:
    logger.info(f'Rotating counter clockwise direction for {angle} deg')
elif angle < 0:
    logger.info(f'Rotating clockwise direction for {-1*angle} deg')

# set default shared variables
gd.shared.init_odom_yaw = None
gd.shared.odom_orient = None
gd.shared.already_rotated = 0.0