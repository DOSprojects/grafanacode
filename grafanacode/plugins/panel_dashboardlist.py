# panel_dashboardlist.py
# V0.5.0 LDO 19/10/2022: initial version
# V0.5.1 LDO 12/11/2022: refactor modules
# V0.6.1 LDO 17/12/2022: release candidate 1
'''
    grafanacode:
    class for generating dashboardlist panels
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
class PanelDashboardList(panel_base.PanelBase):
    '''
    Dataclass encapsulating a dashboardlist panel
    '''
    # logging level of this item
    loglevel           : int = 15
    # attributes
    folderid           = field( default=0,
                                validator=instance_of(int))
    showheadings       = field( default=False,
                                validator=instance_of(bool))
    showsearch         = field( default=False,
                                validator=instance_of(bool))
    showrecent         = field( default=False,
                                validator=instance_of(bool))
    showstarred        = field( default=False,
                                validator=instance_of(bool))
    maxitems           = field( default=10,
                                validator=instance_of(int))
    searchquery        = field( default='',
                                validator=instance_of(str))
    searchtags         = field( default=Factory(list),
                                validator=instance_of(list))
    overrides          = field( default=Factory(panel_base.PropOverrides),
                                validator=instance_of(panel_base.PropOverrides))

    # message
    def __attrs_post_init__(self):
        '''
        Attrs post init, just print a message.
        '''
        print (f'  > Init Panel: {self.title} - type: PanelDashboardList ')

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
                'options': {
                    'showStarred'           : self.showstarred,
                    'showRecentlyViewed'    : self.showrecent,
                    'showSearch'            : self.showsearch,
                    'showHeadings'          : self.showheadings,
                    'maxItems'              : self.maxitems,
                    'query'                 : self.searchquery,
                    'tags'                  : self.searchtags,
                    'folderId'              : self.folderid,
                },
                'type'                      : 'dashlist',
            }
        )
        funcs.deepMerge(hjson, customjson)
        return hjson

#******************************************************************************
# EXTRACT FUNCTIONS : EXTRACT A CREATION SCRIPT FROM A JSON
#******************************************************************************
# pylint: disable=invalid-name
def extractPanel_dashlist(dset, pset):
    '''
    Extract a panel exported from Grafana to a piece of Python code to be used by this module

    Parameters:
        dset (dict): dict with dashboard settings and json to extract (is input and output)
        pset (dict): dict with panel settings and json to extract (is input and output)
    Returns:
        boolean: True
    '''
    pset['codeh'].insert(0, f"{dset['intend']}hdashboard.addPanel(\n" \
                          + f"{dset['intend']}    PanelDashboardList(title='{pset['title']}', ")
    # optional properties
    # function call closing
    pset['codeb'].append(f"{dset['intend']}    )\n"\
                       + f"{dset['intend']})\n")
    return True
