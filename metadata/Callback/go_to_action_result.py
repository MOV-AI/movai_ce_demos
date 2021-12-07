# This callback is associated with the go_to state node.
# log the status of the go_to action
message = msg.status.text
logger.info(f'Navigation action result: {message}')

# exit the node
gd.oport['exit'].send()