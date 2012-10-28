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


    # CONSTANTS
    AUTO_PROJECT_MODE : 0x2
    MANUAL_PROJECT_MODE : 0x4

    NO_RESULT : {'__kl_result__' : 0x2}

pj = kl.pj

try
    window.kl = kl      # Main JS loop case
catch err
    # pass (Worker case)