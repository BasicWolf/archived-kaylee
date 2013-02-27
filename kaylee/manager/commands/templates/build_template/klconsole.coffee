window.kl_console = {}
klc = window.kl_console

klc.HALF_SIZE_STYLE = 0x2

$console = null

klc.init = (id) ->
    $console = $('<div id="console"></div>').appendTo($('body'))
    $console.addClass('kl-console')
    return

klc.print = (s) ->
    $console.append("#{s}<br>")
#   $console.scrollTop($console.prop('scrollHeight'))
    return

klc.set_style = (s) ->
    $console.attr('class', 'kl-console')
    switch (s)
        when klc.HALF_SIZE_STYLE
            $console.addClass('kl-console-half-size')
    return