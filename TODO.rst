v0.3 <-- Future
----

* Google App Engine support
* Better error/exceptions mechanism on client
* Client: operations timeout (e.g. project import timeout)


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

# serializable -> _serializable_

# Rename "task results" -> "task solutions"
