import serial
import webbrowser
import lxml.html
import time

CHECK_DELAY = 5 * 60       ## every X minutes
SITE = "http://www.hackaday.com"

sp = serial.Serial("/dev/ttyUSB0", 38400, timeout = 2)
sp.flush()  # clear out whatever junk is in the serial buffer

def whichHAD():
    '''Fetches the HAD website and parses out the current top post link'''
    site = lxml.html.parse(SITE)
    tree = site.getroot()
    posts = tree.find_class("post")
    firstPost = posts[0]
    firstLink = firstPost.iterdescendants("a").next()
    url = firstLink.attrib['href']
    return url

def LED_on():    
    sp.write('O')  # turn light on

def LED_off():    
    sp.write('F')  # turn light off

## Blink to test LED, make sure working
for i in range(3):
    LED_on()
    time.sleep(0.5)
    LED_off()
    time.sleep(0.5)

## Initialize
## Start out with the current top post, light on
lastHAD = whichHAD()
LED_on()
lastTime = time.time()

while(True):                    # endless loop

    response = sp.read(1)       # get one byte

    ## Look for open website command
    if response == "X":
        print "Received button press, loading"
        webbrowser.open(lastHAD)
        LED_off() 

    thisTime = time.time()

    if (thisTime - lastTime) > CHECK_DELAY:
        currentHAD = whichHAD()
        lastTime = thisTime
        print "Current HAD: %s" % currentHAD
        
        if not lastHAD == currentHAD:
            ## Warn the user!
            LED_on() 
            lastHAD = currentHAD

