# Disable/Unregister map port on start, to be only activated on recieving the save_map topic
gd.iport['get_map'].start_enabled = False
gd.iport['get_map'].unregister()
