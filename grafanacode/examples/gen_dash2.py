# gen_dash2.py
# V0.5.1 LDO 11/12/2022: initial version
'''
    demo to create and upload a dashboard with use of targetbag class
'''

#******************************************************************************
# EXTERNAL MODULE REFERENCES
#******************************************************************************
import sys
sys.path.insert(0, '/prj/dev_pc/grafana/grc_module')
from grafanacode  import *
import cfg        as CFG

#******************************************************************************
# GLOBALS
#******************************************************************************
DEBUGLEVEL         = 99
DEBUG_PRINTPLUGINS = False

#******************************************************************************
# Define some general settings
def define_settings():
    '''
        Some settings can be made once for the hole project and reused.
        
        Good examples are foreground color and thresholds.
    '''
    d_set= {
        'fcolor'      : 'yellow',
        'thresholds'  : {
            'pressure': PropThresholds([
                PropThresholdsItem('dark-blue',             None),
                PropThresholdsItem('light-blue',            10),
                PropThresholdsItem('light-green',           20),
                PropThresholdsItem('dark-green',            30),
                PropThresholdsItem('super-light-yellow',    40),
                PropThresholdsItem('yellow',                55),
                PropThresholdsItem('orange',                60),
                PropThresholdsItem('dark-orange',           70),
                PropThresholdsItem('red',                   80),
                PropThresholdsItem('dark-red',              90),
            ]),
            'temperature': PropThresholds([
                PropThresholdsItem('dark-blue',             None),
                PropThresholdsItem('light-blue',            0),
                PropThresholdsItem('super-light-blue',      10),
                PropThresholdsItem('super-light-green',     20),
                PropThresholdsItem('light-green',           30),
                PropThresholdsItem('semi-dark-green',       40),
                PropThresholdsItem('super-light-yellow',    55),
                PropThresholdsItem('yellow',                60),
                PropThresholdsItem('semi-dark-orange',      75),
                PropThresholdsItem('semi-dark-red',         90),
            ]),
        }
    }
    return d_set

#******************************************************************************
# Define queries
def define_queries():
    # pylint: disable=inconsistent-quotes
    targets = TargetBag()
    # add grafana datasource, here we use internal grafana datasource, to use the random walk
    targets.addDatasource('grafana', {'uid': 'grafana', 'type': 'datasource'})
    #********************************************
    # target for gauge: use built in random walk query
    targets.addTarget('demo', 'tgpress', {"refId": "A", "datasource": {"type": "datasource", "uid": "grafana"}, "queryType": "randomWalk"})
    # target for gauge: use built in random walk query
    #  here it was not necessary to create a second query
    #  because it is the same of the previous one, this could be reused
    #  but it is just an example creating some queries
    targets.addTarget('demo', 'tgtemp', {"refId": "A", "datasource": {"type": "datasource", "uid": "grafana"}, "queryType": "randomWalk"})
    # real live example from an InfluxDB source, not used in the panels
    #  here just as an example
    targets.addTarget('demo', 'some other', TargetInfluxDB(b='tst01', q=textwrap.dedent('''
        |> filter(fn: (r) => r["_measurement"] == "notification")
        |> drop(columns: ["_measurement", "_status"])
        |> group(columns: ["_result"])
        |> drop(columns: ["_value", "_start", "_stop", "_field"])
        ''')))
    return targets

#******************************************************************************
# Define dashboards
def d_demo2(d_set, d_tgt):
    # create dashboards
    print('** CREATE DASHBOARD: dash2')
    # DASHBOARD
    hdashboard = Dashboard(
        filename='d_dash2',                                 # name of the file if we save the dashboard
        title='Dash 2',                                     # dashboard title
        description='demo dashboard',                       # dashboard description
        refresh='5s'                                        # auto refresh the dashboard (to see the color variations)
    )
    # PANELS
    # add a text panel
    hdashboard.addPanel(                                    # add a panel to the dashboard
        PanelText(                                          # it is a text panel
            title='DASHBOARD TITLE',                        # panel title
            gridpos=PropGridPos(5, 16, 0, 0),               # panel size and position (h, w, x, y)
            content=textwrap.dedent('''# AtHome
                                         Multiline
                                        Home Dashboard'''), # specific for this panel: add the content
        )
    )
    # add a gauge panel
    hdashboard.addPanel(                                    # add a panel to the dashboard
        PanelGauge(                                         # it is a gauge panel
            title='Pressure',                               # panel title
            gridpos=PropGridPos(5, 3, 5, 5),                # panel size and position (h, w, x, y)
            datasource=d_tgt.getDatasource('grafana'),      # data source
            targets=[d_tgt.getTarget('demo', 'tgpress')],   # panel query
            min=0,                                          # gauge min
            max=100,                                        # gauge max
            decimals=1,                                     # precision
            units='bar',                                    # units to display
            fcolor=d_set['fcolor'],                         # foreground color, from settings
            thresholds=d_set['thresholds']['pressure'],     # threshold colors, from settings

        )
    )
    # add stat panel
    hdashboard.addPanel(                                    # add a panel to the dashboard
        PanelStat(                                          # it is a stat panel
            title='Temperature',                            # panel title
            gridpos=PropGridPos(8, 5, 10, 5),               # panel size and position (h, w, x, y)
            datasource=d_tgt.getDatasource('grafana'),      # data source
            targets=[d_tgt.getTarget('demo', 'tgtemp')],    # panel query
            units=UNITS.CELSIUS,                            # units to display from the UNITS file
            fcolor=d_set['fcolor'],                         # foreground color, from settings
            graphmode='area',                               # also display a small graph in the stat panel
            thresholds=d_set['thresholds']['temperature'],  # threshold colors, from settings
        )
    )
    return hdashboard
    
#******************************************************************************
# MAIN
#******************************************************************************
if __name__ == '__main__':
    # print available plugins
    if DEBUG_PRINTPLUGINS:
        printPlugins()
    # DEFINE SETTINS
    d_set = define_settings()
    # DEFINE TARGETS
    d_tgt = define_queries()
    # DEFINE DASHBOARD(S)
    d_dash = (d_demo2(d_set, d_tgt))
    # GENERATE
    d_dash.getDashboardJson(overwrite=True, debuglevel=DEBUGLEVEL) # generate the JSON
    # SAVE, make sure map does exist
    dashboardpath = './demo_output/'
    with open(dashboardpath + d_dash.filename, 'w', encoding='utf-8') as outfile:
        outfile.write(d_dash.d_json)        # save to a file
    # UPLOAD, use correct server and credentials
    uploadDashboardToGrafana(d_dash.d_json, CFG.GRAFANA_SERVER, CFG.GRAFANA_USER, CFG.GRAFANA_PWD)
