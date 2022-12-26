Extract
=======

Example use:

.. code-block:: console

	# set username and password in cfg.py
	>>>python extract.py
	available plugins:
	-------------------
	 Targets:
	  target_base
	  target_influxdb
	  target_prometheus
	-------------------
	 Dashboards:
	  dashboard_base
	-------------------
	 Panels:
	  panel_barchart
	  panel_bargauge
	  panel_base
	  panel_boomtable
	  panel_carpetplot
	  panel_dashboardlist
	  panel_dynamicimage
	  panel_flant_statusmap
	  panel_gauge
	  panel_geomap
	  panel_heatmap
	  panel_histogram
	  panel_logs
	  panel_news
	  panel_piechart
	  panel_plotly
	  panel_plotly_windrose
	  panel_row
	  panel_stat
	  panel_statetimeline
	  panel_table
	  panel_text
	  panel_timeseries
	-------------------

	 available extract plugins:
	-------------------
	  barchart : panel_barchart
	  bargauge : panel_bargauge
	  yesoreyeram_boomtable_panel : panel_boomtable
	  petrslavotinek_carpetplot_panel : panel_carpetplot
	  dashlist : panel_dashboardlist
	  dalvany_image_panel : panel_dynamicimage
	  flant_statusmap_panel : panel_flant_statusmap
	  gauge : panel_gauge
	  geomap : panel_geomap
	  heatmap : panel_heatmap
	  histogram : panel_histogram
	  logs : panel_logs
	  news : panel_news
	  piechart : panel_piechart
	  ae3e_plotly_panel : panel_plotly
	  row : panel_row
	  stat : panel_stat
	  state_timeline : panel_statetimeline
	  table : panel_table
	  text : panel_text
	  timeseries : panel_timeseries
	-------------------
	test_switchingdb/test_switching : l1xOL9QGz
	test_windrosedb/test_windrose : HgtEdbAMz

	Start Generation of : test__switching
	  + Create Flux Queries from :    test_switching
	  + Create Dashboard general:    test_switching
		- Create Panel:  type: graph  -  title: windspeed 12-15
		- Create Panel:  type: graph  -  title: windgust 15-20
		- Create Panel:  type: graph  -  title: pomp
		- Create Panel:  type: graph  -  title: uv lamp
		- Create Panel:  type: graph  -  title: solrad 45-50
		- Create Panel:  type: graph  -  title: windspeed 15-20
		- Create Panel:  type: graph  -  title: solrad 45-50
		- Create Panel:  type: graph  -  title: solrad 45-50

	Start Generation of : test_windrose
	  + Create Flux Queries from :    test_windrose
	  + Create Dashboard general:    test_windrose
		- Create Panel:  type: ae3e-plotly-panel  -  title: Wind: Direction - Speed
