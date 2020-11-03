import random
import string
import constants

# Python
# 0   1   2   3   4   5   6   7   8   9
# 10  11  12  13  14  15  16  17  18  19
# 20  21  22  23  24  25  26  27  28  29
# 30  31  32  33  34  35  36  37  38  39
# 40  41  42  43  44  45  46  47  48  49
# 50  51  52  53  54  55  56  57  58  59
# 60  61  62  63  64  65  66  67  68  69
# 70  71  72  73  74  75  76  77  78  79
# 80  81  82  83  84  85  86  87  88  89
# 90  91  92  93  94  95  96  97  98  99

# Legend
# Blank   = -1
# Food    = 0
# Snake1  = 1
# Snake2  = 2
# foodPosition  = randrange(101)
def creatSnakeID():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

def creatGameID():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))

def checkWalls(game):
    snake1 = game.getHostSnake()
    move          = snake1.getMove()
    snakePosition = snake1.getPos()
    collision = False
    if(move == 'R'):
            if(snakePosition[0]%10) == 9 :
                collision = True
            else:
                snakePosition = [snakePosition[0] + 1] + snakePosition


    if(move == 'L'):
            if(snakePosition[0]%10) == 0:
                collision = True
            else:
                snakePosition = [snakePosition[0] - 1] + snakePosition


    if(move == 'D'):
            if(snakePosition[0]+10) > 99:
                collision = True
            else:
                snakePosition = [snakePosition[0] + 10] + snakePosition


    if(move == 'U'):
            if(snakePosition[0]-10) < 0:
                collision = True
            else:
                snakePosition = [snakePosition[0] - 10] + snakePosition
    if(snakePosition[0] in game.getFood() ):
        game.setFood([])
    else:
        del snakePosition[-1]
    snake1.setPos(snakePosition)

    snake2 = game.getP2Snake()
    move          = snake2.getMove()
    snakePosition = snake2.getPos()
    collision = False
    if(move == 'R'):
            if(snakePosition[0]%10) == 9 :
                collision = True
            else:
                snakePosition = [snakePosition[0] + 1] + snakePosition


    if(move == 'L'):
            if(snakePosition[0]%10) == 0:
                collision = True
            else:
                snakePosition = [snakePosition[0] - 1] + snakePosition


    if(move == 'D'):
            if(snakePosition[0]+10) > 99:
                collision = True
            else:
                snakePosition = [snakePosition[0] + 10] + snakePosition


    if(move == 'U'):
            if(snakePosition[0]-10) < 0:
                collision = True
            else:
                snakePosition = [snakePosition[0] - 10] + snakePosition
    if(snakePosition[0] in game.getFood() ):
        game.setFood([])
    else:
        del snakePosition[-1]
    snake2.setPos(snakePosition)
    return collision

def checkCollisions(game):
    snake1 = game.getHostSnake()
    state  = game.getState()
    snake1Pos = snake1.getPos()
    if(state[snake1Pos[0]] == 1 ):
        return 1
    return 0

class snake:
    def __init__(self, position = [0]):
        self.snakeID    = creatSnakeID()
        self.position   = position
        self.move       = 'D'


    def getID(self):
        return self.snakeID

    def getLength(self):
        return len(self.position)

    def getMove(self):
        return self.move

    def setMove(self, move):
        self.move = move

    def getPos(self):
        return self.position

    def setPos(self,position):
        self.position = position

class game():
    def __init__(self):
        self.gameID = creatGameID()
        self.board = [-1] * 100
        self.snake1 = snake([12])
        self.snake2 = snake([67])
        self.board[22] = 1
        self.food = [45]
        self.ready = False
        self.running = False

    def getState(self):
        return self.board

    def setState(self,board):
        self.board = board

    def setReady(self,ready):
        self.ready = ready

    def getReady(self):
        return self.ready

    def getRunning(self):
        return self.running

    def setRunning(self,running):
        self.running = running

    def getFood(self):
        return self.food

    def setFood(self,food):
        self.food = food

    def getID(self):
        return self.gameID

    def getHostSnake(self):
        return self.snake1

    def getP2Snake(self):
        return self.snake2

    def getSnake1ID(self):
        return self.snake1.snakeID

    def getSnakeP2ID(self):
        return self.snake2.snakeID

    def checkWalls(self):
        return checkWalls(self)

    def checkCollisions(self):
        return 0

    def generateFood(self):
        return 0

class boardsss():
    def __int__(self):
        self.state = 0
    def getSate(self):
        print(self.state)