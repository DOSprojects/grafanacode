Basic generate 2
================

Example use:

.. code-block:: console

	# set username and password in cfg.py
	>>>python gen_dash2.py
    ** CREATE DASHBOARD: dash2
    - Init Dashboard: Dash 2 - demo dashboard; file: d_dash2
      > Init Panel: DASHBOARD TITLE - type: PanelText
      > Init Panel: Pressure - type: PanelGauge
      > Init Panel: Temperature - type: PanelStat
    - Generate Dashboard: Dash 2 - demo dashboard; file: d_dash2
        #         20         Dashboard      Dashboard name: Dash 2
        #         20         PropAnnotations
        #            34      RGBA
        #      15            PanelText      Panel name: DASHBOARD TITLE
        #         20         PropGridPos
        #         20         PropLinks
        #      15            PanelGauge     Panel name: Pressure
        #         20         PropMappings
        #         21         PropThresholdsItem
        #         20         PropColor
        #         21         PropThresholdsItem
        #         20         PropColor
        #         21         PropThresholdsItem
        #         20         PropColor
        #         21         PropThresholdsItem
        #         20         PropColor
        #         21         PropThresholdsItem
        #         20         PropColor
        #         21         PropThresholdsItem
        #         20         PropColor
        #         21         PropThresholdsItem
        #         20         PropColor
        #         21         PropThresholdsItem
        #         20         PropColor
        #         21         PropThresholdsItem
        #         20         PropColor
        #         21         PropThresholdsItem
        #         20         PropColor
        #         21         PropThresholdsItem
        #         20         PropColor
        #         20         PropOverrides
        #         20         PropGridPos
        #         20         PropLinks
        #      15            PanelStat      Panel name: Temperature
        #         20         PropMappings
        #         21         PropThresholdsItem
        #         20         PropColor
        #         21         PropThresholdsItem
        #         20         PropColor
        #         21         PropThresholdsItem
        #         20         PropColor
        #         21         PropThresholdsItem
        #         20         PropColor
        #         21         PropThresholdsItem
        #         20         PropColor
        #         21         PropThresholdsItem
        #         20         PropColor
        #         21         PropThresholdsItem
        #         20         PropColor
        #         21         PropThresholdsItem
        #         20         PropColor
        #         21         PropThresholdsItem
        #         20         PropColor
        #         21         PropThresholdsItem
        #         20         PropColor
        #         21         PropThresholdsItem
        #         20         PropColor
        #         20         PropOverrides
        #         20         PropGridPos
        #         20         PropLinks
        #         21         PropTemplating
        #         20         PropTime
        #         20         PropTimePicker
    200 - b'{"id":117,"slug":"dash-2","status":"success","uid":"Ad1mAW5Vz","url":"/grafana/d/Ad1mAW5Vz/dash-2","version":10}'
