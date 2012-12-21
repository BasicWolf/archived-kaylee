v0.2 (dev)
----------
* Pylint the code
* Remove all the disabled message and pylint again
* Add description of every message to .pylintrc


v0.3 (Future)
-------------
* Before you start, reorganize the features below :)
* Default config instead of core.Config defaults
* Kaylee Console API
* Uploading projects through Console API
* Random data seed per application
* Replace dummy controllers/storages with the very basic stuff from contrib.
  Make sure that all the contrib classes that are used in testsuite are
  also tested.
* Add werkzeug as a basic server and mark it as a dependency
* Аdd the Travelling salesman problem as a demo app.
* Add a method to a project which returns a 0.0..1 completed value
* Start thinking of Py3 support
* Test with PyPI
* Add __setitem__ to storages and re-design parameters order (e.g. task_id, node_id, result)
* Rebrand: distributed computing -> crowd computing
* Google App Engine support
* Tornado support

Also
----
* PDB support in Emacs
* Pylint support in Emacs

Interesting links:
# http://www.andromedaproject.org/#!/home
# http://lenta.ru/news/2012/12/10/helpandromeda/


v0.4 (Far future)
-----------------
* Client: sleepy loops and special benchmark. Also, benchmark score support on
  server.
* Client: operations timeout (e.g. project import timeout)
* User management and rankings
