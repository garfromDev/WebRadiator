# -*- coding: utf-8 -*-
import threading
import logging
#  import inspect


# this object is an elementary couple action + time before next action (in sec.) to use with the Sequencer
# action : a function
# duration : in sec.
class Action:
    def __init__(self, action, duration):
        self.action = action
        self.duration = duration

    def __repr__(self):
        return f"{self.action and self.action.__name__ or ''} every {self.duration}"

# the sequencer will repeat each action, then wait for duration, rolling through the sequence of Action
class ActionSequencer:
    # sequence : a Rolling() collection of Action()
    def __init__(self, sequence=None):
        logging.debug("initialising sequencer %s with sequence %s", self, sequence)
        self.sequence = sequence
        self.timer = None

    # start the sequencer if a sequence is given, or shoot the next action (called by the timer from previous call)
    def start(self, sequence=None):
        logging.debug("start sequencer %s", self)
        if sequence is not None:
            self.cancel()  # Setting a new sequence cancel the previous one if there was one
            self.sequence = sequence

        try:
            currentAction = self.sequence.get()
        except:
            logging.debug("sequencer %s did not find next action", self)
            self.timer = None  # not a Rolling we stop
            return
        try:
            logging.debug("perform action %s", currentAction.action.__name__)
            currentAction.action()  # perform the first action
        except Exception as e:
            logging.debug("action failed : %s %s", currentAction, e)

        try:
            dur = currentAction.duration
            self.timer = threading.Timer(dur, self.start)
            self.timer.start()  # this will call start() again after duration, which will perform the next action
            logging.debug("sequencer %s next action %s in %s", self, currentAction.action.__name__, dur)

        except:
            self.timer = None  # duration not valid


    # stop the sequencer
    def cancel(self):
        try:  # because timer may not exist
            self.timer.cancel()
        except:
            pass
