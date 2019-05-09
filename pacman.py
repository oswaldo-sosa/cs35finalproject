from main import directions
import json
import socketio

"""
    Pacman, classic arcade game.

    Most of this code came from https://github.com/grantjenks/free-python-games.
    The code was modified by Brittany Wang, Luis Hernandez Cruz, and Oswaldo Sosa. 
"""

from random import choice
from turtle import *
from freegames import floor, vector
import time

# Create al the elements of the game
state = {'score': 0}
path = Turtle(visible=False)
writer = Turtle(visible=False)
aim = vector(5, 0)
pacman = vector(-40, -80)
ghosts = [
    [vector(-180, 160), vector(5, 0)],
    [vector(-180, -160), vector(0, 5)],
    [vector(100, 160), vector(0, -5)],
    [vector(100, -160), vector(-5, 0)],
]
tiles = [
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0,
    0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
]

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

def square(x, y):
    """ Uses the turtle library to draw a square starting at the coordinate (x,y).
    """
    path.up()
    path.goto(x, y)
    path.down()
    path.begin_fill()

    for count in range(4):
        path.forward(20)
        path.left(90)

    path.end_fill()

def offset(point):
    """ Return the offset of the point based on the tiles on the game board.
    """
    x = (floor(point.x, 20) + 200) / 20
    y = (180 - floor(point.y, 20)) / 20
    index = int(x + y * 20)
    return index

def valid(point):
    """ valid checks whether the inputted point is a valid point in the board.
        If the point is located inside a tile then the point is not valid. Returns
        True if the point is valid, returns False otherwise.
    """
    index = offset(point)

    if tiles[index] == 0:
        return False

    index = offset(point + 19)

    if tiles[index] == 0:
        return False

    return point.x % 20 == 0 or point.y % 20 == 0

def world():
    """ Uses the turtle library to draw the pacman gameboard.
    """
    bgcolor('black')
    path.color('blue')

    for index in range(len(tiles)):
        tile = tiles[index]

        if tile > 0:
            x = (index % 20) * 20 - 200
            y = 180 - (index // 20) * 20
            square(x, y)

            if tile == 1:
                path.up()
                path.goto(x + 10, y + 10)
                path.dot(2, 'white')

def game_frame():
    """ game_frame renders one frame of the game. It contains the logic to
        move the ghosts and pacman on the game board.
    """
    time.sleep(.1)
    writer.undo()
    writer.write(state['score'])

    clear()

    if valid(pacman + aim):
        pacman.move(aim)

    index = offset(pacman)

    if tiles[index] == 1:
        tiles[index] = 2
        state['score'] += 1
        x = (index % 20) * 20 - 200
        y = 180 - (index // 20) * 20
        square(x, y)

    up()
    goto(pacman.x + 10, pacman.y + 10)
    dot(20, 'yellow')

    for point, course in ghosts:
        if valid(point + course):
            point.move(course)
        else:
            options = [
                vector(5, 0),
                vector(-5, 0),
                vector(0, 5),
                vector(0, -5),
            ]
            plan = choice(options)
            course.x = plan.x
            course.y = plan.y

        up()
        goto(point.x + 10, point.y + 10)
        dot(20, 'red')

    update()

    for point, course in ghosts:
        if abs(pacman - point) < 20:
            return True # One of the ghosts got to pacman

def path_move(directions):
    """ path_move takes in a list of directions. The list of directions
        tells pacman which direction to move. If the list is empty then 
        it renders the game using a different function. Gets new directions
        once it has looped through the list and then calls the function again.
    """
    # If there are no directions, then run the game 
    # with no directions
    if directions == []:
        move()
        return
    
    for step in directions:
        movepac(step)

        # If pacman was hit by enemy then end the game
        if game_frame():
            return

    sio.emit('clear', {})

    # Get next directions and call function again
    new_directions = check_directions()
    path_move(new_directions)

def move():
    """ move is able to run the game when no directions are being passed to the game.
        It allows the ghosts to continue moving and pacman moves the same direction
        until a new direction is given. It checks for a new list of directions at the
        end of each game frame.
    """
    hit = False
    while not hit:
        hit = game_frame()

        new_directions = check_directions()
        if new_directions != []:    
            path_move(new_directions)
            return
    return

def change(x, y):
    """ change takes in an x,y coordinate and checks if pacman can move to that point.
        If the point is valid then change pacman's trajectory so that he moves toward
        that point. If the point is not valid, then pacman continues to move the same
        direction.
    """
    if valid(pacman + vector(x, y)):
        aim.x = x
        aim.y = y

def movepac(dir):
    """ movepac takes in a string which is either 'up', 'down', 'left', or 'right' and
        it changes pacman's direction based on the inputted string. If a different 
        string is inputted then pacman's direction will not change.
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
    writer.goto(160, 160)
    writer.color('white')
    writer.write(state['score'])
    listen()
    instructions = check_directions()
    world()
    path_move(instructions)
    done()

main()
