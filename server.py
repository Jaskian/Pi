#!/usr/bin/python
import web
import smbus
import math

urls = (
    '/', 'index'
)

# Power management registers
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c

bus = smbus.SMBus(1)
address = 0x68

def readWord(adr):
    high = bus.read_byte_data(address, adr)
    low = bus.read_byte_data(address, adr+1)
    val = (high << 8) + low
    return val

def readWord2c(adr):
    val = readWord(adr)
    if (val >= 0x8000):
        return -((65535 - val) + 1)    
    else :
	    return val

def dist(a,b):
    return math.sqrt((a*a) + (b*b))

def getYRotation(x,y,z):
#    radians = math.atan2(x, dist(y,z))    
#    return -math.degrees(radians)
	return math.atan2(-y, z) * 180/math.pi
#	return math.atan2(x, math.sqrt(y*y + z*z)) * 180/math.pi

def getXRotation(x,y,z):
#    radians = math.atan2(y, dist(x,z))
#    return math.degrees(radians)
	return math.atan2(-x, math.sqrt(y*y + z*z)) * 180/math.pi
#	return math.atan2(-x, z) * 180/math.pi

class index:
    def GET(self):
        accelXOut = readWord2c(0x3b)
        accelYOut = readWord2c(0x3d)
        accelZOut = readWord2c(0x3f)

        return str(getXRotation(accelXOut,accelYOut,accelZOut))+" "+str(getYRotation(accelXOut,accelYOut,accelZOut))


if __name__ == "__main__":
    bus.write_byte_data(address, power_mgmt_1,0)

    app = web.application(urls, globals())
    app.run()
