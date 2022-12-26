# panel_table.py
# V0.5.0 LDO 19/10/2022: initial version
# V0.5.1 LDO 12/11/2022: refactor modules
# V0.6.1 LDO 17/12/2022: release candidate 1
'''
    grafanacode:
    class for generating table panels
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
class PanelTable(panel_base.PanelBaseExtCommon1):
    '''
    Dataclass encapsulating a table panel
    '''
    # logging level of this item
    loglevel           : int = 15
    # attributes
    align              = field( default='auto',
                                validator=in_(('auto', 'left', 'center', 'right')))
    displaymode        = field( default='auto',
                                validator=in_(('auto', 'color-text', 'color-background', 'color-background-solid', 'gradient-gauge', 'lcd-gauge', 'basic', 'json-view')))
    enablepagination   = field( default=False,
                                validator=instance_of(bool))
    filterable         = field( default=False,
                                validator=instance_of(bool))
    footercalcs        = field( default=['lastNotNull'],
                                validator=deep_iterable(
                                    member_validator=in_(('lastNotNull','min','mean','max','last','firstNotNull','first','sum','count','range','delta','step',
                                                          'diff','logmin','allIsZero','allIsNull','changeCount','distinctCount','diffperc','allValues')),
                                    iterable_validator=instance_of(list)),
                                )
    footerfields       = field( default='',
                                validator=instance_of(str))
    inspect            = field( default=False,
                                validator=instance_of(bool))
    showheader         = field( default=True,
                                validator=instance_of(bool))
    showfooter         = field( default=False,
                                validator=instance_of(bool))

    # message
    def __attrs_post_init__(self):
        '''
        Attrs post init, just print a message.
        '''
        print (f'  > Init Panel: {self.title} - type: PanelTable ')

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
                #'columns'                       : self.columns,
                'fieldConfig'                   : {
                    'defaults'                  : {
                        'custom'                : {
                            'align'             : self.align,
                            'displayMode'       : self.displaymode,
                            'filterable'        : self.filterable,
                            'inspect'           : self.inspect,
                        },
                    },
                },
                'hideTimeOverride'              : self.hidetimeoverride,
                #'minSpan'                       : self.minspan,
                'options'                       : {
                    'enablePagination'          : self.enablepagination,
                    'showHeader'                : self.showheader,
                    'footer'                    : {
                      'show'                    : self.showfooter,
                      'reducer'                 : self.footercalcs,
                      'fields'                  : self.footerfields,

                    },
                },
                'type':                         'table',
            }
        )
        # merge child class JSON
        funcs.deepMerge(hjson, customjson)
        return hjson

#******************************************************************************
# EXTRACT FUNCTIONS : EXTRACT A CREATION SCRIPT FROM A JSON
#******************************************************************************
# pylint: disable=invalid-name
def extractPanel_table(dset, pset):
    '''
    Extract a panel exported from Grafana to a piece of Python code to be used by this module

    Parameters:
        dset (dict): dict with dashboard settings and json to extract (is input and output)
        pset (dict): dict with panel settings and json to extract (is input and output)
    Returns:
        boolean: True
    '''
    pset['codeh'].insert(0, f"{dset['intend']}hdashboard.addPanel(\n" \
                          + f"{dset['intend']}    PanelTable(title='{pset['title']}', ")
    # repeatable optional properties
    panel_base.extractCommons1(dset, pset)
    # optional properties
    item = funcs.cutJsonItem(pset['json'], ['fieldConfig', 'defaults', 'custom', 'filterable'], False)
    if item is not False:
        pset['codeb'].append(f"{pset['intend']}filterable={item},\n")
    item = funcs.cutJsonItem(pset['json'], ['minSpan'], 6)
    if item != 6:
        pset['codeb'].append(f"{pset['intend']}minspan={item},\n")
    item = funcs.cutJsonItem(pset['json'], ['options', 'showHeader'], True)
    if item is not True:
        pset['codeb'].append(f"{pset['intend']}showheader={item},\n")
    # function call closing
    pset['codeb'].append(f"{dset['intend']}    )\n"\
                       + f"{dset['intend']})\n")
    return True
