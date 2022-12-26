cfg.py
======

In your project map, create a ``cfg.py`` file with following contents.
Import the file in your Python code to use.
Although you can, for instance, also include the settings as variables in your code, The included examples solve it this way.

.. code-block:: console

	# cfg.py
	# V0.9 LDO 19/10/2022: initial version
	'''
		grafanacode: Grafana color names
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
