import serial
import webbrowser
import lxml.html
import time

CHECK_DELAY = 5 * 60       ## every X minutes
SITE = "http://www.hackaday.com"

sp = serial.Serial("/dev/ttyUSB0", 38400, timeout = 2)
sp.flush()  # clear out whatever junk is in the serial buffer

sp.write('O')  # toggle light back off 
time.sleep(1)
sp.write('F')  # toggle light back off 
time.sleep(1)
sp.write('O')  # toggle light back off 
time.sleep(1)
sp.write('F')  # toggle light back off 
time.sleep(1)

def whichHAD():
    '''Fetches the HAD website and parses out the current comic number'''
    site = lxml.html.parse(SITE)
    tree = site.getroot()
    posts = tree.find_class("post")
    firstPost = posts[0]
    link = firstPost.iterdescendants("a").next().attrib['href']
    return link
    
lastHAD = whichHAD()
## Default is to always start up with a new link 
lastTime = time.time()

while(True):                    # endless loop

    response = sp.read(1)       # get one byte

    ## Look for open website command
    if response == "X":
        print "Received button press, loading"
        webbrowser.open(lastHAD)
        sp.write('F')  # turn light back off 

    thisTime = time.time()

    if (thisTime - lastTime) > CHECK_DELAY:
        currentHAD = whichHAD()
        lastTime = thisTime
        print "Current HAD: %s" % currentHAD
        
        if not lastHAD == currentHAD:
            ## Warn the user!
            sp.write('O')  # turn light on
            lastHAD = currentHAD

