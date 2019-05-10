from flask import Flask, render_template
from flask_socketio import SocketIO
import ast
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
socketio = SocketIO(app)
directions = []

@app.route('/')
def sessions():
    return render_template('session.html')


def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')

@socketio.on('clear')
def handle_clear(json, methods=['GET', 'POST']):
    global directions
    directions = []
    print(directions)

@socketio.on('send message')
def handle_messages(json, methods=['GET', 'POST']):
    """
        Handles user messages
    """
    print('received message: ' + str(json))
    # respond to people with message
    socketio.emit('server response', json, callback=messageReceived)
    parseResponse(json)

    # send direction update to game
    socketio.emit('direction update', directions)
    print("directions", directions)

def parseResponse(message):
    """
    takes an input message, parses it so that only the following directions:
    left, right, up, and down are accepted and adds it to the list of directions

    Parameters: 
        message (dict): user input
    """
    global directions
    allowed = ['left', 'right', 'up', 'down', 'l', 'r', 'u', 'd']
    if message['message'] in allowed:
        directions.append(message['message'])

@socketio.on('name change')
def handle_name_change(json, methods=['GET', 'POST']):
    """
        handles name changing
    """
    print('User has changed name to: ' + str(json['name']))
    socketio.emit('name changed', json, callback=messageReceived)

@socketio.on('join')
def handle_join(json, methods=['GET', 'POST']):
    """
        handles user joining
    """
    print('User has joined: ' + str(json['name']))
    socketio.emit('joined', json, callback=messageReceived)

def justprint():
    print("hello")

if __name__ == '__main__':
    socketio.run(app, debug=True)
