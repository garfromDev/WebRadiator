# -*- coding: utf-8 -*-
import os
test = os.getenv("RADIATOR_TEST_ENVIRONMENT","").upper() == "TRUE"
if not test:
    import RPi.GPIO as GPIO
import time
import logging

# This module alow to drive RGB Led
class RGB_Displayer:
    # outBlue :
    # The GPIO output that drive the blue Led (in GPIO.BCM notation)
    # outRed :
    # The GPIO output that drive the red Led (in GPIO.BCM notation)
    # outGreen :
    # The GPIO output that drive the green Led (in GPIO.BCM notation)
    # inhibit :
    # function that when return true, forbid to light Led on
    def __init__(self, outRed=23, outGreen=25, outBlue=24, inhibit=lambda x=None : False ):
        self._outRed = outRed
        self._outGreen = outGreen
        self._outBlue = outBlue
        self._inhibit=inhibit
        if test:
            return
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self._outRed, GPIO.OUT)
        GPIO.setup(self._outGreen, GPIO.OUT)
        GPIO.setup(self._outBlue, GPIO.OUT)
        logging.debug("RGB_Displayer initialized")


   # Set the Led to red    
    def setColorRed(self):
        self._turnColorOn(self._outRed)
      

   # Set the Led to green    
    def setColorGreen(self):	    
        self._turnColorOn(self._outGreen)
		
		
   # Set the Led to Blue    
    def setColorBlue(self):   
        self._turnColorOn(self._outBlue)
              
    # turn all Leds off
    def turnOff(self):
        if test:
            return
        GPIO.output(self._outRed, GPIO.LOW)
        GPIO.output(self._outGreen, GPIO.LOW)
        GPIO.output(self._outBlue, GPIO.LOW)
	
    #---------------------------------------
    def _turnColorOn(self, ledOutput):
        self.turnOff()
        if not self._inhibit() and not test:
            GPIO.output(ledOutput, GPIO.HIGH)
    
    
if __name__ == '__main__':
    print("testing RGB_Displayer manually")
    logging.basicConfig(filename='Radiator.log', level=logging.DEBUG, format='%(asctime)s %(message)s')
    test = RGB_Displayer()
    test.setColorRed()
    time.sleep(1)
    test.setColorGreen()
    time.sleep(1)
    test.setColorBlue()
    time.sleep(1)
    test.turnOff()
