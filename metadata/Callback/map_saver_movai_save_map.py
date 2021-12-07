# log
logger.info('Map save was called')

# enable map port
gd.iport['map'].unregister()
sleep(2)
gd.iport['map'].register()