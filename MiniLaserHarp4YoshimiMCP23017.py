import RPi.GPIO as GPIO
import pygame
import time
import random
import math
import pygame_menu
import keyboard
from pynput.keyboard import Key, Controller
import rtmidi
from rtmidi.midiconstants import (ALL_SOUND_OFF, CONTROL_CHANGE,
                                  RESET_ALL_CONTROLLERS) #This is for when you close the program with a gesture.
import wiringpi as wiringpi  

pin_base = 65       # lowest available starting number is 65  
i2c_addr = 0x20     # A0, A1, A2 pins all wired to GND  
pin_base2 = 65+16       # lowest available starting number is 65  
i2c_addr2 = 0x21     # A0, A1, A2 pins all wired to GND  
wiringpi.wiringPiSetup()                    # initialise wiringpi  
wiringpi.mcp23017Setup(pin_base,i2c_addr)   # set up the pins and i2c address  
wiringpi.mcp23017Setup(pin_base2,i2c_addr2) 

pygame.init()
pygame.mixer.init()

midiout = rtmidi.MidiOut()
available_ports = midiout.get_ports()

if available_ports:
	print(available_ports)
	port_number = 0
	for port_name in available_ports:
		if port_name[0:7] == "yoshimi": #Choose the yoshimi software which must be running for this to work.
			break
		port_number += 1
	midiout.open_port(port_number)
	
else:
	print("will fail")
	midiout.open_virtual_port("My virtual output")
	exit()

speed_control = 0.05 # 0.1 = very fast playback, 0.2 = fast history playback, 0.25 = medium speed playback, 0.5 seconds very slow playback

width, height = 1920, 1080
screen = pygame.display.set_mode((width, height))
bg = pygame.image.load('bgimg7.png')
keysimg = pygame.image.load('noteimg.png')
Message = 'Welcome!'
starttime = endtime = 0


#Is this going to be shine light activate note, if so True.
INVERTED = False

Note_Names=["guitar_C4_very-long_piano_harmonics.mp3","guitar_C5_very-long_piano_harmonics.mp3","guitar_Cs3_very-long_forte_normal.mp3","guitar_D3_very-long_piano_normal.mp3","guitar_D5_very-long_forte_harmonics.mp3","guitar_Ds4_very-long_piano_normal.mp3","guitar_E2_very-long_piano_normal.mp3","guitar_Gs2_very-long_forte_normal.mp3","guitar_Gs3_very-long_piano_normal.mp3","guitar_Gs4_very-long_piano_normal.mp3","guitar_A3_very-long_pianissimo_harmonics.mp3","guitar_A3_very-long_piano_harmonics.mp3","guitar_A4_very-long_forte_normal.mp3","guitar_Ds4_very-long_piano_harmonics.mp3","guitar_Ds5_very-long_piano_normal.mp3","guitar_E2_very-long_forte_normal.mp3","guitar_E3_very-long_pianissimo_harmonics.mp3","guitar_E4_very-long_piano_harmonics.mp3","guitar_E5_very-long_forte_harmonics.mp3","guitar_G4_very-long_forte_normal.mp3","guitar_G4_very-long_piano_normal.mp3","guitar_G5_very-long_forte_harmonics.mp3","guitar_Gs3_very-long_forte_normal.mp3","guitar_Gs5_very-long_forte_normal.mp3"]

RisingSpeed = 10
number_of_strings = 24
interval = width / number_of_strings
Score = 0
clock = pygame.time.Clock()
dt = 0
sleeptime = 0.02
pause = False
Offset_from_side = interval/4
Note1_Xposition = 0 + Offset_from_side
Note2_Xposition = 1 * interval + Offset_from_side
Note3_Xposition = 2 * interval + Offset_from_side
Note4_Xposition = 3 * interval + Offset_from_side
Note5_Xposition = 4 * interval + Offset_from_side
Note6_Xposition = 5 * interval + Offset_from_side
Note7_Xposition = 6 * interval + Offset_from_side
Note8_Xposition = 7 * interval + Offset_from_side
Note9_Xposition = 8 * interval + Offset_from_side
Note10_Xposition = 9 * interval + Offset_from_side
Note11_Xposition = 10 * interval + Offset_from_side
Note12_Xposition = 11 * interval + Offset_from_side
Note13_Xposition = 12 * interval + Offset_from_side
Note14_Xposition = 13 * interval + Offset_from_side
Note15_Xposition = 14 * interval + Offset_from_side
Note16_Xposition = 15 * interval + Offset_from_side
Note17_Xposition = 16 * interval + Offset_from_side
Note18_Xposition = 17 * interval + Offset_from_side
Note19_Xposition = 18 * interval + Offset_from_side
Note20_Xposition = 19 * interval + Offset_from_side
Note21_Xposition = 20 * interval + Offset_from_side
Note22_Xposition = 21 * interval + Offset_from_side
Note23_Xposition = 22 * interval + Offset_from_side
Note24_Xposition = 23 * interval + Offset_from_side

HCSR04_FIRST_TRIG = 14
HCSR04_FIRST_ECHO = 15
HCSR04_SECOND_TRIG = 18
HCSR04_SECOND_ECHO = 23
HCSR04_THIRD_TRIG = 24
HCSR04_THIRD_ECHO = 25


time_delay = 0.2
GPIO.setmode(GPIO.BCM)
GPIO.setup(HCSR04_FIRST_ECHO, GPIO.IN)
GPIO.setup(HCSR04_SECOND_ECHO, GPIO.IN)
GPIO.setup(HCSR04_THIRD_ECHO, GPIO.IN)
GPIO.setup(HCSR04_FIRST_TRIG, GPIO.OUT)
GPIO.setup(HCSR04_SECOND_TRIG, GPIO.OUT)
GPIO.setup(HCSR04_THIRD_TRIG, GPIO.OUT)

wiringpi.pinMode(65, 0)
wiringpi.pinMode(66, 0)
wiringpi.pinMode(67, 0)
wiringpi.pinMode(68, 0)
wiringpi.pinMode(69, 0)
wiringpi.pinMode(70, 0)
wiringpi.pinMode(71, 0)
wiringpi.pinMode(72, 0)
wiringpi.pinMode(73, 0)
wiringpi.pinMode(74, 0)
wiringpi.pinMode(75, 0)
wiringpi.pinMode(76, 0)
wiringpi.pinMode(77, 0)
wiringpi.pinMode(78, 0)
wiringpi.pinMode(79, 0)
wiringpi.pinMode(80, 0)
wiringpi.pinMode(65+16, 0)
wiringpi.pinMode(66+16, 0)
wiringpi.pinMode(67+16, 0)
wiringpi.pinMode(68+16, 0)
wiringpi.pinMode(69+16, 0)
wiringpi.pinMode(70+16, 0)
wiringpi.pinMode(71+16, 0)
wiringpi.pinMode(72+16, 0)
wiringpi.pinMode(73+16, 0)
wiringpi.pinMode(74+16, 0)
wiringpi.pinMode(75+16, 0)
wiringpi.pinMode(76+16, 0)
wiringpi.pinMode(77+16, 0)
wiringpi.pinMode(78+16, 0)
wiringpi.pinMode(79+16, 0)
wiringpi.pinMode(80+16, 0)
wiringpi.pullUpDnControl(65, 0) # set internal PUD-OFF
wiringpi.pullUpDnControl(66, 0)
wiringpi.pullUpDnControl(67, 0)
wiringpi.pullUpDnControl(68, 0)
wiringpi.pullUpDnControl(69, 0) # set internal PUD-OFF
wiringpi.pullUpDnControl(70, 0)
wiringpi.pullUpDnControl(71, 0)
wiringpi.pullUpDnControl(72, 0)
wiringpi.pullUpDnControl(73, 0) # set internal PUD-OFF
wiringpi.pullUpDnControl(74, 0)
wiringpi.pullUpDnControl(75, 0)
wiringpi.pullUpDnControl(76, 0)
wiringpi.pullUpDnControl(77, 0) # set internal PUD-OFF
wiringpi.pullUpDnControl(78, 0)
wiringpi.pullUpDnControl(79, 0)
wiringpi.pullUpDnControl(80, 0)
wiringpi.pullUpDnControl(81, 0) # set internal PUD-OFF
wiringpi.pullUpDnControl(82, 0)
wiringpi.pullUpDnControl(83, 0)
wiringpi.pullUpDnControl(84, 0)
wiringpi.pullUpDnControl(85, 0) # set internal PUD-OFF
wiringpi.pullUpDnControl(86, 0)
wiringpi.pullUpDnControl(87, 0)
wiringpi.pullUpDnControl(88, 0)
wiringpi.pullUpDnControl(89, 0) # set internal PUD-OFF
wiringpi.pullUpDnControl(90, 0)
wiringpi.pullUpDnControl(91, 0)
wiringpi.pullUpDnControl(92, 0)
wiringpi.pullUpDnControl(93, 0) # set internal PUD-OFF
wiringpi.pullUpDnControl(94, 0)
wiringpi.pullUpDnControl(95, 0)
wiringpi.pullUpDnControl(96, 0)

Note_1_MCP23017=69
Note_2_MCP23017=70
Note_3_MCP23017=71
Note_4_MCP23017=72
Note_5_MCP23017=73
Note_6_MCP23017=74
Note_7_MCP23017=75
Note_8_MCP23017=76
Note_9_MCP23017=77
Note_10_MCP23017=78
Note_11_MCP23017=79
Note_12_MCP23017=80
Note_13_MCP23017=85
Note_14_MCP23017=86
Note_15_MCP23017=87
Note_16_MCP23017=88
Note_17_MCP23017=89
Note_18_MCP23017=90
Note_19_MCP23017=91
Note_20_MCP23017=92
Note_21_MCP23017=93
Note_22_MCP23017=94
Note_23_MCP23017=95
Note_24_MCP23017=96




Notes = [False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False]
AlreadyPlaying = [False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False]

def draw_background():
    screen.fill(0)
    screen.blit(bg, (0, 0))
    screen.blit(keysimg, (Note1_Xposition, 1000))
    screen.blit(keysimg, (Note2_Xposition, 1000))
    screen.blit(keysimg, (Note4_Xposition, 1000))
    screen.blit(keysimg, (Note5_Xposition, 1000))
    screen.blit(keysimg, (Note6_Xposition, 1000))
    screen.blit(keysimg, (Note7_Xposition, 1000))
    screen.blit(keysimg, (Note8_Xposition, 1000))
    screen.blit(keysimg, (Note9_Xposition, 1000))
    screen.blit(keysimg, (Note10_Xposition, 1000))
    screen.blit(keysimg, (Note11_Xposition, 1000))
    screen.blit(keysimg, (Note12_Xposition, 1000))
    screen.blit(keysimg, (Note13_Xposition, 1000))
    screen.blit(keysimg, (Note14_Xposition, 1000))
    screen.blit(keysimg, (Note15_Xposition, 1000))
    screen.blit(keysimg, (Note16_Xposition, 1000))
    screen.blit(keysimg, (Note17_Xposition, 1000))
    screen.blit(keysimg, (Note18_Xposition, 1000))
    screen.blit(keysimg, (Note19_Xposition, 1000))
    screen.blit(keysimg, (Note20_Xposition, 1000))
    screen.blit(keysimg, (Note21_Xposition, 1000))
    screen.blit(keysimg, (Note22_Xposition, 1000))
    screen.blit(keysimg, (Note23_Xposition, 1000))
    screen.blit(keysimg, (Note24_Xposition, 1000))
    screen.blit(keysimg, (Note3_Xposition, 1000))

Notes_History = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]

with midiout:
	while True:
			Notes = [False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False]
			draw_background()
			events = pygame.event.get()
			for event in events:
				if event.type == pygame.QUIT:
					exit()
			if INVERTED:
				if wiringpi.digitalRead(Note_1_MCP23017) == False:
					Notes[0]  = True
					#pass
					#print("Note 1 played")
				if wiringpi.digitalRead(Note_2_MCP23017) == False:
					Notes[1]  = True
					#pass
					#print("Note 2 played")
				if wiringpi.digitalRead(Note_3_MCP23017) == False:
					Notes[2]  = True
					#pass
					#print("Note 3 played")
				if wiringpi.digitalRead(Note_4_MCP23017) == False:
					Notes[3]  = True
					#pass
					#print("Note 4 played")
				if wiringpi.digitalRead(Note_5_MCP23017) == False:
					Notes[4]  = True
					#pass
					#print("Note 5 played")
				if wiringpi.digitalRead(Note_6_MCP23017) == False:
					Notes[5]  = True
					#pass
					#print("Note 6 played")
				if wiringpi.digitalRead(Note_7_MCP23017) == False:
					Notes[6]  = True
					#pass
					#print("Note 7 played")
				if wiringpi.digitalRead(Note_8_MCP23017) == False:
					Notes[7]  = True
					#pass
					#print("Note 8 played")
				if wiringpi.digitalRead(Note_9_MCP23017) == False:
					Notes[8]  = True
					#pass
					#print("Note 9 played")
				if wiringpi.digitalRead(Note_10_MCP23017) == False:
					Notes[9]  = True
					#pass
					#print("Note 10 played")
				if wiringpi.digitalRead(Note_11_MCP23017) == False:
					Notes[10]  = True
					#pass
					#print("Note 11 played")
				if wiringpi.digitalRead(Note_12_MCP23017) == False:
					Notes[11]  = True
					#pass
					#print("Note 12 played")
				if wiringpi.digitalRead(Note_13_MCP23017) == False:
					Notes[12]  = True
					#pass
					#print("Note 13 played")
				if wiringpi.digitalRead(Note_14_MCP23017) == False:
					Notes[13]  = True
					#pass
					#print("Note 14 played")
				if wiringpi.digitalRead(Note_15_MCP23017) == False:
					Notes[14]  = True
					#pass
					#print("Note 15 played")
				if wiringpi.digitalRead(Note_16_MCP23017) == False:
					Notes[15]  = True
					#pass
					#print("Note 16 played")
				if wiringpi.digitalRead(Note_17_MCP23017) == False:
					Notes[16]  = True
					#pass
					#print("Note 17 played")
				if wiringpi.digitalRead(Note_18_MCP23017) == False:
					Notes[17]  = True
					#pass
					#print("Note 18 played")
				if wiringpi.digitalRead(Note_19_MCP23017) == False:
					Notes[18]  = True
					#pass
					#print("Note 19 played")
				if wiringpi.digitalRead(Note_20_MCP23017) == False:
					Notes[19]  = True
					#pass
					#print("Note 20 played")
				if wiringpi.digitalRead(Note_21_MCP23017) == False:
					Notes[20]  = True
					#pass
					#print("Note 21 played")
				if wiringpi.digitalRead(Note_22_MCP23017) == False:
					Notes[21]  = True
					#pass
					#print("Note 22 played")
				if wiringpi.digitalRead(Note_23_MCP23017) == False:
					Notes[22]  = True
					#pass
					#print("Note 23 played")
				if wiringpi.digitalRead(Note_24_MCP23017) == False:
					Notes[23]  = True
					#print("Note 24 played")
					
			else:
				if wiringpi.digitalRead(Note_1_MCP23017):
					Notes[0]  = True
					#pass
					#print("Note 1 played")
				if wiringpi.digitalRead(Note_2_MCP23017):
					Notes[1]  = True
					#pass
					#print("Note 2 played")
				if wiringpi.digitalRead(Note_3_MCP23017):
					Notes[2]  = True
					#pass
					#print("Note 3 played")
				if wiringpi.digitalRead(Note_4_MCP23017):
					Notes[3]  = True
					#pass
					#print("Note 4 played")
				if wiringpi.digitalRead(Note_5_MCP23017):
					Notes[4]  = True
					#pass
					#print("Note 5 played")
				if wiringpi.digitalRead(Note_6_MCP23017):
					Notes[5]  = True
					#pass
					#print("Note 6 played")
				if wiringpi.digitalRead(Note_7_MCP23017):
					Notes[6]  = True
					#pass
					#print("Note 7 played")
				if wiringpi.digitalRead(Note_8_MCP23017):
					Notes[7]  = True
					#pass
					#print("Note 8 played")
				if wiringpi.digitalRead(Note_9_MCP23017):
					Notes[8]  = True
					#pass
					#print("Note 9 played")
				if wiringpi.digitalRead(Note_10_MCP23017):
					Notes[9]  = True
					#pass
					#print("Note 10 played")
				if wiringpi.digitalRead(Note_11_MCP23017):
					Notes[10]  = True
					#pass
					#print("Note 11 played")
				if wiringpi.digitalRead(Note_12_MCP23017):
					Notes[11]  = True
					#pass
					#print("Note 12 played")
				if wiringpi.digitalRead(Note_13_MCP23017):
					Notes[12]  = True
					#pass
					#print("Note 13 played")
				if wiringpi.digitalRead(Note_14_MCP23017):
					Notes[13]  = True
					#pass
					#print("Note 14 played")
				if wiringpi.digitalRead(Note_15_MCP23017):
					Notes[14]  = True
					#pass
					#print("Note 15 played")
				if wiringpi.digitalRead(Note_16_MCP23017):
					Notes[15]  = True
					#pass
					#print("Note 16 played")
				if wiringpi.digitalRead(Note_17_MCP23017):
					Notes[16]  = True
					#pass
					#print("Note 17 played")
				if wiringpi.digitalRead(Note_18_MCP23017):
					Notes[17]  = True
					#pass
					#print("Note 18 played")
				if wiringpi.digitalRead(Note_19_MCP23017):
					Notes[18]  = True
					#pass
					#print("Note 19 played")
				if wiringpi.digitalRead(Note_20_MCP23017):
					Notes[19]  = True
					#pass
					#print("Note 20 played")
				if wiringpi.digitalRead(Note_21_MCP23017):
					Notes[20]  = True
					#pass
					#print("Note 21 played")
				if wiringpi.digitalRead(Note_22_MCP23017):
					Notes[21]  = True
					#pass
					#print("Note 22 played")
				if wiringpi.digitalRead(Note_23_MCP23017):
					Notes[22]  = True
					#pass
					#print("Note 23 played")
				if wiringpi.digitalRead(Note_24_MCP23017):
					Notes[23]  = True
					#print("Note 24 played")


			if Notes[0] or Notes[1] or Notes[2]:
				#Check FIRST HCSR04 for 2ms max
				START_TIME = time.time()
				#This sends the high signal followed by low signal to send the actual signal for the LEFT FIRST
				GPIO.output(HCSR04_FIRST_TRIG, GPIO.HIGH)
				time.sleep(0.00001)
			
				GPIO.output(HCSR04_FIRST_TRIG, GPIO.LOW)
				#print("left 1 trigger sent")
				
				while GPIO.input(HCSR04_FIRST_ECHO)==0 and (time.time()-START_TIME)<0.002:
					pulse_start_time = time.time()
				while GPIO.input(HCSR04_FIRST_ECHO)==1 and (time.time()-START_TIME)<0.002:
					pulse_end_time = time.time()
				if (time.time()-START_TIME)<0.002:
					pulse_duration = pulse_end_time - pulse_start_time
					distance = round(pulse_duration * 17150, 2)
					print(distance)
			if Notes[3] or Notes[4] or Notes[5]:
				#Check SECOND HCSR04 for 2ms max
				#This sends the high signal followed by low signal to send the actual signal for the SECOND
				START_TIME = time.time()
				GPIO.output(HCSR04_SECOND_TRIG, GPIO.HIGH)
				time.sleep(0.00001)
			
				GPIO.output(HCSR04_SECOND_TRIG, GPIO.LOW)
				#print("left 1 trigger sent")
				
				while GPIO.input(HCSR04_SECOND_ECHO)==0 and (time.time()-START_TIME)<0.002:
					pulse_start_time = time.time()
				while GPIO.input(HCSR04_SECOND_ECHO)==1 and (time.time()-START_TIME)<0.002:
					pulse_end_time = time.time()
				if (time.time()-START_TIME)<0.002:
					pulse_duration = pulse_end_time - pulse_start_time
					distance = round(pulse_duration * 17150, 2)
					print(distance)
			if Notes[6] or Notes[7]:
				#Check THIRD HCSR04 for 2ms max
				#This sends the high signal followed by low signal to send the actual signal for the SECOND
				START_TIME = time.time()
				GPIO.output(HCSR04_THIRD_TRIG, GPIO.HIGH)
				time.sleep(0.00001)
			
				GPIO.output(HCSR04_THIRD_TRIG, GPIO.LOW)
				#print("left 1 trigger sent")
				
				while GPIO.input(HCSR04_THIRD_ECHO)==0 and (time.time()-START_TIME)<0.002:
					pulse_start_time = time.time()
				while GPIO.input(HCSR04_THIRD_ECHO)==1 and (time.time()-START_TIME)<0.002:
					pulse_end_time = time.time()
				if (time.time()-START_TIME)<0.002:
					pulse_duration = pulse_end_time - pulse_start_time
					distance = round(pulse_duration * 17150, 2)
					print(distance)

			Output_String = ""
			Note_Number = 1
			for Note in Notes:
				if Note == True:
					if Output_String == "":
						#Output_String += "Note " + str(Note_Number) + " is playing"
						screen.blit(keysimg, ((Note_Number-1) * interval + Offset_from_side, 950))
						(Notes_History[Note_Number-1]).append(0)
					else:
						#Output_String += " and Note " +str(Note_Number) + " is playing"
						screen.blit(keysimg, ((Note_Number-1) * interval + Offset_from_side, 950))
						(Notes_History[Note_Number-1]).append(0)
				Note_Number+=1
			#if Output_String != "":
				#print(Output_String)
			#Code_Block: History Array: The following code block allows the note history to slowly decrease and remove values on each loop of the program currently set to sleep 0.1 second after the display flip command.
			for Note_Array_Number in range(0,len(Notes_History)):
				for i in range(len(Notes_History[Note_Array_Number])):
					Notes_History[Note_Array_Number][i] += 0.1 #Add the .1 second to each of the values.
			for Note_Array_Number in range(0,len(Notes_History)):
				for time_stamp in Notes_History[Note_Array_Number]:
					if time_stamp > (20*speed_control):
						Notes_History[Note_Array_Number].remove(time_stamp) #Remove any values over 5 in a non-risk manner
			for Note_Array_Number in range(0,len(Notes_History)):
				for i in range(len(Notes_History[Note_Array_Number])):
					screen.blit(keysimg, ((Note_Array_Number) * interval + Offset_from_side, 950-50*math.floor(Notes_History[Note_Array_Number][i]/speed_control)))
			#Code_Block: History Array End
			#------------------------------------------------------###
			#Code Block: Sound PLaying: Code Block for sound generation/playing and stopping
			for Note_To_Play in range(24):
				if Notes[Note_To_Play] == True:
					if AlreadyPlaying[Note_To_Play] == False:
						#This means that the note has been pressed for the first time and should now be turned off at the smae time the Already playing should be turned to on
						note_on = [0x90, 56+Note_To_Play, 20] # channel 1, note unsure, but velocity/volume 20
						midiout.send_message(note_on)
						AlreadyPlaying[Note_To_Play] = True
				if Notes[Note_To_Play] == False:
					if AlreadyPlaying[Note_To_Play] == True:
						#This means that the note is no longer being pressed but it had previously been playing and must now be turned off 
						note_off = [0x90, 56+Note_To_Play, 0] # channel 1, note unsure, but velocity/volume 20
						midiout.send_message(note_off)
						AlreadyPlaying[Note_To_Play] = False
			#Code Block: Sound PLaying End
			
			#Code_Block: Escape Code: Code use to detecting something specific in this case the first 6 breaking together which will casue the program to exit.
			if Notes[0] and Notes[1] and Notes[2] and Notes[3] and Notes[4] and Notes[5]:
				#midiout.send_message([CONTROL_CHANGE, ALL_SOUND_OFF, 0]) # As it says we need to turn off all the sound
				#midiout.send_message([CONTROL_CHANGE, RESET_ALL_CONTROLLERS, 0]) # As it says we need to reset all the controllers for midi
				for Note_To_Play in range(24):
						#This means that the note is no longer being pressed but it had previously been playing and must now be turned off 
						note_off = [0x90, 56+Note_To_Play, 0] # channel 1, note unsure, but velocity/volume 20
						midiout.send_message(note_off)
				time.sleep(0.05)
				break # EXIT the main loop allowing me to delete midiout and not leave things hanging. 
			#Code_Block: Escape Code End
			
			#print(Notes_History) #ONLY PRINT IF NECESSARY FOR DEBUGGING as this can be very messy and confusing in the terminal and can drown out any other information!
			pygame.display.flip()
			time.sleep(0.1)

del midiout
