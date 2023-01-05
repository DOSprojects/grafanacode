# __init__.py
# V0.5.0 LDO 19/10/2022: initial version
# V0.5.1 LDO 12/11/2022: refactor modules
'''
    grafanacode module
    Generate Grafana dashboards from simple Python scripts. This module is based on grafanalib.
    So a lot of the techniques and ideas were borrowed at  `grafanalib` <https://github.com/weaveworks/grafanalib>`_
'''
# use as a module; make all plugins available, based on naming convention

#******************************************************************************
# EXTERNAL MODULE REFERENCES
#******************************************************************************
import os

import grafanacode.c_units  as UNITS
import grafanacode.c_colors as COLORS

#******************************************************************************
# IMPORTS
#******************************************************************************
from .funcs     import *
from .funcs_api import *
from .c_colors  import getColor, RGB, RGBA

path  = os.path.dirname(__file__) + '/plugins'
files = os.listdir(path)
for fname in files:
    if len(fname)<8:
        continue
    if fname == '__init__.py' or fname[-3:]!='.py':
        continue
    if len(fname)>10 and fname[:7] == 'target_':
        exec(f'from .plugins.{fname[:-3]} import *')
    elif len(fname)>13 and fname[:10] == 'dashboard_':
        exec(f'from .plugins.{fname[:-3]} import *')
    elif len(fname)>9 and fname[:6] == 'panel_':
        exec(f'from .plugins.{fname[:-3]} import *')

del path
del files
