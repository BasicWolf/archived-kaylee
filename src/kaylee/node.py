# -*- coding: utf-8 -*-
import time

class Node(object):
    def __init__(self, nid):
        self.id = nid
        self.subscription_timestamp = None

    def subscribe(self):
        self.subscription_timestamp = int(time.time())

    def __hash__(self):
        return hash(self.id)
