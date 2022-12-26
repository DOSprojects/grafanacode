# panel_boomtable.py
# V0.5.0 LDO 19/10/2022: initial version
# V0.5.1 LDO 12/11/2022: refactor modules
# V0.6.1 LDO 17/12/2022: release candidate 1
'''
    grafanacode:
    class for generating yesoreyeram-boomtable panels
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
class PropBoomtableTimeBasedThresholdsItem:
    '''
    Dataclass encapsulating a TimeBasedThresholds item
    '''
    # logging level of this item
    loglevel           : int = 21
    # attributes
    enableddays        = field( default='Sun,Mon,Tue,Wed,Thu,Fri,Sat',
                                validator=instance_of(str))
    hourfrom           = field( default='0000',
                                validator=instance_of(str))
    name               = field( default='tb01',
                                validator=instance_of(str))
    threshold          = field( default='70,90',
                                validator=instance_of(str))
    hourto             = field( default='0530',
                                validator=instance_of(str))

    def getJson(self, dashboard=None, panel=None):
        '''
        Create the json to pack this item.

        Returns:
            dict: panel json code
        '''
        # pylint: disable=unused-argument
        hjson = {
            'enabledDays'   : self.enableddays,
            'from'          : self.hourfrom,
            'name'          : self.name,
            'threshold'     : self.threshold,
            'to'            : self.hourto,
        }
        return hjson

#**********************************************************
# Boomtable
@define(slots=False)
class PropBoomtablePatternsItem:
    '''
    Dataclass encapsulating a PatternsItem item
    '''
    # logging level of this item
    loglevel                   : int = 21
    # attributes
    bgcolors                   = field( default='green|orange|red',
                                        validator=instance_of(str))
    bgcolorsoverrides          = field( default='0->green|2->red|1->yellow',
                                        validator=instance_of(str))
    clickablecellslink         = field( default='',
                                        validator=instance_of(str))
    colname                    = field( default='Value',
                                        validator=instance_of(str))
    decimals                   = field( default=2,
                                        validator=instance_of(int))
    defaultbgcolor             = field( default='transparent',
                                        validator=instance_of(str))
    defaulttextcolor           = field( default='',
                                        validator=instance_of(str))
    delimiter                  = field( default='.',
                                        validator=instance_of(str))
    displaytemplate            = field( default='_value_',
                                        validator=instance_of(str))
    enablebgcolor              = field( default=False,
                                        validator=instance_of(bool))
    enablebgcoloroverrides     = field( default=False,
                                        validator=instance_of(bool))
    enableclickablecells       = field( default=False,
                                        validator=instance_of(bool))
    enabletextcolor            = field( default=False,
                                        validator=instance_of(bool))
    enabletextcoloroverrides   = field( default=False,
                                        validator=instance_of(bool))
    enabletimebasedthresholds  = field( default=False,
                                        validator=instance_of(bool))
    enabletransform            = field( default=False,
                                        validator=instance_of(bool))
    enabletransformoverrides   = field( default=False,
                                        validator=instance_of(bool))
    filtervalueabove           = field( default='',
                                        validator=instance_of(str))
    filtervaluebelow           = field( default='',
                                        validator=instance_of(str))
    format                     = field( default='none',
                                        validator=instance_of(str))
    name                       = field( default='Default Pattern',
                                        validator=instance_of(str))
    nullcolor                  = field( default='darkred',
                                        validator=instance_of(str))
    nulltextcolor              = field( default='black',
                                        validator=instance_of(str))
    nullvalue                  = field( default='No data',
                                        validator=instance_of(str))
    pattern                    = field( default='*',
                                        validator=instance_of(str))
    rowcolwrapper              = field( default='_',
                                        validator=instance_of(str))
    rowname                    = field( default='_series_',
                                        validator=instance_of(str))
    textcolors                 = field( default='red|orange|green',
                                        validator=instance_of(str))
    textcolorsoverrides        = field( default='0->red|2->green|1->yellow',
                                        validator=instance_of(str))
    thresholds                 = field( default='70,90',
                                        validator=instance_of(str))
    timebasedthresholds        = field( default=Factory(list),
                                        validator=deep_iterable(
                                            member_validator=instance_of(PropBoomtableTimeBasedThresholdsItem),
                                            iterable_validator=instance_of(list)))
    tooltiptemplate            = field( default='Series : _series_ <br/>Row Name : _row_name_ <br/>Col Name : _col_name_ <br/>Value : _value_',
                                        validator=instance_of(str))
    transformvalues            = field( default='_value_|_value_|_value_',
                                        validator=instance_of(str))
    transformvaluesoverrides   = field( default='0->down|1->up',
                                        validator=instance_of(str))
    valuename                  = field( default='avg',
                                        validator=instance_of(str))



    def getJson(self, dashboard=None, panel=None):
        '''
        Create the json to pack this item.

        Returns:
            dict: panel json code
        '''
        # pylint: disable=unused-argument
        hjson = {
            'bgColors'                      : self.bgcolors,
            'bgColors_overrides'            : self.bgcolorsoverrides,
            'clickable_cells_link'          : self.clickablecellslink,
            'col_name'                      : self.colname,
            'decimals'                      : self.decimals,
            'defaultBGColor'                : self.defaultbgcolor,
            'defaultTextColor'              : self.defaulttextcolor,
            'delimiter'                     : self.delimiter,
            'displayTemplate'               : self.displaytemplate,
            'enable_bgColor'                : self.enablebgcolor,
            'enable_bgColor_overrides'      : self.enablebgcoloroverrides,
            'enable_clickable_cells'        : self.enableclickablecells,
            'enable_textColor'              : self.enabletextcolor,
            'enable_textColor_overrides'    : self.enabletextcoloroverrides,
            'enable_time_based_thresholds'  : self.enabletimebasedthresholds,
            'enable_transform'              : self.enabletransform,
            'enable_transform_overrides'    : self.enabletransformoverrides,
            'filter'                        : {
              'value_above'                 : self.filtervalueabove,
              'value_below'                 : self.filtervaluebelow,
            },
            'format'                        : self.format,
            'name'                          : self.name,
            'null_color'                    : self.nullcolor,
            'null_textcolor'                : self.nulltextcolor,
            'null_value'                    : self.nullvalue,
            'pattern'                       : self.pattern,
            'row_col_wrapper'               : self.rowcolwrapper,
            'row_name'                      : self.rowname,
            'textColors'                    : self.textcolors,
            'textColors_overrides'          : self.textcolorsoverrides,
            'thresholds'                    : self.thresholds,
            'time_based_thresholds'         : self.timebasedthresholds,
            'tooltipTemplate'               : self.tooltiptemplate,
            'transform_values'              : self.transformvalues,
            'transform_values_overrides'    : self.transformvaluesoverrides,
            'valueName'                     : self.valuename,
       }
        return hjson

#******************************************************************************
# Panel Class
#******************************************************************************
@define(slots=False)
class PanelBoomTable(panel_base.PanelBase):
    '''
    Dataclass encapsulating a boomtable panel
    '''
    # logging level of this item
    loglevel                   : int = 15
    # attributes
    activepatternindex          = field(default=0,
                                        validator=instance_of(int))
    defaultpattern              = field(default=Factory(PropBoomtablePatternsItem),
                                        validator=instance_of(PropBoomtablePatternsItem))
    defaultrowtitle             = field(default='Metric',
                                        validator=instance_of(str))
    patterns                    = field(default=Factory(list),
                                        validator=deep_iterable(
                                                    member_validator=instance_of(PropBoomtablePatternsItem),
                                                    iterable_validator=instance_of(list)))
    rowcolwrapper               = field(default='_',
                                        validator=instance_of(str))
    sortingcolindex             = field(default=-1,
                                        validator=instance_of(int))
    sortingdirection            = field(default='asc',
                                        validator=in_(('asc', 'desc')))
    nonmatchingcellstext        = field(default='',
                                        validator=instance_of(str))
    firstcolumnlink             = field(default='',
                                        validator=instance_of(str))
    fontsize                    = field(default='',
                                        validator=instance_of(str))
    alignmentfirstcolumn        = field(default='left',
                                        validator=optional(in_(('left', 'center', 'right'))))
    alignmentvalues             = field(default='left',
                                        validator=optional(in_(('left', 'center', 'right'))))
    alignmentheader             = field(default='left',
                                        validator=optional(in_(('left', 'center', 'right'))))
    hideheaders                 = field(default=False,
                                        validator=instance_of(bool))
    hidefirstcolumn             = field(default=False,
                                        validator=instance_of(bool))
    debugmode                   = field(default=False,
                                        validator=instance_of(bool))
    nonmatchingcellscolorbg     = field(default='',
                                        validator=instance_of(str))
    nonmatchingcellscolortext   = field(default='',
                                        validator=instance_of(str))

    # message
    def __attrs_post_init__(self):
        '''
        Attrs post init, just print a message.
        '''
        print (f'  > Init Panel: {self.title} - type: PanelBoomTable ')

    def getJson(self, customjson={}, dashboard=None, panel=None):
        '''
        Create the json to pack this panel.

        Parameters:
            customjson (dict): custom or child class json code to add
        Returns:
            dict: panel json code
        '''
        hjson = super().getJson(
            {
                'activePatternIndex'            : self.activepatternindex,
                'defaultPattern'                : self.defaultpattern,
                'default_title_for_rows'        : self.defaultrowtitle,
                'patterns'                      : [],
                'row_col_wrapper'               : self.rowcolwrapper,
                'sorting_props'                 : {
                    'col_index'                 : self.sortingcolindex,
                    'direction'                 : self.sortingdirection,
                },
                'non_matching_cells_text'       : self.nonmatchingcellstext,
                'first_column_link'             : self.firstcolumnlink,
                'font_size'                     : self.fontsize,
                'text_alignment_firstcolumn'    : self.alignmentfirstcolumn,
                'text_alignment_values'         : self.alignmentvalues,
                'text_alignment_header'         : self.alignmentheader,
                'hide_headers'                  : self.hideheaders,
                'hide_first_column'             : self.hidefirstcolumn,
                'debug_mode'                    : self.debugmode,
                'non_matching_cells_color_bg'   : self.nonmatchingcellscolorbg,
                'non_matching_cells_color_text' : self.nonmatchingcellscolortext,


                'type'          : 'yesoreyeram-boomtable-panel',
            }
        )
        funcs.deepMerge(hjson, customjson)
        return hjson

#******************************************************************************
# EXTRACT FUNCTIONS : EXTRACT A CREATION SCRIPT FROM A JSON
#******************************************************************************
# pylint: disable=invalid-name
def extractPanel_yesoreyeram_boomtable_panel(dset, pset):
    '''
    Extract a panel exported from Grafana to a piece of Python code to be used by this module

    Parameters:
        dset (dict): dict with dashboard settinga and json to extract (is input and output)
        pset (dict): dict with panel settinga and json to extract (is input and output)
    Returns:
        boolean: True
    '''
    pset['codeh'].insert(0, f"{dset['intend']}hdashboard.addPanel(\n" \
                          + f"{dset['intend']}    PanelBoomTable(title='{pset['title']}', ")
    # repeatable optional properties
    panel_base.extractCommons1(dset, pset)
    # optional properties
    # function call closing
    pset['codeb'].append(f"{dset['intend']}    )\n"\
                       + f"{dset['intend']})\n")
    return True
