Basic generate 1
================

Example use:

.. code-block:: console

	# set username and password in cfg.py
	>>>python gen_dash1.py
    ** CREATE DASHBOARD: dash1
    - Init Dashboard: Dash 1 - demo dashboard; file: d_dash1
      > Init Panel: DASHBOARD TITLE - type: PanelText
      > Init Panel: Pressure - type: PanelGauge
      > Init Panel: Temperature - type: PanelStat
    - Generate Dashboard: Dash 1 - demo dashboard; file: d_dash1
        #         20         Dashboard      Dashboard name: Dash 1
        #         20         PropAnnotations
        #            34      RGBA
        #      15            PanelText      Panel name: DASHBOARD TITLE
        #         20         PropGridPos
        #         20         PropLinks
        #      15            PanelGauge     Panel name: Pressure
        #         20         PropMappings
        #         21         PropThresholdsItem
        #         20         PropColor
        #         20         PropOverrides
        #         20         PropGridPos
        #         20         PropLinks
        #      15            PanelStat      Panel name: Temperature
        #         20         PropMappings
        #         21         PropThresholdsItem
        #         20         PropColor
        #         20         PropOverrides
        #         20         PropGridPos
        #         20         PropLinks
        #         21         PropTemplating
        #         20         PropTime
        #         20         PropTimePicker
    200 - b'{"id":116,"slug":"dash-1","status":"success","uid":"5KpqpZ54z","url":"/grafana/d/5KpqpZ54z/dash-1","version":40}'