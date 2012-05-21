

"""Exceptions raised by the Kaylee package."""

class KayleeError(Exception):
    """Base class for all Kaylee exceptions.
    """

class InvalidNodeIDError(KayleeError):
    def __init__(self, node_id):
        KayleeError.__init__(self, "{} is not a valid NodeID".format(node_id))

class AppFinishedError(KayleeError):
    def __init__(self, app_name):
        KayleeError.__init__(self, 'All calculations for application {} were '
                                   'completed.'.format(app_name))
