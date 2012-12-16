vX.Y <-- Very far future
* Client: operations timeout (e.g. project import timeout)
* Sleepy loops


v0.4 <-- Far future
----
* Google App Engine support


v0.3 <-- Future
----
* Before you start, reorganize the features below :)
* Default config
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


v0.2 <-- dev
----

* project_imported() -> project_imported(bool success)

* Update benchmark

* Decide if storages should raise an error if the result has been
  submitted previously.

+ Add node registry update()

+ Add node.dirty

+ Modify Storages API, so that PermanentStorage and TemporalStorage
  interfaces look the same.


Interesting links:
# http://www.andromedaproject.org/#!/home
# http://lenta.ru/news/2012/12/10/helpandromeda/
