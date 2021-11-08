import RPi.GPIO as GPIO
import pygame
import time
import random
import math
import pygame_menu
from psonic import *
import keyboard
from pynput.keyboard import Key, Controller

pygame.init()
pygame.mixer.init()



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
"""
# GPIO settings
Note1 = 4
Note2 = 17
Note3= 27
Note4 = 22
Note5 = 10
Note6 = 9
Note7 = 11
Note8 = 0 
Note9 = 5
Note10 = 6
Note11= 13
Note12 = 19
Note13 = 26
Note14 = 21
Note15 = 20
Note16 = 16 
Note17= 12
Note18 = 1
Note19 = 7
Note20 = 8
Note21 = 25
Note22 = 24
Note23 = 23
Note24 = 18 
"""
Note1 = 14
Note2 = 15
Note3 = 18
Note4 = 23
Note5 = 24
Note6 = 25
Note7 = 8
Note8 = 7 
Note9 = 12
Note10 = 16
Note11 = 20
Note12 = 21
Note13 = 4
Note14 = 17
Note15 = 27
Note16 = 22 
Note17 = 10
Note18 = 9
Note19 = 11
Note20 = 5
Note21 = 6
Note22 = 13
Note23 = 19
Note24 = 26 

time_delay = 0.2
GPIO.setmode(GPIO.BCM)
GPIO.setup(Note1, GPIO.IN)
GPIO.setup(Note2, GPIO.IN)
GPIO.setup(Note3, GPIO.IN)
GPIO.setup(Note4, GPIO.IN)
GPIO.setup(Note5, GPIO.IN)
GPIO.setup(Note6, GPIO.IN)
GPIO.setup(Note7, GPIO.IN)
GPIO.setup(Note8, GPIO.IN)
GPIO.setup(Note9, GPIO.IN)
GPIO.setup(Note10, GPIO.IN)
GPIO.setup(Note11, GPIO.IN)
GPIO.setup(Note12, GPIO.IN)
GPIO.setup(Note13, GPIO.IN)
GPIO.setup(Note14, GPIO.IN)
GPIO.setup(Note15, GPIO.IN)
GPIO.setup(Note16, GPIO.IN)
GPIO.setup(Note17, GPIO.IN)
GPIO.setup(Note18, GPIO.IN)
GPIO.setup(Note19, GPIO.IN)
GPIO.setup(Note20, GPIO.IN)
GPIO.setup(Note21, GPIO.IN)
GPIO.setup(Note22, GPIO.IN)
GPIO.setup(Note23, GPIO.IN)
GPIO.setup(Note24, GPIO.IN)

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


while True:
		Notes = [False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False]
		draw_background()
		events = pygame.event.get()
		for event in events:
			if event.type == pygame.QUIT:
				exit()
		if INVERTED:
			if GPIO.input(Note1) == False:
				Notes[0]  = True
				#pass
				#print("Note 1 played")
			if GPIO.input(Note2) == False:
				Notes[1]  = True
				#pass
				#print("Note 2 played")
			if GPIO.input(Note3) == False:
				Notes[2]  = True
				#pass
				#print("Note 3 played")
			if GPIO.input(Note4) == False:
				Notes[3]  = True
				#pass
				#print("Note 4 played")
			if GPIO.input(Note5) == False:
				Notes[4]  = True
				#pass
				#print("Note 5 played")
			if GPIO.input(Note6) == False:
				Notes[5]  = True
				#pass
				#print("Note 6 played")
			if GPIO.input(Note7) == False:
				Notes[6]  = True
				#pass
				#print("Note 7 played")
			if GPIO.input(Note8) == False:
				Notes[7]  = True
				#pass
				#print("Note 8 played")
			if GPIO.input(Note9) == False:
				Notes[8]  = True
				#pass
				#print("Note 9 played")
			if GPIO.input(Note10) == False:
				Notes[9]  = True
				#pass
				#print("Note 10 played")
			if GPIO.input(Note11) == False:
				Notes[10]  = True
				#pass
				#print("Note 11 played")
			if GPIO.input(Note12) == False:
				Notes[11]  = True
				#pass
				#print("Note 12 played")
			if GPIO.input(Note13) == False:
				Notes[12]  = True
				#pass
				#print("Note 13 played")
			if GPIO.input(Note14) == False:
				Notes[13]  = True
				#pass
				#print("Note 14 played")
			if GPIO.input(Note15) == False:
				Notes[14]  = True
				#pass
				#print("Note 15 played")
			if GPIO.input(Note16) == False:
				Notes[15]  = True
				#pass
				#print("Note 16 played")
			if GPIO.input(Note17) == False:
				Notes[16]  = True
				#pass
				#print("Note 17 played")
			if GPIO.input(Note18) == False:
				Notes[17]  = True
				#pass
				#print("Note 18 played")
			if GPIO.input(Note19) == False:
				Notes[18]  = True
				#pass
				#print("Note 19 played")
			if GPIO.input(Note20) == False:
				Notes[19]  = True
				#pass
				#print("Note 20 played")
			if GPIO.input(Note21) == False:
				Notes[20]  = True
				#pass
				#print("Note 21 played")
			if GPIO.input(Note22) == False:
				Notes[21]  = True
				#pass
				#print("Note 22 played")
			if GPIO.input(Note23) == False:
				Notes[22]  = True
				#pass
				#print("Note 23 played")
			if GPIO.input(Note24) == False:
				Notes[23]  = True
				#print("Note 24 played")
				
		else:
			if GPIO.input(Note1):
				Notes[0]  = True
				#pass
				#print("Note 1 played")
			if GPIO.input(Note2):
				Notes[1]  = True
				#pass
				#print("Note 2 played")
			if GPIO.input(Note3):
				Notes[2]  = True
				#pass
				#print("Note 3 played")
			if GPIO.input(Note4):
				Notes[3]  = True
				#pass
				#print("Note 4 played")
			if GPIO.input(Note5):
				Notes[4]  = True
				#pass
				#print("Note 5 played")
			if GPIO.input(Note6):
				Notes[5]  = True
				#pass
				#print("Note 6 played")
			if GPIO.input(Note7):
				Notes[6]  = True
				#pass
				#print("Note 7 played")
			if GPIO.input(Note8):
				Notes[7]  = True
				#pass
				#print("Note 8 played")
			if GPIO.input(Note9):
				Notes[8]  = True
				#pass
				#print("Note 9 played")
			if GPIO.input(Note10):
				Notes[9]  = True
				#pass
				#print("Note 10 played")
			if GPIO.input(Note11):
				Notes[10]  = True
				#pass
				#print("Note 11 played")
			if GPIO.input(Note12):
				Notes[11]  = True
				#pass
				#print("Note 12 played")
			if GPIO.input(Note13):
				Notes[12]  = True
				#pass
				#print("Note 13 played")
			if GPIO.input(Note14):
				Notes[13]  = True
				#pass
				#print("Note 14 played")
			if GPIO.input(Note15):
				Notes[14]  = True
				#pass
				#print("Note 15 played")
			if GPIO.input(Note16):
				Notes[15]  = True
				#pass
				#print("Note 16 played")
			if GPIO.input(Note17):
				Notes[16]  = True
				#pass
				#print("Note 17 played")
			if GPIO.input(Note18):
				Notes[17]  = True
				#pass
				#print("Note 18 played")
			if GPIO.input(Note19):
				Notes[18]  = True
				#pass
				#print("Note 19 played")
			if GPIO.input(Note20):
				Notes[19]  = True
				#pass
				#print("Note 20 played")
			if GPIO.input(Note21):
				Notes[20]  = True
				#pass
				#print("Note 21 played")
			if GPIO.input(Note22):
				Notes[21]  = True
				#pass
				#print("Note 22 played")
			if GPIO.input(Note23):
				Notes[22]  = True
				#pass
				#print("Note 23 played")
			if GPIO.input(Note24):
				Notes[23]  = True
				#print("Note 24 played")
				
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
					play(40+Note_To_Play)
					#This means that the note has been pressed for the first time and should now be turned off at the smae time the Already playing should be turned to on
			if Notes[Note_To_Play] == False:
				if AlreadyPlaying[Note_To_Play] == True:
					#This means that the note is no longer being pressed but it had previously been playing and must now be turned off 
					pass
		#Code Block: Sound PLaying End
		
		#Code_Block: Escape Code: Code use to detecting something specific in this case the first 6 breaking together which will casue the program to exit.
		if Notes[0] and Notes[1] and Notes[2] and Notes[3] and Notes[4] and Notes[5]:
			#midiout.send_message([CONTROL_CHANGE, ALL_SOUND_OFF, 0]) # As it says we need to turn off all the sound
			#midiout.send_message([CONTROL_CHANGE, RESET_ALL_CONTROLLERS, 0]) # As it says we need to reset all the controllers for midi
			#for Note_To_Play in range(24):
					#This means that the note is no longer being pressed but it had previously been playing and must now be turned off 
					#note_off = [0x90, 56+Note_To_Play, 0] # channel 1, note unsure, but velocity/volume 20
					#midiout.send_message(note_off)
			time.sleep(0.05)
			break # EXIT the main loop allowing me to delete midiout and not leave things hanging. 
		#Code_Block: Escape Code End
		
		#print(Notes_History) #ONLY PRINT IF NECESSARY FOR DEBUGGING as this can be very messy and confusing in the terminal and can drown out any other information!
		pygame.display.flip()
		time.sleep(0.1)


