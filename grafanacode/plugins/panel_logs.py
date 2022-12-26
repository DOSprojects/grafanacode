# panel_logs.py
# V0.5.0 LDO 19/10/2022: initial version
# V0.5.1 LDO 12/11/2022: refactor modules
# V0.6.1 LDO 17/12/2022: release candidate 1
'''
    grafanacode:
    class for generating logs panels
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
class PanelLogs(panel_base.PanelBase):
    '''
    Dataclass encapsulating a logs panel
    '''
    # logging level of this item
    loglevel           : int = 15
    # attributes
    showlabels         = field( default=False,
                                validator=instance_of(bool))
    showcommonlabels   = field( default=False,
                                validator=instance_of(bool))
    showtime           = field( default=False,
                                validator=instance_of(bool))
    wraplogmessages    = field( default=False,
                                validator=instance_of(bool))
    sortorder          = field( default='Descending',
                                validator=instance_of(str))
    dedupstrategy      = field( default='none',
                                validator=instance_of(str))
    enablelogdetails   = field( default=False,
                                validator=instance_of(bool))
    overrides          = field( default=Factory(panel_base.PropOverrides),
                                validator=instance_of(panel_base.PropOverrides))
    prettifylogmessage = field( default=False,
                                validator=instance_of(bool))

    # message
    def __attrs_post_init__(self):
        '''
        Attrs post init, just print a message.
        '''
        print (f'  > Init Panel: {self.title} - type: PanelLogs ')

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
                'fieldConfig'           : {
                    'defaults'          : {
                        'custom'        : {},
                    },
                    'overrides'         : self.overrides
                },
                'options': {
                    'showLabels'        : self.showlabels,
                    'showCommonLabels'  : self.showcommonlabels,
                    'showTime'          : self.showtime,
                    'wrapLogMessage'    : self.wraplogmessages,
                    'sortOrder'         : self.sortorder,
                    'dedupStrategy'     : self.dedupstrategy,
                    'enableLogDetails'  : self.enablelogdetails,
                    'prettifyLogMessage': self.prettifylogmessage
                },
                'type': 'logs',
            }
        )
        funcs.deepMerge(hjson, customjson)
        return hjson

#******************************************************************************
# EXTRACT FUNCTIONS : EXTRACT A CREATION SCRIPT FROM A JSON
#******************************************************************************
# pylint: disable=invalid-name
def extractPanel_logs(dset, pset):
    '''
    Extract a panel exported from Grafana to a piece of Python code to be used by this module

    Parameters:
        dset (dict): dict with dashboard settings and json to extract (is input and output)
        pset (dict): dict with panel settings and json to extract (is input and output)
    Returns:
        boolean: True
    '''
    pset['codeh'].insert(0, f"{dset['intend']}hdashboard.addPanel(\n" \
                          + f"{dset['intend']}    PanelLogs(title='{pset['title']}', ")
    # optional properties
    # function call closing
    pset['codeb'].append(f"{dset['intend']}    )\n"\
                       + f"{dset['intend']})\n")
    return True
