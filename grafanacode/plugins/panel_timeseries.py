# panel_timeseries.py
# V0.5.0 LDO 19/10/2022: initial version
# V0.5.1 LDO 12/11/2022: refactor modules
# V0.6.1 LDO 17/12/2022: release candidate 1
'''
    grafanacode:
    class for generating timeseries panels
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
class PanelTimeSeries(panel_base.PanelBaseExtOpt2):
    '''
    Dataclass encapsulating a timeseries panel
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
    axissoftmax       = field( default=None,
                                validator=optional(instance_of((int, float))))
    axissoftmin       = field( default=None,
                                validator=optional(instance_of((int, float))))
    axiswidth          = field( default=None,
                                validator=optional(instance_of(int)))
    baralignment       = field( default=0,
                                validator=optional(in_((-1, 0, 1))))  #-1=before, 0=centre, 1=after
    drawstyle          = field( default='line',
                                validator=optional(in_(('line', 'bars', 'points'))))
    linedash1          = field( default=10,
                                validator=instance_of(int))
    linedash2          = field( default=10,
                                validator=instance_of(int))
    lineinterpolation  = field( default='linear',
                                validator=optional(in_(('linear', 'smooth', 'stepBefore', 'stepAfter'))))
    linestyle          = field( default='solid',
                                validator=optional(in_(('solid', 'dash', 'dot'))))
    pointsize          = field( default=5,
                                validator=instance_of(int))
    scaletype          = field(default='linear',
                                validator=optional(in_(('linear', 'log'))))
    scalelog           = field(default=2,
                                validator=optional(in_((2, 10))))
    showpoints         = field( default='never',
                                validator=optional(in_(('auto', 'always', 'never'))))
    spannulls          = field( default=True,
                                validator=instance_of((bool, int)))
    stackingmode       = field( default='none',
                                validator=in_(('none', 'normal', 'percent')))
    stackinggroup      = field( default='A',
                                validator=instance_of(str))
    thresholdsstyle    = field( default='off',
                                validator=in_(('off', 'line', 'area', 'line+area')))

    # message
    def __attrs_post_init__(self):
        '''
        Attrs post init, just print a message.
        '''
        print (f'  > Init Panel: {self.title} - type: PanelTimeSeries ')

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
                        'barAlignment'          : self.baralignment,
                        'drawStyle'             : self.drawstyle,
                        'lineInterpolation'     : self.lineinterpolation,
                        'lineStyle'             : {
                            'fill'              : self.linestyle,
                            'dash'              : [self.linedash1, self.linedash2],
                        },
                        'pointSize'             : self.pointsize,
                        'showPoints'            : self.showpoints,
                        'spanNulls'             : self.spannulls,
                        'stacking'              : {
                            'mode'              : self.stackingmode,
                            'group'             : self.stackinggroup,
                        },
                        'scaleDistribution':    {
                            'type'              : self.scaletype,
                            'log'               : self.scalelog,
                        },
                        'thresholdsStyle'       : {
                        'mode'                  : self.thresholdsstyle,
                        },
                    },
                },
            },
            'type'                              : 'timeseries',
        })
        #
        # merge child class JSON
        funcs.deepMerge(hjson, customjson)
        return hjson

#******************************************************************************
# EXTRACT FUNCTIONS : EXTRACT A CREATION SCRIPT FROM A JSON
#******************************************************************************
# pylint: disable=invalid-name
def extractPanel_timeseries(dset, pset):
    '''
    Extract a panel exported from Grafana to a piece of Python code to be used by this module

    Parameters:
        dset (dict): dict with dashboard settings and json to extract (is input and output)
        pset (dict): dict with panel settings and json to extract (is input and output)
    Returns:
        boolean: True
    '''
    pset['codeh'].insert(0, f"{dset['intend']}hdashboard.addPanel(\n" \
                          + f"{dset['intend']}    PanelTimeSeries(title='{pset['title']}', ")
    # repeatable optional properties
    panel_base.extractCommons1(dset, pset)
    # optional properties
    # function call closing
    pset['codeb'].append(f"{dset['intend']}    )\n"\
                       + f"{dset['intend']})\n")
    return True
