"""
    kaylee.contrib
    ~~~~~~~~~~~~~~

    This sub-package contains code contributed to Kaylee.
    It includes front-end implementations, Controllers, Storages etc.

    :copyright: (c) 2012 by Zaur Nasibov.
    :license: MIT, see LICENSE for more details.
"""


from .controllers import SimpleController, ResultsComparatorController
from .storages import MemoryTemporalStorage, MemoryPermanentStorage
from .registries import MemoryNodesRegistry
