Reuse of targets, queries
=========================

For InfluxDB some extra possibilities were added. Let's take the three queries below.

    .. code-block:: console

        from(bucket: "ath01")
        |> range(start: v.timeRangeStart, stop: v.timeRangeStop)
        |> filter(fn: (r) => r["_measurement"] == "weather")
        |> filter(fn: (r) => r["_field"] == "temp")
        |> aggregateWindow(every: $__interval, fn: max)

        from(bucket: "ath01")
        |> range(start: v.timeRangeStart, stop: v.timeRangeStop)
        |> filter(fn: (r) => r["_measurement"] == "weather")
        |> filter(fn: (r) => r["_field"] == "temp")
        |> aggregateWindow(every: 5m, fn: max)
        |> aggregateWindow(every: $__interval, fn: mean)

        import "timezone"
        import "experimental"
        option location = timezone.location(name: "Europe/Brussels")
        hstart = experimental.subDuration(d: 5h, from: v.timeRangeStop)
        from(bucket: "ath01")
        |> range(start: hstart, stop: v.timeRangeStop)
        |> filter(fn: (r) => r["_measurement"] == "weather")
        |> filter(fn: (r) => r["_field"] == "temp")
        |> last()


This in fact always the same data-source, with every time some other range, aggregation, ...
A target can be split in some parts: headers, calculations, bucket, range, query and aggregation(s).

    .. code-block:: console

        # headers
        import "timezone"
        import "experimental"
        # calculations
        option location = timezone.location(name: "Europe/Brussels")
        hstart = experimental.subDuration(d: 5h, from: v.timeRangeStop)
        # bucket
        from(bucket: "ath01")
        # range
        |> range(start: hstart, stop: v.timeRangeStop)
        # query
        |> filter(fn: (r) => r["_measurement"] == "weather")
        |> filter(fn: (r) => r["_field"] == "temp")
        # aggregation
        |> last()

Below the options for the targetInfluxDB class are discussed.

    .. code-block:: console

        d_tgt = TargetBag()
        d_tgt.addDatasource('influx', {'uid': 'rifn6UOGz', 'type': 'influxdb'})
        d_tgt.addTarget('weather', 'temperature', targetInfluxDB(b='mybucket', q=textwrap.dedent('''
            |> filter(fn: (r) => r["_measurement"] == "weather")
            |> filter(fn: (r) => r["_field"] == "temp")
            ''')))
        
*set range and aggregation*

    .. code-block:: console

        tgt1 = targetInfluxDB(t=d_tgt.getTarget('weather', 'temperature'), r='default', a=['last'])

    .. code-block:: console

        Results in:
            from(bucket: "mybucket")
            |> range(start: v.timeRangeStart, stop: v.timeRangeStop)
            |> filter(fn: (r) => r["_measurement"] == "weather")
            |> filter(fn: (r) => r["_field"] == "temp")
            |> last()

*set timezone, range and aggregation*

    .. code-block:: console

        d_set['tz'] = 'Europe/Brussels'
        tgt1 = targetInfluxDB(t=d_tgt.getTarget('weather', 'temperature'), tz= d_set['tz'], r='default', a=['last'])

    .. code-block:: console

        Results in:
            import "timezone"
            option location = timezone.location(name: "Europe/Brussels")
            from(bucket: "mybucket")
            |> range(start: v.timeRangeStart, stop: v.timeRangeStop)
            |> filter(fn: (r) => r["_measurement"] == "weather")
            |> filter(fn: (r) => r["_field"] == "temp")
            |> last()

Range options
-------------

*set range and two aggregations*

    .. code-block:: console

        tgt1 = targetInfluxDB(t=d_tgt.getTarget('weather', 'temperature'), r='5h', a=['max()', 'last()'])

    .. code-block:: console

        Results in:
            import "experimental"
            hstart = experimental.subDuration(d: {self.r}, from: v.timeRangeStop)
            from(bucket: "mybucket")
            |> range(start: hstart, stop: v.timeRangeStop)
            |> filter(fn: (r) => r["_measurement"] == "weather")
            |> filter(fn: (r) => r["_field"] == "temp")
            |> max()
            |> last()

*set range start and stop; start is translated as v.timeRangeStart; stop is translated as v.timeRangeStop*

    .. code-block:: console

        tgt1 = targetInfluxDB(t=d_tgt.getTarget('weather', 'temperature'), r=['start', 'stop'], a=['last()'])

    .. code-block:: console

        Results in:
            from(bucket: "mybucket")
            |> range(start: v.timeRangeStart, stop: v.timeRangeStop)
            |> filter(fn: (r) => r["_measurement"] == "weather")
            |> filter(fn: (r) => r["_field"] == "temp")
            |> max()
            |> last()

*set range start and stop; other strings are taken literally; here as start*

    .. code-block:: console

        tgt1 = targetInfluxDB(t=d_tgt.getTarget('weather', 'temperature'), r=['-5d', 'stop'], a=['last()'])

    .. code-block:: console

        Results in:
            from(bucket: "mybucket")
            |> range(start: -5d, stop: v.timeRangeStop)
            |> filter(fn: (r) => r["_measurement"] == "weather")
            |> filter(fn: (r) => r["_field"] == "temp")
            |> max()
            |> last()

*set range start and stop; other strings are taken literally; here as stop (and also both is possible)*

    .. code-block:: console

        tgt1 = targetInfluxDB(t=d_tgt.getTarget('weather', 'temperature'), r=['start', '-2h'], a=['last()'])

    .. code-block:: console

        Results in:
            from(bucket: "mybucket")
            |> range(start: v.timeRangeStart, stop: -2h)
            |> filter(fn: (r) => r["_measurement"] == "weather")
            |> filter(fn: (r) => r["_field"] == "temp")
            |> max()
            |> last()

*set range start and stop: dictionary {'t': 'truncate', 's': 'starttime' , 'd': 'duration'}; all keys are optional*

    .. code-block:: console

        tgt1 = targetInfluxDB(t=d_tgt.getTarget('weather', 'temperature'), r={'s':'1mo', 'd':'5dh'}, a=['last()'])

    .. code-block:: console

        Results in:
            import "experimental"
            htruncs = v.timeRangeStop
            htrunce = v.timeRangeStop
            hstart = experimental.subDuration(d: 1mo, from: htrunce)
            hstop  = experimental.addDuration(d: 5d, to: hstart)
            from(bucket: "mybucket")
            |> range(start: hstart, stop: hstop)
            |> filter(fn: (r) => r["_measurement"] == "weather")
            |> filter(fn: (r) => r["_field"] == "temp")
            |> max()
            |> last()

*set range trucate, start and stop*

    .. code-block:: console

        tgt1 = targetInfluxDB(t=d_tgt.getTarget('weather', 'temperature'), r={'t': '1d', s:'1mo', d:'5dh'}, a=['last()'])

    .. code-block:: console

        Results in:
            import "date"
            import "experimental"
            htruncs = date.truncate(t: v.timeRangeStart, unit: 1d)
            htrunce = date.truncate(t: v.timeRangeStop, unit: 1d)
            hstart = experimental.subDuration(d: 1mo, from: htrunce)
            hstop  = experimental.addDuration(d: 5d, to: hstart)
            from(bucket: "mybucket")
            |> range(start: hstart, stop: hstop)
            |> filter(fn: (r) => r["_measurement"] == "weather")
            |> filter(fn: (r) => r["_field"] == "temp")
            |> max()
            |> last()

Aggregation options
-------------------

*set*

    .. code-block:: console

        tgt1 = targetInfluxDB(t=d_tgt.getTarget('weather', 'temperature'), r='default', a=['last()'])

    .. code-block:: console

        Results in:
            from(bucket: "mybucket")
            |> range(start: v.timeRangeStart, stop: v.timeRangeStop)
            |> filter(fn: (r) => r["_measurement"] == "weather")
            |> filter(fn: (r) => r["_field"] == "temp")
            |> last()



Example use im a panel
----------------------

    .. code-block:: console

        hdashboard.addPanel(
            PanelStat(title='Temperature', gridpos=PropGridPos(3, 2, 0, 0), 
                datasource=d_tgt.getDatasource('influx'),
                targets=[targetInfluxDB(t=d_tgt.getTarget('weather', 'temperature'), r=d_set['tlast'], a=['last()'])],
            )
        )
