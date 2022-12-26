# dashboard_base.py
# V0.5.0 LDO 19/10/2022: initial version
# V0.5.1 LDO 12/11/2022: refactor modules
# V0.6.1 LDO 17/12/2022: release candidate 1
'''
    grafanacode:
    base class for generating dashboards
'''

#******************************************************************************
# EXTERNAL MODULE REFERENCES
#******************************************************************************
from   datetime      import datetime
import json

from attrs           import define, field, Factory
from attr.validators import in_, instance_of, optional, deep_iterable

import grafanacode.c_colors as COLORS
from grafanacode            import funcs
from grafanacode.plugins    import panel_base
from grafanacode.plugins    import target_influxdb

#******************************************************************************
# HELPER FUNCTIONS
#******************************************************************************
class DashboardEncoder(json.JSONEncoder):
    '''
    Encode dashboard objects for json.dumps

    Here we also store the dashboard and panel object. This is because in the case of something like:

    hdashboard.addPanel(PanelText(gridpos=PropGridPos(3, 16, 0, 0)))

    The PropGridpos object does not know it belongs to that PanelText object and not to that Dashboard object.
    Even so the PanelText object does not know it belongs to that Dashboard object.
    Worse: in fact the can belong to many parents.

    But if f.i. we want to use the dashboard.style to color some property, we need to know in which 'parent' we are.
    The solution lies in the fact the rendering of the dashboards goes form dashboard -> panels -> component -> ...
    So here in this JSONEncoder, we store the dashboard and panel if we receive an object of that type
    and we use thes store values to execute the objects ``getJson(self, dashboard=None, panel=None)`` property.

    See: ``getjson = getattr(obj, 'getJson', self.dashboard, self.panel)``


    '''
    # local storage of the dashboard and panel we are in
    dashboard          = field( init=False,
                                default=None)
    panel              = field( init=False,
                                default=None)

    def default(self, o):
        '''
        see JSONEncoder documentation
        '''
        if isinstance(o, Dashboard):
            self.dashboard = o
            self.panel = None
        if isinstance(o, panel_base.PanelBase):
            self.panel = o
        hloglevel   = (o.loglevel if hasattr(o, 'loglevel') else 5)
        hlogstr     = (o.logstr   if hasattr(o, 'logstr')   else '')
        hdebuglevel = (self.dashboard.debuglevel if self.dashboard is not None else 1)
        if hloglevel <= hdebuglevel:
            tab = '\t'
            hintend = hloglevel//10 + 1
            hname = type(o).__name__
            hstr = '    #' + '   '*hintend + str(hloglevel) + '   '*(6-hintend) + f'{hname}{tab}{hlogstr}'
            print (hstr)
        getjson = getattr(o, 'getJson')
        if getjson:
            return getjson(dashboard=self.dashboard, panel=self.panel)
        return json.JSONEncoder.default(self, o)

#******************************************************************************
# Dashboard Property classes: store dashboard property configuration parts
#******************************************************************************
@define(slots=False)
class PropAnnotations:
    '''
    Dataclass encapsulating the dashboard annotations
    '''
    # logging level of this item
    loglevel           : int = 20
    # attributes
    datasource         = field( default={ 'type': 'datasource', 'uid': 'grafana'},
                                validator=optional(instance_of(dict)))
    enable             = field( default=True,
                                validator=instance_of(bool))
    hide               = field( default=True,
                                validator=instance_of(bool))
    iconcolor          = field( default=COLORS.RGBA(0, 211, 255, 1),
                                validator=optional(instance_of((str, panel_base.PropColor, COLORS.RGB, COLORS.RGBA))))
    name               = field( default='Annotations & Alerts',
                                validator=instance_of(str))
    limit              = field( default=100,
                                validator=instance_of(int))
    matchany           = field( default=False,
                                validator=instance_of(bool))
    tags               = field(  default=[],
                                validator=instance_of(list))
    targettype         = field( default='dashboard',
                                validator=instance_of(str))
    atype              = field( default='dashboard',
                                validator=instance_of(str))

    def getJson(self, dashboard=None, panel=None):
        '''
        Create the json to pack this item.

        Parameters:
            dashboard (Dashboard): Dashboard object we are in
            panel (Panel_base): Panel object we are in
        Returns:
            dict: panel json code
        '''
        # pylint: disable=unused-argument
        if type(self.iconcolor)==str:
            self.iconcolor = panel_base.PropColor(self.iconcolor)
        hjson = [{
            'datasource'    : self.datasource,
            'enable'        : self.enable,
            'hide'          : self.hide,
            'iconColor'     : self.iconcolor,
            'name'          : self.name,
            'target'        : {
                'limit'     : self.limit,
                'matchAny'  : self.matchany,
                'tags'      : self.tags,
                'type'      : self.targettype,
            },
            'type'          : self.atype,
        }]
        return hjson

#**********************************************************
@define(slots=False)
class PropDashboardLinkItem:
    '''
    Dataclass encapsulating a dashboardlink item
    '''
    # logging level of this item
    loglevel           : int = 21
    # attributes
    asdropdown         = field( default=False,
                                validator=instance_of(bool))
    icon               = field( default='external link',
                                validator=instance_of(str))
    includevars        = field( default=False,
                                validator=instance_of(bool))
    keeptime           = field( default=False,
                                validator=instance_of(bool))
    newtab             = field( default=False,
                                validator=instance_of(bool))
    tags               = field( default=[],
                                validator=instance_of(list))
    ltype              = field( default='dashboards',
                                validator=instance_of(str))
    title              = field( default='',
                                validator=instance_of(str))
    tooltip            = field( default='',
                                validator=instance_of(str))
    url                = field( default='',
                                validator=instance_of(str))

    def getJson(self, dashboard=None, panel=None):
        '''
        Create the json to pack this item.

        Parameters:
            dashboard (Dashboard): Dashboard object we are in
            panel (Panel_base): Panel object we are in
        Returns:
            dict: panel json code
        '''
        # pylint: disable=unused-argument
        hjson = {
            'asDropdown'    : self.asdropdown,
            'icon'          : self.icon,
            'includeVars'   : self.includevars,
            'keepTime'      : self.keeptime,
            'tags'          : self.tags,
            'targetBlank'   : self.newtab,
            'title'         : self.title,
            'tooltip'       : self.tooltip,
            'type'          : self.ltype,
            'url'           : self.tooltip,
        }
        return hjson

#**********************************************************
@define(slots=False)
class PropTemplating:
    '''
    Dataclass encapsulating the dashboard templating
    '''
    # logging level of this item
    loglevel           : int = 21
    # attributes
    lst = field( default=Factory(list))

    def getJson(self, dashboard=None, panel=None):
        '''
        Create the json to pack this item.

        Parameters:
            dashboard (Dashboard): Dashboard object we are in
            panel (Panel_base): Panel object we are in
        Returns:
            dict: panel json code
        '''
        # pylint: disable=unused-argument
        return {
            'list': self.lst,
        }

#**********************************************************
@define(slots=False)
class PropTime:
    '''
    Dataclass encapsulating the dashboard time
    '''
    # logging level of this item
    loglevel           : int = 20
    # attributes
    s                  = field( default='now-30d',
                                validator=instance_of(str))
    e                  = field( default='now',
                                validator=instance_of(str))

    def getJson(self, dashboard=None, panel=None):
        '''
        Create the json to pack this item.

        Parameters:
            dashboard (Dashboard): Dashboard object we are in
            panel (Panel_base): Panel object we are in
        Returns:
            dict: panel json code
        '''
        # pylint: disable=unused-argument
        hjson = {'from': self.s, 'to': self.e}
        return hjson

#**********************************************************
@define(slots=False)
class PropTimePicker:
    '''
    Dataclass encapsulating the dashboard timepicker
    '''
    # logging level of this item
    loglevel           : int = 20
    # attributes
    refreshintervals   = field( default=['5s', '10s', '30s', '1m', '5m', '15m', '30m', '1h', '2h', '1d'],
                                validator=deep_iterable(
                                    member_validator=instance_of(str),
                                    iterable_validator=instance_of(list)))
    timeoptions        = field( default=['5m', '15m', '1h', '6h', '12h', '24h', '2d', '7d', '30d'],
                                validator=deep_iterable(
                                    member_validator=instance_of(str),
                                    iterable_validator=instance_of(list)))
    hidden             = field( default=False,
                                validator=instance_of(bool))

    def getJson(self, dashboard=None, panel=None):
        '''
        Create the json to pack this item.

        Parameters:
            dashboard (Dashboard): Dashboard object we are in
            panel (Panel_base): Panel object we are in
        Returns:
            dict: panel json code
        '''
        # pylint: disable=unused-argument
        hjson = {
            'refresh_intervals': self.refreshintervals,
            'time_options'     : self.timeoptions,
            'hidden'           : self.hidden
        }
        return hjson

#******************************************************************************
# Dashboard Property classes: store dashboard property configuration parts
#******************************************************************************
@define(slots=False)
class Dashboard:
    '''
    Dashboard dataclass. This class encapsulates all properties and panels of a single Grafana dashboard.
    It creates the final Grafana dashboard JSON by means of its getJson method.
    '''
    # logging level of this item
    loglevel           : int = 20
    logstr             : str = ''
    # number of messages to print during generation
    debuglevel         = field( default=1,
                                validator=instance_of(int))
    # local JSON storage
    d_json             = field( init=False,
                                default={})
    # used for generation
    overwrite          = field( default=False,
                                validator=instance_of(bool))
    filename           = field( default=None,
                                validator=instance_of(str))
    folderid           = field( default=None,
                                validator=optional(instance_of(str)))
    folderuid          = field( default=None,
                                validator=optional(instance_of(str)))
    # DASHBOARD PROPERTIES
    annotations        = field( default=Factory(PropAnnotations),
                                validator=instance_of(PropAnnotations))
    description        = field( default='',
                                validator=instance_of(str))
    editable           = field( default=True,
                                validator=instance_of(bool))
    hidecontrols       = field( default=False,
                                validator=instance_of(bool) )
    id                 = field( default=None,
                                validator=optional(instance_of(int)))
    inputs             = field( default=Factory(list),
                                validator=instance_of(list))
    links              = field( default=Factory(list),
                                validator=deep_iterable(
                                    member_validator=instance_of(PropDashboardLinkItem),
                                    iterable_validator=instance_of(list)))
    panels             = field( default=Factory(list),
                                validator=instance_of(list))
    refresh            = field( default='',
                                validator=instance_of(str))
    schemaversion      = field( default=36,
                                validator=optional(instance_of(int)))
    style              = field( default='dark',
                                validator=optional(in_(COLORS.DASHBOARDSTYLES)))
    tags               = field( default=Factory(list),
                                validator=deep_iterable(
                                member_validator=instance_of(str),
                                iterable_validator=instance_of(list)))
    templating         = field( default=Factory(PropTemplating),
                                validator=instance_of(PropTemplating))
    ##### TEMPLATING NOT USED
    time               = field( default=Factory(PropTime),
                                validator=optional(instance_of(PropTime)))
    timepicker         = field( default=Factory(PropTimePicker),
                                validator=optional(instance_of(PropTimePicker)))
    timezone           = field( default='Europe/Brussels',
                                validator=optional(instance_of(str)))
    title              = field( default=None,
                                validator=instance_of(str))  # mandatory
    @title.validator
    # pylint: disable=invalid-name
    def _check_title(self, attribute, value):
        self.logstr = f'Dashboard name: {value}'
    version            = field( default=0,
                                validator=optional(instance_of(int)))
    uid                = field( default=None,
                                validator=optional(instance_of(str)))
    # shortcuts and extra's
    extraprops         = field( default=None,
                                validator=optional(instance_of(dict)))

    # message
    def __attrs_post_init__(self):
        '''
        Attrs post init, just print a message.
        '''
        print (f'- Init Dashboard: {self.title} - {self.description}; file: {self.filename}')

    # Add panel to this dashboard
    def addPanel(self, panel):
        '''
        Add a panel class to this dashboard

        Parameters:
            panel(PanelBase or derived): the panel dataclass object to be added to the dashboard
        '''
        # pylint: disable=no-member
        self.panels.append(panel)

    def getDashboardJson(self, overwrite=False, debuglevel=1):
        '''
        Create the json to pack the complete dashboard
        All included dataclasses will be resolved with their own _getJson method.

        Parameters:
            customjson (dict): custom or child class json code to add
        Returns:
            dict: panel json code
        '''
        print (f'- Generate Dashboard: {self.title} - {self.description}; file: {self.filename}')
        # set overwrite property
        self.overwrite = overwrite
        # set loglevel property
        self.debuglevel = debuglevel
        # format json
        self.d_json = json.dumps(self, sort_keys=True, indent=2, cls=DashboardEncoder)
        return self.d_json

    def getJson(self, dashboard=None, panel=None):
        '''
        Create the json to pack the 'dashboard' root element.

        Parameters:
            dashboard (Dashboard): Dashboard object we are in
            panel (Panel_base): Panel object we are in
        Returns:
            dict: panel json code
        '''
        # pylint: disable=unused-argument
        hjson = {
            'dashboard'         : {
                '__inputs'      : self.inputs,
                'annotations'   : self.annotations,
                'description'   : self.description,
                'editable'      : self.editable,
                'hideControls'  : self.hidecontrols,
                'id'            : self.id,
                'links'         : self.links,
                'panels'        : self.panels,
                'refresh'       : self.refresh,
                'schemaVersion' : self.schemaversion,
                'style'         : self.style,
                'tags'          : self.tags,
                'templating'    : self.templating,
                'title'         : self.title,
                'time'          : self.time,
                'timepicker'    : self.timepicker,
                'timezone'      : self.timezone,
                'version'       : self.version,
                'uid'           : self.uid,
                },
                'overwrite'     : self.overwrite,
                'filename'      : self.filename,
        }
        if self.folderuid is not None:
            funcs.addJsonItem(hjson, ['folderUid'], self.folderuid)
        if self.folderid is not None:
            funcs.addJsonItem(hjson, ['folderId'], self.folderid)
        # merge the extra props (deep merge)
        funcs.deepMerge(hjson, self.extraprops)
        return hjson

#******************************************************************************
# EXTRACT FUNCTIONS : EXTRACT A CREATION SCRIPT FROM A JSON
#******************************************************************************
# pylint: disable=invalid-name
def extractDashboard_base(dset):
    '''
    Extract one dashboard exported from Grafana to a piece of Python code to be used by this module

    Parameters:
        dset (dict): dict with settinga and json to extract (is input and output)
    Returns:
        boolean: True
    '''
    # create the appropriate dashboard creation script
    # pylint: disable=inconsistent-quotes
    dset['coded'].append("#********************************************************************\n" \
                       + "# DASHBOARD\n"\
                      + f"{dset['intend']}hdashboard = Dashboard(title='{dset['title']}', description='{dset['title']}', tags='{dset['tags']}', links='{dset['links']}'\n" \
                      + f"{dset['intend']})\n")
    # create all panels
    panels = dset['json']['panels']
    for paneljson in panels:
        panel_base.extractPanel(dset, paneljson)
    return True

#**********************************************************
def extractDashboard(dashboardjson, settings={}, extractdashboard=True, extractqueries=True, debuglevel=1):
    '''
    Extract one dashboard exported from Grafana to a piece of Python code to be used by this module

    Parameters:
        dashboardjson (dict): dict with settinga and json to extract (is input and output)
        settings (dict): dict with settinga and json to extract (is input and output)
        extractdashboard (dict): dict with settinga and json to extract (is input and output)
        extractqueries (dict): dict with settinga and json to extract (is input and output)
        debuglevel (dict): dict with settinga and json to extract (is input and output)
    Returns:
        string: Title
        string: python code representing the dashboard
    '''
    if 'dashboard' not in dashboardjson:
        raise Exception('Extract: No \'dashboard\' key found in the dashboard json.')
    #TODO: merge settings
    dset = {
        'debuglevel'        : debuglevel,
        'printmeta'         : True,
        'extractdashboard'  : extractdashboard,
        'extractqueries'    : extractqueries,
        'meta'              : dashboardjson['meta'],
        'json'              : dashboardjson['dashboard'],
        'title'             : funcs.getJsonItem(dashboardjson, ['dashboard', 'title'], 'TITLE'),
        'timestamp'         : datetime.now().strftime('%d-%b-%Y %H:%M:%S'),
        'tags'              : 'd_tags',
        'links'             : 'd_links',
        'removedatasource'  : True,     # remove from panel json
        'removetargets'     : True,     # remove from panel json
        'intend'            : ' '*4,   # intendation of script
        'datasource'        : 'd_tgt.getDatasource(\'InfluxDB\')',
        'targets'           : 'TargetInfluxDB(t=d_tgt.getTarget(\'\', \'\'), r=\'default\')',
        'bucket'            : 'bucket1',
        'codeh'             : [],
        'codeq'             : [],
        'coded'             : [],
    }
    if dset['debuglevel']>0:
        print(f"### dashboard: {dset['title']}")
    # pylint: disable=inconsistent-quotes
    dset['codeh'].append("\n#********************************************************************\n" \
                      + f"# GENERATED {'DASHBOARD' if extractdashboard else ''} - {'QUERIES' if extractqueries else ''} - {dset['timestamp']}\n")
    # create the queries
    if extractqueries:
        if dset['debuglevel']>0:
            print('Extraction of queries')
        target_influxdb.extractFluxQueries(dset)
    # create dashboard
    if extractdashboard:
        if dset['debuglevel']>0:
            print('Extraction of dashboard')
        if dset['debuglevel']>1:
            print(f'  + Create Dashboard general:    {dset["title"]}')
        extractDashboard_base(dset)
    txt = ''.join(dset['codeh']) + '\n' + ''.join(dset['codeq']) + '\n' + ''.join(dset['coded'])
    # print meta json
    if dset['printmeta']:
        txt = "#********************************************************************\n" \
            + "# META \n" \
            + str(dset['meta']) + "\n" \
            + txt
    return dset['title'], txt
