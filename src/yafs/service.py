"""
This module is a generic class to introduce whatever kind of dynamic service to run

"""
import random
import logging

class Service(object):
    """
    Abstract class
    """
    def __init__(self, name):
        self.name = name
        self.logger = logging.getLogger(__name__)

    def run(self):
        return None

class FractionalSelectivityService(Service):
    """
    Fractional selectivity service to replace function based approach.

    Args:
        threshold (float): probability of forwarding

        msg_in (Message): the expected message

        msg_out (Message): the message to be sent

        module_dest (list): module names to forward the message

        p (list): probabilities to forward the message for each module_dest
    """
    def __init__(self, threshold, msg_in, msg_out, module_dest=[], p=[]):
        self.threshold = threshold
        self.msg_in = msg_in
        self.msg_out = msg_out
        self.module_dest = module_dest
        self.p = p
        super(FractionalSelectivityService, self).__init__("FractionalSelectivityService")

    def run(self, msg_in):
        if random.random() > self.threshold or msg_in.name != self.msg_in.name:
            return None

        # maybe remove and force user to specify module_dest always.
        if not self.module_dest:
            self.logger.debug("%s assigned %s from %s to %s" % (self.name, self.msg_out.name, self.msg_in.src, self.msg_out.dst))
            return [(self.msg_out.dst, self.msg_out)]

        messages = []
        for idx, module_dst in enumerate(self.module_dest):
            if random.random() <= self.p[idx]:
                self.logger.debug("%s assigned %s from %s to %s" % (self.name, self.msg_out.name, self.msg_in.src, module_dst))
                messages.append((module_dst, self.msg_out))

        return messages

