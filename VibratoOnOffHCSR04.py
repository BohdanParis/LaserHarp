import math
import RPi.GPIO as GPIO
import time

d1															=7.08
d2															=7.08
location1													=(0,10)
location2													=(10,0)
seperation_needed = 10

def average(items):
	if items == []:
		return 0
	sums=0
	for item in items:
		sums += item
	average_returned = sums/len(items)
	print(average_returned)
	return average_returned


"""	
def find2D(d1,d2):
	a = 2
	b = 2 * ( (d2**2)/20 - (d1**2)/20 ) -20
	c = (( (d2**2)/20 - (d1**2)/20 )) ** 2 + 100 -d2**2
	#print(a,b,c)
	if b**2 - 4*a*c < 0:
		print("NOT TOUCHING")
	else:
		if (-b + math.sqrt(b**2 - 4*a*c))/(2*a) >0:
			x = (-b + math.sqrt(b**2 - 4*a*c))/(2*a)
		else:
			x = (-b - math.sqrt(b**2 - 4*a*c))/(2*a)
		y = x + (d2**2)/20 - (d1**2)/20 
		print("Coodinates are =" + str(x) + "   " + str(y))
"""


try:
		GPIO.setmode(GPIO.BCM)

		PIN_TRIGGER_LEFT_SIDE_1 = 15
		PIN_ECHO_LEFT_SIDE_1 = 14
		
		
		GPIO.setup(PIN_TRIGGER_LEFT_SIDE_1, GPIO.OUT)
		GPIO.setup(PIN_ECHO_LEFT_SIDE_1, GPIO.IN)
		
		
		GPIO.output(PIN_TRIGGER_LEFT_SIDE_1, GPIO.LOW)
	
		print("Waiting for sensor to settle")
		VIBRATO_ON = False
		Previous_Distances = []
		time.sleep(2)
		print("Calculating distance")
		while True:
			#This sends the high signal followed by low signal to send the actual signal for the LEFT FIRST
			GPIO.output(PIN_TRIGGER_LEFT_SIDE_1, GPIO.HIGH)
			time.sleep(0.00001)
			
			GPIO.output(PIN_TRIGGER_LEFT_SIDE_1, GPIO.LOW)
			#print("left 1 trigger sent")
			while GPIO.input(PIN_ECHO_LEFT_SIDE_1)==0:
				pulse_start_time = time.time()
			while GPIO.input(PIN_ECHO_LEFT_SIDE_1)==1:
				pulse_end_time = time.time()

			pulse_duration = pulse_end_time - pulse_start_time
			distance = round(pulse_duration * 17150, 2)
			if distance<40 and distance>0:
				Previous_Distances.append(distance)
			else:
				Previous_Distances.append(Previous_Distances[len(Previous_Distances)-1])

			
			if len(Previous_Distances)==40:
				#Check for the change singal.
				if max(Previous_Distances[1:11]) - Previous_Distances[0] >= seperation_needed:
					#print("first up fine")
					#print(Previous_Distances.index(max(Previous_Distances[1:11])))
					FIRST_PEAK = Previous_Distances.index(max(Previous_Distances[1:11]))
					if min(Previous_Distances[FIRST_PEAK+1:FIRST_PEAK+11]) - Previous_Distances[FIRST_PEAK] <= -10:
						#print("first down fine")
						FIRST_LOW = Previous_Distances.index(min(Previous_Distances[FIRST_PEAK+1:FIRST_PEAK+11]))
						if max(Previous_Distances[FIRST_LOW+1:FIRST_LOW+11]) - Previous_Distances[FIRST_LOW] >= 10:
							#print("second up fine")
							SECOND_PEAK = Previous_Distances.index(max(Previous_Distances[FIRST_LOW+1:FIRST_LOW+11]))
							if min(Previous_Distances[SECOND_PEAK+1:SECOND_PEAK+11]) - Previous_Distances[SECOND_PEAK] <= -10:
								#print("second down is fine")
								SECOND_MIN = Previous_Distances.index(min(Previous_Distances[SECOND_PEAK+1:SECOND_PEAK+11]))
								#NOW WE WOULD LIKE TO EITHER USE VIBRATO OR TURN IT OFF OR ON.
								if VIBRATO_ON == False:
									print("Vibrato on or active")
									Previous_Distances = []
									VIBRATO_ON = True
								elif VIBRATO_ON == True:
									print("Virato off or not active")
									Previous_Distances = []
									VIBRATO_ON = False
								else:
									print("error")
									Previous_Distances = []
			if len(Previous_Distances)==40:
				#Remove earliest one.
				Previous_Distances.pop(0)
			#print("Distance of 1 is:",distance,"cm")
			time.sleep(0.1)
			
finally:
      GPIO.cleanup()
