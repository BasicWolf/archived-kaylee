(function() {
  var $console, klc;

  window.kl_console = {};

  klc = window.kl_console;

  klc.HALF_SIZE_STYLE = 0x2;

  $console = null;

  klc.init = function(id) {
    $console = $('<div id="console"></div>').appendTo($('body'));
    $console.addClass('kl-console');
  };

  klc.print = function(s) {
    $console.append("" + s + "<br>");
  };

  klc.set_style = function(s) {
    $console.attr('class', 'kl-console');
    switch (s) {
      case klc.HALF_SIZE_STYLE:
        $console.addClass('kl-console-half-size');
    }
  };

}).call(this);
