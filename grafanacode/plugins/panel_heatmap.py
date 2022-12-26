# panel_heatmap.py
# V0.5.0 LDO 19/10/2022: initial version
# V0.5.1 LDO 12/11/2022: refactor modules
# V0.6.1 LDO 17/12/2022: release candidate 1
'''
    grafanacode:
    class for generating heatmap panels
'''

#******************************************************************************
# EXTERNAL MODULE REFERENCES
#******************************************************************************
from attrs           import define, field, Factory
from attr.validators import in_, instance_of, optional, deep_iterable

import grafanacode.c_colors as COLORS
from grafanacode            import funcs
from grafanacode.plugins    import panel_base

#******************************************************************************
# Panel Property classes: store panel property configuration parts
#******************************************************************************
@define(slots=False)
class PropHeatmapColor:
    '''
    Dataclass encapsulating the panel color attribute
    '''
    # logging level of this item
    loglevel           : int = 20
    # attributes
    # Maybe cardColor should validate to RGBA object, not sure
    cardcolor          = field( default='#b4ff00',
                                validator=optional(instance_of((str, panel_base.PropColor, COLORS.RGB, COLORS.RGBA))))
    colorscale         = field( default='sqrt',
                                validator=instance_of(str))
    colorscheme        = field( default='interpolateOranges',
                                validator=instance_of(str))
    exponent           = field( default=0.5,
                                validator=instance_of(float))
    mode               = field( default='spectrum',
                                validator=instance_of(str))
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
        if type(self.cardcolor)==str:
            self.cardcolor = panel_base.PropColor(self.cardcolor)
        hjson = {
            'mode':        self.mode,
            'cardColor':   self.cardcolor,
            'colorScale':  self.colorscale,
            'exponent':    self.exponent,
            'colorScheme': self.colorscheme,
        }
        if self.min:
            hjson['min'] = self.min
        if self.max:
            hjson['max'] = self.max
        return hjson

#**********************************************************
@define(slots=False)
class PropHeatmapYAxis:
    '''
    Dataclass encapsulating the panel Yaxis attribute
    '''
    # logging level of this item
    loglevel           : int = 20
    # attributes
    decimals = field(default=None, validator=optional(instance_of(int)))
    format   = field(default=None, validator=optional(instance_of(str)))
    label    = field(default=None, validator=optional(instance_of(str)))
    logbase  = field(default=1,    validator=optional(instance_of(int)))
    min      = field(default=None, validator=optional(instance_of((int, float))))
    max      = field(default=None, validator=optional(instance_of((int, float))))
    show     = field(default=True, validator=optional(instance_of(bool)))

    def getJson(self, dashboard=None, panel=None):
        '''
        Create the json to pack this item.

        Returns:
            dict: panel json code
        '''
        # pylint: disable=unused-argument
        hjson = {
            'decimals': self.decimals,
            'format':   self.format,
            'label':    self.label,
            'logBase':  self.logbase,
            'min':      self.min,
            'max':      self.max,
            'show':     self.show,
        }
        return hjson

#******************************************************************************
# Panel Class
#******************************************************************************
@define(slots=False)
class PanelHeatmap(panel_base.PanelBase):
    '''
    Dataclass encapsulating a heatmap panel
    '''
    # logging level of this item
    loglevel           : int = 15
    # attributes
    legend             = field( default={'show': False},
                                validator=instance_of(dict))
    tooltip            = field( default=Factory(panel_base.PropTooltip),
                                validator=instance_of(panel_base.PropTooltip))
    cardpadding        = field( default=None,
                                validator=optional(instance_of(str)))
    cardround          = field( default=None,
                                validator=optional(instance_of(str)))
    color              = field( default=Factory(PropHeatmapColor),
                                validator=instance_of(PropHeatmapColor))
    dataformat         = field( default='timeseries',
                                validator=in_(('timeseries', 'tsbuckets')))
    heatmap            = field( default=Factory(dict),
                                validator=instance_of(dict))
    hidezerobuckets    = field( default=False,
                                validator=instance_of(bool))
    highlightcards     = field( default=True,
                                validator=instance_of(bool))
    options            = field( default=None)
    xaxisshow          = field( default=instance_of(bool),
                                validator=instance_of(bool))
    xbucketnumber      = field( default=None)
    xbucketsize        = field( default=None)
    yaxis              = field( default=Factory(PropHeatmapYAxis),
                                validator=instance_of(PropHeatmapYAxis))
    ybucketbound       = field( default=None)
    ybucketnumber      = field( default=None)
    ybucketsize        = field( default=None)
    reverseybuckets    = field( default=False,
                                validator=instance_of(bool))

    # message
    def __attrs_post_init__(self):
        '''
        Attrs post init, just print a message.
        '''
        print (f'  > Init Panel: {self.title} - type: PanelHeatmap ')

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
            'cards'             : {
                'cardPadding'   : self.cardpadding,
                'cardRound'     : self.cardround,
            },
            'color'             : self.color,
            'dataFormat'        : self.dataformat,
            'heatmap'           : self.heatmap,
            'hideZeroBuckets'   : self.hidezerobuckets,
            'highlightCards'    : self.highlightcards,
            'legend'            : self.legend,
            'options'           : self.options,
            'reverseYBuckets'   : self.reverseybuckets,
            'tooltip'           : self.tooltip,
            'xAxis'             : {
                'show'          : self.xaxisshow,
            },
            'xBucketNumber'     : self.xbucketnumber,
            'xBucketSize'       : self.xbucketsize,
            'yAxis'             : self.yaxis,
            'yBucketBound'      : self.ybucketbound,
            'yBucketNumber'     : self.ybucketnumber,
            'yBucketSize'       : self.ybucketsize,
            'type'              : 'heatmap',
        })
        # merge child class JSON
        funcs.deepMerge(hjson, customjson)
        return hjson

#******************************************************************************
# EXTRACT FUNCTIONS : EXTRACT A CREATION SCRIPT FROM A JSON
#******************************************************************************
# pylint: disable=invalid-name
def extractPanel_heatmap(dset, pset):
    '''
    Extract a panel exported from Grafana to a piece of Python code to be used by this module

    Parameters:
        dset (dict): dict with dashboard settings and json to extract (is input and output)
        pset (dict): dict with panel settings and json to extract (is input and output)
    Returns:
        boolean: True
    '''
    pset['codeh'].insert(0, f"{dset['intend']}hdashboard.addPanel(\n" \
                          + f"{dset['intend']}    PanelHeatmap(title='{pset['title']}', ")
    # optional properties
    # function call closing
    pset['codeb'].append(f"{dset['intend']}    )\n"\
                       + f"{dset['intend']})\n")
    return True
