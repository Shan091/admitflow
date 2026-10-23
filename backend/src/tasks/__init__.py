"""Background task infrastructure (TaskIQ + Redis broker).

This package owns the broker singleton and every ``@broker.task``-decorated
function. The broker module path matches the SPEC's CLI invocation::

    taskiq worker src.tasks.broker:broker

Workers are separate processes; they import this package and discover tasks
through the broker's auto-registration.
"""
