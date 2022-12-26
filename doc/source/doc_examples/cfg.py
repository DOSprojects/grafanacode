# cfg.py
# V0.5.0 LDO 19/10/2022: initial version
# V0.5.1 LDO 12/11/2022: refactor modules
'''
    grafanacode: Configuration file
    Use::
        import grafanacode_cfg as CFG
        svr=CFG.GRAFANA_SERVER
'''

#******************************************************************************
# EXTERNAL MODULE REFERENCES
#******************************************************************************

#******************************************************************************
# GLOBAL SETTINGS
#******************************************************************************
GRAFANA_API_KEY     = 'azertyuiop1234567890azertyuiop1234567890azertyuiop1234567890azertyuiop12345678=='
GRAFANA_SERVER      = 'xxx.xxx.xxx.xxx:3000'
GRAFANA_USER        = 'username'
GRAFANA_PWD         = 'password'

GRAFANA_DATASOURCES = {
                                                'default'  : {},
                                                'InfluxDB' : {'uid': 'azerty123', 'type': 'influxdb'},
                                          }