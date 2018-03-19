import RPi.GPIO as GPIO
import time

TRIG = 23
ECHO = 24

CM_TO_METER = 1000

SPEED_OF_SOUND = 17150

class UltrasonicSensor:

	def __init__(self):
                GPIO.setmode(GPIO.BCM)	
		#Set the Trigger Pin to send out a pulse
                GPIO.setup(TRIG,GPIO.OUT)
		#Set the Echo Pin to receive a pulse
                GPIO.setup(ECHO,GPIO.IN)

	def __del__(self):
		GPIO.cleanup()

	def getReading(self):

		GPIO.output(TRIG,True)
		time.sleep(0.00001)
		GPIO.output(TRIG,False)

		while GPIO.input(ECHO)==0:
			pulse_start = time.time()
    
		while GPIO.input(ECHO)==1:
			pulse_end = time.time()

   		#Calculate the difference in pulse times
		pulse_duration = pulse_end - pulse_start


		distance = pulse_duration *  SPEED_OF_SOUND

		distance = round(distance,2)

		print(distance)

		#Only return the distance if it is closer than 1m
		if distance < CM_TO_METER:

			#Return distance in meters
			return distance/CM_TO_METER
		else:
			return -1