import csv
import os
from enum import Enum
from typing import List, Tuple

import matplotlib.pyplot as plt
import numpy as np

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
    print()  # Print a new line to make things cleaner
    i = 1
    for file in files:
        print("{}: {}".format(i, file))
        i += 1

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
    i = 1
    for category in DATA_CATEGORIES:
        print("{}: {}".format(i, category))
        i += 1

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


def getDataFromFile(file: str, dataCat: DataCategoriesEnum) -> Tuple[List[str], List[float], List[str]]:
    # DBT = index 31
    # Humidity = 37
    # GHI = 4
    # DNI = 7
    # Dew Point Temp = 34
    # Wind speed = 46

    date = []
    time = []
    data = []
    with open(file, "r") as file:
        reader = csv.reader(file)
        rowIndex = 0
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

        for i, row in enumerate(reader):
            if i == 0 or i == 1:
                continue

            time.append(row[1][0:2])
            data.append(float(row[rowIndex]))
            date.append(row[0])

    return time, data, date


def convertMonthIntToString(monthNumber: int) -> str:
    match monthNumber:
        case 1:
            return "Jan"
        case 2:
            return "Feb"
        case 3:
            return "Mar"
        case 4:
            return "Apr"
        case 5:
            return "May"
        case 6:
            return "Jun"
        case 7:
            return "Jul"
        case 8:
            return "Aug"
        case 9:
            return "Sep"
        case 10:
            return "Oct"
        case 11:
            return "Nov"
        case 12:
            return "Dec"


def createScatterChart(dataList: List[float], timeList: List[str]) -> None:
    plt.scatter(timeList, dataList)
    plt.show()


def processToMinMaxAvgData(dataList: List[float], dateList: List[str]) -> Tuple[List[List[float]], List[str]]:
    minList = []
    maxList = []
    avgList = []
    monthTempList = []
    allDataList = []
    timeList = []

    currentMonth = dateList[0][0:2]
    for i, data in enumerate(dataList):
        if dateList[i][0:2] != currentMonth:
            currentMonth = dateList[i][0:2]
            timeList.append(convertMonthIntToString(int(currentMonth)))

            minNumber = min(monthTempList)
            maxNumber = max(monthTempList)
            avgNumber = sum(monthTempList) / len(monthTempList)

            minList.append(minNumber)
            maxList.append(maxNumber)
            avgList.append(avgNumber)

        monthTempList.append(data)

    allDataList.append(minList)
    allDataList.append(maxList)
    allDataList.append(avgList)

    return allDataList, timeList


def createMinMaxAvgChart(dataList: List[float], dateList: List[str]) -> None:
    (formattedDataList, timeList) = processToMinMaxAvgData(dataList, dateList)
    minList = formattedDataList[0]
    maxList = formattedDataList[1]
    avgList = formattedDataList[2]

    plt.plot(timeList, minList)
    plt.plot(timeList, maxList)
    plt.plot(timeList, avgList)
    plt.show()


# Discrete values for each hour of the year.
# Convert data into discrete via rounding
# Get data of the year in file and push the data into a dictionary
def processToDiscreteData(dataList: List[float], timeList: List[str]) -> tuple[dict[str, list[float]], list[str]]:
    uniqueHoursList = []
    for hour in timeList:
        if hour not in uniqueHoursList:
            uniqueHoursList.append(hour)

    dataByHour = {}
    for i in range(len(timeList)):
        hour = timeList[i]
        temperature = dataList[i]
        if hour in dataByHour:
            dataByHour[hour].append(temperature)
        else:
            dataByHour[hour] = [temperature]

    return dataByHour, uniqueHoursList


def createDiscreteChart(dataList: List[float], timeList: List[str]) -> None:
    dataList, timeList = processToDiscreteData(dataList, timeList)

    plt.bar(timeList, [np.mean(dataList[hour]) for hour in timeList])
    plt.show()


def main() -> None:
    files = getFilteredFiles()
    fileName = getFileChoice(files)
    dataChoiceEnum = getDataChoice()
    chartType = getChartType()

    (timeList, dataList, dateList) = getDataFromFile(fileName, dataChoiceEnum)

    match chartType:
        case ChartTypeEnum.ScatterChart:
            createScatterChart(dataList, timeList)
        case ChartTypeEnum.MinMaxAvg:
            createMinMaxAvgChart(dataList, dateList)
        case ChartTypeEnum.DiscreteValues:
            createDiscreteChart(dataList, timeList)


main()