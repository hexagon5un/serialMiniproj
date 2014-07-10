import serial
import webbrowser
import lxml.html
import time

CHECK_DELAY = 1 * 60 * 60  # 1 hour * 60 min * 60 seconds 
## CHECK_DELAY = 10 ## testing mode 

sp = serial.Serial("/dev/ttyUSB0", 38400, timeout = 2)
sp.flush()  # clear out whatever junk is in the serial buffer

def whichXKCD():
    '''Fetches the XKCD website and parses out the current comic number'''
    xkcd = lxml.html.parse("http://www.xkcd.com")
    comicDiv = xkcd.getroot().get_element_by_id("comic")
    comicLink = comicDiv[0].attrib['href']
    try:    
        comicNumber = int(comicLink.split("/")[3])   ## (@_@) don't like this so checking integer type 
    except ValueError:  ## it wasn't able to convert to integer
        raise RuntimeError("can't parse the link: %s" % comicLink)
    return comicNumber
    
lastXKCD = 1   
## Set to cartoon number one -- will alert you on first check 
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
        print "Current XKCD: %d" % currentXKCD
        
        if not lastXKCD == currentXKCD:
            ## Warn the user!
            sp.write('L')
            lastXKCD = currentXKCD

