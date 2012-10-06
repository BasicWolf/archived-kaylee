v0.2
----
* No need for permanent storage for apps like HashCracker.
* Multiprocessing
* Loader: load contrib classes from path, not from module

CODE CHANGES:
1. project.__next__ -> get_next_task()
2. Replace StopIteration (see 1).
3. Remove project.depleted


v0.1 <-- current
----

. Rename "task results" -> "task solutions"
+ Modify Storages API, so that PermanentStorage and TemporalStorage
  interfaces look the same.
