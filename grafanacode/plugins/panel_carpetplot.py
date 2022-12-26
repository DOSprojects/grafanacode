# panel_carpetplot.py
# V0.5.0 LDO 19/10/2022: initial version
# V0.5.1 LDO 12/11/2022: refactor modules
# V0.6.1 LDO 17/12/2022: release candidate 1
'''
    grafanacode:
    class for generating petrslavotinek-carpetplot panels
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
@define(slots=False)
class PropCarpetplotColorsItem:
    '''
    Dataclass encapsulating a Colors item
    '''
    # logging level of this item
    loglevel           : int = 21
    # attributes
    breakpoint         = field( default=0,
                                validator=instance_of((int, float)))
    color              = field( default=Factory(panel_base.PropColor),
                                validator=instance_of((str, panel_base.PropColor)))

    def getJson(self, dashboard=None, panel=None):
        '''
        Create the json to pack this item.

        Returns:
            dict: panel json code
        '''
        # pylint: disable=unused-argument
        if type(self.color)==str:
            self.color = panel_base.PropColor(self.color)
        hjson = {
            'breakpoint'   : self.breakpoint,
            'color'        : self.color,
       }
        return hjson

#**********************************************************
@define(slots=False)
class PropCarpetplotColors:
    '''
    Dataclass encapsulating a Colors list attribute consisting of PropCarpetplotColorsItem
    '''
    # logging level of this item
    loglevel           : int = 20
    # attributes
    items              = field( default=Factory(list),
                                validator=deep_iterable(
                                    member_validator=instance_of(PropCarpetplotColorsItem),
                                    iterable_validator=instance_of(list)))
    def getJson(self, dashboard=None, panel=None):
        '''
        Create the json to pack this item.

        Returns:
            dict: panel json code
        '''
        # pylint: disable=unused-argument
        return self.items

#**********************************************************
@define(slots=False)
class PropCarpetplotXAxis:
    '''
    Dataclass encapsulating a Xaxis attribute
    '''
    # logging level of this item
    loglevel           : int = 20
    # attributes
    labelformat        = field( default='%a %m/%d',
                                validator=optional(instance_of(str)))
    minbucketwidthtoshowweekends = field(default=4,
                                validator=optional(instance_of(int)))
    show               = field( default=True,
                                validator=optional(instance_of(bool)))
    showcrosshair      = field( default=True,
                                validator=optional(instance_of(bool)))
    showweekends       = field( default=True,
                                validator=optional(instance_of(bool)))

    def getJson(self, dashboard=None, panel=None):
        '''
        Create the json to pack this item.

        Returns:
            dict: panel json code
        '''
        # pylint: disable=unused-argument
        hjson = {
            'labelFormat'                   : self.labelformat,
            'minBucketWidthToShowWeekends'  : self.minbucketwidthtoshowweekends,
            'show'                          : self.show,
            'showCrosshair'                 : self.showcrosshair,
            'showWeekends'                  : self.showweekends,
        }
        return hjson

#**********************************************************
@define(slots=False)
class PropCarpetplotYAxis:
    '''
    Dataclass encapsulating a Yaxis attribute
    '''
    # logging level of this item
    loglevel           : int = 20
    # attributes
    show               = field( default=True,
                                validator=instance_of(bool))
    showcrosshair      = field( default=True,
                                validator=instance_of(bool))

    def getJson(self, dashboard=None, panel=None):
        '''
        Create the json to pack this item.

        Returns:
            dict: panel json code
        '''
        # pylint: disable=unused-argument
        hjson = {
            'show'                          : self.show,
            'showCrosshair'                 : self.showcrosshair,
       }
        return hjson

#******************************************************************************
# Panel Class
#******************************************************************************
@define(slots=False)
class PanelCarpetplot(panel_base.PanelBase):
    '''
    Dataclass encapsulating a carpetplot panel
    '''
    # logging level of this item
    loglevel           : int = 15
    # attributes
    dataformat         = field( default='timeseries',
                                validator=in_(('timeseries', 'tsbuckets')))


    aggregate          = field( default='AVG',
                                validator=instance_of(str))
    colorscheme        = field( default='interpolateSpectral',
                                validator=instance_of(str))
    colorspace         = field( default='RGB',
                                validator=in_(['RGB', 'LAB', 'HSL', 'HCL', 'CUBEHELIX']))
    colormode          = field( default='SPECTRUM',
                                validator=in_(['SPECTRUM', 'CUSTOM']))
    customcolors       = field( default=Factory(PropCarpetplotColors),
                                validator=instance_of(PropCarpetplotColors))
    decimals           = field( default=None,
                                validator=optional(instance_of(int)))
    fragment           = field( default='HOUR',
                                validator=instance_of(str))
    invertcolor        = field( default=False,
                                validator=instance_of(bool))
    nullcolor          = field( default='transparent',
                                validator=instance_of(str))
    legend             = field( default=True,
                                validator=instance_of(bool))
    min                = field( default=None,
                                validator=optional(instance_of((int, float))))
    max                = field( default=None,
                                validator=optional(instance_of((int, float))))
    tooltip            = field( default=True,
                                validator=instance_of(bool))
    units              = field( default=None,
                                validator=optional(instance_of(str)))
    xaxis              = field( default=Factory(PropCarpetplotXAxis),
                                validator=instance_of(PropCarpetplotXAxis))
    yaxis              = field( default=Factory(PropCarpetplotYAxis),
                                validator=instance_of(PropCarpetplotYAxis))

    # message
    def __attrs_post_init__(self):
        '''
        Attrs post init, just print a message.
        '''
        print (f'  > Init Panel: {self.title} - type: PanelCarpetplot ')

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
                'color': {
                    'colorScheme'       : self.colorscheme,
                    'colorSpace'        : self.colorspace,
                    'invert'            : self.invertcolor,
                    'mode'              : self.colormode,
                    'nullColor'         : self.nullcolor,
                    'customColors'      : self.customcolors,
                },
                'legend'                : {
                    'show'              : self.legend,
                },
                'aggregate'             : self.aggregate,
                'fragment'              : self.fragment,
                'tooltip'               : {
                    'show'              : self.tooltip,
                },
                'xAxis'                 : self.xaxis,
                'yAxis'                 : self.yaxis,
                'type'                  : 'petrslavotinek-carpetplot-panel',
            }
        )
        # optional JSON
        if self.decimals is not None:
            funcs.addJsonItem(hjson, ['data', 'decimals'], self.decimals)
        if self.units is not None:
            funcs.addJsonItem(hjson, ['data', 'unitFormat'], self.units)
        if self.min is not None:
            funcs.addJsonItem(hjson, ['scale', 'min'], self.min)
        if self.max is not None:
            funcs.addJsonItem(hjson, ['scale', 'max'], self.max)
        # merge child class JSON
        funcs.deepMerge(hjson, customjson)
        return hjson

#******************************************************************************
# EXTRACT FUNCTIONS : EXTRACT A CREATION SCRIPT FROM A JSON
#******************************************************************************
# pylint: disable=invalid-name
def extractPanel_petrslavotinek_carpetplot_panel(dset, pset):
    '''
    Extract a panel exported from Grafana to a piece of Python code to be used by this module

    Parameters:
        dset (dict): dict with dashboard settings and json to extract (is input and output)
        pset (dict): dict with panel settings and json to extract (is input and output)
    Returns:
        boolean: True
    '''
    pset['codeh'].insert(0, f"{dset['intend']}hdashboard.addPanel(\n" \
                          + f"{dset['intend']}    PanelCarpetplot(title='{pset['title']}', ")
    # optional properties
    # function call closing
    pset['codeb'].append(f"{dset['intend']}    )\n"\
                       + f"{dset['intend']})\n")
    return True
