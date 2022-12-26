# panel_gauge.py
# V0.5.0 LDO 19/10/2022: initial version
# V0.5.1 LDO 12/11/2022: refactor modules
# V0.6.1 LDO 17/12/2022: release candidate 1
'''
    grafanacode:
    class for generating gauge panels
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
class PanelGauge(panel_base.PanelBaseExtOpt1):
    '''
    Dataclass encapsulating a gauge panel
    '''
    # logging level of this item
    loglevel           : int = 15
    # attributes
    thresholdlabels    = field( default=True,
                                validator=instance_of(bool))
    thresholdmarkers   = field( default=True,
                                validator=instance_of(bool))

    # message
    def __attrs_post_init__(self):
        '''
        Attrs post init, just print a message.
        '''
        print (f'  > Init Panel: {self.title} - type: PanelGauge ')

    def getJson(self, customjson={}, dashboard=None, panel=None):
        '''
        Create the json to pack this panel.

        Parameters:
            customjson (dict): custom or child class json code to add
        Returns:
            dict: panel json code
        '''
        # pylint: disable=unused-argument
        hjson = super().getJson({
                'options'                   : {
                    'showThresholdLabels'   : self.thresholdlabels,
                    'showThresholdMarkers'  : self.thresholdmarkers,
                },
                'type'                      : 'gauge',
        })
        # merge child class JSON
        funcs.deepMerge(hjson, customjson)
        return hjson

#******************************************************************************
# EXTRACT FUNCTIONS : EXTRACT A CREATION SCRIPT FROM A JSON
#******************************************************************************
# pylint: disable=invalid-name
def extractPanel_gauge(dset, pset):
    '''
    Extract a panel exported from Grafana to a piece of Python code to be used by this module

    Parameters:
        dset (dict): dict with dashboard settings and json to extract (is input and output)
        pset (dict): dict with panel settings and json to extract (is input and output)
    Returns:
        boolean: True
    '''
    pset['codeh'].insert(0, f"{dset['intend']}hdashboard.addPanel(\n" \
                          + f"{dset['intend']}    PanelGauge(title='{pset['title']}', ")
    # repeatable optional properties
    panel_base.extractCommons1(dset, pset)
    # optional properties
    item = funcs.cutJsonItem(pset['json'], ['options', 'showThresholdLabels'], None)
    if item is not None:
        pset['codeb'].append(f"{pset['intend']}thresholdlabels='{item}',\n")
    item = funcs.cutJsonItem(pset['json'], ['options', 'showThresholdMarkers'], None)
    if item is not None:
        pset['codeb'].append(f"{pset['intend']}thresholdmarkers='{item}',\n")
    # function call closing
    pset['codeb'].append(f"{dset['intend']}    )\n"\
                       + f"{dset['intend']})\n")
    return True
