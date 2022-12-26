# panel_text.py
# V0.5.0 LDO 19/10/2022: initial version
# V0.5.1 LDO 12/11/2022: refactor modules
# V0.6.1 LDO 17/12/2022: release candidate 1
'''
    grafanacode:
    class for generating stat panels
'''

#******************************************************************************
# EXTERNAL MODULE REFERENCES
#******************************************************************************
from attrs           import define, field, Factory
from attr.validators import in_, instance_of, optional, deep_iterable

from grafanacode         import funcs
from grafanacode.plugins import panel_base

#******************************************************************************
# Panel Property classes: store panel property configuration parts
#******************************************************************************

#******************************************************************************
# Panel Class
#******************************************************************************
@define(slots=False)
class PanelStat(panel_base.PanelBaseExtOpt1):
    '''
    Dataclass encapsulating a stat panel
    '''
    # logging level of this item
    loglevel           : int = 15
    # attributes
    colormode          = field( default='value',
                                validator=optional(in_(['none', 'value', 'background'])))
    graphmode          = field( default='none',
                                validator=optional(in_(['none', 'area'])))
    justify            = field( default='center',
                                validator=optional(in_(['auto', 'center'])))
    textmode           = field( default='value',
                                validator=instance_of(str))

     # message
    def __attrs_post_init__(self):
        '''
        Attrs post init, just print a message.
        '''
        print (f'  > Init Panel: {self.title} - type: PanelStat ')

    def getJson(self, customjson={}, dashboard=None, panel=None):
        '''
        Create the json to pack this panel.

        Parameters:
            customjson (dict): custom or child class json code to add
        Returns:
            dict: panel json code
        '''
        # pylint: disable=unused-argument
        hjson = super().getJson(
            {
                'options'               : {
                    'colorMode'         : self.colormode,
                    'graphMode'         : self.graphmode,
                    'justifyMode'       : self.justify,
                    'textMode'          : self.textmode,
                },
                'type'                  : 'stat',
        })
        # merge child class JSON
        funcs.deepMerge(hjson, customjson)
        return hjson

#******************************************************************************
# EXTRACT FUNCTIONS : EXTRACT A CREATION SCRIPT FROM A JSON
#******************************************************************************
# pylint: disable=invalid-name
def extractPanel_stat(dset, pset):
    '''
    Extract a panel exported from Grafana to a piece of Python code to be used by this module

    Parameters:
        dset (dict): dict with dashboard settings and json to extract (is input and output)
        pset (dict): dict with panel settings and json to extract (is input and output)
    Returns:
        boolean: True
    '''
    pset['codeh'].insert(0, f"{dset['intend']}hdashboard.addPanel(\n" \
                          + f"{dset['intend']}    PanelStat(title='{pset['title']}', ")
    # repeatable optional properties
    panel_base.extractCommons1(dset, pset)
    # optional properties
    item = funcs.cutJsonItem(pset['json'], ['options', 'graphMode'], None)
    if item is not None:
        pset['codeb'].append(f"{pset['intend']}graphmode='{item}',\n")
    item = funcs.cutJsonItem(pset['json'], ['options', 'textMode'], None)
    if item is not None:
        pset['codeb'].append(f"{pset['intend']}textmode='{item}',\n")
    # function call closing
    pset['codeb'].append(f"{dset['intend']}    )\n"\
                       + f"{dset['intend']})\n")
    return True
