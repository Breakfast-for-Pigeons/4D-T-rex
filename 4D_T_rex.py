#!/usr/bin/python3
########################################################################
#                        4D Tyrannosaurus rex                          #
########################################################################
# Description:                                                         #
# This program hacks a toy dinosaur. A button is pressed to make the   #
# dinosaur move and roar.                                              #
# This program is also a demonstration of controlling a motor using    #
# the gpiozero module.                                                 #
# This program is also an example of adding color to text displayed to #
# the screen.                                                          #
#                                                                      #
#                                                                      #
# Author: Paul Ryan                                                    #
#                                                                      #
########################################################################

########################################################################
#                          Import files                                #
########################################################################

from gpiozero import Motor, Button, OutputDevice
from time import sleep
from signal import pause
import pygame
import random
import os, sys, logging

########################################################################
#                           Variables                                  #
########################################################################

t_rex_motor = Motor(20, 16, True)				# forward, backward, pwm
t_rex_motor_enable = OutputDevice(21)
black_button = Button(12)
red_button = Button(9)

########################################################################
#                           Initialize                                 #
########################################################################

pygame.mixer.init()

logging.basicConfig(filename='Files/T_rex.log', filemode='w',
	level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s', 
	datefmt='%m/%d/%y %I:%M:%S %p:')

########################################################################
#                            Functions                                 #
########################################################################
'''
This is the main function. It will wait until one of two buttons is
pressed. One button will start the program and the other button will
stop the program. Pressing Ctrl-C will also stop the program.
'''
def main():
	
	try:
		logging.info("START")
		# STEP01: Check to see that the necessary files exist.
		file_check()
		# STEP02: Check to see if files are accessible.
		permission_check()
		# STEP03: Read the dinosaur_facts.txt file to populate the dino_facts list.
		dino_facts = read_file("Files/dinosaur_facts.txt")
		# STEP04: Check to see if the file is empty
		empty_file_check(dino_facts)
		# STEP05: Acknowledge that prelimiary checks are complete
		logging.info("Prelimiary checks are complete. Starting program...")
		# STEP06: Display program header
		print_header()
		# STEP07: Pre-load the first sound file
		roar, roar_length = get_roar()
		# STEP08: Prompt the user to press a button
		prompt_user_for_input()
		
		while True:
			
			if black_button.is_pressed:
				# Print out a random dinosaur fun fact
				print_dinosaur_fact(dino_facts)
				# Move the T. rex for the duration of the sound file
				activate_T_rex(roar, roar_length)
				# Load the next sound file
				roar, roar_length = get_roar()
				# Prompt the user to press a button
				prompt_user_for_input()
				
				
			if red_button.is_pressed:
				stop_the_program()
				
	except KeyboardInterrupt:
		stop_the_program()

'''
The file_check function checks to see if the necessary files exist.
If they all exist, the program will continue.
If a file is missing, the program will print a message and exit.
'''
def file_check():
	
	file_missing_flag = 0
	
	logging.info("FILE CHECK")
	# Check to see if dinosaur_facts.txt file exists
	if os.path.isfile('Files/dinosaur_facts.txt'):
		logging.info("dinosaur_facts.txt file was found!")
	else:
		detail_log.error("dinosaur_facts.txt file was not found! Make sure that the dinosaur_facts.txt file exists in the Files folder.")
		file_missing_flag = 1
	# Check to see if T_Rex1.mp3 file exists
	if os.path.isfile('Sounds/T_rex1.mp3'):
		logging.info("T_rex1.mp3 file was found!")
	else:
		logging.error("T_rex1.mp3 file was not found! Make sure that the T_rex1.mp3 file exists in the 'Sounds' folder.")
		file_missing_flag = 1
	# Check to see if T_Rex2.mp3 file exists
	if os.path.isfile('Sounds/T_rex2.mp3'):
		logging.info("T_rex2.mp3 file was found!")
	else:
		logging.error("T_rex2.mp3 file was not found! Make sure that the T_rex2.mp3 file exists in the 'Sounds' folder.")
		file_missing_flag = 1
	# Check to see if T_Rex3.mp3 file exists
	if os.path.isfile('Sounds/T_rex3.mp3'):
		logging.info("T_rex3.mp3 file was found!")
	else:
		logging.error("T_rex3.mp3 file was not found! Make sure that the T_rex3.mp3 file exists in the 'Sounds' folder.")
		file_missing_flag = 1
	# Check to see if T_Rex4.mp3 file exists
	if os.path.isfile('Sounds/T_rex4.mp3'):
		logging.info("T_rex4.mp3 file was found!")
	else:
		logging.error("T_rex4.mp3 file was not found! Make sure that the T_rex4.mp3 file exists in the 'Sounds' folder.")
		file_missing_flag = 1
	# Check to see if T_Rex5.mp3 file exists
	if os.path.isfile('Sounds/T_rex5.mp3'):
		logging.info("T_rex5.mp3 file was found!")
	else:
		logging.error("T_rex5.mp3 file was not found! Make sure that the T_rex5.mp3 file exists in the 'Sounds' folder.")
		file_missing_flag = 1
	# Check to see if T_Rex6.mp3 file exists
	if os.path.isfile('Sounds/T_rex6.mp3'):
		logging.info("T_rex6.mp3 file was found!")
	else:
		logging.error("T_rex6.mp3 file was not found! Make sure that the T_rex6.mp3 file exists in the 'Sounds' folder.")
		file_missing_flag = 1
	# Check to see if T_Rex7.mp3 file exists
	if os.path.isfile('Sounds/T_rex2.mp3'):
		logging.info("T_rex7.mp3 file was found!")
	else:
		logging.error("T_rex7.mp3 file was not found! Make sure that the T_rex7.mp3 file exists in the 'Sounds' folder.")
		file_missing_flag = 1
	# Check to see if T_Rex8.mp3 file exists
	if os.path.isfile('Sounds/T_rex8.mp3'):
		logging.info("T_rex8.mp3 file was found!")
	else:
		logging.error("T_rex8.mp3 file was not found! Make sure that the T_rex8.mp3 file exists in the 'Sounds' folder.")
		file_missing_flag = 1
	
	# If there are no missing files, return to the main function
	# Otherwise print out message and exit the program
	if file_missing_flag == 0:
		return
	else:
		print("\033[1;31;40mErrors were encountered. Check the log in the 'Files' folder for more details.\033[1;31;40m")
		stop_the_program()

'''
The permission_check function checks to see if the user has permission
to read the necessary files. If so, the program will continue. If not,
messages are printed out to the screen and the program will exit.
'''
def permission_check():
	
	permission_flag = 0
	
	logging.info("PERMISSION CHECK")
	# Check to see if user has read access to dinosaur_facts.txt
	if os.access('Files/dinosaur_facts.txt', os.R_OK):
		logging.info("User has permission to read the dinosaur_facts.txt file.")
	else:
		logging.error("User does not have permission to read the dinosaur_facts.txt file.")
		permission_flag = 1
	# Check to see if user has read access to  T_Rex1.mp3
	if os.access('Sounds/T_rex1.mp3', os.R_OK):
		logging.info("User has permission to read the T_Rex1.mp3 file.")
	else:
		logging.error("User does not have permission to read the T_Rex1.mp3 file.")
		permission_flag = 1
	# Check to see if user has read access to  T_Rex2.mp3
	if os.access('Sounds/T_rex2.mp3', os.R_OK):
		logging.info("User has permission to read the T_Rex2.mp3 file.")
	else:
		logging.error("User does not have permission to read the T_Rex2.mp3 file.")
		permission_flag = 1
	# Check to see if user has read access to  T_Rex3.mp3
	if os.access('Sounds/T_rex3.mp3', os.R_OK):
		logging.info("User has permission to read the T_Rex3.mp3 file.")
	else:
		logging.error("User does not have permission to read the T_Rex3.mp3 file.")
		permission_flag = 1
	# Check to see if user has read access to  T_Rex4.mp3
	if os.access('Sounds/T_rex4.mp3', os.R_OK):
		logging.info("User has permission to read the T_Rex4.mp3 file.")
	else:
		logging.error("User does not have permission to read the T_Rex4.mp3 file.")
		permission_flag = 1
	# Check to see if user has read access to  T_Rex5.mp3
	if os.access('Sounds/T_rex5.mp3', os.R_OK):
		logging.info("User has permission to read the T_Rex5.mp3 file.")
	else:
		logging.error("User does not have permission to read the T_Rex5.mp3 file.")
		permission_flag = 1
	# Check to see if user has read access to  T_Rex6.mp3
	if os.access('Sounds/T_rex6.mp3', os.R_OK):
		logging.info("User has permission to read the T_Rex6.mp3 file.")
	else:
		logging.error("User does not have permission to read the T_Rex6.mp3 file.")
		permission_flag = 1
	# Check to see if user has read access to  T_Rex7.mp3
	if os.access('Sounds/T_rex7.mp3', os.R_OK):
		logging.info("User has permission to read the T_Rex7.mp3 file.")
	else:
		logging.error("User does not have permission to read the T_Rex7.mp3 file.")
		permission_flag = 1
	# Check to see if user has read access to  T_Rex8.mp3
	if os.access('Sounds/T_rex8.mp3', os.R_OK):
		logging.info("User has permission to read the T_Rex8.mp3 file.")
	else:
		logging.error("User does not have permission to read the T_Rex8.mp3 file.")
		permission_flag = 1
	
	if permission_flag == 0:
		return
	else:
		print("\033[1;31;40mErrors were encountered. Check the log in the 'Files' folder for more details.\033[1;31;40m")
		stop_the_program()

'''
The read_file function will read the dinosaur facts file and each 
line of the file will be an element in the fun_facts list. It will then
return the dino_facts list to the main function.
If the program is unable to read the file, it will display an error
message and then exit the program.
If the dino_facts file is empty, an error message will be displayed
and the program will exit.
'''
def read_file(file_name):
	logging.info("READING DINOSAUR_FACTS.TXT")
	with open(file_name, "r") as f:   # open the file as read-only
		dino_facts = f.readlines()

	return dino_facts

'''
This empty_file_check function checks to see if the file is empty. If it
is, the program will print a message to the screen. If not, the program
will continue.
'''
def empty_file_check(file_name):
	logging.info("EMPTY FILE CHECK")
	if file_name == []:
		logging.error("The dinosaur.txt file is empty. The program won't work.")
		print("\033[1;31;40mErrors were encountered. Check the log in the 'Files' folder for more details.\033[1;31;40m")
		stop_the_program()
	else:
		logging.info("The dinosaur.txt file is not empty.(This is good. We don't want an empty file.)")

'''
The print_header function will print out the program header to the
screen.
'''
def print_header():
	print("\n")
	print("\033[1;37;40m==========================================================================================================")
	print("\033[1;37;40m   _  _   ____    _____                                                                                   ")
	print("\033[1;37;40m  | || | |  _ \  |_   _|   _ _ __ __ _ _ __  _ __   ___  ___  __ _ _   _ _ __ _   _ ___   _ __ _____  __  ")
	print("\033[1;37;40m  | || |_| | | |   | || | | | '__/ _` | '_ \| '_ \ / _ \/ __|/ _` | | | | '__| | | / __| | '__/ _ \ \/ /  ")
	print("\033[1;37;40m  |__   _| |_| |   | || |_| | | | (_| | | | | | | | (_) \__ \ (_| | |_| | |  | |_| \__ \ | | |  __/>  <   ")
	print("\033[1;37;40m     |_| |____/    |_| \__, |_|  \__,_|_| |_|_| |_|\___/|___/\__,_|\__,_|_|   \__,_|___/ |_|  \___/_/\_\  ")
	print("\033[1;37;40m                       |___/                                                                              ")
	print("\033[1;37;40m==========================================================================================================")                                                      
	print("\n")

'''
The get_roar function will randomly select one of the T. rex roar
sound files and return it and its file length to the main function.
'''
def get_roar():
	
	roar1 = "Sounds/T_rex1.mp3"
	roar2 = "Sounds/T_rex2.mp3"
	roar3 = "Sounds/T_rex3.mp3"
	roar4 = "Sounds/T_rex4.mp3"
	roar5 = "Sounds/T_rex5.mp3"
	roar6 = "Sounds/T_rex6.mp3"
	roar7 = "Sounds/T_rex7.mp3"
	roar8 = "Sounds/T_rex8.mp3"

	roar1_length = 6.5    # lenth of file in seconds
	roar2_length = 3      # lenth of file in seconds
	roar3_length = 4      # lenth of file in seconds
	roar4_length = 5.5    # lenth of file in seconds
	roar5_length = 4      # lenth of file in seconds
	roar6_length = 6      # lenth of file in seconds
	roar7_length = 4.5    # lenth of file in seconds
	roar8_length = 4      # lenth of file in seconds
	
	roars = [roar1, roar2, roar3, roar4, roar5, roar6, roar7, roar8]
	
	roar = random.choice(roars)   # Selects random sound file
	
	if roar == roar1:
		return roar, roar1_length
	elif roar == roar2:
		return roar, roar2_length
	elif roar == roar3:
		return roar, roar3_length
	if roar == roar4:
		return roar, roar4_length
	elif roar == roar5:
		return roar, roar5_length
	elif roar == roar6:
		return roar, roar6_length
	elif roar == roar7:
		return roar, roar7_length
	else:
		return roar, roar8_length

'''
The prompt_user_for_input function prompts a user to push a button.
'''
def prompt_user_for_input():
	print("\033[1;37;40mPush the \033[1;30;47mblack button\033[1;37;40m to activate the \033[1;30;47mT. Rex\033[1;37;40m.")
	print("\033[1;37;40mPush the \033[1;31;40mred button \033[1;37;40mor press Ctrl-C to \033[1;31;40mstop \033[1;37;40mthe program.\n")

'''
The print_dinosaur_fact function prints out a random fact about 
dinosaurs. The dino_facts file needs to be sent to this function.
'''
def print_dinosaur_fact(dino_facts):
	print("\033[1;34;40mDINOSAUR FUN FACT:")
	print(random.choice(dino_facts))

'''
The activate_T_rex funciton takes 2 inputs: roar and roar_length.
This function will play the sound file and then activate the motor for
the duration of the sound file.
'''
def activate_T_rex(roar, roar_length):
	try:
		t_rex_motor.value = 0.6       # Controls the motor speed
	except ValueError:
		logging.error("A bad value was specified for t_rex_motor. The value should be between 0 and 1.")
		print("\033[1;31;40mAn error was encountered. Check the detail log for more information\n")
		stop_the_program()
	pygame.mixer.music.load(roar)     # Loads the sound file
	t_rex_motor_enable.on()           # Starts the motor
	pygame.mixer.music.play()         # Plays the sound file
	sleep(roar_length)                # Length of sound file in seconds
	t_rex_motor_enable.off()          # Stops the motor

'''
The release_gpio_pins function realeases the gpio pins.
'''
def release_gpio_pins():
	t_rex_motor.close()
	t_rex_motor_enable.close()
	red_button.close()
	black_button.close()

def stop_the_program():
	release_gpio_pins()
	print("\033[1;37;40mExiting program.\n")
	logging.info("END")
	exit()
		
if __name__ == '__main__':
	main()
