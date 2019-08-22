# Columbus module stores project-wide configuration and file paths

import os

root = os.path.join(os.path.dirname(__file__), '..')
data = os.path.join(root, '..','data/')
version_file = os.path.join(root, 'VERSION')
version = open(version_file, 'r').read()

global current_config
