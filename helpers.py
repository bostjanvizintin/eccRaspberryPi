import time
import urllib
import urllib2
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
#from adc import *

SPI_PORT = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

def sendError(errorCode, hash, server):
	print errorCode
	

def delay(miliseconds):
	startTime = time.time()*1000
	while(1):
		if(startTime< time.time()*1000 - miliseconds):
			break

def getSensorValue(port, sampleTime, mvPerAmp):
	#print "mvPerAmp for sensor " + str(port) + " : " + str(mvPerAmp)
	result = 0
	readValue = 0
	maxValue = 0
	minValue = 1024
	ampsRms = 0

	startTime = time.time()*1000
	while((time.time()*1000 - startTime) < sampleTime):
		readValue = mcp.read_adc(port)
		#print "ReadValue for " + str(port) + " : " + str(readValue)
		if(readValue > maxValue):
			maxValue =  readValue
		elif(readValue < minValue):
			minValue = readValue
		result = ((maxValue - minValue) * 5.0) /1024.0
		vrms = (result/2) * 0.707
		ampsRms = (vrms * 1000) / mvPerAmp

	#print "maxValue: " + str(maxValue)
	#print "minValue: " + str(minValue)
	#print "ampsRms: " + str(ampsRms)
	return ampsRms

def postMeasurement(server, idSensor, value):
	try:
		url = 'http://' + server + '/pi/measurement/' + str(idSensor) + '/' + str(value)
		response = urllib.urlopen(url).read()
		print url
	except:
		sendError(102)
