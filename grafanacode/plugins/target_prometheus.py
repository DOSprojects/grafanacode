# target_prometheus.py
# V0.5.0 LDO 19/10/2022: initial version
# V0.5.1 LDO 12/11/2022: refactor modules
# V0.6.1 LDO 17/12/2022: release candidate 1
'''
    grafanacode:
    class for generating Prometheus targets

    always use DOUBLE QUOTES (NO SINGLE QUOTES) in the grafana (flux) sources
'''

#******************************************************************************
# EXTERNAL MODULE REFERENCES
#******************************************************************************
from attrs           import define, field, Factory
from attr.validators import in_, instance_of, optional, deep_iterable

from grafanacode         import funcs
from grafanacode.plugins import target_base

#******************************************************************************
# Target class
#******************************************************************************
@define(slots=False)
class TargetPrometheus(target_base.TargetBase):
    '''
    Dataclass encapsulating one InfluxDB target mappinsitem.
    '''
    # logging level of this item
    loglevel           : int = 51
    # attributes
    datasource         = field( default=Factory(dict),
                                validator=optional(instance_of(dict)))
    exemplar           = field( default=False,
                                validator=optional(instance_of(bool)))
    expr               = field( default=None,
                                validator=optional(instance_of(str)))
    format             = field( default='time_series',
                                validator=optional(in_(('time_series', 'table', 'heatmap'))))
    hide               = field( default=None,
                                validator=optional(instance_of(bool)))
    instant            = field( default=True,
                                validator=optional(instance_of(bool)))
    interval           = field( default='',
                                validator=optional(instance_of(str)))
    legendformat       = field( default='',
                                validator=optional(instance_of(str)))
    refid              = field( default=None,
                                validator=optional(instance_of(str)))

    def getJson(self, dashboard=None, panel=None):
        '''
        Create the json to pack this target.

        Returns:
            dict: target json code
        '''
        # pylint: disable=unused-argument
         # auto fetch uid????
        hjson = {
            'datasource'    : self.datasource,
            'exemplar'      : self.exemplar,
           'expr'          : self.expr,
            'format'        : self.format,
            'instant'       : self.instant,
            'interval'      : self.interval,
            'legendFormat'  : self.legendformat,
            'refId'         : self.refid,
        }
        if self.hide is not None:
            hjson['hide'] = self.hide
        return hjson

# pylint: disable=pointless-string-statement
'''
(windows_os_virtual_memory_bytes{instance=~'$server.*'} - windows_os_virtual_memory_free_bytes{instance=~'$server.*'})/ windows_os_virtual_memory_bytes{instance=~'$server.*'} * 100
1 - (windows_logical_disk_free_bytes{job='windows',volume=~'C:'}/windows_logical_disk_size_bytes{job='windows',volume=~'C:'})
100 - (avg by (instance) (irate(windows_cpu_time_total{job='windows',mode='idle'}[2m])) * 100)
max (irate(windows_net_bytes_sent_total{instance=~'$server',nic!~'isatap.*|VPN.*'}[$interval]))*8
time() - windows_system_system_up_time{job='windows'}
windows_os_info{job='windows'} * on(instance) group_right(product) windows_cs_hostname
windows_cs_physical_memory_bytes{job='windows'} - 0
windows_cs_logical_processors{job='windows'} - 0
avg by (instance) (windows_cpu_core_frequency_mhz{job='windows'})*1000000 - 0
windows_net_bytes_sent_total{instance=~'$server'}
changes(ALERTS_FOR_STATE{alertname='ServerDown'}[30d])
'''

#******************************************************************************
# EXTRACT FUNCTIONS : EXTRACT A CREATION SCRIPT FROM A JSON
#******************************************************************************
