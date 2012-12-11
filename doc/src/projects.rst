.. _projects:

Projects
========

.. module:: kaylee

This section examines various Kaylee projects topics in-depth.

Modes
-----

There are two types of Kaylee projects: :ref:`automatic <auto_project_mode>`
and :ref:`manual <manual_project_mode>`.

.. _auto_project_mode:

Automatic projects
..................

An "auto" project dispatches tasks which are suitable for fully-automated
processing and require no human interaction. In fact the user of the browser
in which Kaylee client is running (aka Kaylee Node) does not even have to
know about it. The project's code is executed in a Kaylee-controlled web
worker and does not interfere with the browser's main javascript loop.

The auto mode is suitable for all kind of automated data processing
applications, for example hash-cracking, complex function optimization, graph
traversal, etc. The `BOINC <BOINC>`_ platform implements this approach to
distributed data processing.

Web workers' code is kept and loaded from external javascript files. That is
why they do not have access to the following JavaScript objects [1]_:

* The window object
* The document object
* The parent object


.. _manual_project_mode:

Manual projects
...............

A "manual" project dispatches tasks that are hard to process automatically
and which are solved faster and more accurate by a human. For example:
text, image, voice or video recognition, heuristic data analysis etc.
The real-world example projects are `reCAPTCHA <RECAPTCHA>`_,
`The Space Game <SPACEGAME>`_ and `The Andromeda Proeject <ANDROMEDA>`_.


Defining in code
................

The project mode is defined in :class:`project class <Project>` as follows::

    from kaylee.project import Project, AUTO_PROJECT_MODE, MANUAL_PROJECT_MODE

    class MyProject(Project):
        mode = MANUAL_PROJECT_MODE

.. _SPACEGAME: http://www.thespacegame.org/
.. _ANDROMEDA: http://www.andromedaproject.org/

.. [1] http://www.w3schools.com/html5/html5_webworkers.asp
