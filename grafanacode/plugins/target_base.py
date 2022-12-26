# target_base.py
# V0.5.0 LDO 19/10/2022: initial version
# V0.5.1 LDO 12/11/2022: refactor modules
# V0.6.1 LDO 17/12/2022: release candidate 1
'''
    grafanacode:
    base class for generating targets
    and collection class to store targets and datasources

    always use DOUBLE QUOTES (NO SINGLE QUOTES) in the grafana sources (queries)
'''

#******************************************************************************
# EXTERNAL MODULE REFERENCES
#******************************************************************************
from attrs           import define, field, Factory
from attr.validators import in_, instance_of, optional, deep_iterable

from grafanacode         import funcs

#******************************************************************************
# Target / Query storage class: store a bag of targets / queries (for reuse)
#******************************************************************************
@define(slots=False)
class TargetBag:
    '''
    class containing Datasource and Target objects
    '''
    # logging level of this item
    loglevel           : int = 5
    # attributes
    # datasource collection
    datasources        = field( init=False,
                                default=Factory(dict))
    # targets collection
    targets            = field( init=False,
                                default={0 : {}})


    def addDatasource(self, key='', data=None):
        '''
        Add a Datasource json dict to the collection.

        Parameters:
            key (string): name of the Datasource
            data (object): Datasource json or object
        '''
        if data is None:
            raise ValueError(f'Datasource {key} has no data attribute')
        self.datasources[key] = data

    def getDatasource(self, key=''):
        '''
        Get a Datasource json dict from the collection.

        Parameters:
            key (string): name of the Datasource
        Returns:
            object: Datasource json or object
        '''
        if key=='default':
            return None
        if key in self.datasources:
            return { 'type': self.datasources[key]['type'], 'uid': self.datasources[key]['uid']}
        else:
            raise ValueError(f'Datasource {key} not found')

    def addTarget(self, group=0, key=None, target=None):
        '''
        Add a Target json dict to the collection. The collection consists of a number of groups.
        the group <0> is created by default, but if the group does not exists if gets created.

        Parameters:
            group (string, int): name or number defining the Target collection group
            key (string): name of the Target (in the group)
            data (object): Target json or object
        '''
        if key is None:
            raise ValueError(f'Target {group} has no key attribute')
        if target is None:
            raise ValueError(f'Target {group} {key} has no data attribute')
        else:
            if group not in self.targets:
                self.targets[group] = {}
            self.targets[group][key] = target

    def getTarget(self, group=0, key=0):
        '''
        Get a Target json dict from the collection.

        Parameters:
            group (string, int): name or number defining the Target collection group
            key (string): name of the Target (in the group)
        Returns:
            object: Target json or object
        '''
        target = self.targets[group][key]
        return target

#******************************************************************************
# Target storage base class
#******************************************************************************
@define(slots=False)
class TargetBase:
    '''
    Dataclass encapsulating one target mappinsitem.
    This class can be subclassed to hold specific targets, e.g. InfluxDB, Prometheus, ...
    '''
    # logging level of this item
    loglevel           : int = 50
    # attributes
    q                  = field( default=None,
                                validator=optional(instance_of(str)))
    # used to refine
    t                  = field( default=None,
                                validator=optional(instance_of(object)))
