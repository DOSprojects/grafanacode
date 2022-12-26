# panel_plotly.py
# V0.5.0 LDO 19/10/2022: initial version
# V0.5.1 LDO 12/11/2022: refactor modules
# V0.6.1 LDO 17/12/2022: release candidate 1
'''
    grafanacode:
    class for generating ae3e-plotly panels
'''

#******************************************************************************
# EXTERNAL MODULE REFERENCES
#******************************************************************************
import textwrap

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
class PanelPlotly(panel_base.PanelBase):
    '''
    Dataclass encapsulating a ae3e plotly panel
    '''
    # logging level of this item
    loglevel           : int = 15
    # attributes
    configuration      = field( default=Factory(dict),
                                validator=instance_of(dict))
    data               = field( default=Factory(str),
                                validator=instance_of(str))
    layout             = field( default=Factory(dict),
                                validator=instance_of(dict))
    script             = field( default=textwrap.dedent("""
                                    console.log(data)
                                    var trace = {
                                      x: data.series[0].fields[0].values.buffer,
                                      y: data.series[0].fields[1].values.buffer
                                    };
                                    return {data:[trace],layout:{title:'My Chart'}};"""),
                                validator=instance_of(str))
    clickscript        = field( default='',
                                validator=instance_of(str))

    # message
    def __attrs_post_init__(self):
        '''
        Attrs post init, just print a message.
        '''
        print (f'  > Init Panel: {self.title} - type: PanelPlotly ')

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
                'fieldConfig'           : {
                    'defaults'          : {},
                    'overrides'         : []
                },
                'options': {
                    'configuration'     : {},
                    'data'              : self.data,
                    'layout'            : self.layout,
                    'onclick'           : self.clickscript,
                    'script'            : self.script,
                },
                'type'                  : 'ae3e-plotly-panel',
            }
        )
        funcs.deepMerge(hjson, customjson)
        return hjson

#******************************************************************************
# EXTRACT FUNCTIONS : EXTRACT A CREATION SCRIPT FROM A JSON
#******************************************************************************
# pylint: disable=invalid-name
def extractPanel_ae3e_plotly_panel(dset, pset):
    '''
    Extract a panel exported from Grafana to a piece of Python code to be used by this module

    Parameters:
        dset (dict): dict with dashboard settings and json to extract (is input and output)
        pset (dict): dict with panel settings and json to extract (is input and output)
    Returns:
        boolean: True
    '''
    pset['codeh'].insert(0, f"{dset['intend']}hdashboard.addPanel(\n" \
                          + f"{dset['intend']}    PanelPlotly(title='{pset['title']}', ")
    # optional properties
    # function call closing
    pset['codeb'].append(f"{dset['intend']}    )\n"\
                       + f"{dset['intend']})\n")
    return True
