import serial
import minimalmodbus
import datetime
from siliconcraft.sc2004mbs import SC2004MBS

# Configuration
minimalmodbus.BAUDRATE = 9600
minimalmodbus.TIMEOUT = 1.0

minimalmodbus.BYTESIZE = 8
minimalmodbus.PARITY = serial.PARITY_NONE
minimalmodbus.STOPBITS = 1

slaveId = 1
deviceId = 'COM3'

# Construct and instantiate the display
instrument = minimalmodbus.Instrument(deviceId, slaveId)
display = SC2004MBS(instrument)

#Display text
text = minimalmodbus.Instrument('COM3', 1) # port name, slave address (in decimal)
text.write_string(0, 'This is Sparta', 7)  #Write text in the first row


#current DateTime
dt= datetime.datetime.now()
dd=dt.strftime("%d/%m/%Y %H:%M:%S").format(dt)
text.write_string(10, dd, 10)

#Leds glow based on corresponding Switch state
while True:
    pins = display.io_pins() # Read the pins
    switches = pins[0:4] # Seperate the classes
    leds = pins[4:8]
    for id in range(0, 4):
        display.set_led(id, switches[id])




"""
result = []
for switch in switches:
    if switch:
        result.append('X')
    else:
        result.append('O')

print("Switches: {0} {1} {2} {3}".format(*result))


i = 0
while i<len(switches):
    if switches[i] == True:
        print ("Leds are active")
    else:
        print ("Leds aren't active")
    i = i+1
"""