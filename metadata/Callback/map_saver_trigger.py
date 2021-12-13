# log
logger.info('Map save was called')

# enable map port
gd.iport['get_map'].unregister()
sleep(2)
gd.iport['get_map'].register()