#!/usr/bin/python3
"""
4D Tyrannosaurus rex

Description:
This program controls the motor of a toy dinosaur. A button is
pressed to make the T. rex move and roar.

....................

Functions:
- file_check: Checks to see if the necessary files exist
- permission_check: Checks to see if the user has permission to read
  the necessary files
- create_list: Reads a file, creates a list
- empty_file_check: Checks to see if the dino_facts list is empty
- print_header: Prints a header
- prompt_user_for_input: Prompts user to push a button
- get_roar: Gets one random sound file
- print_dinosaur_fact: Prints a random dinosaur fact
- activate_t_rex: Starts the T. rex motor
- release_gpio_pins: Realeases the GPIO pins.
- stop_the_program: Stops the program

....................

Author: Paul Ryan

This program was written on a Raspberry Pi using the Geany IDE.
"""

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

T_REX_MOTOR = Motor(20, 16, True)               # forward, backward, pwm
T_REX_MOTOR_ENABLE = OutputDevice(21)
WHITE_BUTTON = Button(12)
RED_BUTTON = Button(9)

########################################################################
#                           Initialize                                 #
########################################################################

pygame.mixer.init()

# Logging
LOG = 'Files/t_rex.log'
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter(fmt='%(asctime)s %(levelname)s: %(message)s',
                              datefmt='%m/%d/%y %I:%M:%S %p:')
file_handler = logging.FileHandler(LOG, 'w')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

########################################################################
#                            Functions                                 #
########################################################################


def main():
    """
    This is the main function. It will wait until one of two buttons is
    pressed. One button will activate the T. rex and the other button
    will stop the program. Pressing Ctrl-C will also stop the program.
    """

    try:
        logger.info("START")
        # STEP01: Check to see that the necessary files exist.
        file_check()
        # STEP02: Check to see if files are accessible.
        permission_check()
        # STEP03: Check to see if the file is empty
        empty_file_check()
        # STEP04: Read the dinosaur_facts.txt file to populate the
        # dino_facts list.
        dino_facts = create_list("Files/dinosaur_facts.txt")
        # STEP05: Acknowledge that prelimiary checks are complete
        logger.info("Prelimiary checks are complete. Starting program...")
        # STEP06: Display program header
        print_header()
        # STEP07: Pre-load the first sound file
        roar, roar_length = get_roar()
        # STEP08: Prompt the user to press a button
        prompt_user_for_input()

        while True:

            if WHITE_BUTTON.is_pressed:
                # Print out a random dinosaur fun fact
                print_dinosaur_fact(dino_facts)
                # Move the T. rex for the duration of the sound file
                activate_t_rex(roar, roar_length)
                # Load the next sound file
                roar, roar_length = get_roar()
                # Prompt the user to press a button
                prompt_user_for_input()

            if RED_BUTTON.is_pressed:
                stop_the_program()

    except KeyboardInterrupt:
        stop_the_program()


def file_check():
    """
    Checks to see if the necessary files exist

    This function checks to see if the necessary files exist.
    If they all exist, the program will continue.
    If a file is missing, the program will print out a message to the
    screen and then exit.
    """

    file_missing_flag = 0

    sounds = ['T_rex1.ogg', 'T_rex2.ogg', 'T_rex3.ogg', 'T_rex4.ogg',
              'T_rex5.ogg', 'T_rex6.ogg', 'T_rex7.ogg', 'T_rex8.ogg']

    logger.info("FILE CHECK")
    # Check to see if dinosaur_facts.txt file exists
    if os.path.isfile('Files/dinosaur_facts.txt'):
        logger.info("dinosaur_facts.txt file was found!")
    else:
        logger.error("dinosaur_facts.txt file was not found! Make sure " +
                     "that the dinosaur_facts.txt file exists in the Files " +
                     "folder.")
        file_missing_flag = 1

    # Check to see if sound files exists
    for sound in sounds:
        if os.path.isfile('Sounds/' + sound):
            logger.info("%s file was found!", sound)
        else:
            logger.error("%s file was not found! Make sure " +
                         "that the %s file exists in the " +
                         "'Sounds' folder.", sound, sound)
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
    """
    Checks to see if the user has permission to read the necessary files

    This function checks to see if the user has permission to read the
    necessary files. If so, the program will continue. If not, the
    program will print out a message to the screen and then exit.
    """

    permission_flag = 0

    sounds = ['T_rex1.ogg', 'T_rex2.ogg', 'T_rex3.ogg', 'T_rex4.ogg',
              'T_rex5.ogg', 'T_rex6.ogg', 'T_rex7.ogg', 'T_rex8.ogg']

    logger.info("PERMISSION CHECK")
    # Check to see if user has read access to dinosaur_facts.txt
    if os.access('Files/dinosaur_facts.txt', os.R_OK):
        logger.info("User has permission to read the dinosaur_facts.txt " +
                    "file.")
    else:
        logger.error("User does not have permission to read the " +
                     "dinosaur_facts.txt file.")
        permission_flag = 1

    # Check to see if user has read access to sound files
    for sound in sounds:
        if os.access('Sounds/' + sound, os.R_OK):
            logger.info("User has permission to read the " +
                        "%s file.", sound)
        else:
            logger.error("User does not have permission to read the " +
                         "%s file.", sound)
            permission_flag = 1

    if permission_flag == 0:
        return
    else:
        print("\033[1;31;40m\nCould not run the program. Check the log " +
              "in the 'Files' folder for more information.")
        stop_the_program()


def empty_file_check():
    """
    Checks to see if a file is empty

    This function will check to see if a file is empty. If it is, the
    program will print a message to the screen and then exit. If the
    file is not empty, the program will continue.
    """

    files = ['dinosaur_facts.txt']

    logger.info("EMPTY FILE CHECK")
    # Check to see if the files are empty
    for file_name in files:
        if os.stat('Files/' + file_name).st_size == 0:
            logger.error("The %s file is empty.", file_name)
            print("\033[1;31;40m\nCould not run the program. Check the log " +
                  "in the 'Files' folder for more information.\n")
            stop_the_program()
        else:
            logger.info("The %s file is not empty." +
                        "This is good. We don't want an empty file.",
                        file_name)


def create_list(file_name):
    """
    Reads a file, creates a list

    This function reads a facts file and use it to create a list. Each
    line of the file will be an element in the list. It will then return
    the list to the main function. If the program is unable to populate
    the list, it will display an error message and then exit the program.

    Arguments:
        file_name: a facts file

    Returns:
        created_list: a list of facts
    """
    logger.info("CREATING LIST")
    logger.info("Reading file: %s", file_name)
    try:
        with open(file_name, "r") as facts:     # open the file as read-only
            created_list = facts.readlines()
        logger.info("After reading %s, the list was successfully populated.",
                    file_name)
    except IOError:
        print("\033[1;31;40mErrors were encountered. Check the log in the " +
              "'Files' folder for more information.")
        logger.error("The %s file could not be created" +
                     " into a list.", file_name)
        stop_the_program()

    return created_list


def print_header():
    """
    Prints a header


    This function will print out the program header to the
    screen.

    This is the only part of the program that doesn't adhere to the PEP
    standards (It exceeds recommended line length). I decided that
    "Readability Counts" and "Beautiful is better than ugly" from The
    Zen of Python should trump the PEP standards in this case. I had
    rewritten it to meet the PEP standard, but is was ugly and
    unreadable. This is much better. The program still compiles and runs
    OK.
    """

    # The r prefix is to let Pylint know that it is a raw string.
    # It prevents the Pylint message "Anomolous backslash in string:
    # string constant might be missing an r prefix"
    print("\n\033[1;37;40m")                        # print white header
    print(r"==========================================================================================================")
    print(r"   _  _   ____    _____                                                                                   ")
    print(r"  | || | |  _ \  |_   _|   _ _ __ __ _ _ __  _ __   ___  ___  __ _ _   _ _ __ _   _ ___   _ __ _____  __  ")
    print(r"  | || |_| | | |   | || | | | '__/ _` | '_ \| '_ \ / _ \/ __|/ _` | | | | '__| | | / __| | '__/ _ \ \/ /  ")
    print(r"  |__   _| |_| |   | || |_| | | | (_| | | | | | | | (_) \__ \ (_| | |_| | |  | |_| \__ \ | | |  __/>  <   ")
    print(r"     |_| |____/    |_| \__, |_|  \__,_|_| |_|_| |_|\___/|___/\__,_|\__,_|_|   \__,_|___/ |_|  \___/_/\_\  ")
    print(r"                       |___/                                                                              ")
    print(r"==========================================================================================================")
    print("\n")


def prompt_user_for_input():
    """
    Prompts user to push a button

    This function prompts a user to push a button.
    """

    # First line - print all white text
    print("\033[1;37;40mPush the white button to activate the T. Rex.")
    # Second line
    print("\033[1;37;40mPush the " +                 # print white text
          "\033[1;31;40mred button " +               # print red text
          "\033[1;37;40mor press Ctrl-C to " +       # print white text
          "\033[1;31;40mstop " +                     # print red text
          "\033[1;37;40mthe program.\n")             # print white text


def get_roar():
    """
    Gets one random sound file

    This function will randomly select one of the T. rex roar
    sound files.

    Returns:
        a sound file and the length of the file in seconds
    """

    # The key/value pair is sound file name : length of file in seconds
    roars = {'Sounds/T_rex1.ogg': 6.5, 'Sounds/T_rex2.ogg': 3,
             'Sounds/T_rex3.ogg': 4, 'Sounds/T_rex4.ogg': 5.5,
             'Sounds/T_rex5.ogg': 4, 'Sounds/T_rex6.ogg': 6,
             'Sounds/T_rex7.ogg': 4.5, 'Sounds/T_rex8.ogg': 4}

    return random.choice(list(roars.items()))


def print_dinosaur_fact(dino_facts):
    """
    Prints a random dinosaur fact

    This function will select a random fact from the dino_facts list and
    print it out.

    Arguments:
        dino_facts: a list of dinosaur_facts
    """

    print("\033[1;34;40mDINOSAUR FUN FACT:")
    print(random.choice(dino_facts))


def activate_t_rex(sound, sound_length):
    """
    Starts the T. rex motor

    This function will play the sound file and activate the T. rex motor
    for the duration of the sound file.

    Arguments:
        sound: The randomly selected T. rex sound file
        sound_length: The length of the sound file in seconds
    """

    try:
        T_REX_MOTOR.value = 0.7        # Controls the motor speed
    except ValueError:
        logger.error("A bad value was specified for the T_REX_MOTOR." +
                     "The value should be between 0 and 1.",
                     exc_info=True)
        print("\033[1;31;40mAn error was encountered. Check the log in the " +
              "'Files' folder for more information.\n")
        stop_the_program()
    pygame.mixer.music.load(sound)     # Loads the sound file
    T_REX_MOTOR_ENABLE.on()            # Starts the motor
    pygame.mixer.music.play()          # Plays the sound file
    sleep(sound_length)                # Length of sound file in seconds
    T_REX_MOTOR_ENABLE.off()           # Stops the motor


def release_gpio_pins():
    """
    Realeases the GPIO pins.
    """

    T_REX_MOTOR.close()
    T_REX_MOTOR_ENABLE.close()
    RED_BUTTON.close()
    WHITE_BUTTON.close()


def stop_the_program():
    """
    Stops the program

    This function will call the release_gpio_pins function, print a
    message to the screen, and then exit the program.
    """

    release_gpio_pins()
    print("\033[1;37;40mExiting program.\n")
    logger.info("END")
    exit()


if __name__ == '__main__':
    main()
