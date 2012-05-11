kl = window.kl
kl.console = {}
klc = kl.console

klc.init = (id) ->
    klc.$console = $("##{id}").addClass('console')

klc.print = (s) ->
    klc.$console.append("#{s}<br>")