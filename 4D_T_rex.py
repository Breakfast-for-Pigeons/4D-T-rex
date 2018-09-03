#!/usr/bin/python3
'''
4D Tyrannosaurus rex

Description:
This program controls the motor of a toy dinosaur. A button is
pressed to make the T. rex move and roar.

This program is also an example of adding color to text displayed to
the screen.

Author: Paul Ryan
'''
########################################################################
#                          Import modules                              #
########################################################################

import os
import logging
import random
from time import sleep
from gpiozero import Motor, Button, OutputDevice
import pygame

########################################################################
#                           Variables                                  #
########################################################################

t_rex_motor = Motor(20, 16, True)               # forward, backward, pwm
t_rex_motor_enable = OutputDevice(21)
white_button = Button(12)
red_button = Button(9)

########################################################################
#                           Initialize                                 #
########################################################################

pygame.mixer.init()

logging.basicConfig(filename='Files/T_rex.log', filemode='w',
                    level=logging.INFO,
                    format='%(asctime)s %(levelname)s: %(message)s',
                    datefmt='%m/%d/%y %I:%M:%S %p:')

########################################################################
#                            Functions                                 #
########################################################################


def main():
    '''
    This is the main function. It will wait until one of two buttons is
    pressed. One button will activate the T. rex and the other button
    will stop the program. Pressing Ctrl-C will also stop the program.
    '''

    try:
        logging.info("START")
        # STEP01: Check to see that the necessary files exist.
        file_check()
        # STEP02: Check to see if files are accessible.
        permission_check()
        # STEP03: Read the dinosaur_facts.txt file to populate the
        # dino_facts list.
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

            if white_button.is_pressed:
                # Print out a random dinosaur fun fact
                print_dinosaur_fact(dino_facts)
                # Move the T. rex for the duration of the sound file
                activate_t_rex(roar, roar_length)
                # Load the next sound file
                roar, roar_length = get_roar()
                # Prompt the user to press a button
                prompt_user_for_input()

            if red_button.is_pressed:
                stop_the_program()

    except KeyboardInterrupt:
        stop_the_program()


def file_check():
    '''
    The file_check function checks to see if the necessary files exist.
    If they all exist, the program will continue.
    If a file is missing, the program will print out a message to the
    screen and then exit.
    '''

    file_missing_flag = 0

    sounds = ['T_rex1.ogg', 'T_rex2.ogg', 'T_rex3.ogg', 'T_rex4.ogg',
              'T_rex5.ogg', 'T_rex6.ogg', 'T_rex7.ogg', 'T_rex8.ogg']

    logging.info("FILE CHECK")
    # Check to see if dinosaur_facts.txt file exists
    if os.path.isfile('Files/dinosaur_facts.txt'):
        logging.info("dinosaur_facts.txt file was found!")
    else:
        logging.error("dinosaur_facts.txt file was not found! Make sure " +
                      "that the dinosaur_facts.txt file exists in the Files " +
                      "folder.")
        file_missing_flag = 1

    # Check to see if sound files exists
    for sound in sounds:
        if os.path.isfile('Sounds/' + sound):
            logging.info("{} file was found!".format(sound))
        else:
            logging.error("{} file was not found! Make sure ".format(sound) +
                          "that the {} file exists in the ".format(sound) +
                          "'Sounds' folder.")
            file_missing_flag = 1

    # If there are no missing files, return to the main function
    # Otherwise print out message and exit the program
    if file_missing_flag == 0:
        return
    else:
        print("\033[1;31;40m\nCould not run the program. Some files are " +
              "missing. Check the log in the 'Files' folder for more " +
              "information.\n")
        stop_the_program()


def permission_check():
    '''
    The permission_check function checks to see if the user has
    permission to read the necessary files. If so, the program will
    continue. If not, the program will print out a message to the screen
    and then exit.
    '''

    permission_flag = 0

    sounds = ['T_rex1.ogg', 'T_rex2.ogg', 'T_rex3.ogg', 'T_rex4.ogg',
              'T_rex5.ogg', 'T_rex6.ogg', 'T_rex7.ogg', 'T_rex8.ogg']

    logging.info("PERMISSION CHECK")
    # Check to see if user has read access to dinosaur_facts.txt
    if os.access('Files/dinosaur_facts.txt', os.R_OK):
        logging.info("User has permission to read the dinosaur_facts.txt " +
                     "file.")
    else:
        logging.error("User does not have permission to read the " +
                      "dinosaur_facts.txt file.")
        permission_flag = 1

    # Check to see if user has read access to sound files
    for sound in sounds:
        if os.access('Sounds/' + sound, os.R_OK):
            logging.info("User has permission to read the " +
                         "{} file.".format(sound))
        else:
            logging.error("User does not have permission to read the " +
                          "{} file.".format(sound))
            permission_flag = 1

    if permission_flag == 0:
        return
    else:
        print("\033[1;31;40m\nCould not run the program. Check the log " +
              "in the 'Files' folder for more information.")
        stop_the_program()


def read_file(file_name):
    '''
    The read_file function has one parameter: file_name. In this
    program, the argument passed in will be the dinosaur_facts.txt file
    located in the 'Files' folder. Each line of the file will be an
    element in the dino_facts list. It will then return the dino_facts
    list to the main function. If the program is unable to populate the
    list, it will display an error message and then exit the program.
    '''

    logging.info("READING DINOSAUR_FACTS.TXT")
    try:
        with open(file_name, "r") as facts:     # open the file as read-only
            dino_facts = facts.readlines()
        logging.info("The dino_facts list was successfully populated.")
    except IOError:
        print("\033[1;31;40mErrors were encountered. Check the log in the " +
              "'Files' folder for more information.")
        logging.error("The dino_facts list could not be populated.")
        stop_the_program()

    return dino_facts


def empty_file_check(list_name):
    '''
    The empty_file_check function has one parameter: file_name. In this
    program, the argument passed in will be the dino_facts list. It will
    check to see if the list is empty. If it is, the program will print
    a message to the screen. If it is not empty, the program will
    continue.
    '''

    logging.info("EMPTY FILE CHECK")
    if list_name == []:
        logging.error("The dinosaur.txt file is empty. The program won't " +
                      "work.")
        print("\033[1;31;40mErrors were encountered. Check the log in the " +
              "'Files' folder for more information.")
        stop_the_program()
    else:
        logging.info("The dinosaur.txt file is not empty.(This is good. We " +
                     "don't want an empty file.)")


def print_header():
    '''
    The print_header function will print out the program header to the
    screen.
    This is the only part of the program that doesn't adhere to the PEP
    standards (It exceeds recommended line length). I decided that
    "Readability Counts" and "Beautiful is better than ugly" from The
    Zen of Python should trump the PEP standards in this case. I had
    rewritten it to meet the PEP standard, but is was ugly and
    unreadable. This is much better. The program still compiles and runs
    OK.
    '''

    print("\n\033[1;37;40m")                        # print white header
    print("==========================================================================================================")
    print("   _  _   ____    _____                                                                                   ")
    print("  | || | |  _ \  |_   _|   _ _ __ __ _ _ __  _ __   ___  ___  __ _ _   _ _ __ _   _ ___   _ __ _____  __  ")
    print("  | || |_| | | |   | || | | | '__/ _` | '_ \| '_ \ / _ \/ __|/ _` | | | | '__| | | / __| | '__/ _ \ \/ /  ")
    print("  |__   _| |_| |   | || |_| | | | (_| | | | | | | | (_) \__ \ (_| | |_| | |  | |_| \__ \ | | |  __/>  <   ")
    print("     |_| |____/    |_| \__, |_|  \__,_|_| |_|_| |_|\___/|___/\__,_|\__,_|_|   \__,_|___/ |_|  \___/_/\_\  ")
    print("                       |___/                                                                              ")
    print("==========================================================================================================")
    print("\n")


def prompt_user_for_input():
    '''
    The prompt_user_for_input function prompts a user to push a button.
    '''

    # First line - print all white text
    print("\033[1;37;40mPush the white button to activate the T. Rex.")
    # Second line
    print("\033[1;37;40mPush the " +                 # print white text
          "\033[1;31;40mred button " +               # print red text
          "\033[1;37;40mor press Ctrl-C to " +       # print white text
          "\033[1;31;40mstop " +                     # print red text
          "\033[1;37;40mthe program.\n")             # print white text


def get_roar():
    '''
    The get_roar function will randomly select one of the T. rex roar
    sound files and then return it and its file length to the main
    function.
    '''

    # The key/value pair is sound file name : length of file in seconds
    roars = {'Sounds/T_rex1.ogg': 6.5, 'Sounds/T_rex2.ogg': 3,
             'Sounds/T_rex3.ogg': 4, 'Sounds/T_rex4.ogg': 5.5,
             'Sounds/T_rex5.ogg': 4, 'Sounds/T_rex6.ogg': 6,
             'Sounds/T_rex7.ogg': 4.5, 'Sounds/T_rex8.ogg': 4}

    return random.choice(list(roars.items()))


def print_dinosaur_fact(dino_facts):
    '''
    The print_dinosaur_fact function takes the dino_facts list as its
    input. It will select a random fact and print it out.
    '''

    print("\033[1;34;40mDINOSAUR FUN FACT:")
    print(random.choice(dino_facts))


def activate_t_rex(sound, sound_length):
    '''
    The activate_t_rex function has two parameters: sound and sound
    length.
    "sound" is the name of a sound file and "sound_length" is the length
    of the sound file in seconds. The arguments passed to this function
    will be one of the randomly selected roars and its length. This
    function will play the sound file and activate the motor for the
    duration of the sound file.
    '''

    try:
        t_rex_motor.value = 0.6              # Controls the motor speed
    except ValueError:
        logging.error("A bad value was specified for the t_rex_motor." +
                      "The value should be between 0 and 1.")
        print("\033[1;31;40mAn error was encountered. Check the log in the " +
              "'Files' folder for more information.\n")
        stop_the_program()
    pygame.mixer.music.load(sound)     # Loads the sound file
    t_rex_motor_enable.on()            # Starts the motor
    pygame.mixer.music.play()          # Plays the sound file
    sleep(sound_length)                # Length of sound file in seconds
    t_rex_motor_enable.off()           # Stops the motor


def release_gpio_pins():
    '''
    The release_gpio_pins function realeases the gpio pins.
    '''

    t_rex_motor.close()
    t_rex_motor_enable.close()
    red_button.close()
    white_button.close()


def stop_the_program():
    '''
    The stop_the_program function will call the release_gpio_pins
    function, print a message to the screen, and then exit the program.
    '''

    release_gpio_pins()
    print("\033[1;37;40mExiting program.\n")
    logging.info("END")
    exit()


if __name__ == '__main__':
    main()
