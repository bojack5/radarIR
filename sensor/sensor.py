from smbus import SMBus
import time

bus = SMBus(1)

bus.write_byte(0x48, 0x40)
bus.read_byte(0x48)

while(True):
    voltaje = bus.read_byte(0x48)

    print "voltaje = %s mV"%(voltaje)
    time.sleep(0.5)

