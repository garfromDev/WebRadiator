*** Settings ***
Documentation	Essais de robot pour tester HeatMode, ATTENTION tests durent 20mn
Library		testLibs/HeatModeLibrary.py

*** Test Cases ***
Confort Mode
	set mode to confort
	output plus should be	 LOW
	output minus should be	 LOW
	color should be	         RED

Eco Mode
	set mode to eco
	output plus should be	 HIGH
	output minus should be	 HIGH
	color should be	         BLUE

Confort minus one mode
#we want mode to be CONFORT during 4 min 57 sec, checking every sec
# we want mode to be ECO during 3 sec, checking every sec
# we want mode to come back to CONFORT
	set mode to confort minus one
	mode should be	'CONFORT'
	Wait Until Keyword Succeeds	4 min 58sec	1 sec	mode should be	'ECO'
	Wait Until Keyword Succeeds	4 sec		1 sec	mode should be	'CONFORT'

Confort minus two mode
#we want mode to be CONFORT during 4 min 53 sec, checking every sec
# we want mode to be ECO during 7 sec, checking every sec
# we want mode to come back to CONFORT
	set mode to confort minus two
	mode should be	'CONFORT'
	Wait Until Keyword Succeeds	4 min 54sec	1 sec	mode should be	'ECO'
	Wait Until Keyword Succeeds	8 sec		1 sec	mode should be	'CONFORT'

Custom confort ratio 50
#we want mode to be CONFORT during 2 min 30 sec, checking every sec
# we want mode to be ECO during 2 mn 30 sec, checking every sec
# we want mode to come back to CONFORT
	set mode to custom ratio of	50
	mode should be	'CONFORT'
	Wait Until Keyword Succeeds	2 min 31sec	1 sec	mode should be	'ECO'
	Wait Until Keyword Succeeds	2 min 31sec	1 sec	mode should be	'CONFORT'

Custom confort ratio 80
#we want mode to be CONFORT during 4 min , checking every sec
# we want mode to be ECO during 1 mn , checking every sec
# we want mode to come back to CONFORT
	set mode to custom ratio of	80
	mode should be	'CONFORT'
	Wait Until Keyword Succeeds	4 min 1 sec 	1 sec	mode should be	'ECO'
	Wait Until Keyword Succeeds	1 min 1sec	1 sec	mode should be	'CONFORT'

*** Keywords ***
mode should be 
	[Arguments]	${mode}
	run keyword if	${mode}=='CONFORT'	output plus should be	 LOW	 	
	run keyword if	${mode}=='CONFORT'	output minus should be	 LOW
	run keyword if	${mode}=='ECO'		output plus should be	 HIGH
	run keyword if	${mode}=='ECO'		output minus should be	 HIGH
