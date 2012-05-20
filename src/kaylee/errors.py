

"""Exceptions raised by the Kaylee package."""

class KayleeError(Exception):
    """Base class for all Kaylee exceptions.
    """

class InvalidNodeIDError(KayleeError):
    def __init__(self, nid):
        KayleeError.__init__(self, "{} is not a valid NodeID".format(nid))

