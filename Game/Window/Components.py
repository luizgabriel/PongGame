from tkinter import Canvas, Frame
from Game.Components import Scene
import Game.Math

class GameCanvas(Canvas):

    def __init__(self, master):
        Canvas.__init__(self, master)
        self.initializeComponents()

    def initializeComponents(self):
        self.configure(width=self.getFrame().getApplication().width,
                       height=self.getFrame().getApplication().height,
                       bg='black',
                       bd=0,
                       highlightthickness=0,
                       relief='ridge')
        self.focus_set()
        self.scene = Scene.call(self, "MainScene")

    def getPosition(self, id):
        coords = self.coords(id)
        return Game.Math.Vector2d(coords[0], coords[1])

    def getFrame(self):
        return self.master

    def debugPoint(self, position, size = 7, duration = 5000):
        debugPointId = self.create_rectangle(position.x - size /2, position.y - size / 2, position.x + size / 2, position.y + size / 2, fill='red')
        self.getFrame().getApplication().after(duration, lambda : self.delete(debugPointId))

    debugPoints = {}
    def debugDPoint(self, position, size = 7, tag = 'default', color = 'red'):
        if self.getFrame().getApplication().canDebug:
            if tag in self.debugPoints:
                self.delete(self.debugPoints[tag])

            self.debugPoints[tag] = self.create_rectangle(position.x - size /2, position.y - size / 2, position.x + size / 2, position.y + size / 2, fill=color, tags=tag)

    debugVectors = {}
    def debugDVector(self, position, thickness = 1, tag = 'default', color = 'blue'):
        if self.getFrame().getApplication().canDebug:
            if tag in self.debugVectors:
                self.delete(self.debugVectors[tag])

            self.debugVectors[tag] = self.create_line(0, 0, position.x, position.y, arrow = 'last', width = thickness, dash=(5,3), fill=color, tags=tag)


class MainFrame(Frame):

    def __init__(self, master):
        Frame.__init__(self, master)
        self.initializeComponents()

    def initializeComponents(self):
        self.configure(width=self.master.width, height=self.master.height)
        self.canvas = GameCanvas(self)
        self.canvas.pack()

    def getApplication(self):
        return self.master