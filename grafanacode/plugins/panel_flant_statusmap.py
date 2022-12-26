# panel_flant_statusmap.py
# V0.5.0 LDO 19/10/2022: initial version
# V0.5.1 LDO 12/11/2022: refactor modules
# V0.6.1 LDO 17/12/2022: release candidate 1
'''
    grafanacode:
    class for generating flant-statusmap panels
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
class PropStatusmapColor:
    '''
    Dataclass encapsulating the panel color attribute
    '''
    # logging level of this item
    loglevel           : int = 20
    # attributes
    # Maybe cardColor should validate to RGBA object, not sure
    cardcolor          = field( default='#b4ff00',
                                validator=optional(instance_of(str)))
    colorscale         = field( default='sqrt',
                                validator=optional(instance_of(str)))
    colorscheme        = field( default='GnYlRd',
                                validator=optional(instance_of(str)))
    exponent           = field( default=0.5,
                                validator=optional(instance_of((int, float))))
    mode               = field( default='spectrum',
                                validator=optional(instance_of(str)))
    thresholds         = field( default=[],
                                validator=optional(instance_of(list)))
    min                = field( default=None,
                                validator=optional(instance_of((int, float))))
    max                = field( default=None,
                                validator=optional(instance_of((int, float))))

    def getJson(self, dashboard=None, panel=None):
        '''
        Create the json to pack this item.

        Returns:
            dict: panel json code
        '''
        # pylint: disable=unused-argument
        hjson = {
            'cardColor'     : self.cardcolor,
            'colorScale'    : self.colorscale,
            'colorScheme'   : self.colorscheme,
            'exponent'      : self.exponent,
            'min'           : self.min,
            'max'           : self.max,
            'mode'          : self.mode,
            'thresholds'    : self.thresholds
        }
        return hjson

#**********************************************************
@define(slots=False)
class PropStatusmapLegend:
    '''
    Dataclass encapsulating the panel legend attribute
    '''
    # logging level of this item
    loglevel           : int = 20
    # attributes
    alignastable       = field( default=False,
                                validator=instance_of(bool))
    avg                = field( default=False,
                                validator=instance_of(bool))
    current            = field( default=False,
                                validator=instance_of(bool))
    hideempty          = field( default=False,
                                validator=instance_of(bool))
    hidezero           = field( default=False,
                                validator=instance_of(bool))
    min                = field( default=None,
                                validator=optional(instance_of((int, float))))
    max                = field( default=None,
                                validator=optional(instance_of((int, float))))
    rightside          = field( default=False,
                                validator=instance_of(bool))
    show               = field( default=True,
                                validator=instance_of(bool))
    sidewidth          = field( default=None)
    sort               = field( default=None)
    sortdesc           = field( default=False)
    total              = field( default=False,
                                validator=instance_of(bool))
    values             = field( default=None)

    def getJson(self, dashboard=None, panel=None):
        '''
        Create the json to pack this item.

        Returns:
            dict: panel json code
        '''
        # pylint: disable=unused-argument
        values = ((self.avg or self.current or self.max or self.min)
                  if self.values is None else self.values)

        hjson = {
            'alignAsTable'  : self.alignastable,
            'avg'           : self.avg,
            'current'       : self.current,
            'hideEmpty'     : self.hideempty,
            'hideZero'      : self.hidezero,
            'min'           : self.min,
            'max'           : self.max,
            'show'          : self.show,
            'total'         : self.total,
            'rightSide'     : self.rightside,
            'sideWidth'     : self.sidewidth,
            'sort'          : self.sort,
            'sortDesc'      : self.sortdesc,
            'values'        : values,
        }
        return hjson

#**********************************************************
@define(slots=False)
class PropStatusmapXAxis:
    '''
    Dataclass encapsulating the panel Xaxis attribute
    '''
    # logging level of this item
    loglevel           : int = 20
    # attributes
    mode               = field( default='time',
                                validator=optional(in_(['time', 'series'])))
    name               = field( default=None,
                                validator=optional(instance_of(str)))
    values             = field( default=Factory(list),
                                validator=optional(instance_of(list)))
    show               = field( default=True,
                                validator=optional(instance_of(bool)))

    def getJson(self, dashboard=None, panel=None):
        '''
        Create the json to pack this item.

        Returns:
            dict: panel json code
        '''
        # pylint: disable=unused-argument
        hjson = {
            'mode':   self.mode,
            'name':   self.name,
            'values': self.values,
            'show':   self.show,
        }
        return hjson

#******************************************************************************
# Panel Class
#******************************************************************************
@define(slots=False)
class PanelStatusmap(panel_base.PanelBase):
    '''
    Dataclass encapsulating a flant statusmap panel
    '''
    # logging level of this item
    loglevel           : int = 15
    # attributes
    alert              = field( default=None)
    cards              = field( default={'cardRound': None, 'cardMinWidth': 5, 'cardHSpacing': 2, 'cardVSpacing': 2},
                                validator=instance_of(dict))
    color              = field( default=Factory(PropStatusmapColor),
                                validator=instance_of(PropStatusmapColor))
    isnew              = field( default=True,
                                validator=instance_of(bool))
    legend             = field( default=Factory(PropStatusmapLegend),
                                validator=instance_of(PropStatusmapLegend),)
    nullpointmode      = field( default='null')
    tooltip            = field( default=Factory(panel_base.PropTooltip),
                                validator=instance_of(panel_base.PropTooltip),)
    xaxis              = field( default=Factory(PropStatusmapXAxis),
                                validator=instance_of(PropStatusmapXAxis))
    yaxis              = field( default=Factory(list),
                                validator=instance_of(list))

    # message
    def __attrs_post_init__(self):
        '''
        Attrs post init, just print a message.
        '''
        print (f'  > Init Panel: {self.title} - type: PanelStatusmap ')

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
            'color':            self.color,
            'isNew':            self.isnew,
            'legend':           self.legend,
            'nullPointMode':    self.nullpointmode,
            'tooltip':          self.tooltip,
            'xaxis':            self.xaxis,
            'yaxis':            self.yaxis,
            'type':             'flant-statusmap-panel',
        }
        # optional JSON
        if self.alert is not None:
            hjson['alert'] = self.alert
        # merge child class JSON
        funcs.deepMerge(hjson, customjson)
        return hjson

#******************************************************************************
# EXTRACT FUNCTIONS : EXTRACT A CREATION SCRIPT FROM A JSON
#******************************************************************************
# pylint: disable=invalid-name
def extractPanel_flant_statusmap_panel(dset, pset):
    '''
    Extract a panel exported from Grafana to a piece of Python code to be used by this module

    Parameters:
        dset (dict): dict with dashboard settings and json to extract (is input and output)
        pset (dict): dict with panel settings and json to extract (is input and output)
    Returns:
        boolean: True
    '''
    pset['codeh'].insert(0, f"{dset['intend']}hdashboard.addPanel(\n" \
                          + f"{dset['intend']}    PanelStatusmap(title='{pset['title']}', ")
    # optional properties
    # function call closing
    pset['codeb'].append(f"{dset['intend']}    )\n"\
                       + f"{dset['intend']})\n")
    return True
