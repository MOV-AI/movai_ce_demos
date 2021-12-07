# This callback is associated with the align_to_cart node.

# log
logger.info('Starting align to cart')

# Get parameters
# distance to move [m]
gd.shared.move_back_dist = gd.params['move_distance_to_cart']
# velocity [m/s]
gd.shared.final_speed = gd.params['final_speed']
# minimum rotation angle threshold [rad]
gd.shared.min_rot = gd.params['min_rot']
# angular velocity for Step 1 [rad/s]
gd.shared.rot1_w = gd.params['rot_w1']
# minimum moving distance threshold in Step 2
gd.shared.min_lin1 = gd.params['min_lin1']
# linear velocity in Step 2
gd.shared.move_vel1 = gd.params['move_vel1']
# angular velocity for Step 3 [rad/s]
gd.shared.rot2_w = gd.params['rot_w2']
# maximum linear velocity (x axis)
gd.shared.max_vel_lin = gd.params['max_vel_lin']
# maximum angular velocity (z axis)
gd.shared.max_vel_ang = gd.params['max_vel_ang']

# initialize flags
# gd.shared.begin = True
# a true value means that we have the TF information of the goal to align to
gd.shared.receive_tf = False
# a true value means that we have recieved the initial odometry message
gd.shared.init_odom = None
# a true value means that we have succesfully aligned to the goal TF
gd.shared.success = False
# TODO: what is this?
gd.shared.wait = False
# a true value means that the align is currently on going
gd.shared.executing = False

# set the middle man TF to listen to
gd.iport['tf_sub'].child_frame = gd.params['generated_tag_frame']

# trigger tf generator
gd.oport['enable_tf_generator'].send(True)
# log
logger.debug('Starting the tf generator')
# set the source_status, which is a variable if True, says that we have already,
# enabled the tf generator node
gd.shared.source_status = True
