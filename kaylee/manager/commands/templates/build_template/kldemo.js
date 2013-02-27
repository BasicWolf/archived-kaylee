(function() {
  var on_message_logged, on_node_registered, on_node_subscribed, on_node_unsubscibed, on_project_imported, on_result_sent, on_server_error, on_task_completed, on_task_received, _tasks_counter;

  _tasks_counter = 1;

  $(document).ready(function() {
    kl_console.init('console');
    kl_console.print('<b>Kaylee status console</b><br>');
    kl.node_registered.bind(on_node_registered);
    kl.node_subscribed.bind(on_node_subscribed);
    kl.node_unsubscibed.bind(on_node_unsubscibed);
    kl.project_imported.bind(on_project_imported);
    kl.task_received.bind(on_task_received);
    kl.task_completed.bind(on_task_completed);
    kl.result_sent.bind(on_result_sent);
    kl.message_logged.bind(on_message_logged);
    kl.server_error.bind(on_server_error);
    return kl.register();
  });

  on_node_registered = function(data) {
    var app, apps;
    apps = data.applications.join(', ');
    app = data.applications[0];
    kl_console.print("Your node is registered by ID                      <span class='cem'>" + data.node_id + "</span>.");
    kl_console.print("Available applications:                       <span class='cem'>" + apps + "</span>.");
    kl_console.print("Subscribing to                      <span class='cem'>" + app + "</span>.");
    return kl.subscribe(app);
  };

  on_node_subscribed = function(config) {
    var sconfig;
    sconfig = JSON.stringify(config, null, ' ');
    return kl_console.print("Application configuration received:                      <span class='cem'>" + sconfig + "</span>.");
  };

  on_node_unsubscibed = function(data) {
    return kl_console.print("Node unsubscibed: <span class='cem'>" + data + "</span>");
  };

  on_project_imported = function(app_name) {
    return kl_console.print("Project files imported successfully.");
  };

  on_task_received = function(data) {
    return kl_console.print("Task [<span class='cem'>id=" + data.id + " /                      #" + _tasks_counter + "</span>] received.");
  };

  on_task_completed = function(data) {
    kl_console.print("Task [<span class='cem'>#" + _tasks_counter + "</span>]                      completed.");
    return _tasks_counter += 1;
  };

  on_result_sent = function() {
    return kl_console.print("The result has been sent to the server.");
  };

  on_server_error = function(message) {
    return kl_console.print("<span class='cerr'>SERVER ERROR: </span> " + message);
  };

  on_message_logged = function(message) {
    return kl_console.print("<span class='cem'>LOG:</span> " + message);
  };

  window.onerror = function(message, url, linenumber) {
    return kl_console.print("<span class='cerr'>ERROR: </span> " + message + ";", " at " + url + ":" + linenumber);
  };

}).call(this);
