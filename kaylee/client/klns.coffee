###
#    klns.coffee
#    ~~~~~~~~~~~~~~~
#
#    Base Kaylee namespace declarations
#
#    :copyright: (c) 2012 by Zaur Nasibov.
#    :license: MIT, see LICENSE for more details.
###

# Kaylee namespace
kl =
    pj : {}      # Project namespace
    config : {}  # Kaylee client configuration

try
    window.kl = kl      # Main JS loop case
catch err
    # pass (Worker case)
