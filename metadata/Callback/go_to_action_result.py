# This callback is associated with the go_to state node.
# log the status of the go_to action
message = msg.status.text
logger.info(f'Navigation action result: {message}')

# if navigation returns status 3 (Sucess) go to exit port, else go to failure port
if msg.status.status == 3:
    gd.oport['success'].send()
else:
    # exit the node
    gd.oport['failure'].send()
