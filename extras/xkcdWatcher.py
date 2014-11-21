import serial
import webbrowser
import lxml.html
import time

CHECK_DELAY = 1 * 60 * 60  # 1 hour * 60 min/hr * 60 seconds/min = 3600 secs = 1 hr
# CHECK_DELAY = 10 ## 10 seconds in testing mode 

sp = serial.Serial("/dev/tty.usbserial-AM01QY9L", 38400, timeout = 2)
sp.flush()  # clear out whatever junk is in the serial buffer

def whichXKCD():
    '''Fetches the XKCD website and parses out the current comic number'''
    xkcd = lxml.html.parse("http://www.xkcd.com")
    comicDiv = xkcd.getroot().get_element_by_id("comic")
    comicLink = comicDiv[0].attrib['src']
    try:    
        comicName = comicLink.split("/")[4]   
    except ValueError:  ## it wasn't able to convert to integer
        raise RuntimeError("can't parse the link: %s" % comicLink)
    return comicName
    
lastXKCD = ""   
## Set to blank cartoon -- will alert you on first check 
lastTime = time.time()

while(True):                    # endless loop

    response = sp.read(1)       # get one byte

    ## Look for open website command
    if response == "X":
        print "Received button press, loading"
        webbrowser.open("http://xkcd.com")
        sp.write('L')  # toggle light back off 

    thisTime = time.time()

    if (thisTime - lastTime) > CHECK_DELAY:
        currentXKCD = whichXKCD()
        lastTime = thisTime
        print "Current XKCD: %s" % currentXKCD
        
        if not lastXKCD == currentXKCD:
            ## Warn the user!
            sp.write('L')
            lastXKCD = currentXKCD
