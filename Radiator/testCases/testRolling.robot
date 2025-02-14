*** Settings ***
Documentation	Testing Rolling.py module 
Library		testLibs/RollingLibrary.py

*** Test Cases ***
Empty list #expected not to raise an error
 	create rolling list with	[]
	get next
	
rolling over edge
	${LST}	Create List	"toto"	5	'c'	145.12
	create rolling list with	${LST}
	get next
	result should be	"toto"
	get next
	get next
	result should be	'c'
	Repeat Keyword	21 times	get next
	result should be	145.12

Big list
	${big} =	Evaluate	range(10000)
	create rolling list with	${big}
	Repeat Keyword	10000 times	get next	
	result should be	9999

	
