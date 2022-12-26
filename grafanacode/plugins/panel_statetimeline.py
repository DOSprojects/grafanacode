# panel_statetimeline.py
# V0.5.0 LDO 19/10/2022: initial version
# V0.5.1 LDO 12/11/2022: refactor modules
# V0.6.1 LDO 17/12/2022: release candidate 1
'''
    grafanacode:
    class for generating state-timeline panels
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
class PanelStateTimeline(panel_base.PanelBaseExtCommon1):
    '''
    Dataclass encapsulating a statetimeline panel
    '''
    # logging level of this item
    loglevel           : int = 15
    # attributes
    alignvalue         = field( default='left',
                                validator=in_(('left', 'center', 'right')))
    colwidth           = field( default=0.9,
                                validator=instance_of(float))
    fillopacity        = field( default=0,
                                validator=instance_of(int))
    legend             = field( default=Factory(panel_base.PropLegend),
                                validator=instance_of(panel_base.PropLegend))
    linewidth          = field( default=1,
                                validator=instance_of(int))
    mergevalues        = field( default=True,
                                validator=instance_of(bool))
    showvalue          = field( default='auto',
                                validator=in_(('auto', 'always', 'never')))
    spannulls          = field( default=False,
                                validator=instance_of((bool, int)))
    tooltipmode        = field( default='single',
                                validator=optional(in_(('single', 'multi', 'none'))))
    tooltipsort        = field( default='none',
                                validator=optional(in_(['none', 'asc', 'desc'])))
    rowheight          = field( default=0.97,
                                validator=instance_of(float))

    # message
    def __attrs_post_init__(self):
        '''
        Attrs post init, just print a message.
        '''
        print (f'  > Init Panel: {self.title} - type: PanelStateTimeline ')

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
                'fieldConfig'               : {
                    'defaults'              : {
                        'custom'            : {
                            'lineWidth'     : self.linewidth,
                            'fillOpacity'   : self.fillopacity,
                            'spanNulls'     : self.spannulls,
                        },
                   },
                },
                'options'                   : {
                    'colWidth'              : self.colwidth,
                    'mergeValues'           : self.mergevalues,
                    'showValue'             : self.showvalue,
                    'alignValue'            : self.alignvalue,
                    'rowHeight'             : self.rowheight,
                    'legend'                : self.legend,
                    'tooltip'               : {
                        'mode'              : self.tooltipmode,
                        'sort'              : self.tooltipsort,
                    },
                },
                'type'                      : 'state-timeline',
            }
        )
        # merge child class JSON
        funcs.deepMerge(hjson, customjson)
        return hjson

#******************************************************************************
# EXTRACT FUNCTIONS : EXTRACT A CREATION SCRIPT FROM A JSON
#******************************************************************************
# pylint: disable=invalid-name
def extractPanel_state_timeline(dset, pset):
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
    # optional properties
    # function call closing
    pset['codeb'].append(f"{dset['intend']}    )\n"\
                       + f"{dset['intend']})\n")
    return True
