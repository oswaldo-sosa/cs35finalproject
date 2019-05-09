
"""
    Snake, classic arcade game.

    Most of this code came from https://github.com/grantjenks/free-python-games.
    The code was modified by Brittany Wang, Luis Hernandez Cruz, and Oswaldo Sosa.
"""

from main import directions
import json
import socketio
from turtle import *
from random import *
from freegames import square, vector
import time

food = vector(0, 0)
snake = [vector(10, 0)]
aim = vector(0, -10)
dirs = []

# standard Python
sio = socketio.Client()

@sio.on('direction update')
def on_connect(new_dirs):
    """ on_connect updates the global variable containing the inputted directions
        from the chat application. Uses socketio to send requests to the chat 
        application.
    """ 
    global dirs
    dirs = new_dirs
    print("direction update: " + str(dirs))

def change(x, y):
    """ change takes in an x,y coordinate and changes the trajectory of the snake to 
        that x,y coordinate.
    """
    aim.x = x
    aim.y = y

def inside(head):
    """ Return True if head is inside the board boundaries.
    """ 
    return -200 < head.x < 190 and -200 < head.y < 190

def game_frame():
    """ game_frame renders one frame of the game. It contains the logic for
        the game.    
    """
    time.sleep(.15)
    head = snake[-1].copy()
    head.move(aim)
    
    if not inside(head) or head in snake:
        square(head.x, head.y, 9, 'red')
        update()
        return True

    snake.append(head)

    if head == food:
        print('Snake:', len(snake))
        food.x = randrange(-15, 15) * 10
        food.y = randrange(-15, 15) * 10
    else:
        snake.pop(0)

    clear()

    for body in snake:
        square(body.x, body.y, 9, 'black')

    square(food.x, food.y, 9, 'green')
    update()


def path_move(directions):
    """ path_move takes in a list of directions. The list of directions
        tells the snake which direction to move. If the list is empty then 
        it renders the game using a different function. Gets new directions
        once it has looped through the list and then calls the function again.
    """
    # If there are no directions, then run the game 
    # with no directions
    if directions == []:
        move()
        return

    for step in directions:
        movesnake(step)
        
        # If invalid move then end the game
        if game_frame():
            return

    sio.emit('clear', {})

    # Get next directions and call function again
    new_directions = check_directions()
    path_move(new_directions)

def move():
    """ move is able to run the game when no directions are being passed to the game.
        It checks for a new list of directions at the end of each game frame.
    """
    lost = False
    while not lost:
        lost = game_frame()

        new_directions = check_directions()
        if new_directions != []:    
            path_move(new_directions)
            return
    return

def movesnake(dir):
    """ movesnake takes in a string which is either 'up', 'down', 'left', or 'right' and
        it changes the snake's direction based on the inputted string. If a different 
        string is inputted then the snake's direction will not change.
    """
    if dir == 'left':
        change(-5, 0)
    elif dir == 'right':
        change(5, 0)
    elif dir == 'up':
        change(0, 5)
    elif dir == 'down':
        change(0, -5)

def check_directions():
    """ check_directions checks the global variable dirs to see if new
        directions have been passed from the chat application. If new
        directions were sent, return that new list of directions. If
        no directions were sent then return an empty list.
    """
    global dirs
    if len(dirs) != 0:
        olddirs = dirs
        dirs = []
        return olddirs

    return []

def main():
    """ run the game
    """
    sio.connect('http://localhost:5000')
    sio.emit('clear', {})
    setup(420, 420, 370, 0)
    hideturtle()
    tracer(False)
    listen()
    onkey(lambda: change(10, 0), 'Right')
    onkey(lambda: change(-10, 0), 'Left')
    onkey(lambda: change(0, 10), 'Up')
    onkey(lambda: change(0, -10), 'Down')
    starter_path = check_directions()
    path_move(starter_path)
    done()

main()