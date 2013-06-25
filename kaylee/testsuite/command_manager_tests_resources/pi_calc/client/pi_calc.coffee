pj = kl.pj

pj.init = (app_config) ->
    # Uncomment to store app_config to pj.config for later use
    # pj.config = app_config

    # Uncomment to notify Kaylee directly that the project has been imported
    # kl.project_imported.trigger()

    # OR

    # Uncomment if one or more additional scripts are required
    # scripts = [
    #     script_url_1,
    #     ...
    # ]
    # kl.include(scripts, kl.project_imported.trigger)
    return

pj.process_task = (task) ->
    # Uncomment and add processing result
    # e.g. {speed: speed_x}
    # kl.task_completed.trigger({});
    return