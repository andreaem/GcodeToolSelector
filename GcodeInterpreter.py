import re


toolpivot = 15 #Tools 1-8 are on the turret and move in X and Z. 21-28 are on the tailstock, for drilling and the like.

w = open("output.ngc", "w")

def ngcO (line, fileio = w): #ngc output line
    line = line + "\n"
    w.write (line);
    pass

f = open("gcode.ngc", "r")


code = f.readline()
toolnum = False
while (code):
    if code[0] == "T":
        #Switch the text to mark the file fixed
        if bool (re.search("TAILSTOCKUNFIXED", code)) :
            ngcO ("TAILSTOCKFIXED")
            print ("FOUND")
        #Its a set tool command so home everyone 
        else:
            print ("TOOL CHANGE, to number ", code[1:3]) #all tool selections are of the form T## 
            toolnum = code[1:3]            
            #Send all tool arms home and then set tool
            ngcO ("G53 G0 X-0.125") 
            ngcO ("G53 G0 A-0.125")
            ngcO (code)
    else:
        #ngcO (code[:-1]) #-1 gets rid of the line break
    
        if int(toolnum) < toolpivot:
            #These tools run on x and z axis
            ngcO (code)            
            pass
        else :
            #these are Z only tools
            if re.search ("^G\d\d\s.X*",code):
                print ("X motion found in z only tool, DELETED")
            else:
                ngcO (code)

    code = f.readline()
    
w.close()