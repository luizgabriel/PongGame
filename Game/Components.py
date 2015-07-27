from Game.Math import Vector2d
import time
import threading

current_time = lambda: int(round(time.time() * 1000))


class Scene:

    difficulty = 1

    def __init__(self, canvas):
        self.canvas = canvas
        self.canvas.delete("all")
        self.initEntities()

    def initEntities(self):
        pass

    @staticmethod
    def call(canvas, scene):
        import Game.Kernel
        module = Game.Kernel.loadModule("Game.Scenes." + scene)
        classR = getattr(module, scene)
        return classR(canvas)

    def getApplication(self):
        return self.canvas.getFrame().getApplication()


class Entity:
    lastUpdateTime = current_time()

    def __init__(self, scene, id=None):
        self.id = id
        self.scene = scene
        self.screenWidth = self.getApplication().width
        self.screenHeight = self.getApplication().height
        threading._start_new_thread(Entity.update, (self,))

    def onUpdate(self, delta_time, after):
        after()

    def update(self):
        frame_rate = self.getApplication().frame_rate
        time_per_frame = 1000 / frame_rate
        delta_time = current_time() - self.lastUpdateTime
        if delta_time < 0: delta_time = 0
        self.getApplication().after(int(time_per_frame - delta_time), lambda: self.onUpdate(delta_time, self.update))
        self.lastUpdateTime = current_time()

    def bind(self, key, callback):
        self.getApplication().bind(key, callback)

    def getApplication(self):
        return self.scene.canvas.getFrame().getApplication()

    def getCanvas(self):
        return self.scene.canvas

    def move(self, position):
        self.getCanvas().move(self.id, position.x, position.y)

    def getPosition(self):
        return self.getCanvas().getPosition(self.id)


class Player(Entity):
    width = 20
    height = 80
    velocity = 0.3
    tag = "player"

    canMoveUp = False
    canMoveDown = False

    def __init__(self, scene):
        Entity.__init__(self, scene)
        self.id = self.getCanvas().create_rectangle(0, 0, self.width, self.height, fill='white', tags=self.tag)
        self.onInit()

    def onInit(self):
        pass

    def onUpdate(self, delta_time, after):

        if self.canMoveUp and self.getPosition().y >= 0:
            self.move(Vector2d(0, -self.velocity) * self.scene.difficulty * delta_time)
            self.getCanvas().debugDVector(self.getPosition(), tag=self.__class__.__name__)

        if self.canMoveDown and self.getPosition().y + self.height <= self.getApplication().height:
            self.move(Vector2d(0, self.velocity) * self.scene.difficulty * delta_time)
            self.getCanvas().debugDVector(self.getPosition(), tag=self.__class__.__name__)

        after()

    def inSight(self, ball):
        ballPosition = ball.getPosition()
        playerPosition = self.getPosition()
        return ballPosition.y + ball.size / 2 > playerPosition.y and ballPosition.y + ball.size / 2 < playerPosition.y + self.height

    def moveUpPress(self, event):
        self.canMoveUp = True

    def moveUpRelease(self, event):
        self.canMoveUp = False

    def moveDownPress(self, event):
        self.canMoveDown = True

    def moveDownRelease(self, event):
        self.canMoveDown = False
