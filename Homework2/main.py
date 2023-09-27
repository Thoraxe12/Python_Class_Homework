# Get all files in current input dir                                ---DONE---
# Filter files down to only TMY3 files                              ---DONE---
# Ask user which file                                               ---DONE---
# Trap input errors                                                 ---DONE---
# Create file object with valid input                               ---Bad Way To Do It---
# Create an enum with all the data categories                       ---DONE---
# Give the user a selection among (at a minimum): dry bulb temperature, humidity,
# global horizontal irradiation(GHI), direct normal Irradiance(DNI),
# dew point temperature, and wind                                   ---DONE---
# Ask the user if they would like to plot                           ---DONE---
#   scatter chart by hour of the day
# 	monthly minimum, maximum, and average
# 	discrete values for each hour of the year.
# Trap input errors                                                 ---DONE---
# Create file object using "with" for auto closing.                 ---DONE---
# Use file object to create 2D list of file contents                ---DONE---
# Filter contents list down to the user selected data category      ---DONE---
# Create chart - Learn how to do now
import csv
# From TMY3 manual:
# The 12 selected typical months for each station were chosen using statistics determined by
# considering five elements: global horizontal radiation, direct normal radiation, dry bulb
# temperature, dew point temperature, and wind speed. These elements are considered the most
# important for simulating solar energy conversion systems and building systems.

import os
from enum import Enum
from typing import List

DATA_CATEGORIES = ["Dry Bulb Temperature", "Humidity", "Global Horizontal Irradiation",
                   "Direct Normal Irradiance", "Dew Point Temperature", "Wind Speed"]
DATA_CATEGORIES_LEN = len(DATA_CATEGORIES)


class DataCategoriesEnum(Enum):
    # dry bulb temperature, humidity, and global horizontal irradiation(GHI)
    # direct normal Irradiance(DNI), dew point temperature, and wind speed

    DBT = 1
    HUMIDITY = 2
    GHI = 3
    DNI = 4
    DPT = 5
    WS = 6


class ChartTypeEnum(Enum):
    #   scatter chart by hour of the day
    # 	monthly minimum, maximum, and average
    # 	discrete values for each hour of the year.

    ScatterChart = 1
    MinMaxAvg = 2
    DiscreteValues = 3


def getFilteredFiles() -> List[str]:
    # Get all files in current dir
    allFiles = os.listdir()
    # Filter list of files down to only csv files and return
    return list(filter(lambda file: file.find(".CSV") != -1, allFiles))


def getFileChoice(files: List[str]) -> str:
    # Print all filenames with index in front of filename for user choice.
    # Out of Loop because files can be to max source size of 1020. This is too many operations to repeat.
    print()
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
        return files[userChoice - 1]


def getDataChoice() -> DataCategoriesEnum:
    print()
    for i, category in enumerate(DATA_CATEGORIES):
        print("{}: {}".format(i + 1, category))

    while True:
        userChoice = input("Enter a number between 1 - {}: ".format(DATA_CATEGORIES_LEN))

        if not userChoice.isdigit():
            print("Error! Please enter numbers only!\n")
            continue

        userChoice = int(userChoice)

        match userChoice:
            case 1:
                return DataCategoriesEnum.DBT
            case 2:
                return DataCategoriesEnum.HUMIDITY
            case 3:
                return DataCategoriesEnum.GHI
            case 4:
                return DataCategoriesEnum.DNI
            case 5:
                return DataCategoriesEnum.DPT
            case 6:
                return DataCategoriesEnum.WS
            case _:
                print("Error! Please enter a number between 1 - {}: ".format(DATA_CATEGORIES_LEN))


def getChartType() -> ChartTypeEnum:
    # Ask the user if they would like to plot
    #   scatter chart by hour of the day
    # 	monthly minimum, maximum, and average
    # 	discrete values for each hour of the year.

    while True:
        print("\nHow would you like to plot?\n"
              "1. Scatter chart by hour of the day\n"
              "2. Monthly minimum, maximum, and average\n"
              "3. Discrete values for each hour of the year")
        userInput = input("Enter a number between 1 - 3: ")

        if not userInput.isdigit():
            print("Error! Please enter numbers only.\n")
            continue

        userInput = int(userInput)

        match userInput:
            case 1:
                return ChartTypeEnum.ScatterChart
            case 2:
                return ChartTypeEnum.MinMaxAvg
            case 3:
                return ChartTypeEnum.DiscreteValues
            case _:
                print("Error! Please enter numbers only.\n")


def getDataFromFile(file: str, dataCat: DataCategoriesEnum) -> List[str]:
    # DBT = index 31
    # Humidity = 37
    # GHI = 4
    # DNI = 7
    # Dew Point Temp = 34
    # Wind speed = 46

    data = []
    with open(file, "r") as file:
        reader = csv.reader(file)

        for i, row in enumerate(reader):
            if i == 0 or i == 1:
                continue

            match dataCat:
                case DataCategoriesEnum.DBT:
                    rowIndex = 31
                case DataCategoriesEnum.HUMIDITY:
                    rowIndex = 37
                case DataCategoriesEnum.GHI:
                    rowIndex = 4
                case DataCategoriesEnum.DNI:
                    rowIndex = 7
                case DataCategoriesEnum.DPT:
                    rowIndex = 34
                case DataCategoriesEnum.WS:
                    rowIndex = 46

            data.append(row[rowIndex])

    return data


def main() -> None:
    files = getFilteredFiles()
    fileIndex = getFileChoice(files)
    dataChoiceEnum = getDataChoice()


def driver() -> None:
    dataChoice = getDataChoice()
    file = getFileChoice(getFilteredFiles())
    print(getDataFromFile(file, dataChoice))


driver()
