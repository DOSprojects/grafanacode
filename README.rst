******
Readme
******

Description
===========

This module aims to generate `Grafana <http://grafana.org/>`_ dashboards from Python scripts.
The module is tested with Grafana version 9. Older versions of Grafana might have another API and another JSON structure and are thus unsupported.

Use Case
========

According to their website, Grafana is a web-based application to query, visualize, alert on, and understand your data no matter where it’s stored.
With Grafana you can create, explore, and share all of your data through beautiful, flexible dashboards.

The configuration is done through a GUI, which is very user friendly.
Developing a dashboard can be done via trial and error or on progressive insight.
The configurations are stored in a Sqlite3 database.
There is a basic version control and the dashboards and panels are portable via json.
The json of a dashboard or a panel can be inspected via the GUI.
Grafana has a web API that can be used to interact with the installation.
Also `provisioning <https://grafana.com/docs/grafana/latest/administration/provisioning/>`_ can be used.
Then the generated config files will have to be stored at the appropriate location.

But, sometimes we want more...

* a robust configuration that can be backup-ed

    * The database can get corruption.
    * There can arise issues during upgrades.

* manageable via GIT
* roll-out dashboards and panels over different installations
* roll-out changes easily over all panels and dashboards

    * change the foreground color over all panels and all dashboards
    * change a data source over all panels and all dashboards
    * add a timezone offset in all queries

* have a unified look and feel 
* have a compact notation (json files are very verbose and lengthy)

Solution: Config in code

* Grafana configuration in Python

    * set of Python dataclasses
    * supporting multiple panel types
    * supporting multiple data sources
    * supporting other configurations (alarming, ...)

* User functions

    * implement some communication via the Grafana API
    * download a dashboard from a Grafana installation as json
    * upload a dashboard to a Grafana installation as json
    * convert a python script to uploadable json
    * convert a json to a python script

the grafanacode tool
====================

As already said, the configuration will be done in Python.
Although this is all relative simple code, some knowledge of python will be useful.
We will use Python 3 with some additional libraries. Under the hood we make extensive use of the `attrs library <https://www.attrs.org>`_.
If you install it via ``pip`` (see below), these dependencies will be installed together with the tool, 


Usage
=====

This module contains a number of functionalities:

* Save one or more Grafana dashboards.
* Export one or more Grafana dashboards to Python code (*).
* Generate one or more Grafana dashboards.
* Upload one or more Grafana dashboards to a running system.

(*) The export is not complete. Some additional work needs to be done before the code can run.
But the script contains already most of the code

Take a look at the included examples for more info.

**IMPORTANT NOTE:**

In order to reduce typing there is only one namespace: grafanacode.
So when in the documentation there is: ``grafanacode.plugins.panel_base.PropGridPos``, you have to type ``grafanacode.PropGridPos``. 
Or when you ``from grafanacode import *``, you simply type ``PropGridPos``.
I know this is strongly disadvised. Nevertheless, in this case, importing the grafanacode objects in your namespace implies little risk. On the other side, t makes the code much more compact and readable, which is one of the main aims of this module.


Installation
============

grafanacode is just a Python package, so:

    .. code-block:: console

        pip install grafanacode

Support
=======

This library is under development.
So breaking changes are always possible.

grafanacode works with Python 3.9 and 3.10.

Development setup
=================

Every Python development system will do, but on Windows OS, I prefer Anaconda.

To install Anaconda:

* Download Anaconda from https://www.anaconda.com/; chose windows installer
* Double click to install; Accept all defaults (personally I install this at another location).
* Start Anaconda
* Click on Anaconda Navigator
* Setup a virtual environment; I called this *grafanacode*
* Click on ``environments``
* Click on ``create`` at the bottom
* Fill in the popup; chose ``Python 3``
* Select environment
* Start a Command prompt
    * Click on the green play button
    * Chose ``open terminal``
    * In the command prompt, between brackets, you can see the virtual environment you are in.
* Install dependencies

    .. code-block:: console

        pip install attrs
        pip install requests
        pip install sphinx-rtd-theme
        pip install sphinx-toolbox
        pip install pprinter
        pip install pylint
        pip install docutils==0.16
        pip install hypothesis


Generate dashboards
===================

Take a look at the example scripts. 
