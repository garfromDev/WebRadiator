# -*- coding: utf-8 -*-
from . import const as CST
import os
import subprocess

""" This utility module define constant """
#VERSION will be valid only when launched from the local repo

CST.MIN = 60                    # conversion of minutes to second
CST.SEC = 1
CST.WEEKCALJSON = "week.json"   # the file that defines the weekly calendar
CST.BASE_PATH = os.getenv("CALENDAR_PATH") or "./"         # the path for other files
CST.CALENDAR_PATH = os.getenv("CALENDAR_PATH") or "./"         # the path to the weekly calendar file
CST.METACACHING = 5 * CST.MIN   # caching duration for meta mode check
CST.TEMPCACHING = 2 * CST.MIN   # caching duration for temperature check
CST.MAIN_TIMING = 1 * CST.MIN   # main looprefreshing
if os.getenv("RADIATOR_TEST_ENVIRONMENT", "False").upper() == "TRUE":
    CST.MAIN_TIMING = 5 * CST.SEC
    CST.METACACHING = 5 * CST.SEC
CST.CONFORT = "confort"         # confort meta mode
CST.CONFORTPLUS = "confortPlus" # confort plus meta mode
CST.ECO = "eco"                 # eco meta mode
CST.UNKNOW = "unknow"           # unknow meta mode
CST.MAX_DELTA_TEMP = 0.4        # maximum temperature span between 2 simultaneous measurement for filtering (in °C)
CST.LM35_INTERVAL = 0.01        # interval in sec between 2 measure for filtering temperature measurement
CST.LOG_FILE = "Radiator.log"
