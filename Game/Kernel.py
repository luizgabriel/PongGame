from tkinter import *
from Game.Window.Components import MainFrame


def loadModule(name):
    mod = __import__(name)
    components = name.split('.')
    for comp in components[1:]:
        mod = getattr(mod, comp)
    return mod


class Application(Tk):
    width = 800
    height = 600
    frame_rate = 60  # fps
    canDebug = False

    def __init__(self):
        Tk.__init__(self)
        self.initializeComponents()

    def debug(self, tag, *args):
        if self.canDebug:
            args_string = ''.join(str(e) + ', ' for e in args)
            args_string = args_string[0:len(args_string) - 2]
            print("[%s] %s" % (tag, args_string))

    def initializeComponents(self):
        self.title("Pong Game")
        self.configure(width=self.width, height=self.height)

        self.mainFrame = MainFrame(self)
        self.mainFrame.pack()


    def run(self):
        self.mainloop()
