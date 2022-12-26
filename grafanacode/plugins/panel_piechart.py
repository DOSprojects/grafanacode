# panel_piechart.py
# V0.5.0 LDO 19/10/2022: initial version
# V0.5.1 LDO 12/11/2022: refactor modules
# V0.6.1 LDO 17/12/2022: release candidate 1
'''
    grafanacode:
    class for generating piechart panels
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
class PanelPieChart(panel_base.PanelBaseExtOpt2):
    '''
    Dataclass encapsulating a pychart panel
    '''
    # logging level of this item
    loglevel           : int = 15
    # attributes
    # attr verwijderen
    hidefromgraph      = field( init=False, default=None)
    linewidth          = field( init=False, default=None)
    fillopacity        = field( init=False, default=None)
    thresholdmode      = field( init=False, default=None)
    thresholds         = field( init=False, default=None)
    #
    labels             = field( default=[],
                                validator=deep_iterable(
                                    member_validator=in_(('name', 'value','percent')),
                                    iterable_validator=instance_of(list)))
    pietype            = field( default='pie',
                                validator=optional(in_(('pi', 'donut'))))
    strokewidth        = field( default=1,
                                validator=instance_of(int))

    # message
    def __attrs_post_init__(self):
        '''
        Attrs post init, just print a message.
        '''
        print (f'  > Init Panel: {self.title} - type: PanelPieChart ')

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
                    'displayLabels'     : self.labels,
                    'pieType'           : self.pietype,
                    'strokeWidth'       : self.strokewidth,
                },
               'type'                   : 'piechart',
            }
        )
        # merge child class JSON
        funcs.deepMerge(hjson, customjson)
        return hjson

#******************************************************************************
# EXTRACT FUNCTIONS : EXTRACT A CREATION SCRIPT FROM A JSON
#******************************************************************************
# pylint: disable=invalid-name
def extractPanel_piechart(dset, pset):
    '''
    Extract a panel exported from Grafana to a piece of Python code to be used by this module

    Parameters:
        dset (dict): dict with dashboard settings and json to extract (is input and output)
        pset (dict): dict with panel settings and json to extract (is input and output)
    Returns:
        boolean: True
    '''
    pset['codeh'].insert(0, f"{dset['intend']}hdashboard.addPanel(\n" \
                          + f"{dset['intend']}    PanelPieChart(title='{pset['title']}', ")
    # optional properties
    # function call closing
    pset['codeb'].append(f"{dset['intend']}    )\n"\
                       + f"{dset['intend']})\n")
    return True
