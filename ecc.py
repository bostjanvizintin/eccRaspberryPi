import urllib
import json
import time
from helpers import *

HASH = 'ij43mif5z8ec3w23z89jnv85e9o0p8e1'
SERVER = '192.168.0.103'
UPDATE_TIME = 60*1000
SENSORBOX = []
MIN_VALUE_TO_POST = 0.18

url = 'http://' + SERVER + '/pi/getSensorBoxData/' + HASH

print "Printing url: "
print url
print "\n"


try:
	#print "Inside try statement\n"
	response = urllib.urlopen(url).read()
	SENSORBOX = json.loads(response)['sensorBox']
except:
	#print "Inside except statement\n"
	sendError(101, HASH, SERVER)

#print SENSORBOX

numOfSensors = len(SENSORBOX['sensors'])
values = [0]*numOfSensors
updatedAt = [time.time()*1000]*numOfSensors
numOfReadings = [0]*numOfSensors
lastUpdateWasZero = [False]*numOfSensors

while(1):
	#print "Inside while statement\n"
	for i in range(0, numOfSensors):
		#print "Inside first for loop\n"
		values[i] += getSensorValue(SENSORBOX['sensors'][i]['input']-1, SENSORBOX['sensors'][i]['sampleTime'], SENSORBOX['sensors'][i]['sensorMvPerAmp'])
		#print values[i]
		numOfReadings[i]+=1
	
	for i in range(0, numOfSensors):
		#print "inside second for loop\n"	
		if(time.time()*1000 - updatedAt[i] > + UPDATE_TIME):
			if not(lastUpdateWasZero[i] and values[i]/numOfReadings[i] < MIN_VALUE_TO_POST):
				if values[i]/numOfReadings[i] < MIN_VALUE_TO_POST:
					lastUpdateWasZero[i] = True
				else:
					lastUpdateWasZero[i] = False
				postMeasurement(SERVER, SENSORBOX['sensors'][i]['id'], values[i]/numOfReadings[i])
				updatedAt[i] = time.time()*1000
				numOfReadings[i] = 0
				values[i] = 0
			
			
