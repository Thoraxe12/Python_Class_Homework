# Get all files in current input dir    ---DONE---
# Filter files down to only TMY3 files  ---DONE---
# Ask user which file                   ---DONE---
# Trap input errors                     ---DONE---
# Create file object with valid input   ---Bad Way To Do It---
# Create an enum with all the data categories  ---DONE---
# Give the user a selection among (at a minimum): dry bulb temperature, humidity, and global horizontal irradiation(GHI)
# direct normal Irradiance(DNI), dew point temperature, and wind speed
# Ask the user if they would like to plot:
#   scatter chart by hour of the day
# 	monthly minimum, maximum, and average
# 	discrete values for each hour of the year.
# Trap input errors
# Create file object using "with" for auto closing.
# Use file object to create 2D list of file contents
# Filter contents list down to the user selected data category
# Create chart - Learn how to do later

# From TMY3 manual:
# The 12 selected typical months for each station were chosen using statistics determined by
# considering five elements: global horizontal radiation, direct normal radiation, dry bulb
# temperature, dew point temperature, and wind speed. These elements are considered the most
# important for simulating solar energy conversion systems and building systems.

import csv
from typing import List
from enum import Enum
import os

DATA_CATEGORIES = ["dry bulb temperature", "humidity", "global horizontal irradiation",
                   "direct normal Irradiance", "dew point temperature", "wind speed"]
DATA_CATEGORIES_LEN = len(DATA_CATEGORIES)


class DataCategoriesEnum(Enum):
    # dry bulb temperature, humidity, and global horizontal irradiation(GHI)
    # direct normal Irradiance(DNI), dew point temperature, and wind speed

    DBT = 1
    HUMIDITY = 2
    GHI = 3
    DNI = 4
    DPT = 5
    WP = 6


def getFilteredFiles() -> List[str]:
    # Get all files in current dir
    allFiles = os.listdir()
    # Filter list of files down to only csv files and return
    return list(filter(lambda file: file.find(".CSV") != -1, allFiles))


def getFileChoice(files: List[str]) -> int:
    # Print all filenames with index in front of filename for user choice.
    # Out of Loop because files can be to max source size of 1020. This is too many operations to repeat.
    for i, file in enumerate(files):
        print("{}: {}".format(i + 1, file))

    # Main func loop
    while True:
        # Get input but use len so the user can have any number of files
        userChoice = input("Enter a number between 1 - {}: ".format(len(files)))

        # Check if user gave input with bad chars or symbols
        # This is a guard clause. 1 of 2 ways to do error checking and correcting
        if not userChoice.isdigit():
            print("Error! Please enter numbers only!\n")
            continue

        userChoice = int(userChoice)

        if userChoice < 1 or userChoice > len(files):
            print("Error! Please enter a number between 1 - {}\n".format(len(files)))
            continue

        # No need for an else branch
        return userChoice - 1


def getDataChoice() -> int:
    for i, category in enumerate(DATA_CATEGORIES):
        print("{}: {}".format(i + 1, category))

    while True:
        userChoice = input("Enter a number between 1 - {}: ".format(DATA_CATEGORIES_LEN))

        if not userChoice.isdigit():
            print("Error! Please enter numbers only!\n")
            continue

        userChoice = int(userChoice)
        if userChoice < 1 or userChoice > DATA_CATEGORIES_LEN:
            print("Error! Please enter a number between 1 - {}: ".format(DATA_CATEGORIES_LEN))
            continue

        return userChoice


def main() -> None:
    files = getFilteredFiles()
    fileIndex = getFileChoice(files)


def driver() -> None:
    print(getDataChoice())


driver()
