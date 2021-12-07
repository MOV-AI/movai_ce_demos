# This callback is associated with the align_to_cart node.

# log
logger.debug(f'Align to cart is executing status: {gd.shared.executing}')

# if the tf generator node has been started, then stop it
# set the source flag to False (meaning that we stopped the source)
if gd.shared.source_status:
    # stop the tf generator node, to save resource
    gd.oport['enable_tf_generator'].send(False)
    # set the source_status to False, telling the system that we have stopped,
    # the tf generator
    gd.shared.source_status = False

# the node has used set amount of time, (check the timeout_timer port for the value)
# and not able to finish the align task. So we transition through the timeout port
if gd.shared.executing is False:
    # # reset the begin shared variable
    # gd.shared.begin = False
    # unregister timeout_timer callback
    gd.iport['timeout_timer'].unregister()
    # transition the node through the timeout out port
    gd.oport['timeout'].send()
