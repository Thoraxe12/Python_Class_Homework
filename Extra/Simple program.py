# Ask user for a number
# Store input in a var

# Ask the user for a number from 1-4
# Store the input into a var

# Check if the input is bad

# Check input if its 1
# add 5 to the number

# if its 2
# multiply by 4

# if its 3
# divide by 3

# if its 4
# subtract by 9

# Print the number

while True:
    userNumber = input("Enter a number please: ")
    userSecondNumber = input("Enter a number between 1-4: ")

    if not (userNumber.isdigit() and userSecondNumber.isdigit()):
        print("Error! Gave bad input!\n\n")
        continue

    userNumber = int(userNumber)
    userSecondNumber = int(userSecondNumber)

    if userSecondNumber < 1 or userSecondNumber > 4:
        print("Error! The second number must be 1-4\n\n")
        continue

    match userSecondNumber:
        case 1:
            userNumber += 5
        case 2:
            userNumber *= 4
        case 3:
            userNumber /= 3
        case 4:
            userNumber -= 9

    print("The number is now {}".format(userNumber))

    userRunAgain = input("Would you like to run again? (Y/N)\n")
    if userRunAgain.lower() == "y":
        continue

    break
