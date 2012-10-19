kl = window.kl
kl.console = {}
klc = kl.console

klc.HALF_SIZE_STYLE = 0x2

klc.init = (id) ->
    klc.$console = $('body').append('<div id="console"></div>')
    klc.$console.addClass('kl-console')

klc.print = (s) ->
    klc.$console.append("#{s}<br>")
#   klc.$console.scrollTop(klc.$console.prop('scrollHeight'))

klc.set_style = (s) ->
    klc.$console.attr('class', 'kl-console')
    switch (s)
        when klc.HALF_SIZE_STYLE
            klc.$console.addClass('kl-console-half-size')