# generated from ros_environment/env-hooks/_parent_package_path.py.em

from __future__ import print_function
import os
from collections import OrderedDict
env_name = 'CMAKE_PREFIX_PATH'
paths = [path for path in os.environ[env_name].split(os.pathsep)] if env_name in os.environ and os.environ[env_name] != '' else []
workspaces = [path for path in paths if os.path.exists(os.path.join(path, '.catkin'))]
workspaces = list(OrderedDict.fromkeys([os.path.normpath(ws) for ws in workspaces]))
paths = []
for workspace in workspaces:
    filename = os.path.join(workspace, '.catkin')
    data = ''
    with open(filename) as f:
        data = f.read()
    if data == '':
        paths.append(os.path.join(workspace, 'share'))
        if os.path.isdir(os.path.join(workspace, 'stacks')):
            paths.append(os.path.join(workspace, 'stacks'))
    else:
        for source_path in data.split(';'):
            paths.append(source_path)
print(os.pathsep.join(paths))
