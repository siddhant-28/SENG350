from flask import  Flask,send_from_directory, jsonify, make_response, request ,redirect, abort, render_template, g, send_file
from flask_socketio import SocketIO, emit, join_room, leave_room
from random import randrange
from apscheduler.schedulers.background import BackgroundScheduler
import game_logic
import time

app = Flask(__name__)
socketio = SocketIO(app)

currgames = {}


def sensor():

    for game in currgames:

        if(currgames[game].getRunning() == True):
            if(currgames[game].checkWalls()):
                socketio.emit('gameOver', room=game)
                currgames.pop(game)
                print("gameOver1")
            snake1 = currgames[game].getHostSnake()
            snake1pos = snake1.getPos()

            snake2 = currgames[game].getP2Snake()
            snake2pos = snake2.getPos()
            if(snake1pos.count(snake1pos[0]) > 1):
                socketio.emit('gameOver', room=game)
                currgames.pop(game)
                print("gameOver")

            boardstate = [-1] * 100
            for cords in snake1pos:
                boardstate[cords] = 1
            for cords in snake2pos:
                boardstate[cords] = 2
            if not currgames[game].getFood():
                foodPosition = randrange(101)
                while boardstate[foodPosition] != -1:
                    foodPosition = randrange(101)
                currgames[game].setFood([foodPosition])
            for food in currgames[game].getFood():
                boardstate[food] = 0

            return_dict = {}
            return_dict['boardState'] = boardstate
            socketio.emit('boardState',return_dict, room=game)



sched = BackgroundScheduler(daemon=True)
sched.add_job(sensor,'interval',seconds=2)
sched.start()


@socketio.on('hostGame')
def hostGame():
    # Initialize a new game and add it do the dictionary
    game       = game_logic.game()
    gameID     = game.getID()
    snakeID = game.getSnake1ID()
    currgames[gameID] = game

    # Bind the User to the Specific GameID
    join_room(gameID)

    # Send GameID and the SnakeID of the user
    return_dict = {}
    return_dict['gameID'] =  gameID
    return_dict['snakeID'] = snakeID
    socketio.emit('startInfo',return_dict)



@socketio.on('move')
def move(data):
    gameID = data['gameID']
    move   = data['move']
    snakeID = data['snakeID']
    snake1ID = currgames[gameID].getSnake1ID()
    snake2ID = currgames[gameID].getSnakeP2ID()
    if(snake1ID == snakeID):
        snake1 = currgames[gameID].getHostSnake()
        snake1.setMove(move)
    if(snake2ID == snakeID):
        snake2 = currgames[gameID].getP2Snake()
        snake2.setMove(move)


@socketio.on('startGame')
def startGame(data):
    gameID = data['gameID']
    currgames[gameID].setRunning(True)

@socketio.on('joinGame')
def joinGame(data):
    gameID  = data['gameID']
    snakeID = currgames[gameID].getSnakeP2ID()
    currgames[gameID].setReady(True)
    join_room(gameID)
    # Send GameID and the SnakeID of the user
    return_dict = {}
    return_dict['gameID'] =  gameID
    return_dict['snakeID'] = snakeID
    socketio.emit('gameInfo', return_dict)
    socketio.emit('gameReady',room=gameID)

@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/game')
def game():
    return render_template('game.html')

@app.route('/stylesheet')
def stylesheet():
    return send_from_directory('css', '/static/CSS/main.css')

@app.route('/javascript')
def javascript():
    return send_from_directory('js', '/static/js/scripts.js')

if __name__ == '__main__':
    app.static_folder = 'static'
    app.run()