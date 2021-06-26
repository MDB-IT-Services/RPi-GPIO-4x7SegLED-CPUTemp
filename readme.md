*Code modified, tweaked and tailored from code by bertwert 
on RPi forum thread topic 91796*

 **              (       )  
    (          )\ ) ( /(  
  ( )\ (   (  (()/( )\()) 
  )((_))\  )\  /(_)|(_)\  
 ((_)_((_)((_)(_))__ ((_) 
 | _ ) __| __/ __\ \ / / 
 | _ \ _|| _|\__ \\ V /  
 |___/___|___|___/ |_|**

2017-11-04 - MDB IT Services
Temperature readings, conversion and scrolling functionality added by Beesy

**This script is designed for the following:
Common cathode or anode 3461 A/B series 4 digit 7 segment displays
3.3v GPIO pin output, combined with 100R resistors between the segment pins and the GPIO**

The 3461 has a forward voltage of 1.8v and max current of 20mA. 3.3v input with 100R resistors
gives adequate brightness but limits input current to 15mA to extend the life of the display.

If you are using as 3461A series common cathode display, alter
the `DisplayType` variable below from 'B' to'A' and the relevant mappings
will be inverted to set the correct GPIO pins to their opposite defaults.

If you are using 5v GPIO, you must use higher value resistors to prevent over current reaching the LED segments.
#Failure to do so will likely damage your display. Ohms law allows you to calculate the required resistors.

`R = (V(i) - V(f)) / I`

**R** is the resistor value required.
**V(i)** is the input voltage from the GPIO. Raspberry Pi is 3.3v. Arduino breakout boards can be 5v.
**V(f)** is the 'forward voltage' of the LED. Refer to the datasheet to confirm. 3461B has a forward voltage of 1.8v
**I** is the desired current in Amps. The 3461B has a current tolerance of 20mA (0.02A).
The configuration described in this script is based upon using 15mA (0.015A) to leave headroom from the maximum.

If using 5v GPIO, the calculation would be as follows:

`R = (V(i) - V(f)) / I
R = (5v - 1.8v) / 0.015A
R = 3.2v / 0.015A
R = 213.333 Ohms`

It is therefore recommended to use 220R resistors when using 5v GPIO.

If any of your values differ by setup (GPIO voltage) or display (forward voltage / current tolerance)
simply plug those values into the equation and work out the appropriate resistance needed.
A general rule is to use 75% of the current tolerance of the display for the best trade off
between segment brightness and LED lifespan.

If the required resistance is between values of resistor, it is advisable to use the higher value
at the cost of brightness in order to extend the life of the display. Resistors of smaller values can be
connected in series to make up the value. eg 100R and 220R in series would give 320R resistance overall.

Use Digit Mapper.xlsx to map out pin outs for custom segment display. Enter a 'y' in each segment you wish to be lit, 
then copy the output array for your version of display (A or B) and add it to the mapping variables. Non-alpha numeric 
layouts can be added, but you will need to assign them an alpha-numeric character in order to display them. 
Preferably choose one of the undisplayable characters from the lists contained in the Excel document to avoid confusion 
with otherwise valid displayable characters.
