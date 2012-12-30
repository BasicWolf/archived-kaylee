v0.3
----
* Replace dummy controllers/storages with the very basic stuff from contrib.
  Make sure that all the contrib classes that are used in testsuite are
  also tested.
* Refactor demo Kaylee.js path (e.g. static/js/kaylee/ -> static/kaylee/js)
* Add __setitem__ to storages and re-design parameters order (e.g. task_id, node_id, result)
* Default config instead of core.Config defaults
* Config verification

v0.4
----
* Kaylee Core management API
* Uploading projects through management API
* Random data seed per application
* Werkzeug support
* Google App Engine support
* Tornado support


Feature requests
----------------
* Аdd the Travelling salesman problem as a demo app.
* Add a method to a project which returns a 0.0..1 completed value
* Start thinking of Py3 support
* Test with PyPI
* Rebrand: distributed computing -> crowd computing
* Client: sleepy loops and special benchmark. Also, benchmark score support on
  server.
* Client: operations timeout (e.g. project import timeout)
* User management and rankings


Refactoring requests
--------------------
* NodeID consructor
* NodeID from_object (do we need it?)

Also
----
* PDB support in Emacs
* Pylint support in Emacs

Interesting links:
# http://www.andromedaproject.org/#!/home
# http://lenta.ru/news/2012/12/10/helpandromeda/

