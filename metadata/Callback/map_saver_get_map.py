from tf.transformations import euler_from_quaternion  # cannot import outside

# getting parameters
name = gd.params.get('map_name', 'saved_map')
filepath = gd.params.get('filepath', '')
threshold_free = gd.params.get('threshold_free', 25)
threshold_occupied = gd.params.get('threshold_occupied', 65)

# Logging info about the map to save
info = msg.info
data = msg.data
logger.info(f'Saving map: {name}')
logger.info(f'{info.width} X {info.height} map @ {info.resolution:.3f} m/cell')


# Colors to use
black = 0
white = 254
grey = 205

# Creating 2d array to store image data, full grey start
width, height = info.width, info.height
img_data = numpy.full((height, width), grey, dtype=numpy.uint8)

# Go over each pixel and populate it with the right color
for y in range(height):
    for x in range(width):
        i = x + (height - y - 1) * width
        if data[i] >= 0 and data[i] <= threshold_free:
            img_data[y, x] = white
        elif data[i] >= threshold_occupied:
            img_data[y, x] = black


# Create an image from the array and convert to binary
img = fromarray(img_data, 'L')  # PIL.Image module
buf = io.BytesIO()
img.save(buf, format='PNG')
img_save = buf.getvalue()

# Upload image to Redis
try:
    p = Package('maps')
except:
    p = Package('maps', new=True)

logger.debug(f'Uploading {name}.png to database')
f = p.add('File', f'{name}.png')
f.Value = img_save
f.FileLabel = name

# Get the yaw angle from the quaternion
orientation_q = info.origin.orientation
orientation_list = [orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w]
(roll, pitch, yaw) = euler_from_quaternion(orientation_list)

# Build yaml file with default ROS format
yaml_data = f"""image: {name}.png
resolution: {info.resolution:.6f}
origin: [{info.origin.position.x:.6f}, {info.origin.position.y:.6f}, {yaw:.6f}]
negate: 0
occupied_thresh: 0.65
free_thresh: 0.196
"""

# Upload yaml to Redis
logger.debug(f'Uploading {name}.yaml to database')
f = p.add('File', f'{name}.yaml')
f.Value = yaml_data
f.FileLabel = name

# Same image and yaml to file
if filepath:
    logger.debug(f'Saving file {filepath}/{name}.png ')
    img.save(f'{filepath}/{name}.png')

    logger.debug(f'Saving file {filepath}/{name}.yaml ')
    f = open(f'{filepath}/{name}.yaml', 'w')
    f.write(yaml_data)
    f.close()

logger.info('Map saved with success')
