# panel_plotly_windrose.py
# V0.5.0 LDO 19/10/2022: initial version
# V0.5.1 LDO 12/11/2022: refactor modules
# V0.6.1 LDO 17/12/2022: release candidate 1
'''
    grafanacode:
    class for generating ae3e-plotly windrose panels

    This class is derived from PanelPlotly.

    Mind the ``EXTRACTCHILDCLASS = True`` at the end of the file,
    This is needed for a derived class to prevent the base class method to be hidden while extracting panels.
'''

#******************************************************************************
# EXTERNAL MODULE REFERENCES
#******************************************************************************
import textwrap

from attrs           import define, field, Factory
from attr.validators import in_, instance_of, optional, deep_iterable

from grafanacode         import funcs
from grafanacode.plugins import panel_base
from grafanacode.plugins import panel_plotly

#******************************************************************************
# Panel Property classes: store panel property configuration parts
#******************************************************************************

#******************************************************************************
# Panel Class
#******************************************************************************
@define(slots=False)
class PanelPlotlyWindrose(panel_plotly.PanelPlotly):
    '''
    Dataclass encapsulating a windrose panel based on the ae3e plotly panel
    '''
    # logging level of this item
    loglevel           : int = 16
    # attributes
    scriptpre          = field( default='',
                                validator=instance_of(str))
    scriptpost         = field( default='',
                                validator=instance_of(str))

    # message
    def __attrs_post_init__(self):
        '''
        Attrs post init, print a message.

        Also subclass code
        '''
        print (f'  > Init Panel: {self.title} - type: PanelPlotlyWindrose ')
        self.script = textwrap.dedent('''
                    // some vars
                    var i, j, k, dir, spd;
                    // get data
                    console.log(data);
                    if (data.state!="Done") {    // retuns 2 times, once "Loading", once "Done"
                      return JSON.parse('[{"type": "barpolar"}, {"type": "barpolar"}]');
                    }
                    //***** original data
                    // direction
                    var dir_raw = data.series[0].fields[1].values.buffer;
                    var n_dir_raw = dir_raw.length;
                    console.log("dir"); console.log(dir_raw); console.log(n_dir_raw);
                    // speed
                    var spd_raw = data.series[1].fields[1].values.buffer;
                    var n_spd_raw = spd_raw.length;
                    console.log("speed"); console.log(spd_raw); console.log(n_spd_raw);
                    //***** some strings, arrays
                    var spdtrips = [2, 4, 6, 10, 15, 20, 30, 40, 60, 80, 100];
                    var n_spdtrips = spdtrips.length;
                    var dirtrips = [22.5, 67.5, 112.5, 157.5, 202.5, 247.5, 292.5, 337.5, 361];
                    var n_dirtrips = dirtrips.length;
                    let dirnames = '["Noord", "NO", "Oost", "ZO", "Zuid", "ZW", "West", "NW"]';
                    let spdcolors = ['"#0033ff"', '"#29b6f6"', '"#00ff00"', '"#bfff00"', '"#dce775"', '"#ffff00"', '"#ffb74d"', '"#ff8000"', '"#ff9999"', '"#ff0000"', '"#6a1b9a"'];
                    let spdnames = ['"0<"', '"2<"', '"4<"', '"6<"', '"10<"', '"15<"', '"20<"', '"30<"', '"40<"', '"60<"', '"80<"', '"100<"'];
                    //***** create bins from data
                    var bins = [];  // array [speed][dir]
                    for (i = 0; i < n_spdtrips; i++){
                      bins.push([]);
                      for (j = 0; j < n_dirtrips; j++){
                        bins[i].push(0);
                      }
                    }
                    //***** Loop through data and add correct bin
                    for (i = 0; i < n_dir_raw; i++) {
                      dir = dir_raw[i];
                      spd = spd_raw[i];
                    loops:
                      for (j = 0; j < n_spdtrips; j++) {
                        if (spd < spdtrips[j]) {
                          for (k = 0; k < n_dirtrips; k++) {
                            if (dir < dirtrips[k]) {
                              bins[j][k]++;
                              break loops;
                            }
                          }
                        }
                      }
                    }
                    // merge first and last dir (0-22.5° and 337.5-0°)
                    for (i = 0; i < n_spdtrips; i++) {
                      bins[i][0] = bins[i][0] + bins[i][n_dirtrips-1];
                      bins[i].pop();
                    }
                    // numbers to percent
                    for (i = 0; i < n_spdtrips; i++) {
                      for (j = 0; j < n_dirtrips - 1; j++) {
                        bins[i][j] = bins[i][j] / n_dir_raw * 100;
                      }
                    }
                    console.log("final"); console.log(n_dirtrips); console.log(bins);
                    // format uitput
                    var series = "[";
                    for (i = 0; i < n_spdtrips; i++) {
                      series = series + '{"r" : [' + bins[i] + '], "theta" : ' + dirnames + ', "name" : ' + spdnames[i] + ', "marker" : {"color" : ' + spdcolors[i] + '}, "type": "barpolar"}';
                      if (i < n_spdtrips-1) {
                        series = series + ',';
                      } else {
                        series = series + ']';
                      }
                    }
                    var seriesjson = JSON.parse(series);
                    console.log(seriesjson);
                    return {data : seriesjson};
                    ''')
        self.clickscript=''
        self.configuration={'displayModeBar': False}
        self.layout={
            'font': {'color': 'white', 'size': 16},
            'legend': {'font': {'size': 16}},
            'margin': {'b': 30, 't': 30},
            'paper_bgcolor': '#141619',
            'plot_bgcolor': '#141619',
            'polar': {
                'angularaxis': {
                    'color': 'lightgrey',
                    'direction': 'clockwise',
                    'rotation': 90,
                    'tickcolor': 'white',
                    'tickfont': {'color': 'white', 'size': 14},
                    'ticklen': 10,
                    'ticks': 'outside',
                    'type': 'category'
                },
                'bargap': 3,
                'barmode': 'stack',
                'barnorm': 'percent',
                'bgcolor': 'black',
                'radialaxis': {
                    'angle': 45,
                    'autorange': True,
                    'color': 'lightgrey',
                    'dtick': 10,
                    'range': [0, 25.694001093848453],
                    'tick0': 0,
                    'tickangle': 90,
                    'tickcolor': 'white',
                    'tickfont': {'color': 'white', 'size': 10},
                    'ticklen': 10,
                    'tickmode': 'linear',
                    'ticks': 'outside',
                    'ticksuffix': '%',
                    'type': 'linear'
                },
            },
            'xaxis': {'autorange': True, 'type': 'date'},
            'type': 'scatter',
        }

    def getJson(self, customjson={}, dashboard=None, panel=None):
        '''
        Create the json to pack this panel.

        Parameters:
            customjson (dict): custom or child class json code to add
        Returns:
            dict: panel json code
        '''
        # pylint: disable=unused-argument
        hjson = super().getJson()
        if self.scriptpre!= '':
            hjson['options']['script'] = self.scriptpre + '\r\n' + hjson['options']['script']
        if self.scriptpost!= '':
            hjson['options']['script'] = hjson['options']['script'] + '\r\n' + self.scriptpre
        funcs.deepMerge(hjson, customjson)
        return hjson

#******************************************************************************
# EXTRACT FUNCTIONS : EXTRACT A CREATION SCRIPT FROM A JSON
#******************************************************************************
# needed, otherwise base class method can be hidden
EXTRACTCHILDCLASS = True
