import serial
import webbrowser

sp = serial.Serial("/dev/ttyUSB0", 38400, timeout = 2)
sp.flush()  # clear out whatever junk is in the serial buffer

while(True):                    # endless loop

    response = sp.read(1)       # get one byte

    ## Look for open website command
    if response == "X":
        print "Received button press"
        webbrowser.open("http://www.littlehacks.org/serialEasterEgg.html")
    
    ## Send blink-LED command
    sp.write('L') 
    print "Sending blink command"    

