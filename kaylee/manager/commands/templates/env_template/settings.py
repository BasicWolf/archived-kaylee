# Indicates whether Kaylee will automatically return a next action
# when a result is accepted from a node.
AUTO_GET_ACTION = True

# A string that can be explicitly used in all the configurations
# which require a secret key (for encryption, signing etc).
SECRET_KEY = '{{ SECRET_KEY }}'

# A directory in which Kaylee searches for user projects
PROJECTS_DIR = '{{ PROJECTS_DIR }}'

# Nodes registry configuration
REGISTRY = {
   'name' : 'MemoryNodesRegistry',
   'config' : {
       'timeout' : '30m'
   },
}

# Session data manager configuration
SESSION_DATA_MANAGER = {
    'name' : 'NodeSessionDataManager',
    'config' : {}
}



# Add the applications' configurations here
APPLICATIONS = [

]
