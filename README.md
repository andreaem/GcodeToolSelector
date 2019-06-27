# GcodeToolSelector
Changes G-Code to facilitate a lathe with multiple cutting heads


To run type:

python3 GcodeInterpreter.py

This will look for a file called gcode.ngc in the same directory as the python file, it will convert based on the following rules, and then output a file called output.ngc


***Looks for all codes beginning with the letter "T" ***

-If it's the word TAILSTOCKUNFIXED it replaces it with TAILSTOCKFIXED, showing that the program was run.

-If it's followed by two numbers and then stuff, eg T21 M6 G43 it checks what the two digits are right after the "T" 

It remembers that two digit code as the TOOL NUMBER

It adds these two lines of code to home the tool:

G53 G0 X-0.125

G53 G0 A-0.125

-If it's a T not followed by two digits or the characters above it reports an error and stops.

*** OTHERWISE ***

if the TOOL NUMBER is less than the TOOL PIVOT (which has been set to 15 at the top) it reproduced the line of code without changes

if the TOOL NUMBER is greater than the TOOL PIVOT, it skips any X axis command
