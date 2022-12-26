# panel_barchart.py
# V0.5.0 LDO 19/10/2022: initial version
# V0.5.1 LDO 12/11/2022: refactor modules
# V0.6.1 LDO 17/12/2022: release candidate 1
'''
    grafanacode:
    class for generating barchart panels
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
class PanelBarChart(panel_base.PanelBaseExtOpt2):
    '''
    Dataclass encapsulating a barchart panel
    '''
    # logging level of this item
    loglevel           : int = 15
    # attributes
    axisgridshow       = field( default=True,
                                validator=instance_of(bool))
    axislabel          = field( default='',
                                validator=instance_of(str))
    axisplacement      = field( default='auto',
                                validator=optional(in_(('auto', 'left', 'right', 'hidden'))))
    axissoftmax        = field( default=None,
                                validator=optional(instance_of((int, float))))
    axissoftmin        = field( default=None,
                                validator=optional(instance_of((int, float))))
    axiswidth          = field( default=None,
                                validator=optional(instance_of(int)))
    barwidth           = field( default=0.97,
                                validator=instance_of(float)) # 0 to 1
    barradius          = field( default=0,
                                validator=instance_of(float)) # 0 to 0.5
    colorbyfield       = field( default=None,
                                validator=optional(instance_of(str)))
    groupwidth         = field( default=0.7,
                                validator=instance_of(float))
    scaletype          = field( default='linear',
                                validator=optional(in_(('linear', 'log'))))
    scalelog           = field( default=2,
                                validator=optional(in_((2, 10))))
    showvalue          = field( default='auto',
                                validator=in_(('auto', 'always', 'never')))
    stackingmode       = field( default='none',
                                validator=in_(('none', 'normal', 'percent')))
    stackinggroup      = field( default='A',
                                validator=instance_of(str))
    xfield             = field( default=None,
                                validator=optional(instance_of(str)))
    xlabellength       = field( default=None,
                                validator=optional(instance_of(int)))
    xlabelrotation     = field( default=0,
                                validator=in_((-90, -45, 0, 45, 90)))
    xlabelspacing      = field( default=0,
                                validator=in_((-300, -200, -100, 0, 100, 200, 300)))

    # message
    def __attrs_post_init__(self):
        '''
        Attrs post init, just print a message.
        '''
        print (f'  > Init Panel: {self.title} - type: PanelBarChart ')

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
            'fieldConfig'                       : {
                'defaults'                      : {
                    'color'                     : {
                        'mode'                  : self.colorscheme,
                    },
                    'custom'                    : {
                        'axisGridShow'          : self.axisgridshow,
                        'axisLabel'             : self.axislabel,
                        'axisPlacement'         : self.axisplacement,
                        'axisSoftMax'           : self.axissoftmax,
                        'axisSoftMin'           : self.axissoftmin,
                        'axisWidth'             : self.axiswidth,
                        'scaleDistribution':    {
                            'type'              : self.scaletype,
                            'log'               : self.scalelog,
                        },
                    },
                },
            },
            'options'                           : {
                'xField'                        : self.xfield,
                'xTickLabelMaxLength'           : self.xlabellength,
                'xTickLabelRotation'            : self.xlabelrotation,
                'xTickLabelSpacing'             : self.xlabelspacing,
                'barWidth'                      : self.barwidth,
                'barRadius'                     : self.barradius,
                'colorByField'                  : self.colorbyfield,
                'groupWidth'                    : self.groupwidth,
                'showValue'                     : self.showvalue,
                'stacking'                      : {
                    'mode'                      : self.stackingmode,
                    'group'                     : self.stackinggroup,
                },

            },
            'type'                              : 'barchart',
        })
        #
        # merge child class JSON
        funcs.deepMerge(hjson, customjson)
        return hjson

#******************************************************************************
# EXTRACT FUNCTIONS : EXTRACT A CREATION SCRIPT FROM A JSON
#******************************************************************************
# pylint: disable=invalid-name
def extractPanel_barchart(dset, pset):
    '''
    Extract a panel exported from Grafana to a piece of Python code to be used by this module

    Parameters:
        dset (dict): dict with dashboard settings and json to extract (is input and output)
        pset (dict): dict with panel settings and json to extract (is input and output)
    Returns:
        boolean: True
    '''
    pset['codeh'].insert(0, f"{dset['intend']}hdashboard.addPanel(\n" \
                          + f"{dset['intend']}    PanelBarChart(title='{pset['title']}', ")
    # repeatable optional properties
    panel_base.extractCommons1(dset, pset)
    # optional properties
    # function call closing
    pset['codeb'].append(f"{dset['intend']}    )\n"\
                       + f"{dset['intend']})\n")
    return True
