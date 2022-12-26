# extract.py
# V0.5.0 LDO 19/10/2022: initial version
# V0.5.1 LDO 12/11/2022: refactor modules
'''
    extract all panels from Grafana installation
'''

#******************************************************************************
# EXTERNAL MODULE REFERENCES
#******************************************************************************
import sys
sys.path.insert(0, '/prj/dev_pc/grafana/grc_module')
import grafanacode as grc

#******************************************************************************
# GLOBAL SETTINGS
#******************************************************************************
GRAFANA_API_KEY     = 'azertyuiop1234567890azertyuiop1234567890azertyuiop1234567890azertyuiop12345678=='
GRAFANA_SERVER      = 'xxx.xxx.xxx.xxx:3000'
GRAFANA_USER        = 'username'
GRAFANA_PWD         = 'password'

#******************************************************************************
# MAIN
#******************************************************************************
if __name__ == '__main__':
    # print available plugins
    grc.printPlugins()
    # print available extract plugins
    grc.printPluginsExtract()
    # get dashboards from Grafana
    dashboards = grc.getAllDashboards(GRAFANA_SERVER, GRAFANA_USER, GRAFANA_PWD)
    dashboards = grc.filterByProperty(dashboards, 'type', 'dash-db')
    #dashboards = grc.filterByProperty(dashboards, 'uid', 'llA4lWOVk')
    for d in dashboards:
        dashboarddata = grc.getJsonItem(d, ['title'], '*' + ' : ' ) + grc.getJsonItem(d, ['uri'], '*') + ' : ' + grc.getJsonItem(d, ['uid'], '*')
        print(dashboarddata)
    if len(dashboards)>=1:
        for d in dashboards:
            dashboardjson = grc.getDashboardFomGrafana(d['uid'], GRAFANA_SERVER, GRAFANA_USER, GRAFANA_PWD, verify=False)
            filetitle, txtdashboard =  grc.extractDashboard(dashboardjson, settings={}, extractdashboard=True, extractqueries=True, debuglevel=99)
            fname = 'extract/extract_' + grc.cleanFilename(filetitle) + '.py'
            with open(fname, 'w', encoding='utf-8') as outfile:
                outfile.write(txtdashboard)
