import RPi.GPIO as GPIO
import datetime
import time
import os
import math
GPIO.setmode(GPIO.BCM)

#Set the variant of 3461X 4 digit 7 segment display being used.
#A series is common cathode, segment pins are HIGH, digit pins are LOW to light segments
#B series is common anode, segment pins are LOW, digit pins are HIGH to light segments
DisplayType = 'B'

 
# Map the GPIO ports for each of the 7seg input pins
segments =  (11,4,23,8,7,10,18,25)
# 7seg_segment_pins (11,7,4,2,1,10,5,3) +  100R inline resistor
 
for segment in segments:
    GPIO.setup(segment, GPIO.OUT)
    GPIO.output(segment, 0)
 
# Map the GPIO ports for the digit 0-3 pins 
digits = (22,27,17,24)
# 7seg_digit_pins (12,9,8,6) digits 0-3 respectively
 
for digit in digits:
    GPIO.setup(digit, GPIO.OUT)
    GPIO.output(digit, 1)

#Map the segments required LIT for each character

if DisplayType == 'B':
    #Common anode display. Segment pins are LOW for lit.
    num = {' ':(1,1,1,1,1,1,1),
        '0':(0,0,0,0,0,0,1),
        '1':(1,0,0,1,1,1,1),
        '2':(0,0,1,0,0,1,0),
        '3':(0,0,0,0,1,1,0),
        '4':(1,0,0,1,1,0,0),
        '5':(0,1,0,0,1,0,0),
        '6':(0,1,0,0,0,0,0),
        '7':(0,0,0,1,1,1,1),
        '8':(0,0,0,0,0,0,0),
        '9':(0,0,0,0,1,0,0),
        'A':(0,0,0,1,0,0,0),
        'C':(0,1,1,0,0,0,1),
        'F':(0,1,1,1,0,0,0)}
    
    #Set the direction of the relevant ground pins
    #based on the common anode configuration
    GroundActive = 1
    GroundPassive = 0
    
else:
    #Common cathode display. Segment pins are HIGH for lit.
    num = {' ':(0,0,0,0,0,0,0),
        '0':(1,1,1,1,1,1,0),
        '1':(0,1,1,0,0,0,0),
        '2':(1,1,0,1,1,0,1),
        '3':(1,1,1,1,0,0,1),
        '4':(0,1,1,0,0,1,1),
        '5':(1,0,1,1,0,1,1),
        '6':(1,0,1,1,1,1,1),
        '7':(1,1,1,0,0,0,0),
        '8':(1,1,1,1,1,1,1),
        '9':(1,1,1,1,0,1,1),
        'A':(1,1,1,0,1,1,1),
        'C':(1,0,0,1,1,1,0),
        'F':(1,0,0,0,1,1,1)}
    
    #Set the direction of the relevant ground pins
    #based on the common cathode configuration
    GroundActive = 0
    GroundPassive = 1

# Function to return CPU temperature from the OS sensors, as a character string
def getCPUtemperature():
    retval = os.popen('vcgencmd measure_temp').readline()
    return(retval.replace('temp=','').replace("'C\n",""))




#Choose the refresh rate for temp readings in seconds or decimals thereof
lngRefreshSecs = 0.5

#Choose the number of seconds to diplay each conversion unit for.
lngUnitShowSecs = 5

#Default the intLoop variable to enter the loop for the first time
intLoop = 0
 
try:
    while True:
        
        timestamp = datetime.datetime.now() + datetime.timedelta(hours=0, minutes=0, seconds=lngUnitShowSecs)
        
        #Increment or reset the intLoop variable to advance
        #the scrolling through the 3 temperature units
        if intLoop < 4:
            intLoop = intLoop + 1
        else:
            intLoop=2

        #Display each unit of tempertature reading for a period of time based on the lngUnitShowSecs variable
        while datetime.datetime.now() < timestamp:
            
            #Set the refresh interval loop based on lngRefreshSecs variable
            timestamp2 = datetime.datetime.now() + datetime.timedelta(hours=0, minutes=0, seconds=lngRefreshSecs)
            
            #Refresh the temp reading each time round at the lngRefreshSecs interval
            #Take the raw Celcuis (C) value, or convert it to Fahrenheit (F) or Kelvin (A) [for Absolute]
            temp=float(getCPUtemperature())
            if intLoop == 1 or intLoop == 4:
                #Fahrenheit
                temp=round(int(1.8*temp+32),1)
                tempout = str(temp).replace('.','') + 'F'
                if intLoop == 4:
                    intLoop = 1
            elif intLoop == 2:
                #Kelvin
                temp=round(int(temp+273.15),0)
                tempout = str(temp).replace('.','') + 'A'
                
            elif intLoop ==3:
                #Celsius
                tempout = str(temp).replace('.','') + 'C'
                
            while datetime.datetime.now() < timestamp2:
                
                #Format the string and display the value across the 4 digits
                s = str(tempout).rjust(4)
                
                #Loop through each of the 4 digits one by one
                #Then loop through each of the 7 segments per digit
                #Set each mapped GPIO pin on the digit and segment(s) to be lit
                for digit in range(4):
                    for loop in range(0,7):
                        GPIO.output(segments[loop], num[s[digit]][loop])
                        
                        #If the output in this loop is Celsius, display the decimal point.
                        
                        #The GroundActive and GroundPassive variables are used in reverse
                        #to appropriately ground or activate the decimal point pin
                        #depending on which display configuration is being used
                        if (digit == 1) and intLoop >= 3:
                            GPIO.output(25, GroundPassive)
                        else:
                            GPIO.output(25, GroundActive)
                    
                    #Flip the appropriate digit pin HIGH/LOW to show the digit for a split second.
                    #0.0001 second pause gives sufficient speed for the display to appear to show
                    #all digits solidly due to the latency of the human eye.
                            
                    #Increase this time delay to show at visible speed the lighting
                    #of each individual digit separately
                    GPIO.output(digits[digit], GroundActive)
                    time.sleep(0.0001)
                    GPIO.output(digits[digit], GroundPassive)
            
finally:
    #Unconfigure the GPIO pin mappings
    GPIO.cleanup()
