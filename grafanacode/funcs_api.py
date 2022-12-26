# funcs_api.py
# V0.5.0 LDO 19/10/2022: initial version
# V0.5.1 LDO 12/11/2022: refactor modules
# V0.6.1 LDO 17/12/2022: release candidate 1
'''
    grafanacode: utility functions for interacting with a grafana installation
'''

#******************************************************************************
# EXTERNAL MODULE REFERENCES
#******************************************************************************
import requests

from attrs           import define, field, Factory
from attr.validators import in_, instance_of, optional, deep_iterable

import grafanacode.c_colors as COLORS

#******************************************************************************
# GRAFANA (API) FUNCTIONS
#******************************************************************************

def getGrafanaJson(datain):
    '''
    Get then json dictionary from a Grafana dashboard; correct the boolean and null representation to Python

    Parameters:
        datain (dict): dict input json
    Returns:
        dict: json corrected for Python: false->False, true->True, null->None
    '''
    data = datain.content.decode('UTF-8')
    data = data.replace(':false', ':False').replace(':true', ':True').replace(':null', ':None')
    dataout = eval(data)
    return dataout

#******************************************************************************
def getAllDashboards(server, user, pwd, verify=False):
    '''
    Get all dashboards from a Grafana installation

    Args:
        server (str): server name (e.g. xxx.xxx.xxx.xxx:3000)
        user (str): user name
        pwd (str): password
        verify (bool): verify
    Returns:
        dict: all dashboards
    '''
    headers = {
        'Content-Type': 'application/json',
    }
    retval = requests.get(url=f'http://{user}:{pwd}@{server}/api/search', headers=headers, verify=verify, timeout=5)
    retval = getGrafanaJson(retval)
    return retval
#******************************************************************************
def getDashboardFomGrafana(uid, server, user, pwd, verify=False):
    '''
    Download a specific dashboard from a Grafana installation

    Parameters:
        uid (str): dashboard uid
        server (str): server name (e.g. xxx.xxx.xxx.xxx:3000)
        user (str): user name
        pwd (str): password
        verify (bool): verify
    Returns:
        dict: dashboard json
    '''
    headers = {
        'Content-Type': 'application/json',
    }
    retval = requests.get(f'http://{user}:{pwd}@{server}/api/dashboards/uid/{uid}', headers=headers, verify=verify, timeout=5)
    retval = getGrafanaJson(retval)
    # probably add error handling
    return retval

#******************************************************************************
def uploadDashboardToGrafana(jsondict, server, user, pwd, verify=False):
    '''
    Upload a dashboard to a Grafana installation

    Parameters:
        json (dict): dashboard json
        server (str): server name (e.g. xxx.xxx.xxx.xxx:3000)
        user (str): user name
        pwd (str): password
        verify (bool): verify
    Returns:
        nothing
    '''
    headers = {
#        'Authorization': f'Bearer {grafana_api_key}',
        'Content-Type': 'application/json',
    }
    retval = requests.post(f'http://{user}:{pwd}@{server}/api/dashboards/db', data=jsondict, headers=headers, verify=verify, timeout=5)
    # probably add error handling
    print(f'{retval.status_code} - {retval.content}')
#******************************************************************************
def getAllDatasources(server, user, pwd, verify=False):
    '''
    Get all datasources from a Grafana installation

    Parameters:
        server (str): server name (e.g. xxx.xxx.xxx.xxx:3000)
        user (str): user name
        pwd (str): password
        verify (bool): verify
    Returns:
        dict: all datasources
    '''
    headers = {
        'Content-Type': 'application/json',
    }
    retval = requests.get(url=f'http://{user}:{pwd}@{server}/api/datasources', headers=headers, verify=verify, timeout=5)
    retval = getGrafanaJson(retval)
    return retval
#******************************************************************************
# Get all Grafana data sources
def getDatasourceFromGrafana(uid, server, user, pwd, verify=False):
    '''
    Download a specific datasource from a Grafana installation

    Parameters:
        uid (str): datasource uid
        server (str): server name (e.g. xxx.xxx.xxx.xxx:3000)
        user (str): user name
        pwd (str): password
        verify (bool): verify
    Returns:
        dict: datasource json
    '''
    headers = {
        'Content-Type': 'application/json',
    }
    retval = requests.get(f'http://{user}:{pwd}@{server}/api/datasources/uid/{uid}', headers=headers, verify=verify, timeout=5)
    retval = getGrafanaJson(retval)
    # probably add error handling
    return retval
