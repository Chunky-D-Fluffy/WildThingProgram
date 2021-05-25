import os
import time
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
import RPi.GPIO as GPIO

LspeedPin = 18
LbackwardPin = 14
LforwardPin = 2
RspeedPin = 27
RbackwardPin = 15
RforwardPin = 3

GPIO.setwarnings(False)

GPIO.setup(LspeedPin, GPIO.OUT)
GPIO.setup(LbackwardPin, GPIO.OUT)
GPIO.setup(LforwardPin, GPIO.OUT)
GPIO.setup(RspeedPin, GPIO.OUT)
GPIO.setup(RbackwardPin, GPIO.OUT)
GPIO.setup(RforwardPin, GPIO.OUT)

Lspeed = GPIO.PWM(LspeedPin, 1000)
Rspeed = GPIO.PWM(RspeedPin, 1000)

spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

cs = digitalio.DigitalInOut(board.D22)

mcp = MCP.MCP3008(spi,cs)


lastX = 0
lastY = 0
tolerance = 250

finalXPos = 0
finalYPos = 0

def right():
    Lspeed.start(10)
    Rspeed.start(10)
    GPIO.output(LbackwardPin,GPIO.LOW)
    GPIO.output(RbackwardPin,GPIO.HIGH)
    GPIO.output(LforwardPin,GPIO.HIGH)
    GPIO.output(RforwardPin,GPIO.LOW)
    print('right')
def left():
    Lspeed.start(10)
    Rspeed.start(10)
    GPIO.output(LbackwardPin,GPIO.HIGH)
    GPIO.output(RbackwardPin,GPIO.LOW)
    GPIO.output(LforwardPin,GPIO.LOW)
    GPIO.output(RforwardPin,GPIO.HIGH)
    print('left')
def forward():
    Lspeed.start(10)
    Rspeed.start(10)
    GPIO.output(LbackwardPin,GPIO.LOW)
    GPIO.output(RbackwardPin,GPIO.HIGH)
    GPIO.output(LforwardPin,GPIO.HIGH)
    GPIO.output(RforwardPin,GPIO.LOW)
    print('forward')
def backward():
    Lspeed.start(10)
    Rspeed.start(10)
    GPIO.output(LbackwardPin,GPIO.HIGH)
    GPIO.output(RbackwardPin,GPIO.HIGH)
    GPIO.output(LforwardPin,GPIO.LOW)
    GPIO.output(RforwardPin,GPIO.LOW)
    print('backward')
def stop():
    Lspeed.start(0)
    Rspeed.start(0)
    print('stop')
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
    if finalYPos < 20:
        forward()
    elif finalYPos > 80:
        backward()
    elif finalXPos < 20:
        left()
    elif finalXPos > 80:
        right()
    else:
        stop()
    print('X: ', finalXPos)
    print('Y: ', finalYPos)
    time.sleep(.1)
    


