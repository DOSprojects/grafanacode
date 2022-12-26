# panel_row.py
# V0.5.0 LDO 19/10/2022: initial version
# V0.5.1 LDO 12/11/2022: refactor modules
# V0.6.1 LDO 17/12/2022: release candidate 1
'''
    grafanacode:
    class for generating row panels
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
class PanelRow:
    '''
    Dataclass encapsulating a row panel
    '''
    # logging level of this item
    loglevel           : int = 15
    # attributes
    collapsed          = field( default=False,
                                validator=instance_of(bool))
    datasource         = field( default=None,
                                validator=optional(instance_of(dict)))
    gridpos            = field( default=Factory(panel_base.PropGridPos),
                                validator=instance_of(panel_base.PropGridPos))
    id                 = field( default=None,
                                validator=optional(instance_of(int)))
    targets            = field( default=None,
                                validator=optional(instance_of(list)))
    title              = field( default='',
                                validator=instance_of(str))
    # shortcuts and extra's
    extraprops         = field( default=None,
                                validator=optional(instance_of(dict)))

    # message
    def __attrs_post_init__(self):
        '''
        Attrs post init, just print a message.
        '''
        print (f'  > Init Row Panel: {self.title} - Row')

    def getJson(self, customjson={}, dashboard=None, panel=None):
        '''
        Create the json to pack this panel.

        Parameters:
            customjson (dict): custom or child class json code to add
        Returns:
            dict: panel json code
        '''
        # pylint: disable=unused-argument
        hjson = {
                    'collapsed' : self.collapsed,
                    'gridPos'   : self.gridpos,
                    'id'        : self.id,
                    'panels'    : [],
                    'title'     : self.title,
                    'type'      : 'row',
        }
        # optional JSON
        if self.targets is not None:
            hjson['targets'] = self.targets
        if self.datasource is not None:
            hjson['datasource'] = self.datasource
        #  merge child class JSON and extra prop
        funcs.deepMerge(hjson, customjson)
        funcs.deepMerge(hjson, self.extraprops)
        return hjson

#******************************************************************************
# EXTRACT FUNCTIONS : EXTRACT A CREATION SCRIPT FROM A JSON
#******************************************************************************
# pylint: disable=invalid-name
def extractPanel_row(dset, pset):
    '''
    Extract a panel exported from Grafana to a piece of Python code to be used by this module

    Parameters:
        dset (dict): dict with dashboard settings and json to extract (is input and output)
        pset (dict): dict with panel settings and json to extract (is input and output)
    Returns:
        boolean: True
    '''
    pset['codeh'].insert(0, f"{dset['intend']}hdashboard.addPanel(\n" \
                          + f"{dset['intend']}    PanelRow(title='{pset['title']}', ")
    # optional properties
    item = funcs.cutJsonItem(pset['json'], ['collapsed'], False)
    pset['codeb'].append(f"{pset['intend']}collapsed={item},\n")
    # function call closing
    pset['codeb'].append(f"{dset['intend']}    )\n"\
                       + f"{dset['intend']})\n")
    return True
