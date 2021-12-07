# This callback is associated with the tf_gen node.

# start or stop certain callbacks based on the value of the incoming message.
# this callback is responsible for stopping and starting the node functionality
if msg.data == True:
    # log
    logger.debug('Starting tf generator')
    # start the tag_detections callback that recieve the tag_detections from apriltag_ros node
    gd.iport['tag_detections'].register()
    # start the TF subscriber for the tag TF
    gd.iport['tag_tf_sub'].register()
else:
    # log
    logger.debug('Stopping tf generator')
    # stop the tag_detections callback that recieve the tag_detections from apriltag_ros node
    gd.iport['tag_detections'].unregister()
    # stop the TF subscriber for the tag TF
    gd.iport['tag_tf_sub'].unregister()