.. Natural Selection documentation master file, created by
   sphinx-quickstart on Tue Sep 22 22:57:54 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. _changelog-page:

Changelog
**************************

History
==========================

Version 0.3.0 (2023-02-16)
--------------------------

* Bumped up to minor 3, close to releasing version 1.0 after http server is implemented.
* Added the `hot_load` property to API calls, making it load on call instead of only on start.
* Added the `hot_load` property to HTML page, making it load on call instead of only on start.
* Added the `hot_load` property to add file, making it load on call instead of only on start.

Version 0.2.7 (2023-02-15)
--------------------------

* Complete revamp of internal versioning.

Version 0.2.6 (2023-02-15)
--------------------------

* Fixed the same bug, but the root cause. The fact that modules are imported before proper install.

Version 0.2.5 (2023-01-18)
--------------------------

* Fixed a bug where requests is not installed


Version 0.2.4 (2022-09-02)
--------------------------

* Added ability to get nodes by using Unix style paths to get to nodes.
* Added a safe load environment variable "RICKLE_SAFE_LOAD" to override all lambda loads (as a safety measure).
* Added ``search_path`` to search for a key in the Rickle.
* Removed ``includes_self_reference`` due to confusion.
* Added a third way to load CSV files, see example documentation.
* Added ``load_as_rick`` to ``add_api_json_call``.


Version 0.2.3 (2022-03-13)
--------------------------

* Merged but cleaned up contributions by Fabian.

Version 0.2.2 (2022-02-14)
--------------------------

* Added ``do_recursive`` param to ``.get`` to optionally do a deeper recursive search.
* Do you agree that valentine's day is bullshit? Because my gf doesn't.

Version 0.2.1 (2021-12-08)
--------------------------

* Added ``add_class_definition`` to define classes.
* Created a new class, ``ObjectRickler``, to dump (almost) any object or convert to Rickle.
* Added ``add_module_import`` to Rickle, with functionality to add global Python module imports.

Version 0.2.0 (2021-12-06)
--------------------------

* Renamed project to ``Rickled`` to avoid any possible lawsuits from money hungry media execs.
* Pickle Rick was a great name, possibly even considered a parody which is protected under copyright law.
* But rather safe than sued..

Version 0.1.14 (2021-10-28)
--------------------------

* Added new ``add_html_page`` to load HTML text.
* Added new ``add_csv_file`` to load CSV files as either a list of lists, or list of PickleRicks.

Version 0.1.13 (2021-10-07)
--------------------------

* Added ability to load from multiple YAML files or JSON files from start up.

Version 0.1.12 (2021-09-23)
--------------------------

* Fixed major bug, YAML was not loaded!
* Adding preload arguments for load and replace values within YAML files using ``_|PARAM|_``
* Added new API JSON call method, to load and create a Rick from an API response ``add_api_json_call``.
* Added new ability to load other YAML, JSON, or text files from within, using ``add_from_file``.
* Added ``add_base64`` to load base 64 encoded data.

Version 0.1.11 (2021-09-09)
--------------------------

* Fixed bug in ``get`` for finding values.
