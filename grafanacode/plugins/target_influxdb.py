# target_influxdb.py
# V0.5.0 LDO 19/10/2022: initial version
# V0.5.1 LDO 12/11/2022: refactor modules
# V0.6.1 LDO 17/12/2022: release candidate 1
'''
    grafanacode:
    class for generating InfluxDB Flux targets

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
class TargetInfluxDB(target_base.TargetBase):
    '''
    Dataclass encapsulating one InfluxDB target mappingsitem.

    .. code-block:: text

        h: additional headers
        c: additional calculations
        b: bucketname
        r: range
            = 'default'                         |> range(start: v.timeRangeStart, stop: v.timeRangeStop)
            = '<hstart>'                        |> range(start: v.timeRangeStop-hstart, stop: v.timeRangeStop)
            = ['<hstart>','<hstop>']            |> range(start: <hstart>, stop: <hstop>)
                                                    if hstart = start then hstart = v.timeRangeStart
                                                    if hstop  = stop  then hstop  = v.timeRangeStop
         = {'t': '<optional trunc>', 's': '<start>', 'd': '<duration>|stop'}
                                                    if 'd' = stop then stop = v.timeRangeStop
                                                htrunc = date.truncate(t: v.timeRangeStop, unit: {t})
                                                hstart = experimental.subDuration(d: {s}, from: htrunc)
                                                hstop  = experimental.addDuration(d: {d}, to: hstart)
                                                |> range(start: hstart, stop: hstop)
                                                  OR
                                                |> range(start: hstart, stop: v.timeRangeStop)
        a: aggregations at the end (in order of list)
            = ['last', ...]                   |> last()
            = [{'w':}, ...]                   |> aggregateWindow(every: $__interval, fn: <w>)
            = [{'w':, 'i':}, ...]             |> aggregateWindow(every: <i>, fn: <w>)
            = [{'w':, 'i':, 'e': True}, ...]  |> aggregateWindow(every: <i>, fn: <w>)
            = [{'d':[..]}, ...]               |> drop(columns: [..])
    '''
    # pylint: disable=invalid-name, too-many-instance-attributes
    # logging level of this item
    loglevel           : int = 51
    # attributes
    # add local time headers
    tz             = field( default=None,
                            validator=optional(instance_of(str)))
    # bucket
    b              = field( default=None,
                            validator=optional(instance_of(str)))
    # additional headers
    h              = field( default=None,
                            validator=optional(instance_of(str)))
    # calcs before range block
    c              = field( default=None,
                            validator=optional(instance_of(str)))
    # selection range
    r              = field( default=None,
                            validator=optional(instance_of((str, list, dict))))
    # final aggregation
    a              = field( default=Factory(list),
                            validator=optional(instance_of(list)))
    # real output fields
    datasource     = field( default=Factory(dict),
                            validator=optional(instance_of(dict)))
    hide           = field( default=None,
                            validator=optional(instance_of(bool)))
    query          = field( default=None,
                            validator=optional(instance_of(str)))
    refid          = field( default=None,
                            validator=optional(instance_of(str)))

    def prepQ(self):
        '''
        Prepare the target query string out of the atributes tz, b, h, c, r, a.

        Returns:
            string: Target query string
        '''
        # pylint: disable=no-member, too-many-locals, too-many-branches, too-many-statements
        # first take settings from child; parent settings take advantage over child settings
        if self.t is not None:
            if self.tz is None and self.t.tz is not None:
                self.tz = self.t.tz
            if self.b is None and self.t.b is not None:
                self.b = self.t.b
            if self.h is None and self.t.h is not None:
                self.h = self.t.h
            if self.c is None and self.t.c is not None:
                self.c = self.t.c
            if self.r is None and self.t.r is not None:
                self.r = self.t.r
            if self.q is None and self.t.q is not None:
                self.q = self.t.q
            if self.a is None and self.t.a is not None:
                self.a = self.t.a
        # query
        if self.q and self.q[0] == '\n':
            self.q = self.q [1:]
        if self.q and self.q[-1] == '\n':
            qry_q = self.q
        else:
            qry_q = self.q + '\r\n'
        # headers
        if self.h is None:
            qry_h = ''
        else:
            qry_h = self.h + '\r\n'
        # calcs
        if self.c is None:
            qry_c = ''
        else:
            qry_c = self.c + '\r\n'
        # bucket
        if self.b is None:
            qry_b = ''
        else:
            qry_b = f'from(bucket: "{self.b}")\r\n'
        # localtime
        if self.tz is not None:
            qry_h = qry_h + 'import "timezone"\r\n'
            qry_c = 'option location = timezone.location(name: "{self.tz}")\r\n' + qry_c
        # range
        if self.r is None:
            qry_r = ''
        elif self.r == 'default':
            qry_r = '|> range(start: v.timeRangeStart, stop: v.timeRangeStop)\r\n'
        elif type(self.r) == str:
            qry_h = qry_h + 'import "experimental"\r\n'
            qry_c = qry_c + f'hstart = experimental.subDuration(d: {self.r}, from: v.timeRangeStop)\r\n'
            qry_r = '|> range(start: hstart, stop: v.timeRangeStop)\r\n'
        elif type(self.r) == list:
            tstart = self.r[0]
            tstop = self.r[1]
            if tstart=='start':
                tstart = 'v.timeRangeStart'
            if tstop=='stop':
                tstop = 'v.timeRangeStop'
            qry_r = f'|> range(start: {tstart}, stop:  {tstop})\r\n'
        elif type(self.r) == dict:
            addexp  = False
            adddate = False
            if 't' in self.r:
                adddate = True
                qry_c = qry_c + f'htruncs = date.truncate(t: v.timeRangeStart, unit: {self.r["t"]})\r\n'
                qry_c = qry_c + f'htrunce = date.truncate(t: v.timeRangeStop, unit: {self.r["t"]})\r\n'
            else:
                qry_c = qry_c + 'htruncs = v.timeRangeStop\r\n'
                qry_c = qry_c + 'htrunce = v.timeRangeStop\r\n'
            if 's' in self.r:
                addexp = True
                qry_c = qry_c + f'hstart = experimental.subDuration(d: {self.r["s"]}, from: htrunce)\r\n'
            else:
                if 't' in self.r:
                    qry_c = qry_c + 'hstart = htruncs\r\n'
                else:
                    qry_c = qry_c + 'hstart = v.timeRangeStart\r\n'
            if 'd' in self.r:
                addexp = True
                qry_c = qry_c + f'hstop  = experimental.addDuration(d: {self.r["d"]}, to: hstart)\r\n'
            else:
                qry_c = qry_c + 'hstop = v.timeRangeStop\r\n'
            if addexp:
                qry_h = qry_h + 'import "experimental"\r\n'
            if adddate:
                qry_h = qry_h + 'import "date"\r\n'
            qry_r = '|> range(start: hstart, stop: hstop)\r\n'
        else:
            raise ValueError(f'targetInfluxDB: wrong range: {self.r}')
        # final aggregation
        # pylint: disable=too-many-nested-blocks
        qry_a = ''
        if self.a is not None and len(self.a)>0:
            for item in self.a:
                if type(item) == str:
                    qry_a = qry_a +  f'|> {item}\r\n'
                elif type(item) == dict:
                    if 'd' in item:
                        if type(item['d']) == list:
                            delcols = ''
                            for delitem in item['d']:
                                delcols = delcols + f'"{delitem}", '
                            qry_a = qry_a + f'|> drop(columns: [{delcols}])\r\n'
                        else:
                            raise ValueError(f'targetInfluxDB: wrong aggregation delete columns: {item["d"]} in {self.a}')
                    else:
                        crempty = 'false'
                        if 'e' in item and item['e'] is True:
                            crempty = 'true'
                        if 'i' in item:
                            interval = item['i']
                        else:
                            interval = 'v.windowPeriod'
                        qry_a = qry_a + f'|> aggregateWindow(every: {interval}, fn: {item["w"]}, createEmpty: {crempty})\r\n'
                else:
                    raise ValueError(f'targetInfluxDB: wrong aggregation: {item} in {self.a}')
        self.query = qry_h + qry_c + qry_b + qry_r + qry_q + qry_a
        return self.query

    def getJson(self, dashboard=None, panel=None):
        '''
        Create the json to pack this target.

        Returns:
            dict: target json code
        '''
        # pylint: disable=unused-argument
        self.prepQ()
        hjson = {
            'datasource'    : self.datasource,
            'query'         : self.query,
            'refId'         : self.refid
        }
        if self.hide is not None:
            hjson['hide'] = self.hide
        return hjson

#******************************************************************************
# EXTRACT FUNCTIONS : EXTRACT A CREATION SCRIPT FROM A JSON
#******************************************************************************
def extractFluxQueries(dset):
    '''
    Extract a dashboard exported from Grafana all Flux queries

    Parameters:
        dset (dict): json of the dashboard to extract
    Returns:
        boolean: True
    '''
    # pylint: disable=inconsistent-quotes
    # create the appropriate dashboard creation script
    dset['codeq'].append("#********************************************************************\n" \
                       + "# QUERIES \n")
    # from all panels
    panels = dset['json']['panels']
    for paneljson in panels:
        ptitle   = funcs.getJsonItem(paneljson, ['title'], '')
        ptargets = funcs.cutJsonItem(paneljson, ['targets'], [])
        dset['codeq'].append(f"{dset['intend']}targets.addTarget('{dset['title']}', '{ptitle}', TargetInfluxDB(b='{dset['bucket']}', q=textwrap.dedent('''\n")
        if len(ptargets)>0:
            ptargets = ptargets[0]
            pqry = funcs.getJsonItem(ptargets, ['query'], '')
            pqry = pqry.replace('\'', '"').replace('\r', '').split('\n')
            for query in pqry:
                query = query.strip()
                if len(query)>0:
                    dset['codeq'].append(f"{dset['intend']}    {query}\n")
        dset['codeq'].append(f"{dset['intend']}    ''')))\n")
    return True
