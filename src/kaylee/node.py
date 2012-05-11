class Node(object):
    def __init__(self, nid):
        self.id = nid

    def __hash__(self):
        return hash(self.id)
