*** Settings ***
Documentation	Testing Heat Calendrar libray
Library		testLibs/HeatCalendarLibrary.py
Test Setup	set calendar	testCases/test.json

*** Test Cases ***
mode eco
#Monday
	set time to	2018 02 26 02 45
	result should be	eco

mode confort
#Sunday
	set time to	2018 03 04 12 11
	result should be	confort

out of range
	set time to	2018 02 26 00 00
	result should be	unknow


 
