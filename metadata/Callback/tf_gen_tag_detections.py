# This callback is associated with the tf_gen node.

# parameters
expected_tag_id = gd.params['expected_tag_id']
apriltag_tf_suffix = gd.params['apriltag_tf_suffix']

# receive tag detections message
tag_detections = msg.detections

# stop this callback as we only need to subscribe to it once
gd.iport['tag_detections'].unregister()

# log
logger.debug(f'Current apritag detections: {tag_detections}')

# iterate through each tag in the detections,
# if found the tag which is mentioned in the expected_tag_id parameters,
# calculate the distance to the tag to validate it.
all_tags = {}
for tag in tag_detections:
    tag_id = tag.id[0]
    logger.debug(f'Tag ID: {tag_id}')
    logger.debug(f'Expected Tag: {expected_tag_id}')
    if str(tag_id) == str(expected_tag_id):
        x = tag.pose.pose.pose.position.x
        y = tag.pose.pose.pose.position.y
        z = tag.pose.pose.pose.position.z
        
        tag_distance = math.sqrt(math.pow(x,2) + math.pow(y,2) + math.pow(z,2))
        all_tags[tag_id] = tag_distance

# log
logger.debug(f'All tag ids and distances from camera: {all_tags}')

# if reliable distance is detected for the expected tag,
# then enable the TF subscriber to generate the new TF
if all_tags:
    # get the frame name of the apriltag TF
    tag_frame = apriltag_tf_suffix + str(tag_id)
    # save to shared variable, to be used in other callbacks
    gd.shared.tag_frame = tag_frame
    # set the child frame in the TF subscriber port
    gd.iport['tag_tf_sub'].child_frame = tag_frame
    # registere the TF subscriber for the apriltag TF 
    gd.iport['tag_tf_sub'].register()
else:
    # warn the user if the expected tag is not found in the apriltag detections
    logger.warn(f'Expected tag: {expected_tag_id} but found: {all_tags.keys}')
