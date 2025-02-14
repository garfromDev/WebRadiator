# -*- coding: utf-8 -*-
import os
from .logger_provider import logger

test = os.getenv("RADIATOR_TEST_ENVIRONMENT", "").upper() == "TRUE"

if not test:
    import RPi.GPIO as GPIO
from .Rolling import Rolling
from .ActionSequencer import Action, ActionSequencer
from .HeatingStateDisplayer import HeatingStateDisplayer


# This module allows to drive pilot wire

class ComfortMode(object):
    """ abstract representation of confort mode
        use make_hot() and make_cold() to change desired confort mode
    """
    minus1 = 'minus1'
    minus2 = 'minus2'
    confort = 'confort'
    _mode_list = [minus2, minus1, confort]
    _current_index = 1

    def __init__(self, confort_mode=minus1):
        self._set(confort_mode)

    def _set(self, confort_mode):
        self.confort_mode = confort_mode
        self._current_index = self._mode_list.index(confort_mode)

    def make_hot(self):
        new_mode = self._mode_list[min(self._current_index + 1, len(self._mode_list) - 1)]
        return ComfortMode(new_mode)

    def make_cold(self):
        new_mode = self._mode_list[max(self._current_index - 1, 0)]
        return ComfortMode(new_mode)

    def __repr__(self):
        return self._mode_list[self._current_index]

    def __eq__(self, other):
        return self._current_index == other._current_index


class ComfortMinus1(ComfortMode):
    def __init__(self):
        super(ComfortMinus1, self).__init__(ComfortMode.minus1)


class ComfortMinus2(ComfortMode):
    def __init__(self):
        super(ComfortMinus2, self).__init__(ComfortMode.minus2)


class Comfort(ComfortMode):
    def __init__(self):
        super(Comfort, self).__init__(ComfortMode.confort)


class HeatMode(object):
    # outPlusWaveform :
    # The GPIO output that drive the first OptoTriac (in GPIO.BCM notation)
    # this output supress negative waveform
    # outMinusWaveform :
    # The GPIO output that drive the second OptoTriac (in GPIO.BCM notation)
    # this output supress positive waveform
    def __init__(self, out_plus_waveform=19, out_minus_waveform=12, state_displayer=HeatingStateDisplayer()):
        self._outPlusWaveform = out_plus_waveform
        self._outMinusWaveform = out_minus_waveform
        self.sequencer = ActionSequencer()
        self._confortMinus1Seq = Rolling([Action(self._setConfortMode, duration=297),
                                          Action(self._setEcoMode, duration=3)])
        self._confortMinus2Seq = Rolling([Action(self._setConfortMode, duration=293),
                                          Action(self._setEcoMode, duration=7)])
        self._displayer = state_displayer
        self.initDone = False

    # Must be called once prior to use to initialize HW setting
    def hw_init(self):
        if not test:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self._outPlusWaveform, GPIO.OUT)
            GPIO.setup(self._outMinusWaveform, GPIO.OUT)
        self.initDone = True

    # Set the pilot wire to confort mode = no sinusoid
    def set_confort_mode(self):
        # self.sequencer.cancel()
        self._setConfortMode()
        self._displayer.displayConfortMode()

    # Set the pilot wire to eco mode = full sinusoid
    def set_eco_mode(self):
        # self.sequencer.cancel()
        self._setEcoMode()
        self._displayer.displayEcoMode()

    # set the pilot wire to confort minus 1 degree (4'57 flat, 3" sinusoid)
    def set_confort_minus1(self):
        return self.set_confort_mode()
        logger.debug("starting sequencer with sequence confortMinus1Seq")
        self.sequencer.start(self._confortMinus1Seq)
        self._displayer.displayConfortMinus1Mode()

    # set the pilot wire to confort minus 2 degree (4'53 flat, 7" sinusoid)
    def set_confort_minus2(self):
        return self.set_confort_mode()
        logger.debug("starting sequencer with sequence confortMinus2Seq")
        self.sequencer.start(self._confortMinus2Seq)
        self._displayer.displayConfortMinus2Mode()

    # set the pilot wire to a ratio of confort mode
    # allowed ration from 10 to 90
    def set_confort_ratio(self, ratio):
        eco_time = (5 * 60 * (100 - ratio)) / 100
        conf_time = (5 * 60 * ratio) / 100
        ratio_seq = Rolling([Action(self.set_confort_mode, duration=conf_time),
                            Action(self.set_eco_mode, duration=eco_time)
                            ])
        self.sequencer.start(ratio_seq)
        self._displayer.displayRatioMode(ratio)

    def set_from_confort_mode(self, new_mode):
        """
        :param ComfortMode new_mode: the mode to apply
        Apply the mode if confort, minus1, minus2, does nothing else
        """
        # import pdb; pdb.set_trace()
        logger.debug("HeatMode setting confort mode to %s", new_mode)
        if new_mode == Comfort():
            self.set_confort_mode()
        elif new_mode == ComfortMinus1():
            self.set_confort_minus1()
        elif new_mode == ComfortMinus2():
            self.set_confort_minus2()
        else:
            logger.error("Heatmode unknow mode %s", new_mode)

    # -----------------------------------------------------------
    # set the Triac control output to parameters value
    # will initialize HW if hw has not been initialized
    def _setOutputs(self, plus, minus):
        if test:
            return
        if not self.initDone:
            self.hw_init()
        GPIO.output(self._outPlusWaveform, plus)
        GPIO.output(self._outMinusWaveform, minus)

    def _setConfortMode(self):
        if not test:
            self._setOutputs(plus=GPIO.LOW, minus=GPIO.LOW)

    def _setEcoMode(self):
        if not test:
            self._setOutputs(plus=GPIO.HIGH, minus=GPIO.HIGH)


if __name__ == '__main__':
    print("testing Heatmode manually")
    # logging.basicConfig(filename='Radiator.log', level=logging.DEBUG, format='%(asctime)s %(message)s')
    test = HeatMode()
# test.setConfortMinus1()
