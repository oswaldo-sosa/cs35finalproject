
"""Snake, classic arcade game.
Excercises
1. How do you make the snake faster or slower?
2. How can you make the snake go around the edges?
3. How would you move the food?
4. Change the snake to respond to arrow keys.
"""

from turtle import *
from random import *
from freegames import square, vector
import time

food = vector(0, 0)
snake = [vector(10, 0)]
aim = vector(0, -10)

def change(x, y):
    "Change snake direction."
    aim.x = x
    aim.y = y

def inside(head):
    "Return True if head inside boundaries."
    return -200 < head.x < 190 and -200 < head.y < 190

def move():
    "Move snake forward one segment."
    head = snake[-1].copy()
    while inside(head) or not (head in snake):
        head = snake[-1].copy()
        head.move(aim)

        if not inside(head) or head in snake:
            square(head.x, head.y, 9, 'red')
            update()
            return

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

        new_directions = create_path()
        if new_directions != []:    
            path_move(new_directions)
            return
    return


def path_move(directions):
    """
    """
    if directions == []:
        move()
        return

    for step in directions:
        time.sleep(.1)
        head = snake[-1].copy()
        movesnake(step)
        head.move(aim)

        if not inside(head) or head in snake:
            square(head.x, head.y, 9, 'red')
            update()
            return

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

    new_directions = create_path()
    path_move(new_directions)

def movesnake(dir):
    """ 
    """
    if dir == 'left':
        change(-5, 0)
    elif dir == 'right':
        change(5, 0)
    elif dir == 'up':
        change(0, 5)
    elif dir == 'down':
        change(0, -5)

def create_path():
    """
    """
    options = [ "left", "right", "up", "down"]
    
    path = []
    for i in range(10):
        path.append(choice(options))
    
    options2 = [True,False]

    if choice(options2):
        path = []
    
    return path

setup(420, 420, 370, 0)
hideturtle()
tracer(False)
listen()
onkey(lambda: change(10, 0), 'Right')
onkey(lambda: change(-10, 0), 'Left')
onkey(lambda: change(0, 10), 'Up')
onkey(lambda: change(0, -10), 'Down')
starter_path = create_path()
path_move(starter_path)
done()