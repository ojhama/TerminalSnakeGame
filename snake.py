import curses
from random import randint

# Window setup
curses.initscr()
xMax = 60
yMax = 20
win = curses.newwin(yMax, xMax, 0, 0)
win.keypad(1)
curses.noecho()
curses.curs_set(0)
win.border(0)
win.nodelay(1)

# snake, food and score initialization
snake = [(6, 15), (6, 14), (6, 13)]
food = (15, 25)
win.addch(food[0], food[1], '#')
score = 0

# defining exist key
ESC = 27

# setting default moving direction as right
key = curses.KEY_RIGHT

# loop untill ESC key pressed
while key != ESC:
    # Addding score text at top left corner
    win.addstr(0, 2, ' SCORE ' + str(score) + ' ')

    # setting different sppeds while moving vertically and horizontally
    if key in [curses.KEY_UP or curses.KEY_DOWN]:
        win.timeout(150-(len(snake)) // 8)
    else:
        win.timeout(150-(len(snake)*2) // 5)

    # checking if any valid key was presses. If not. keep the last key entry
    prev_key = key
    event = win.getch()
    key = event if event != -1 else prev_key
    if key not in [curses.KEY_LEFT, curses.KEY_RIGHT, curses.KEY_UP, curses.KEY_DOWN, ESC]:
        key = prev_key

    # getting the head y,x of snake
    y = snake[0][0]
    x = snake[0][1]

    # creating new head as per the key pressed
    if key == curses.KEY_DOWN:
        y += 1
    if key == curses.KEY_UP:
        y -= 1
    if key == curses.KEY_LEFT:
        x -= 1
    if key == curses.KEY_RIGHT:
        x += 1

    # if new head is going out of the boundry, teleporting it to the begining of the opposite boundry
    if y == 0:
        y = yMax-2
    if y == yMax-1:
        y = 1
    if x == 0:
        x = xMax-2
    if x == xMax-1:
        x = 1

    # inserting new head in the snake co-ordinate list
    snake.insert(0, (y, x))

    # if the new head falls on same spot as any of the body spots then game over
    if snake[0] in snake[1:]:
        break

    # if snake head falls on same spot of the food, then creating a new food at different location
    # ( not removing tail, so that size increases by 1 every time it eats food )
    # and if the new head does not fall on the food, then removing the tail of snake to let it keep moving with the same size
    if snake[0] == food:
        score += 1
        food = ()
        while food == ():
            food = (randint(1, yMax-2), randint(1, xMax-2))
            if food in snake:
                food = ()
        win.addch(food[0], food[1], '#')
    else:
        last = snake.pop()
        win.addch(last[0], last[1], ' ')

    # after all the changes, printing the snake cordinates on the screen
    for c in snake:
        win.addch(c[0], c[1], '0')

# after game over, deleting the snake and food from the screen
for c in snake:
    win.addch(c[0], c[1], ' ')
win.addch(food[0], food[1], ' ')

# setting and displaying game over and score message on the screen
messg = "GAME OVER !! FINAL SCORE : "
messg2 = "PRESS ESC KEY TO EXIT!"
win.border(0)
win.addstr(8, xMax//2-len(messg)//2, messg + str(score))
win.addstr(10, xMax//2-len(messg2)//2+1, messg2)

# waiting for user to press ESC key to exit from game
key = -1
while key != ESC:
    key = win.getch()
curses.endwin()
