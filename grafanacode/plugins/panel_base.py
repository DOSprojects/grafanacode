# panel_base.py
# V0.5.0 LDO 19/10/2022: initial version
# V0.5.1 LDO 12/11/2022: refactor modules
# V0.6.1 LDO 17/12/2022: release candidate 1
'''
    grafanacode:
    base class for generating panels
'''

#******************************************************************************
# EXTERNAL MODULE REFERENCES
#******************************************************************************
from attrs           import define, field, Factory
from attr.validators import in_, instance_of, optional, deep_iterable

import grafanacode.c_units  as UNITS
import grafanacode.c_colors as COLORS
from grafanacode            import funcs
#******************************************************************************
# Panel Property classes: store panel property configuration parts
#******************************************************************************
@define(slots=False)
class PropColor:
    '''
    Dataclass encapsulating the panel colors attribute
    '''
    # logging level of this item
    loglevel           : int = 20
    # attributes
    color              = field( default='SL_BLUE',
                                validator=optional(instance_of((str, COLORS.RGB, COLORS.RGBA))))
    ashex              = field( default=False,
                                validator=instance_of(bool))

    def getJson(self, dashboard=None, panel=None):
        '''
        Create the json to pack this item.

        Parameters:
            dashboard (Dashboard): Dashboard object we are in
            panel (Panel_base): Panel object we are in
        Returns:
            dict: panel json code
        '''
        # pylint: disable=unused-argument
        if dashboard is not None and dashboard.style == 'light':
            htheme = 'light'
        else:
            htheme = 'dark'
        hjson = COLORS.getColor(self.color, htheme, self.ashex)
        return hjson
#**********************************************************
@define(slots=False)
class PropGridPos:
    '''
    Dataclass encapsulating the panel gridposition attribute
    '''
    # logging level of this item
    loglevel           : int = 20
    # attributes
    h                  = field( default=0,
                                validator=instance_of(int))
    w                  = field( default=0,
                                validator=instance_of(int))
    x                  = field( default=0,
                                validator=instance_of(int))
    y                  = field( default=0,
                                validator=instance_of(int))

    def getJson(self, dashboard=None, panel=None):
        '''
        Create the json to pack this item.

        Parameters:
            dashboard (Dashboard): Dashboard object we are in
            panel (Panel_base): Panel object we are in
        Returns:
            dict: panel json code
        '''
        # pylint: disable=unused-argument
        hjson = {'h': self.h, 'w': self.w, 'x': self.x, 'y': self.y}
        return hjson
#**********************************************************
@define(slots=False)
class PropLinksItem:
    '''
    Dataclass encapsulating one panel linkitem
    '''
    # logging level of this item
    loglevel           : int = 21
    # attributes
    title              = field( default=None,
                                validator=instance_of(str))
    url                = field( default=None,
                                validator=instance_of(str))
    newtab             = field( default=None,
                                validator=instance_of(bool))

    def getJson(self, dashboard=None, panel=None):
        '''
        Create the json to pack this item.

        Parameters:
            dashboard (Dashboard): Dashboard object we are in
            panel (Panel_base): Panel object we are in
        Returns:
            dict: panel json code
        '''
        # pylint: disable=unused-argument
        hjson = {
            'title'         : self.title,
            'url'           : self.url,
            'targetBlank'   : self.newtab,
        }
        return hjson

#**********************************************************
@define(slots=False)
class PropLinks:
    '''
    Dataclass encapsulating the panel links list attribute consisting of PropLinksItem
    '''
    # logging level of this item
    loglevel           : int = 20
    # attributes
    links              = field( default=Factory(list),
                                validator=deep_iterable(
                                    member_validator=instance_of(PropLinksItem),
                                    iterable_validator=instance_of(list)))

    def getJson(self, dashboard=None, panel=None):
        '''
        Create the json to pack this item.

        Parameters:
            dashboard (Dashboard): Dashboard object we are in
            panel (Panel_base): Panel object we are in
        Returns:
            dict: panel json code
        '''
        # pylint: disable=unused-argument
        hjson = self.links
        return hjson

#**********************************************************
@define(slots=False)
class PropRepeat:
    '''
    Dataclass encapsulating the panel repeat attribute
    '''
    # logging level of this item
    loglevel           : int = 20
    # attributes
    variable           = field( default=None,
                                validator=instance_of(str))
    direction          = field( default=None,
                                validator=in_(('h', 'v')))
    maxperrow          = field( default=None,
    validator=optional(instance_of(int)))
    @maxperrow.validator
    # pylint: disable=invalid-name
    def _check_maxperrow(self, attribute, value):
        if ((value is not None) and not isinstance(value, int)):
            raise ValueError(f'{attribute} should either be None or an integer')

#    def getJson(self, dashboard=None, panel=None): # handled in panelbase

#**********************************************************
# Statusmap, Heatmap
@define(slots=False)
class PropTooltip:
    '''
    Dataclass encapsulating the panel tooltip attribute
    '''
    # logging level of this item
    loglevel           : int = 20
    # attributes
    msresolution       = field( default=True,
                                validator=instance_of(bool))
    shared             = field( default=True,
                                validator=instance_of(bool))
    sort               = field( default=0,
                                validator=instance_of(int))
    valuetype          = field( default='cumulative',
                                validator=instance_of(str))

    def getJson(self, dashboard=None, panel=None):
        '''
        Create the json to pack this item.

        Parameters:
            dashboard (Dashboard): Dashboard object we are in
            panel (Panel_base): Panel object we are in
        Returns:
            dict: panel json code
        '''
        # pylint: disable=unused-argument
        return {
            'msResolution': self.msresolution,
            'shared':       self.shared,
            'sort':         self.sort,
            'value_type':   self.valuetype,
        }

#******************************************************************************
# PanelBaseExtCommon1 Property classes: store panel property configuration parts
#******************************************************************************
@define(slots=False)
class PropMappingsItem:
    '''
    Dataclass encapsulating one panel mappingsitem
    '''
    # logging level of this item
    loglevel           : int = 21
    # attributes
    mvalue             = field( default=None,
                                validator=optional(instance_of((int, float, str))))
    mfrom              = field( default=None,
                                validator=optional(instance_of((int, float))))
    mto                = field( default=None,
                                validator=optional(instance_of((int, float))))
    mregex             = field( default=None,
                                validator=optional(instance_of(str)))
    mspecial           = field( default=None,
                                validator=optional(in_(['null', 'nan', 'null+nan', 'empty', 'true', 'false'])))
    mtext              = field( default=None,
                                validator=optional(instance_of(str)))
    mcolor             = field( default=None,
                                validator=optional(instance_of((str, PropColor, COLORS.RGB, COLORS.RGBA))))
    mindex             = field( init=False,
                                default=0) # no input, calculated afterwards in PropMappings.getJson

    def getJson(self, dashboard=None, panel=None):
        '''
        Create the json to pack this item.

        Parameters:
            dashboard (Dashboard): Dashboard object we are in
            panel (Panel_base): Panel object we are in
        Returns:
            dict: panel json code
        '''
        # pylint: disable=unused-argument
        if type(self.mcolor)==str:
            self.mcolor = PropColor(self.mcolor)
        hresult = {'index': self.mindex}
        if self.mtext is not  None:
            hresult['text'] = self.mtext
        if self.mcolor is not  None:
            hresult['color'] = self.mcolor
        hoptions = {}
        if self.mvalue is not  None:
            htype = 'value'
            hoptions[str(self.mvalue)] = hresult
        elif self.mfrom is not  None and self.mto is not  None:
            htype = 'range'
            hoptions['from'] = self.mfrom
            hoptions['to'] = self.mto
            hoptions['result'] = hresult
        elif self.mregex is not  None:
            htype = 'regex'
            hoptions['pattern'] = self.mregex
            hoptions['result'] = hresult
        elif self.mspecial is not  None:
            htype = 'special'
            hoptions['match'] = self.mspecial
            hoptions['result'] = hresult
        else:
            raise ValueError('PropMappingsItem has no mvalue, mfrom/mto; mregex or mspecial')
        hjson = {
            'type'              : htype,
            'options'           : hoptions,
        }
        return hjson

#**********************************************************
@define(slots=False)
class PropMappings:
    '''
    Dataclass encapsulating the panel mappings list attribute consisting of PropMappingsItem
    '''
    # logging level of this item
    loglevel           : int = 20
    # attributes
    items              = field( default=Factory(list),
                                validator=deep_iterable(
                                    member_validator=instance_of(PropMappingsItem),
                                    iterable_validator=instance_of(list)))
    def getJson(self, dashboard=None, panel=None):
        '''
        Create the json to pack this item.

        Parameters:
            dashboard (Dashboard): Dashboard object we are in
            panel (Panel_base): Panel object we are in
        Returns:
            dict: panel json code
        '''
        # pylint: disable=unused-argument, not-an-iterable
        # set mappings indexes
        if self.items:
            i = 0
            for item in self.items:
                item.mindex = i
                i += 1
        return self.items

#**********************************************************
@define(slots=False)
class PropOverridesItem:
    '''
    Dataclass encapsulating one panel overrideitem
    '''
    # logging level of this item
    loglevel           : int = 21
    # attributes
    oname              = field( default=None,
                                validator=optional(instance_of(str)))
    oregex             = field( default=None,
                                validator=optional(instance_of(str)))
    otype              = field( default=None,
                                validator=optional(instance_of(str)))
    oquery             = field( default=None,
                                validator=optional(instance_of(str)))
    prop               = field( default=None,
                                validator=instance_of(list))

    def getJson(self, dashboard=None, panel=None):
        '''
        Create the json to pack this item.

        Parameters:
            dashboard (Dashboard): Dashboard object we are in
            panel (Panel_base): Panel object we are in
        Returns:
            dict: panel json code
        '''
        # pylint: disable=unused-argument
        if self.oname is not None:
            hmatcher = {'id': 'byName', 'options': self.oname}
        elif self.oregex is not None:
            hmatcher = {'id': 'byRegexp', 'options': self.oregex}
        elif self.otype is not None:
            hmatcher = {'id': 'byType', 'options': self.otype}
        elif self.oquery is not None:
            hmatcher = {'id': 'byFrameRefID', 'options': self.oquery}
        else:
            raise ValueError('PropOverridesItem has no oname, oregex; otype or oquery')
        hjson = {
            'matcher'       : hmatcher,
            'properties'    : self.prop,
        }
        return hjson

#**********************************************************
@define(slots=False)
class PropOverrides:
    '''
    Dataclass encapsulating the panel overrides list attribute consisting of PropOverridesItem
    '''
    # logging level of this item
    loglevel           : int = 20
    # attributes
    items              = field( default=Factory(list),
                                validator=deep_iterable(
                                    member_validator=instance_of(PropOverridesItem),
                                    iterable_validator=instance_of(list)))
    def getJson(self, dashboard=None, panel=None):
        '''
        Create the json to pack this item.

        Parameters:
            dashboard (Dashboard): Dashboard object we are in
            panel (Panel_base): Panel object we are in
        Returns:
            dict: panel json code
        '''
        # pylint: disable=unused-argument
        return self.items

#**********************************************************
# Threshold items must be specified (numerical order)
@define(slots=False)
class PropThresholdsItem:
    '''
    Dataclass encapsulating one panel threshold item
    '''
    # logging level of this item
    loglevel           : int = 21
    # attributes
    color              = field( default=PropColor('super-light-blue'),
                                validator=optional(instance_of((str, PropColor, COLORS.RGB, COLORS.RGBA))))
    value              = field( default=None,
                                validator=optional(instance_of((int, float))))

    def getJson(self, dashboard=None, panel=None):
        '''
        Create the json to pack this item.

        Parameters:
            dashboard (Dashboard): Dashboard object we are in
            panel (Panel_base): Panel object we are in
        Returns:
            dict: panel json code
        '''
        # pylint: disable=unused-argument
        if type(self.color)==str:
            self.color = PropColor(self.color)
        hjson = {
            'color': self.color,
            'value': None if self.value is None else self.value,
        }
        return hjson

#**********************************************************
@define(slots=False)
class PropThresholds:
    '''
    Dataclass encapsulating the panel thresholds list attribute consisting of PropThresholdsItem
    '''
    # logging level of this item
    loglevel           : int = 20
    # attributes
    items              = field( default=Factory(list),
                                validator=deep_iterable(
                                    member_validator=instance_of(PropThresholdsItem),
                                    iterable_validator=instance_of(list)))

    def getJ(self, fcolor):
        '''
        The fcolor attribute maps to the key <0> of the thresholds attribute.

        Parameters:
            fcolor (string): forecolor of the panel
        Returns:
            dict: items attribute
        '''
        # pylint: disable=no-member
        if fcolor is not None:
            self.items.insert(0, PropThresholdsItem(fcolor, None))
        return self.items

    def getJson(self, dashboard=None, panel=None):
        '''
        Create the json to pack this item.

        Parameters:
            dashboard (Dashboard): Dashboard object we are in
            panel (Panel_base): Panel object we are in
        Returns:
            dict: panel json code
        '''
        # pylint: disable=unused-argument
        return self.items

#******************************************************************************
# PanelBaseExtOpt2 Property classes: store panel property configuration parts
#******************************************************************************
@define(slots=False)
class PropLegend:
    '''
    Dataclass encapsulating the panel legend attribute
    '''
    # logging level of this item
    loglevel           : int = 20
    # attributes
    showlegend         = field( default=False,
                                validator=instance_of(bool))
    displaymode        = field( default='table',
                                validator=optional(in_(('hidden', 'list', 'table'))))
    placement          = field( default='bottom',
                                validator=optional(in_(('bottom', 'right'))))
    calcs              = field( default=['lastNotNull', 'min', 'max', 'mean'],
                                validator=deep_iterable(
                                    member_validator=in_(('lastNotNull','min','mean','max','last','firstNotNull','first','sum','count','range','delta','step',
                                                          'diff','logmin','allIsZero','allIsNull','changeCount','distinctCount','diffperc','allValues')),
                                    iterable_validator=instance_of(list)))
    values             = field( default=[],
                                validator=deep_iterable(
                                    member_validator=in_(('value','percent')),
                                    iterable_validator=instance_of(list)))
    values             = field( default=Factory(list),
                                validator=instance_of(list))
    width              = field( default=None,
                                validator=optional(instance_of(int)))

    def getJson(self, dashboard=None, panel=None):
        '''
        Create the json to pack this item.

        Parameters:
            dashboard (Dashboard): Dashboard object we are in
            panel (Panel_base): Panel object we are in
        Returns:
            dict: panel json code
        '''
        # pylint: disable=unused-argument
        hjson = {
            'showLegend'    : self.showlegend,
            'displayMode'   : self.displaymode,
            'placement'     : self.placement,
            'calcs'         : self.calcs,
            'values'        : self.values,
            'width'         : self.width,
        }
        return hjson

#******************************************************************************
# Panel Base Class
#******************************************************************************
@define(slots=False)
class PanelBase:
    '''
    Base Panel dataclass. This class encapsulates all properties of a single Grafana panel.
    It creates the final panel JSON by means of its getJson method.
    This class will not be called directly, but subclassed to specify a specific type of panel.
    '''
    # logging level of this item
    loglevel           : int = 10
    logstr             : str = ''
    # attributes
    #cachetimeout       = field( default=None)                           # wasda?????
    #editable           = field( default=True,
    #                            validator=instance_of(bool))
    datasource         = field( default=None,
                                validator=optional(instance_of(dict)))
    gridpos            = field( default=Factory(PropGridPos),
                                validator=instance_of(PropGridPos))
    hidetimeoverride   = field( default=None,
                                validator=optional(instance_of(bool)))  # in Grafana GUI in query options
    id                 = field( default=None,
                                validator=optional(instance_of(int)))
    interval           = field( default=None,
                                validator=optional(instance_of(int)))   # in Grafana GUI in query options
    links              = field( default=Factory(PropLinks),
                                validator=instance_of(PropLinks))
    maxdatapoints      = field( default=None,
                                validator=optional(instance_of(int)))   # in Grafana GUI in query options
    repeat             = field( default=None,
                                validator=optional(instance_of(PropRepeat)))
    targets            = field( default=None,
                                validator=optional(instance_of(list)))
    timefrom           = field( default=None,
                                validator=optional(instance_of(str)))   # in Grafana GUI in query options
    timeregions        = field( default=None,
                                validator=optional(instance_of(list)))
    timezone           = field( default=None,
                                validator=optional(instance_of(str)))
    timeshift          = field( default=None,
                                validator=optional(instance_of(str)))   # in Grafana GUI in query options
    title              = field( default='',
                                validator=instance_of(str))
    @title.validator
    # pylint: disable=invalid-name
    def _check_title(self, attribute, value):
        self.logstr = f'Panel name: {value}'
    transformations    = field( default=None,
                                validator=optional(instance_of(list)))
    transparent        = field( default=False,
                                validator=instance_of(bool))
    # shortcuts and extra's
    extraprops         = field( default=None,
                                validator=optional(instance_of(dict)))

    # message
    def __attrs_post_init__(self):
        '''
        Attrs post init, just print a message.
        '''
        print (f'  > Init Panel: {self.title} - PanelBase')

    def getJson(self, customjson={}, dashboard=None, panel=None):
        '''
        Create the json to pack this panel.

        Parameters:
            customjson (dict): custom or child class json code to add
            dashboard (Dashboard): Dashboard object we are in
            panel (Panel_base): Panel object we are in
        Returns:
            dict: panel json code
        '''
        # pylint: disable=unused-argument
        self.logstr = self.title
        hjson = {
            'gridPos'           : self.gridpos,
            'id'                : self.id,
            'links'             : self.links,
            'title'             : self.title,
            'transparent'       : self.transparent,
        }
        # optional JSON
        #if self.cachetimeout is not None:
        #    hjson['cacheTimeout'] = self.cachetimeout
        #if self.editable is not None:
        #    hjson['editable'] = self.editable
        if self.targets is not None:
            hjson['targets'] = self.targets
        if self.datasource is not None:
            hjson['datasource'] = self.datasource
        if self.interval is not None:
            hjson['interval'] = self.interval
        if self.hidetimeoverride is not None:
            hjson['hideTimeOverride'] = self.hidetimeoverride
        if self.maxdatapoints is not None:
            hjson['maxDataPoints'] = self.maxdatapoints
        if self.repeat is not None:
            hjson['repeat'] = self.repeat.variable
            hjson['repeatDirection'] = self.repeat.direction
            hjson['maxPerRow'] = self.repeat.maxperrow
        if self.timeregions is not None:
            hjson['timeRegions'] = self.timeregions
        if self.timezone is not None:
            hjson['timezone'] = self.timezone
        if self.timefrom is not None:
            hjson['timeFrom'] = self.timefrom
        if self.timeshift is not None:
            hjson['timeShift'] = self.timeshift
        if self.transformations is not None:
            hjson['transformations'] = self.transformations
        #  merge child class JSON and extra prop
        funcs.deepMerge(hjson, customjson)
        funcs.deepMerge(hjson, self.extraprops)
        return hjson

#******************************************************************************
# Base Class with some extra common properties
@define(slots=False)
class PanelBaseExtCommon1(PanelBase):
    '''
    Panel subclass with some additional attributes.
    This class will not be called directly, but subclassed to specify a specific type of panel.
    '''
    # logging level of this item
    loglevel           : int = 11
    # attributes
    colorscheme        = field( default='thresholds',
                                validator=in_(('value', 'fixed', 'thresholds', 'palette-classic', 'continuous-GrYlRd', 'continuous-RdYlGr', 'continuous-BlYlRd')))
    decimals           = field( default=None,
                                validator=optional(instance_of(int)))
    displayname        = field( default=None,
                                validator=optional(instance_of(str)))
    fcolor             = field( default=PropColor('super-light-blue'),
                                validator=optional(instance_of((str, PropColor, COLORS.RGB, COLORS.RGBA))))
    mappings           = field( default=Factory(PropMappings),
                                validator=instance_of(PropMappings))
    max                = field( default=None,
                                validator=optional(instance_of((int, float))))
    min                = field( default=None,
                                validator=optional(instance_of((int, float))))
    novalue            = field( default=None,
                                validator=optional(instance_of(str)))
    overrides          = field( default=Factory(PropOverrides),
                                validator=instance_of(PropOverrides))
    thresholdmode      = field( default='absolute',
                                validator=in_(('absolute', 'percentage')))
    thresholds         = field( default=Factory(PropThresholds),
                                validator=optional(instance_of(PropThresholds)))
    units              = field( default=None,
                                validator=optional(instance_of(str)))
     # message
    def __attrs_post_init__(self):
        '''
        Attrs post init, just print a message.
        '''
        print (f'  > Init Panel: {self.title} -  type:  PanelBaseExtCommon1 ')

    def getJson(self, customjson={}, dashboard=None, panel=None):
        '''
        Create the json to pack this panel.

        Parameters:
            customjson (dict): custom or child class json code to add
            dashboard (Dashboard): Dashboard object we are in
            panel (Panel_base): Panel object we are in
        Returns:
            dict: panel json code
        '''
        # pylint: disable=unused-argument
        if type(self.fcolor)==str:
            self.fcolor = PropColor(self.fcolor)
        hjson = super().getJson({
            'fieldConfig'           : {
                'defaults'          : {
                    'mappings'      : self.mappings,
                    'thresholds'    : {
                        'mode'      : self.thresholdmode,
                    },
                },
                'overrides'         : self.overrides,
            },
        })
        # optional JSON
        if self.colorscheme is not None:
            funcs.addJsonItem(hjson, ['fieldConfig', 'defaults', 'color', 'mode'], self.colorscheme)
        if self.decimals is not None:
            funcs.addJsonItem(hjson, ['fieldConfig', 'defaults', 'decimals'], self.decimals)
        if self.decimals is not None:
            funcs.addJsonItem(hjson, ['fieldConfig', 'defaults', 'decimals'], self.decimals)
        if self.min is not None:
            funcs.addJsonItem(hjson, ['fieldConfig', 'defaults', 'min'], self.min)
        if self.max is not None:
            funcs.addJsonItem(hjson, ['fieldConfig', 'defaults', 'max'], self.max)
        if self.units is not None:
            funcs.addJsonItem(hjson, ['fieldConfig', 'defaults', 'unit'], self.units)
        # thresholds
        funcs.addJsonItem(hjson, ['fieldConfig', 'defaults', 'thresholds', 'steps'], self.thresholds.getJ(self.fcolor))
        #  merge child class JSON
        funcs.deepMerge(hjson, customjson)
        return hjson

#******************************************************************************
# Base Class with some extra properties
@define(slots=False)
class PanelBaseExtOpt1(PanelBaseExtCommon1):
    '''
    Panel subclass with some additional attributes.
    This class will not be called directly, but subclassed to specify a specific type of panel.
    '''
    # logging level of this item
    loglevel           : int = 12
    # attributes
    calcs              = field( default=['lastNotNull'],
                                validator=deep_iterable(
                                    member_validator=in_(('lastNotNull','min','mean','max','last','firstNotNull','first','sum','count','range','delta','step',
                                                          'diff','logmin','allIsZero','allIsNull','changeCount','distinctCount','diffperc','allValues')),
                                    iterable_validator=instance_of(list)))
    fields             = field( default='',
                                validator=instance_of(str))
    orientation        = field( default='auto',
                                validator=optional(in_(['auto', 'horizontal', 'vertical'])))
    reducelimit        = field( default=25,
                                validator=instance_of(int))  # Max number of rows to display when reducevalues = AllValues=True
    reducevalues       = field( default=False,
                                validator=instance_of(bool)) # Calculate=False or AllValues=True
    titlesize          = field( default=None,
                                validator=optional(instance_of(int)))
    valuesize          = field( default=None,
                                validator=optional(instance_of(int)))

     # message
    def __attrs_post_init__(self):
        '''
        Attrs post init, just print a message.
        '''
        print (f'  > Init Panel: {self.title} -   type:   PanelBaseExtOpt1 ')

    def getJson(self, customjson={}, dashboard=None, panel=None):
        '''
        Create the json to pack this panel.

        Parameters:
            customjson (dict): custom or child class json code to add
            dashboard (Dashboard): Dashboard object we are in
            panel (Panel_base): Panel object we are in
        Returns:
            dict: panel json code
        '''
        # pylint: disable=unused-argument
        hjson = super().getJson({
            'options'               : {
                'orientation'       : self.orientation,
                'reduceOptions'     : {
                    'calcs'         : self.calcs,
                    'fields'        : self.fields,
                    'values'        : self.reducevalues,
                    'limit'         : self.reducelimit,
                },
            },
        })
        # optional JSON
        if self.titlesize is not None:
            funcs.addJsonItem(hjson, ['options', 'text', 'titleSize'], self.titlesize)
        if self.valuesize is not None:
            funcs.addJsonItem(hjson, ['options', 'text', 'valueSize'], self.valuesize)
        # merge child class JSON
        funcs.deepMerge(hjson, customjson)
        return hjson

#******************************************************************************
# Base Class with some extra properties
@define(slots=False)
class PanelBaseExtOpt2(PanelBaseExtCommon1):
    '''
    Panel subclass with some additional attributes.
    This class will not be called directly, but subclassed to specify a specific type of panel.
    '''
    # logging level of this item
    loglevel           : int = 12
    # attributes
    datalinks          = field( default=Factory(PropLinks),
                                validator=instance_of(PropLinks))
    fillopacity        = field( default=0,
                                validator=instance_of(int))
    gradientmode       = field( default='none',
                                validator=optional(in_(['none', 'opacity', 'hue', 'scheme'])))
    hidefromgraph      = field( default=False,
                                validator=instance_of(bool))
    hidefromlegend     = field( default=False,
                                validator=instance_of(bool))
    hidefromtooltip    = field( default=False,
                                validator=instance_of(bool))
    hidefromviz        = field( default=False,
                                validator=instance_of(bool))
    legend             = field( default=Factory(PropLegend),
                                validator=instance_of(PropLegend))
    linewidth          = field( default=1,
                                validator=instance_of(int))
    tooltipmode        = field( default='single',
                                validator=optional(in_(('single', 'multi', 'none'))))
    tooltipsort        = field( default='none',
                                validator=optional(in_(['none', 'asc', 'desc'])))

     # message
    def __attrs_post_init__(self):
        '''
        Attrs post init, just print a message.
        '''
        print (f'  > Init Panel: {self.title} -   type:   PanelBaseExtOpt2 ')

    def getJson(self, customjson={}, dashboard=None, panel=None):
        '''
        Create the json to pack this panel.

        Parameters:
            customjson (dict): custom or child class json code to add
            dashboard (Dashboard): Dashboard object we are in
            panel (Panel_base): Panel object we are in
        Returns:
            dict: panel json code
        '''
        # pylint: disable=unused-argument
        hjson = super().getJson({
            'fieldConfig'                       : {
                'defaults'                      : {
                    'custom'                    : {
                        'gradientMode'          : self.gradientmode,
                        'hideFrom'              : {
                            'tooltip'           : self.hidefromtooltip,
                            'viz'               : self.hidefromviz,
                            'legend'            : self.hidefromlegend,
                            'graph'            : self.hidefromgraph,
                        },
                        'lineWidth'             : self.linewidth,
                        'fillOpacity'           : self.fillopacity,
                    },
                'links'                         : self.datalinks,
                },
            },
            'options'                           : {
                'legend'                        : self.legend,
                'tooltip'                       : {
                    'mode'                      : self.tooltipmode,
                    'sort'                      : self.tooltipsort,
                }
            },
        })
        # merge child class JSON
        funcs.deepMerge(hjson, customjson)
        return hjson

#******************************************************************************
# EXTRACT FUNCTIONS : EXTRACT A CREATION SCRIPT FROM A JSON
#******************************************************************************
def extractPanelBaseMappings(dset, pset, item):
    '''
    Extract one panel mappings part exported from Grafana to a piece of Python code to be used by this module

    Parameters:
        dset (dict): dict with dashboard settinga and json to extract (is input and output)
        pset (dict): dict with panel settinga and json to extract (is input and output)
        item (dict): json of the mappings to extract
    Returns:
        boolean: True
    '''
    if item != []:
        pset['codeb'].append(f"'{pset['intend']}mappings=PropMappings([\n")
        for i in item:
            htype    = funcs.getJsonItem(i, ['type'], '')
            hoptions = funcs.getJsonItem(i, ['options'], {})
            hvalue   = funcs.getJsonKey(hoptions)
            hfrom    = funcs.getJsonItem(hoptions, ['from'], None)
            hto      = funcs.getJsonItem(hoptions, ['to'], None)
            hregex   = funcs.getJsonItem(hoptions, ['regex'], None)
            hspecial = funcs.getJsonItem(hoptions, ['special'], None)
            htext    = funcs.getJsonItem(hoptions, ['result', 'text'], None)
            hcolor   = funcs.getJsonItem(hoptions, ['result', 'color'], None)
            hresult = ''
            if htext is not None:
                hresult = hresult + f", mtext='{htext}'"
            if hcolor is not None:
                hresult = hresult + f", mcolor='{hcolor}'"
            if htype=='value':
                pset['codeb'].append(f"{pset['intend']}    PropMappingsItem(mvalue='{hvalue}', {hresult}),\n")
            elif htype=='range':
                pset['codeb'].append(f"{pset['intend']}    PropMappingsItem(mfrom={hfrom}, mto={hto}, {hresult}),\n")
            elif htype=='regex':
                pset['codeb'].append(f"{pset['intend']}    PropMappingsItem(mregex='{hregex}', mfrom={hfrom}, mto={hto}, {hresult}),\n")
            elif htype=='special':
                pset['codeb'].append(f"{pset['intend']}    PropMappingsItem(mspecial='{hspecial}', {hresult}),\n")
            else:
                pset['codeb'].append(f"{pset['intend']}    PropMappingsItem(XXX {item} XXX),\n")
        pset['codeb'].append("{pset['intend']}])\n")
    return True

def extractPanelBaseOverrides(dset, pset, item):
    '''
    Extract one panel overrides part exported from Grafana to a piece of Python code to be used by this module

    Parameters:
        dset (dict): dict with dashboard settings and json to extract (is input and output)
        pset (dict): dict with panel settings and json to extract (is input and output)
        item (dict): json of the mappings to extract
    Returns:
        boolean: True
     '''
    # pylint: disable=inconsistent-quotes
    if item != []:
        pset['codeb'].append("{pset['intend']}overrides=PropOverrides([\n")
        for i in item:
            hmtxt = ''
            hptxt = ''
            hmatcher = funcs.getJsonItem(i, ['matcher'], None)
            hprop    = funcs.getJsonItem(i, ['properties'], None)
            if hmatcher is not None:
                hid  = funcs.getJsonItem(hmatcher, ['id'], None)
                hopt = funcs.getJsonItem(hmatcher, ['options'], None)
                if (hid is not None) and (hopt is not None):
                    if hid=='byName':
                        hmtxt = f"oname='{hopt}',"
                    elif hid=='byRegexp':
                        hmtxt = f"oregex='{hopt}',"
                    elif hid=='byType':
                        hmtxt = f"otype='{hopt}',"
                    elif hid=='byFrameRefID':
                        hmtxt = f"oquery='{hopt}',"
                    else:
                        hmtxt = f"TODO matcher '{hmatcher}',"
                else:
                    hmtxt = f"TODO matcher '{hmatcher}',"
            if (hprop is not None and type(hprop)==list):
                hptxt = f"prop={hprop},"
            pset['codeb'].append(f"{pset['intend']}    PropOverridesItem({hmtxt} {hptxt}),\n")
        pset['codeb'].append(f"{pset['intend']}]),\n")
    return True

def extractPanelBaseTresholds(dset, pset, item):
    '''
    Extract one panel thresholds part exported from Grafana to a piece of Python code to be used by this module.
    This also includes the foregroundcolor (fcolor).

    Parameters:
        dset (dict): dict with dashboard settinga and json to extract (is input and output)
        pset (dict): dict with panel settinga and json to extract (is input and output)
        item (dict): json of the mappings to extract
    Returns:
        boolean: True
     '''
    if item != []:
        pset['codeb'].append(f"{pset['intend']}fcolor='{item[0]['color']}',\n")
        item.pop(0)
        if len(item) != 0:
            pset['codeb'].append(f"{pset['intend']}thresholds=PropThresholds([\n")
            for i in item:
                pset['codeb'].append(f"{pset['intend']}    PropThresholdItem('{i['color']}', {i['value']}),\n")
            pset['codeb'].append(f"{pset['intend']}]),\n")
    return True


def extractPanelBase(dset, pset):
    '''
    Extract common properties of one panel exported from Grafana to a piece of Python code to be used by this module

    Parameters:
        dset (dict): dict with dashboard settinga and json to extract (is input and output)
        pset (dict): dict with panel settinga and json to extract (is input and output)
    Returns:
        boolean: True
    '''
    # pylint: disable=inconsistent-quotes
    pset['codeh'].append(f"gridpos=PropGridPos({pset['gridpos']['h']}, {pset['gridpos']['w']}, {pset['gridpos']['x']}, {pset['gridpos']['y']}),\n" \
                       + f"{pset['intend']}datasource={pset['datasource']},\n" \
                       + f"{pset['intend']}targets=[{pset['targets']}],\n")
    # optional properties
    item = funcs.cutJsonItem(pset['json'], ['maxDataPoints'], None)
    if item is not None:
        pset['codeb'].append(f"{pset['intend']}maxdatapoints={item},\n")
    item = funcs.cutJsonItem(pset['json'], ['transparent'], False)
    if item is not False:
        pset['codeb'].append(f"{pset['intend']}transparent={item},\n")
    item = funcs.cutJsonItem(pset['json'], ['timeFrom'], None)
    if item is not None:
        pset['codeb'].append(f"{pset['intend']}timefrom='{item}',\n")
    item = funcs.cutJsonItem(pset['json'], ['timeShift'], None)
    if item is not None:
        pset['codeb'].append(f"{pset['intend']}timeshift='{item}',\n")
    item = funcs.cutJsonItem(pset['json'], ['links'], [])
    if item != []:
        pset['codeb'].append(f"{pset['intend']}links={item},\n")
    item = funcs.cutJsonItem(pset['json'], ['fieldConfig', 'defaults', 'noValue'], '-')
    if item != '-':
        pset['codeb'].append(f"{pset['intend']}novalue='{item}',\n")
    # mappings
    item = funcs.cutJsonItem(pset['json'], ['fieldConfig', 'defaults', 'mappings'], [])
    extractPanelBaseMappings(dset, pset, item)
    # overrides
    item = funcs.cutJsonItem(pset['json'], ['fieldConfig', 'overrides'], [])
    extractPanelBaseOverrides(dset, pset, item)
    return True

#**********************************************************
# some common extracts grouped
def extractCommons1(dset, pset):
    '''
    Extract commons1 subpanel attributes from a panel exported from Grafana to a piece of Python code to be used by this module

    Parameters:
        dset (dict): dict with dashboard settinga and json to extract (is input and output)
        pset (dict): dict with panel settinga and json to extract (is input and output)
    Returns:
        boolean: True
    '''
    # pylint: disable=too-many-branches, too-many-statements, inconsistent-quotes
    # FIELDCONFIG
    item = funcs.cutJsonItem(pset['json'], ['fieldConfig', 'defaults', 'min'], None)
    if item is not None:
        pset['codeb'].append(f"{pset['intend']}min={item},\n")
    item = funcs.cutJsonItem(pset['json'], ['fieldConfig', 'defaults', 'max'], None)
    if item is not None:
        pset['codeb'].append(f"{pset['intend']}max={item},\n")
    item = funcs.cutJsonItem(pset['json'], ['fieldConfig', 'defaults', 'unit'], None)
    if item is not None:
        pset['codeb'].append(f"{pset['intend']}units=\'{item}\',\n")
    item = funcs.cutJsonItem(pset['json'], ['fieldConfig', 'defaults', 'decimals'], None)
    if item is not None:
        pset['codeb'].append(f"{pset['intend']}decimals={item},\n")
    item = funcs.cutJsonItem(pset['json'], ['fieldConfig', 'defaults', 'custom', 'align'], None)
    if item is not None:
        pset['codeb'].append(f"{pset['intend']}align=\'{item}\',\n")
    item = funcs.cutJsonItem(pset['json'], ['fieldConfig', 'defaults', 'custom', 'displayMode'], None)
    if item is not None:
        pset['codeb'].append(f"{pset['intend']}displaymode=\'{item}\',\n")
    item = funcs.cutJsonItem(pset['json'], ['fieldConfig', 'defaults', 'thresholds', 'mode'], None)
    if item is not None:
        pset['codeb'].append(f"{pset['intend']}thresholdmode=\'{item}\',\n")
    # mappings
    item = funcs.cutJsonItem(pset['json'], ['fieldConfig', 'defaults', 'thresholds', 'steps'], [])
    extractPanelBaseTresholds(dset, pset, item)
    # OPTIONS
    item = funcs.cutJsonItem(pset['json'], ['options', 'colorMode'], None)
    if item is not None:
        pset['codeb'].append(f"{pset['intend']}stylecolormode=\'{item}\',\n")
    item = funcs.cutJsonItem(pset['json'], ['options', 'justifyMode'], None)
    if item is not None:
        pset['codeb'].append(f"{pset['intend']}justify=\'{item}\',\n")
    item = funcs.cutJsonItem(pset['json'], ['options', 'orientation'], None)
    if item is not None:
        pset['codeb'].append(f"{pset['intend']}orientation=\'{item}\',\n")
    item = funcs.cutJsonItem(pset['json'], ['options', 'reduceOptions', 'calcs'], [])
    if len(item) != 0:
        pset['codeb'].append(f"{pset['intend']}calcs={item},\n")
    item = funcs.cutJsonItem(pset['json'], ['options', 'reduceOptions', 'fields'], None)
    if item is not None:
        pset['codeb'].append(f"{pset['intend']}fields=\'{item}\',\n")
    item = funcs.cutJsonItem(pset['json'], ['options', 'reduceOptions', 'values'], None)
    if item is not None:
        pset['codeb'].append(f"{pset['intend']}reducevalues=\'{item}\',\n")
    item = funcs.cutJsonItem(pset['json'], ['options', 'reduceOptions', 'limit'], None)
    if item is not None:
        pset['codeb'].append(f"{pset['intend']}reducelimit=\'{item}\',\n")
    item = funcs.cutJsonItem(pset['json'], ['fieldConfig', 'defaults', 'thresholds', 'mode'], None)
    if item is not None:
        pset['codeb'].append(f"{pset['intend']}thresholdmode=\'{item}\',\n")
    return True

#**********************************************************
def extractPanelElse(dset, pset):
    '''
    Extract unknown panel exported from Grafana to a piece of Python code to be used by this module

    Parameters:
        dset (dict): dict with dashboard settinga and json to extract (is input and output)
        pset (dict): dict with panel settinga and json to extract (is input and output)
    Returns:
        boolean: True
    '''
    # pylint: disable=inconsistent-quotes
    pset['codeh'].insert(0, f"{dset['intend']}hdashboard.addPanel(\n" \
                          + f"{dset['intend']}    PanelUNKNOWN(title='{pset['title']}', ")
    # repeatable optional properties
    extractCommons1(dset, pset)
    # function call closing
    pset['codeh'].append(f"{dset['intend']}    )\n"\
                       + f"{dset['intend']})\n")
    return True

#**********************************************************
def extractPanel(dset, paneljson):
    '''
    Extract one panel exported from Grafana to a piece of Python code to be used by this module

    Parameters:
        dset (dict): dict with settinga and json to extract (is input and output)
    Returns:
        boolean: True
    '''
    # pylint: disable=inconsistent-quotes
    # always need to be present
    pset = {
        'json'          : paneljson,
        'type'          : funcs.getJsonItem(paneljson, ['type']),
        'title'         : funcs.getJsonItem(paneljson, ['title'], 'TITLE'),
        'gridpos'       : funcs.cutJsonItem(paneljson, ['gridPos']),
        'datasource'    : dset['datasource'],
        'targets'       : dset['targets'],
        'ver'           : funcs.cutJsonItem(paneljson, ['pluginVersion'], ''),
        'intend'        : ' '*12,
        'codeh'         : [],   # header code
        'codeb'         : [],   # body code
    }
    # print message
    if dset['debuglevel']>10:
        print(f"    - Create Panel:  type: {pset['type']}  -  title: {pset['title']}")
    # remove these
    if dset['removedatasource']:
        funcs.cutJsonItem(pset['json'], ['datasource'], '')
    if dset['removetargets']:
        funcs.cutJsonItem(pset['json'], ['targets'], '')
    #
    extractPanelBase(dset, pset)
    # panel type specific - create the appropriate panel creation script
    plugins   = funcs.getPluginsExtract()
    panelname = pset['type'].replace('-', '_')
    if panelname in plugins:
        module   = f'import grafanacode.plugins.{plugins[panelname]} as pnl'
        function = f'pnl.extractPanel_{panelname}(dset, pset)'
        try:
            exec(module)
            eval(function)
        except ImportError as error:
            print(f'IMPORT {module} FAILED: {error}')
            extractPanelElse(dset, pset)
    else:
        extractPanelElse(dset, pset)
    # add panel code to dashboard
    dset['coded'].append(''.join(pset['codeh']) + ''.join(pset['codeb']))
    dset['coded'].append(f"\nREST:\n{paneljson}\n\n")
    return True
