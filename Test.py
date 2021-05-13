import os
import time
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
import RPi.GPIO as GPIO

spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

cs = digitalio.DigitalInOut(board.D22)

mcp = MCP.MCP3008(spi,cs)

lastX = 0
lastY = 0
tolerance = 250

finalXPos = 0
finalYPos = 0

def remapRange(value, leftMin, leftMax, rightMin, rightMax):
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin
    
    valueScaled = int(value - leftMin)/ int(leftSpan)
    
    return int(rightMin + (valueScaled * rightSpan))

while True:
    xChanged = False
    yChanged = False
    
    x = AnalogIn(mcp, MCP.P0)
    y = AnalogIn(mcp, MCP.P1)
    
    print('x: ', x.value)
    print('y: ', y.value)

    xValue = x.value
    yValue = y.value
    
    xAdjust = abs(xValue - lastX)
    yAdjust = abs(yValue - lastY)
    
    if xAdjust > tolerance:
        xChanged = True
    
    if yAdjust > tolerance:
        yChanged = True
        
    if xChanged:
        finalXPos = remapRange(xValue, 0, 65535, 0, 100)
        lastX = xValue
        
    if yChanged:
        finalYPos = remapRange(yValue, 0, 65535, 0, 100)
        lastY = yValue
    
    print('X: ', finalXPos)
    print('Y: ', finalYPos)
    time.sleep(.1)


   


