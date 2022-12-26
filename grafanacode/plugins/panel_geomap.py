# panel_geomap.py
# V0.5.0 LDO 19/10/2022: initial version
# V0.5.1 LDO 12/11/2022: refactor modules
# V0.6.1 LDO 17/12/2022: release candidate 1
'''
    grafanacode:
    class for generating geomap panels
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
class PropGeomapLayersItem:
    '''
    Dataclass encapsulating a layers attribute
    '''
    # logging level of this item
    loglevel           : int = 21
    # attributes
    showlegend         = field( default=True,
                                validator=instance_of(bool))
    colorfield         = field( default='metric',
                                validator=instance_of(str))
    colorfixed         = field( default='dark-green',
                                validator=optional(instance_of((str, panel_base.PropColor, COLORS.RGB, COLORS.RGBA))))
    opacity            = field( default=0.4,
                                validator=instance_of(float))
    rotationfixed      = field( default=0,
                                validator=instance_of(int))
    rotationmax        = field( default=360,
                                validator=instance_of(str))
    rotationmin        = field( default=-360,
                                validator=instance_of(str))
    rotationmode       = field( default='mod',
                                validator=instance_of(str))
    sizefield          = field( default='metric',
                                validator=instance_of(str))
    sizefixed          = field( default=5,
                                validator=instance_of(str))
    sizemax            = field( default=15,
                                validator=instance_of(str))
    sizemin            = field( default=5,
                                validator=instance_of(str))
    symbolfixed        = field( default='img/icons/marker/circle.svg',
                                validator=instance_of(str))
    symbolmode         = field( default='fixed',
                                validator=instance_of(str))
    fontsize           = field( default=12,
                                validator=instance_of(str))
    textoffsetx        = field( default=0,
                                validator=instance_of(str))
    textoffsety        = field( default=0,
                                validator=instance_of(str))
    textalign          = field( default='center',
                                validator=instance_of(str))
    textbaseline       = field( default='middle',
                                validator=instance_of(str))
    locationlatitude   = field( default='lat',
                                validator=instance_of(str))
    locationlongitude  = field( default='lon',
                                validator=instance_of(str))
    locationmode       = field( default='coords',
                                validator=instance_of(str))
    name               = field( default='Layer 1',
                                validator=instance_of(str))
    tooltip            = field( default=True,
                                validator=instance_of(str))
    layertype          = field( default='markers',
                                validator=instance_of(str))


    def getJson(self, dashboard=None, panel=None):
        '''
        Create the json to pack this item.

        Returns:
            dict: panel json code
        '''
        # pylint: disable=unused-argument
        if type(self.colorfixed)==str:
            self.colorfixed = panel_base.PropColor(self.colorfixed)
        hjson = {
            'name'                  : self.name,
            'config'                : {
              'showLegend'          : self.showlegend,
              'style'               : {
                'color'             : {
                  'field'           : self.colorfield,
                  'fixed'           : self.colorfixed,
                },
                'opacity'           : self.opacity,
                'rotation'          : {
                  'fixed'           : self.rotationfixed,
                  'max'             : self.rotationmax,
                  'min'             : self.rotationmin,
                  'mode'            : self.rotationmode,
                },
                'size'              : {
                  'field'           : self.sizefield,
                  'fixed'           : self.sizefixed,
                  'max'             : self.sizemax,
                  'min'             : self.sizemin,
                },
                'symbol'            : {
                  'fixed'           : self.symbolfixed,
                  'mode'            : self.symbolmode,
                },
                'textConfig'        : {
                  'fontSize'        : self.fontsize,
                  'offsetX'         : self.textoffsetx,
                  'offsetY'         : self.textoffsety,
                  'textAlign'       : self.textalign,
                  'textBaseline'    : self.textbaseline,
                }
              }
            },
            'location'              : {
              'latitude'            : self.locationlatitude,
              'longitude'           : self.locationlongitude,
              'mode'                : self.locationmode,
            },
            'tooltip'               : self.tooltip,
            'type'                  : self.layertype,
            }
        return hjson

#**********************************************************
@define(slots=False)
class PropGeomapLayers:
    '''
    Dataclass encapsulating a layers attribute
    '''
    # logging level of this item
    loglevel           : int = 20
    # attributes
    items              = field( default=Factory(list),
                                validator=deep_iterable(
                                    member_validator=instance_of(PropGeomapLayersItem),
                                    iterable_validator=instance_of(list)))
    def getJson(self, dashboard=None, panel=None):
        '''
        Create the json to pack this item.

        Returns:
            dict: panel json code
        '''
        # pylint: disable=unused-argument
        return self.items


#******************************************************************************
# Panel Class
#******************************************************************************
@define(slots=False)
class PanelGeomap(panel_base.PanelBase):
    '''
    Dataclass encapsulating a geomap panel
    '''
    # logging level of this item
    loglevel           : int = 15
    # attributes
    basemapname        = field( default='Basemap',
                                validator=optional(instance_of(str)))
    basemaptype        = field( default='default',
                                validator=optional(instance_of(str)))
    colorscheme        = field( default='thresholds',
                                validator=in_(('value', 'fixed', 'thresholds', 'palette-classic', 'continuous-GrYlRd', 'continuous-RdYlGr', 'continuous-BlYlRd')))
    fcolor             = field( default='super-light-blue',
                                validator=optional(instance_of((str, panel_base.PropColor, COLORS.RGB, COLORS.RGBA))))
    hidefromtooltip    = field( default=True,
                                validator=optional(instance_of(bool)))
    hidefromviz        = field( default=True,
                                validator=optional(instance_of(bool)))
    hidefromlegend     = field( default=True,
                                validator=optional(instance_of(bool)))
    hidefromgraph      = field( default=True,
                                validator=optional(instance_of(bool)))
    layers             = field( default=Factory(PropGeomapLayers),
                                validator=optional(instance_of(PropGeomapLayers)))
    mappings           = field( default=Factory(panel_base.PropMappings),
                                validator=instance_of(panel_base.PropMappings))
    mousewheelzoom     = field( default=False,
                                validator=optional(instance_of(bool)))
    overrides          = field( default=Factory(panel_base.PropOverrides),
                                validator=instance_of(panel_base.PropOverrides))
    showattribution    = field( default=False,
                                validator=optional(instance_of(bool)))
    showdebug          = field( default=False,
                                validator=optional(instance_of(bool)))
    showscale          = field( default=False,
                                validator=optional(instance_of(bool)))
    showzoom           = field( default=True,
                                validator=optional(instance_of(bool)))
    thresholdmode      = field( default='absolute',
                                validator=in_(('absolute', 'percentage')))
    thresholds         = field( default=Factory(panel_base.PropThresholds),
                                validator=optional(instance_of(panel_base.PropThresholds)))
    tooltipmode        = field( default='details',
                                validator=optional(instance_of(str)))
    viewid             = field( default='fit',
                                validator=optional(instance_of(str)))
    viewlat            = field( default=46,
                                validator=optional(instance_of((int, float))))
    viewlon            = field( default=14,
                                validator=optional(instance_of((int, float))))
    viewzoom           = field( default='fit',
                                validator=optional(instance_of(int)))

    # message
    def __attrs_post_init__(self):
        '''
        Attrs post init, just print a message.
        '''
        print (f'  > Init Panel: {self.title} - type: PanelGeomap ')

    def getJson(self, customjson={}, dashboard=None, panel=None):
        '''
        Create the json to pack this panel.

        Parameters:
            customjson (dict): custom or child class json code to add
        Returns:
            dict: panel json code
        '''
        # pylint: disable=unused-argument
        if type(self.fcolor)==str:
            self.fcolor = panel_base.PropColor(self.fcolor)
        hjson = super().getJson({
            'fieldConfig'                   : {
                'defaults'                  : {
                    'color'                 : {
                        'mode'              : self.thresholdmode,
                    },
                    'custom'                : {
                        'hideFrom'          : {
                            'tooltip'       : self.hidefromtooltip,
                            'viz'           : self.hidefromviz,
                            'legend'        : self.hidefromlegend,
                            'graph'         : self.hidefromgraph,
                        },
                    },
                    'mappings'              : self.mappings,
                    'thresholds'            : {
                        'mode'              : self.thresholdmode,
                    },
                },
                'overrides'                 : self.overrides,
            },
            'options'                       : {
                'basemap'                   : {
                  'name'                    : self.basemapname,
                  'type'                    : self.basemaptype,
                },
                'controls'                  : {
                    'showZoom'              : self.showzoom,
                    'mouseWheelZoom'        : self.mousewheelzoom,
                    'showAttribution'       : self.showattribution,
                    'showScale'             : self.showscale,
                    'showDebug'             : self.showdebug,
                },
                'layers'                    : self.layers,
                'tooltip'                   : {
                    'mode'                  : self.tooltipmode,
                },
                'view'                      : {
                    'id'                    : self.viewid,
                    'lat'                   : self.viewlat,
                    'lon'                   : self.viewlon,
                    'zoom'                  : self.viewzoom,
                },
            },
            'type'                          : 'geomap',
        })
        # optional JSON
        if self.colorscheme is not None:
            funcs.addJsonItem(hjson, ['fieldConfig', 'defaults', 'color', 'mode'], self.colorscheme)
        # thresholds
        funcs.addJsonItem(hjson, ['fieldConfig', 'defaults', 'thresholds', 'steps'], self.thresholds.getJ(hjson, self.fcolor))
        #  merge child class JSON
        funcs.deepMerge(hjson, customjson)
        return hjson

#******************************************************************************
# EXTRACT FUNCTIONS : EXTRACT A CREATION SCRIPT FROM A JSON
#******************************************************************************
# pylint: disable=invalid-name
def extractPanel_geomap(dset, pset):
    '''
    Extract a panel exported from Grafana to a piece of Python code to be used by this module

    Parameters:
        dset (dict): dict with dashboard settings and json to extract (is input and output)
        pset (dict): dict with panel settings and json to extract (is input and output)
    Returns:
        boolean: True
    '''
    pset['codeh'].insert(0, f"{dset['intend']}hdashboard.addPanel(\n" \
                          + f"{dset['intend']}    PanelGeomap(title='{pset['title']}', ")
    # repeatable optional properties
    panel_base.extractCommons1(dset, pset)
    # optional properties
    # function call closing
    pset['codeb'].append(f"{dset['intend']}    )\n"\
                       + f"{dset['intend']})\n")
    return True
