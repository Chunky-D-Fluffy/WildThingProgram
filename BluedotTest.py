import os
import time
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
import RPi.GPIO as GPIO
from bluedot import BlueDot
from signal import pause

spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

cs = digitalio.DigitalInOut(board.D22)

mcp = MCP.MCP3008(spi,cs)

bd = BlueDot()

a = 1

def remapRange(value, leftMin, leftMax, rightMin, rightMax):
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin
    
    valueScaled = int(value - leftMin)/ int(leftSpan)
    
    return int(rightMin + (valueScaled * rightSpan))
def dpad(pos):
    global a
    a = 0
    
def stop():
    global a
    a = 1
    
def actuallyTurnOff():
    print('stop')

def run(): 
    lastX = 0
    lastY = 0
    tolerance = 250

    finalXPos = 0
    finalYPos = 0
    
    xChanged = False
    yChanged = False
    
    x = AnalogIn(mcp, MCP.P0)
    y = AnalogIn(mcp, MCP.P1)

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

while True:
    bd.when_pressed = dpad
    bd.when_released = stop
    print('a: ', a)
    
    if a == 0:
        actuallyTurnOff()
    if a == 1:
        run()



