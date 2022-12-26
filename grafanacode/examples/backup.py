# backup.py
# V0.5.0 LDO 19/10/2022: initial version
# V0.5.1 LDO 12/11/2022: refactor modules
'''
    backup all dashboards from a Grafana Installation
'''

#******************************************************************************
# EXTERNAL MODULE REFERENCES
#******************************************************************************
import sys
sys.path.insert(0, '/prj/dev_pc/grafana/grc_module')
import json
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
    # get dashboards from Grafana
    dashboards = grc.getAllDashboards(GRAFANA_SERVER, GRAFANA_USER, GRAFANA_PWD)
    dashboards = grc.filterByProperty(dashboards, 'type', 'dash-db')
    #dashboards = grc.filterByProperty(dashboards, 'uid', 't7p9QVTGk')
    for d in dashboards:
        txt = grc.getJsonItem(d, ['title'], '*' + ' : ' ) + grc.getJsonItem(d, ['uri'], '*') + ' : ' + grc.getJsonItem(d, ['uid'], '*')
        print(txt)
    if len(dashboards)>1:
        for d in dashboards:
            din   = grc.getDashboardFomGrafana(d['uid'], GRAFANA_SERVER, GRAFANA_USER, GRAFANA_PWD, verify=False)
            title = grc.getJsonItem(din, ['dashboard', 'title'])
            jsonstr  = json.dumps(din, indent=4)
            #
            fname = 'backup/bak_' + grc.cleanFilename(title) + '.json'
            with open(fname, 'w', encoding='utf-8') as outfile:
                outfile.write(jsonstr)
