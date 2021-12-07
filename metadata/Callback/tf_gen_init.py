# This callback is associated with the tf_gen node.

# diable the tag_tf andthe tag_detections port. This is to stop the node functionality
# and to enable the node function only on trigger from another node or terminal
gd.iport['tag_tf_sub'].start_enabled = False
gd.iport['tag_detections'].start_enabled = False

# parameters
camera = gd.params['camera']

# define static rotation matrix for back and front camera
camera_back_rot_matrix = numpy.array([[0, -1, 0, 0], [0, 0, -1, 0], \
                                                [1,  0, 0, 0], [0, 0,  0, 1]])
camera_front_rot_matrix = numpy.array([[ 0, -1, 0, 0], [0, 0, 1, 0], \
                                        [-1,  0, 0, 0], [0, 0, 0, 1]])

# choose the rotation matrix based on the choosen camera
if camera == "back":
    transformationMatrix = camera_back_rot_matrix
elif camera == "front":
    transformationMatrix = camera_front_rot_matrix

# get the quaternion from matrtix
gd.shared.rotation = tf.transformations.quaternion_from_matrix(transformationMatrix)
