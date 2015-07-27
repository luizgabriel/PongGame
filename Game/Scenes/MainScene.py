from Game.Components import Scene, Player, Entity
from Game.Math import Vector2d

class MainScene(Scene):

    score1 = 0
    score2 = 0

    def initEntities(self):
        self.player1 = Player1(self)
        self.player2 = Player2(self)
        self.ball = Ball(self)

        self.divisor = self.canvas.create_line(self.getApplication().width / 2, 10, self.getApplication().width / 2,
                                               self.getApplication().height - 10, fill="white")
        self.score1Id = self.createScoreOne()
        self.score2Id = self.createScoreTwo()

        self.getApplication().after(5000, self.increaseDifficulty)

    def increaseDifficulty(self):
        self.difficulty += 0.2

    def addToScoreOne(self):
        self.score1 += 1
        self.canvas.delete(self.score1Id)
        self.score1Id = self.createScoreOne()

    def addToScoreTwo(self):
        self.score2 += 1
        self.canvas.delete(self.score2Id)
        self.score2Id = self.createScoreTwo()

    def createScoreOne(self):
        return self.canvas.create_text(self.getApplication().width / 2 - 30, 30, text=self.score1, font="Arial 30", fill='white')

    def createScoreTwo(self):
        return self.canvas.create_text(self.getApplication().width / 2 + 30, 30, text=self.score2, font="Arial 30", fill='white')

class Ball(Entity):
    size = 20
    velocity = 0.2
    directionRightDown = Vector2d(velocity, velocity)
    directionRightUp = Vector2d(velocity, -velocity)
    directionLeftDown = Vector2d(-velocity, velocity)
    directionLeftUp = Vector2d(-velocity, -velocity)
    curDirection = directionRightDown #Start Direction

    def __init__(self, scene):
        Entity.__init__(self, scene)
        self.id = self.getCanvas().create_oval(0, 0, self.size, self.size, fill='white')
        self.onInit()

    def onInit(self):
        self.startPositionLeft = Vector2d(6 + Player.width, (self.getApplication().height / 2) - (self.size / 2))
        self.startPositionRight = Vector2d(self.getApplication().width - (6 + Player.width), (self.getApplication().height / 2) - (self.size / 2))
        self.move(self.startPositionLeft)

    def onUpdate(self, delta_time, after):

        curPosition = self.getPosition()
        player1 = self.scene.player1
        player2 = self.scene.player2
        tolerance = 3

        #Scenary Bounds Detection
        if curPosition.y + self.size >= self.getApplication().height and self.curDirection == self.directionRightDown:
            self.getApplication().debug("BALL", curPosition, "dir = RIGHT")
            self.curDirection = self.directionRightUp

        if curPosition.y <= 0 and self.curDirection == self.directionRightUp:
            self.getApplication().debug("BALL", curPosition, "dir = RIGHT")
            self.curDirection = self.directionRightDown

        if curPosition.y + self.size >= self.getApplication().height and self.curDirection == self.directionLeftDown:
            self.getApplication().debug("BALL", curPosition, "dir = LEFT")
            self.curDirection = self.directionLeftUp

        if curPosition.y <= 0 and self.curDirection == self.directionLeftUp:
            self.getApplication().debug("BALL", curPosition, "dir = LEFT")
            self.curDirection = self.directionLeftDown

        #Colision Detection
        if abs(curPosition.x - (5 + player1.width)) <= tolerance and player1.inSight(self):
            if self.curDirection == self.directionLeftUp:
                self.curDirection = self.directionRightUp
            elif self.curDirection == self.directionLeftDown:
                self.curDirection = self.directionRightDown

        if abs(curPosition.x - (self.getApplication().width - (player2.width * 2))) <= tolerance and player2.inSight(self):
            if self.curDirection == self.directionRightUp:
                self.curDirection = self.directionLeftUp
            elif self.curDirection == self.directionRightDown:
                self.curDirection = self.directionLeftDown

        #Point Detection
        if curPosition.x < 0:
            self.onBallFeltToLeftSide()

        elif curPosition.x > self.getApplication().width:
            self.onBallFeltToRightSide()

        self.move(self.curDirection * self.scene.difficulty * delta_time)
        self.getCanvas().debugDVector(self.getPosition(), tag = self.__class__.__name__)
        after()

    def onBallFeltToLeftSide(self):
        self.scene.addToScoreOne()
        self.move(-self.getPosition() + self.startPositionRight)

    def onBallFeltToRightSide(self):
        self.scene.addToScoreTwo()
        self.move(-self.getPosition() + self.startPositionLeft)


class Player1(Player):
    def onInit(self):
        Player.onInit(self)
        startPosition = Vector2d(5, (self.getApplication().height / 2) - (self.height / 2))
        self.move(startPosition)
        self.bind("<KeyPress-w>", self.moveUpPress)
        self.bind("<KeyRelease-w>", self.moveUpRelease)
        self.bind("<KeyPress-s>", self.moveDownPress)
        self.bind("<KeyRelease-s>", self.moveDownRelease)


class Player2(Player):
    def onInit(self):
        Player.onInit(self)
        startPosition = Vector2d(self.getApplication().width - self.width - 5,
                                 (self.getApplication().height / 2) - (self.height / 2))
        self.move(startPosition)
        self.bind("<KeyPress-o>", self.moveUpPress)
        self.bind("<KeyRelease-o>", self.moveUpRelease)
        self.bind("<KeyPress-l>", self.moveDownPress)
        self.bind("<KeyRelease-l>", self.moveDownRelease)
