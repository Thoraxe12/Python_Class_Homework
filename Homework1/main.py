import turtle
from turtle import Screen


def has_bad_chars(user_input: str, err_msg: str) -> bool:
    hasSymbols = False
    for char in user_input:
        if not char.isdigit():
            print(err_msg)
            hasSymbols = True
            break

    return hasSymbols


def get_shape() -> int:
    userInput = 1
    validInput = False
    while not validInput:
        print("1. Squares\n"
              "2. Rectangles\n"
              "3. Circles\n"
              "4. Triangles\n"
              "5. 5-point stars\n"
              "Enter a number between 1-5: ", end="")
        userInput = input()

        if has_bad_chars(userInput, "Error! Please enter numbers only.\n\n"):
            continue

        userInput = int(userInput)

        if userInput < 1 or userInput > 5:
            validInput = False
            print("Error! User choice was not a number between 1-5."
                  "\nPlease Try Again!\n")
        else:
            validInput = True
    return userInput


def get_rows_and_cols() -> (int, int):
    (rowInput, colInput) = 1, 1
    while True:
        print("How many rows would you like?\n"
              "Enter a number 1 - 20: ", end="")
        rowInput = input()

        if has_bad_chars(rowInput, "Error! Please enter numbers only for number of rows\n\n"):
            continue

        print("How many columns would you like?\n"
              "Enter a number 1 - 20: ", end="")
        colInput = input()

        if has_bad_chars(colInput, "Error! Please enter numbers only for number of columns\n\n"):
            continue

        rowInput = int(rowInput)
        colInput = int(colInput)

        if rowInput < 1 or rowInput > 20 or colInput < 1 or colInput > 20:
            print("Error! Please only enter numbers between 1-20")
        else:
            break
    return rowInput, colInput


def get_color(colors: list[str]) -> int:
    colorChoice = 0
    validInput = False
    while not validInput:
        for i, _ in enumerate(colors):
            print("{}. {}".format(i, colors[i]))

        print("Enter 0 - 9: ", end="")
        colorChoice = input()

        if has_bad_chars(colorChoice, "Enter numbers only 0 - 9"):
            continue

        colorChoice = int(colorChoice)

        if colorChoice < 0 or colorChoice > 9:
            continue
        else:
            validInput = True

    return colorChoice


def draw_shapes(t: turtle.Turtle, shape: int, rows: int, cols: int, color: str):
    t.color(color)

    TURTLE_SIZE = 20
    t.penup()
    screen = Screen()
    X_POS = TURTLE_SIZE / 2 - screen.window_width() / 2 + 25
    t.goto(X_POS, (screen.window_height() / 2 - TURTLE_SIZE / 2) - 100)
    t.pendown()

    for _ in range(rows):
        for _ in range(cols):
            if shape == 1:
                draw_square(t)
            elif shape == 2:
                draw_rectangle(t)
            elif shape == 3:
                draw_circle(t)
            elif shape == 4:
                draw_triangle(t)
            else:
                draw_5_point_star(t)

            currentPosition = t.pos()
            t.penup()
            t.setpos(currentPosition[0] + 50, currentPosition[1])
            t.pendown()

        currentPosition = t.pos()
        t.penup()
        t.setpos(X_POS, currentPosition[1] - 50)
        t.pendown()


def draw_square(t: turtle.Turtle):
    for _ in range(4):
        t.forward(50)
        t.left(90)


def draw_rectangle(t: turtle.Turtle):
    t.forward(50)
    t.left(90)
    t.forward(30)
    t.left(90)
    t.forward(50)
    t.left(90)
    t.forward(30)
    t.left(90)


def draw_circle(t: turtle.Turtle):
    t.circle(25)


def draw_triangle(t: turtle.Turtle):
    for _ in range(3):
        t.forward(25)
        t.left(120)


def draw_5_point_star(t: turtle.Turtle):
    for _ in range(5):
        t.forward(25)
        t.right(144)


if __name__ == "__main__":
    main_turtle = turtle.Turtle()
    colors = ["navy", "blue", "pale green", "slate gray", "goldenrod", "dark red", "firebrick", "deep pink", "purple",
              "magenta"]

    while True:
        shape = get_shape()
        (rows, cols) = get_rows_and_cols()
        colorIndex = get_color(colors)
        draw_shapes(main_turtle, shape, rows, cols, colors[colorIndex])

        print("Would you like to run it again?\n"
              "Y/N: ", end="")

        userRunAgain = input()
        if userRunAgain.lower() != "y":
            break

        main_turtle.reset()
        main_turtle.clear()
