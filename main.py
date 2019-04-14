from flask import Flask, render_template
from flask_socketio import SocketIO
import ast
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
socketio = SocketIO(app)


@app.route('/')
def sessions():
    return render_template('session.html')


def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')


@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    print('received my event: ' + str(json))
    socketio.emit('my response', json, callback=messageReceived)
    directions = []
    parseResponse(json, directions)
    print("directions", directions)

def parseResponse(message, directions):
    """
    takes an input message, parses it so that only the following directions:
    left, right, up, and down are accepted and put it in a list

    Parameters: 
        message (dict): user input
        directions (list): live directions list 

    Returns: 
        directions (list): list that contains only 'left', 'right', 'up', 'down'
    """
    allowed = ['left', 'right', 'up', 'down', 'l', 'r', 'u', 'd']
    if message['message'] in allowed:
        directions.append(message['message'])
    return directions
    
def broadcastJoin(methods=['Get', 'POST']):
    print('User has joined')

@socketio.on('name change')
def handle_my_custom_event1(json, methods=['GET', 'POST']):
    print('User has changed name to: ' + str(json['name']))
    socketio.emit('name changed', json, callback=messageReceived)

@socketio.on('join')
def handle_my_custom_event1(json, methods=['GET', 'POST']):
    print('User has joined: ' + str(json['name']))
    socketio.emit('joined', json, callback=messageReceived)

@socketio.on('send message')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    print('received message: ' + str(json))
    socketio.emit('server response', json, callback=messageReceived)


if __name__ == '__main__':
    socketio.run(app, debug=True)
