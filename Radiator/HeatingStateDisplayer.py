# -*- coding: utf-8 -*-

import logging
from .RGB_Displayer import RGB_Displayer
from .Rolling import Rolling
from .ActionSequencer import Action, ActionSequencer
import time

class HeatingStateDisplayer:
    """
    This object will display Heating State to local user
    current implementation use RGB_Displayer to dispaly status using one RGB led
    """
    def __init__(self, displayer=RGB_Displayer()):
        self._displayer = displayer
        self._displayer.turnOff()
        self._sequencer=ActionSequencer() #used to blink the LED
        self._minus2Sequence=Rolling([Action(self._displayer.setColorGreen, duration=4),
                                      Action(self._displayer.turnOff, duration=1)])


    def displayConfortMode(self):
        self._sequencer.cancel()
        self._displayer.setColorRed()


    def displayEcoMode(self):
        self._sequencer.cancel()
        self._displayer.setColorBlue()


    def displayConfortMinus1Mode(self):
        self._sequencer.cancel()
        self._displayer.setColorGreen()


    def displayConfortMinus2Mode(self):
        self._sequencer.start(self._minus2Sequence)


    def displayRatioMode(self, ratio):
        pass #pas d'affichage prévu


if __name__ == '__main__':
    print("testing HeatingStateDisplayer manually")
    logging.basicConfig(filename='Radiator.log', level=logging.DEBUG, format='%(asctime)s %(message)s')
    test = HeatingStateDisplayer()
    test.displayConfortMode()
    print("Red Led light on")
    time.sleep(2)
    test.displayEcoMode()
    print("Blue Led light on")
    time.sleep(2)
    test.displayConfortMinus2Mode()
    print("Green LED blink")
    time.sleep(6)
    test._sequencer.cancel()
