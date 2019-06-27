import re

toolpivot = 15 #Tools 1-8 are on the turret and move in X and Z. 21-28 are on the tailstock, for drilling and the like.
toolnum = False #there is no tool being used yet

#open read and write filestreams
w = open("output.ngc", "w")
w.write(";This file has been processed with the GcodeInterpreter")
f = open("gcode.ngc", "r")

'''
Write a line of gocde to the file
'''
def ngcO (line, fileio = w):
    line = line + "\n"
    w.write (line);

#read first line of code and itterate until end of file
code = f.readline()
while (code):
    if code[0] == "T":
        #Switch the text to mark the file fixed
        if bool (re.search("TAILSTOCKUNFIXED", code)) :
            ngcO (";TAILSTOCKFIXED")
            print ("FOUND")
        #Its a set tool command so home everyone 
        elif bool (re.search("^T\d\d\s.*", code)) :            
            print ("TOOL CHANGE, to number ", code[1:3]) #all tool selections are of the form T## 
            toolnum = code[1:3]            
            #Send all tool arms home and then set tool
            ngcO ("; Adding 2 lines to home both tools before a tool change")
            ngcO ("G53 G0 X-0.125") 
            ngcO ("G53 G0 A-0.125")
            ngcO (code)
        else:
            print ("ERROR a faulty tool code was found")
            ngcO ("ERROR A FAULTY TOOL CODE WAS FOUND")
            break 
    else:
        #this command isn't a toolchange 
        
        if int(toolnum) < toolpivot:
            #either the toolnum has not been set, int(False)=0 or 
            #the tool is less than the tool pivot so
            #These tools run on x and z axis so no changes made
            ngcO (code)
        else :
            #these are Z only tools so remove any X motion
            if re.search ("^G\d\d\s.X*",code):
                code = ";X motion on Z only tool - " + code
            else:
                ngcO (code)
    #Get the next line of code
    code = f.readline()

#clean up open filestreams
f.close()
w.close()