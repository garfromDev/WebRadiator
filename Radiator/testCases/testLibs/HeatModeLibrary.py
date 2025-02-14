import os.path
import subprocess
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from .HeatMode import HeatMode
import RPi.GPIO as GPIO

MINUS = 24
PLUS = 23

class HeatModeLibrary(object):

    def __init__(self):
        self._heat = HeatMode(outPlusWaveform=PLUS, outMinusWaveform=MINUS) 
        # DO not run this test suite on actual HW, or change these number to actual one
        #self._heat = HeatMode(23,24)

    def set_mode_to_confort(self):
        self._heat.set_confort_mode()
        
    def set_mode_to_eco(self):
        self._heat.set_eco_mode()
        
    def output_plus_should_be(self, expected):
        self._output_X_should_be( PLUS, expected)
        
    def output_minus_should_be(self, expected):
        self._output_X_should_be( MINUS, expected)
        
    def set_mode_to_confort_minus_one(self):
        self._heat.set_confort_minus1()
        
    def set_mode_to_confort_minus_two(self):
        self._heat.set_confort_minus2()
        
    def set_mode_to_custom_ratio_of(self, ratio):
        self._heat.set_confort_ratio(int(ratio))

    def color_should_be(self, color):
        ucolor = color.upper()
        maping = { "BLUE":24, "RED":23, "GREEN":25}
        others = set(maping.keys())
        others.discard(ucolor)
        self._output_X_should_be(maping[color], GPIO.HIGH) #output for this color led should be high
        for c in others:
             self._output_X_should_be(maping[c], GPIO.LOW) #other output should be low
        
    def _output_X_should_be(self, output, expected):
        """ verifie que la sortie soit au niveau attendu HIGH ou LOW"""
        level = { "HIGH":GPIO.HIGH, "LOW":GPIO.LOW}[expected]
        actual = GPIO.input(output)
        if actual != level:
            raise AssertionError('output %s : actual %s != expected %s' % (output, actual, level))
