# gen_dash1.py
# V0.5.1 LDO 11/12/2022: initial version
'''
    basic demo to create and upload a dashboard
'''

#******************************************************************************
# EXTERNAL MODULE REFERENCES
#******************************************************************************
import sys
sys.path.insert(0, '/prj/dev_pc/grafana/grc_module')
from   grafanacode  import *
import cfg          as CFG

#******************************************************************************
# GLOBALS
#******************************************************************************
DEBUGLEVEL         = 99
DEBUG_PRINTPLUGINS = False

#******************************************************************************
# MAIN
#******************************************************************************
if __name__ == '__main__':
    # print available plugins
    if DEBUG_PRINTPLUGINS:
        printPlugins()
    # create dashboards
    print('** CREATE DASHBOARD: dash1')
    # DASHBOARD
    hdashboard = Dashboard(
        filename='d_dash1',                     # name of the file if we save the dashboard
        title='Dash 1',                         # dashboard title
        description='demo dashboard',           # dashboard description
    )
    # PANELS
    # grafana datasource, here we use internal grafana datasource, to use the random walk
    grafanasource = {'uid': 'grafana', 'type': 'datasource'}
    # built in random walk query
    # pylint: disable=inconsistent-quotes
    randomwalk =  {"refId": "A", "datasource": {"type": "datasource", "uid": "grafana"}, "queryType": "randomWalk"}
    # pylint: enable=inconsistent-quotes
    # add a text panel
    hdashboard.addPanel(                        # add a panel to the dashboard
        PanelText(                              # it is a text panel
            title='DASHBOARD TITLE',            # panel title
            gridpos=PropGridPos(3, 16, 0, 0),   # panel size and position (h, w, x, y)
            content=('# Demo Dashboard text'),  # specific for this panel: add the content
        )
    )
    # add a gauge panel
    hdashboard.addPanel(                        # add a panel to the dashboard
        PanelGauge(                             # it is a gauge panel
            title='Pressure',                   # panel title
            gridpos=PropGridPos(5, 3, 5, 3),    # panel size and position (h, w, x, y)
            datasource=grafanasource,           # data source
            targets=[randomwalk],               # panel query
            min=0,                              # gauge min
            max=100,                            # gauge max
            decimals=1,                         # precision
            units='bar',                        # units to display
        )
    )
    # add stat panel
    hdashboard.addPanel(                        # add a panel to the dashboard
        PanelStat(                              # it is a stat panel
            title='Temperature',                # panel title
            gridpos=PropGridPos(5, 3, 10, 3),   # panel size and position (h, w, x, y)
            datasource=grafanasource,           # data source
            targets=[randomwalk],               # panel query
            units=UNITS.CELSIUS,                # units to display from the UNITS file
            fcolor='yellow',                    # foreground color
            graphmode='area',                   # also display a small graph in the stat panel
        )
    )
    # GENERATE
    hdashboard.getDashboardJson(overwrite=True, debuglevel=DEBUGLEVEL) # generate the JSON
    # SAVE, make sure map does exist
    dashboardpath = './demo_output/'
    with open(dashboardpath + hdashboard.filename, 'w', encoding='utf-8') as outfile:
        outfile.write(hdashboard.d_json)        # save to a file
    # UPLOAD, use correct server and credentials
    uploadDashboardToGrafana(hdashboard.d_json, CFG.GRAFANA_SERVER, CFG.GRAFANA_USER, CFG.GRAFANA_PWD)
