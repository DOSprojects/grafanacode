# panel_dynamicimage.py
# V0.5.0 LDO 19/10/2022: initial version
# V0.5.1 LDO 12/11/2022: refactor modules
# V0.6.1 LDO 17/12/2022: release candidate 1
'''
    grafanacode:
    class for generating dalvany_impage panels
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
class PanelDynamicImage(panel_base.PanelBase):
    '''
    Dataclass encapsulating a dalvany image panel
    '''
    # logging level of this item
    loglevel           : int = 15
    # attributes
    width              = field(default=75,
                                validator=optional(instance_of(int)))
    height             = field(default=75,
                                validator=optional(instance_of(int)))
    iconfield          = field(default='',
                                validator=optional(instance_of(str)))
    baseurl            = field(default='',
                                validator=optional(instance_of(str)))
    suffix             = field(default='',
                                validator=optional(instance_of(str)))

    # message
    def __attrs_post_init__(self):
        '''
        Attrs post init, just print a message.
        '''
        print (f'  > Init Panel: {self.title} - type: PanelDynamicImage ')

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
                'options'                       : {
                    'icon_field'                : self.iconfield,
                    'width'                     : self.width,
                    'height'                    : self.height,
                    'slideshow'                 : {
                      'enable'                  : False,
                      'duration'                : 5000,
                      'transition'              : 'Slide',
                      'transition_duration'     : 1000,
                      'pauseOnHover'            : True,
                    },
                    'singleFill'                : True,
                    'alt_field'                 : '',
                    'tooltip'                   : False,
                    'tooltip_include_field'     : True,
                    'tooltip_field'             : '',
                    'tooltip_include_date'      : False,
                    'tooltip_date_elapsed'      : False,
                    'open_url'                  : {
                      'enable'                  : False,
                      'base_url'                : '',
                      'metric_field'            : '',
                      'suffix'                  : '',
                    },
                    'overlay'                   : {
                      'field'                   : '',
                      'position'                : 'Top right',
                      'width'                   : {
                        'size'                  : 5,
                        'unit'                  : '%',
                      },
                      'height'                  : {
                        'size'                  : 5,
                        'unit'                  : '%',
                      },
                      'bindings'                : {
                        'bindings'              : [],
                        'unbounded'             : '#66666620',
                        'has_text'              : True,
                      }
                    },
                    'underline'                 : {
                      'field'                   : '',
                      'text_size'               : '14',
                    },
                    'baseUrl'                   : self.baseurl,
                    'suffix'                    : self.suffix,
                },
                'type'                          : 'dalvany-image-panel',
        })
        funcs.deepMerge(hjson, customjson)
        return hjson

#******************************************************************************
# EXTRACT FUNCTIONS : EXTRACT A CREATION SCRIPT FROM A JSON
#******************************************************************************
# pylint: disable=invalid-name
def extractPanel_dalvany_image_panel(dset, pset):
    '''
    Extract a panel exported from Grafana to a piece of Python code to be used by this module

    Parameters:
        dset (dict): dict with dashboard settings and json to extract (is input and output)
        pset (dict): dict with panel settings and json to extract (is input and output)
    Returns:
        boolean: True
    '''
    pset['codeh'].insert(0, f"{dset['intend']}hdashboard.addPanel(\n" \
                          + f"{dset['intend']}    PanelDynamicImage(title='{pset['title']}', ")
    # optional properties
    item = funcs.cutJsonItem(pset['json'], ['options', 'baseUrl'], None)
    if item is not None:
        pset['codeb'].append(f"{pset['intend']}baseurl='{item}',\n")
    item = funcs.cutJsonItem(pset['json'], ['options', 'icon_field'], None)
    if item is not None:
        pset['codeb'].append(f"{pset['intend']}iconfield='{item}',\n")
    item = funcs.cutJsonItem(pset['json'], ['options', 'suffix'], None)
    if item is not None:
        pset['codeb'].append(f"{pset['intend']}suffix='{item}',\n")
    item = funcs.cutJsonItem(pset['json'], ['options', 'height'], None)
    if item is not None:
        pset['codeb'].append(f"{pset['intend']}height={item},\n")
    item = funcs.cutJsonItem(pset['json'], ['options', 'width'], None)
    if item is not None:
        pset['codeb'].append(f"{pset['intend']}width={item},\n")
    # function call closing
    pset['codeb'].append(f"{dset['intend']}    )\n"\
                       + f"{dset['intend']})\n")
    return True
