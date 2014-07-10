import serial
import webbrowser
import lxml.html
import time

CHECK_DELAY = 5 * 60       ## every X minutes
SITE = "http://www.hackaday.com"

sp = serial.Serial("/dev/ttyUSB0", 38400, timeout = 2)
sp.flush()  # clear out whatever junk is in the serial buffer

sp.write('O')  # turn light on
time.sleep(1)
sp.write('F')  # turn light back off 
time.sleep(1)
sp.write('O')  # turn light on
time.sleep(1)
sp.write('F')  # turn light back off 
time.sleep(1)

def whichHAD():
    '''Fetches the HAD website and parses out the current top post link'''
    site = lxml.html.parse(SITE)
    tree = site.getroot()
    posts = tree.find_class("post")
    firstPost = posts[0]
    firstLink = firstPost.iterdescendants("a").next()
    url = firstLink.attrib['href']
    return url
    
lastHAD = whichHAD()
sp.write('O')  # turn light on
## Start out with the current top post, light on
lastTime = time.time()

while(True):                    # endless loop

    response = sp.read(1)       # get one byte

    ## Look for open website command
    if response == "X":
        print "Received button press, loading"
        webbrowser.open(lastHAD)
        sp.write('F')  # turn light off 

    thisTime = time.time()

    if (thisTime - lastTime) > CHECK_DELAY:
        currentHAD = whichHAD()
        lastTime = thisTime
        print "Current HAD: %s" % currentHAD
        
        if not lastHAD == currentHAD:
            ## Warn the user!
            sp.write('O')  # turn light on
            lastHAD = currentHAD

