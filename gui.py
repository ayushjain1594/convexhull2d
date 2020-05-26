import tkinter as tk
import threading
import time

from convexhull import ConvexHull2D
from display import Display, DisplayJarvis, DisplayGraham

class GUI(tk.Frame):
    def __init__(self):
        self.root = tk.Tk()
        
        #super().__init__()
        self.master = self.root
        self.canvas = self.initializeUserInterface()
        
        self.setupCanvasObjectContainer()
        
        self.delay = 200 # in miliseconds
        self.cvx = ConvexHull2D(n=50, delay=self.delay,
            max_x=self.w-200, max_y=self.h-200)

        # varible used to prematurely stop algorithms
        self.killthread = False

        #self.executeJarvis()
        #self.executeGraham()
        self.root.mainloop()


    def setupCanvasObjectContainer(self):
        '''Method to setup container for 
        canvas elements 
        '''
        self.cvsobjects = {
            'points': {},
            'r_lines': {},
            'circles': {},
            'texts': {},
            'lines': {},
        }


    def clearCanvas(self):
        '''Method to clear canvas of any elements
        '''
        self.setupCanvasObjectContainer()
        self.canvas.delete('all')
        '''
        for objtype in self.cvsobjects.keys():
            for elementkey in self.cvsobjects[objtype].keys():
                self.canvas.delete(
                    self.cvsobjects[objtype][elementkey]
                )
        '''


    def generateNewPoints(self):
        '''Method to generate new points
        '''

        # clear all canvas
        self.clearCanvas()
        try:
            count = int(self.inputCount.get())
            self.cvx = ConvexHull2D(n=count, delay=self.delay,
                max_x=self.w-200, max_y=self.h-200)
        except ValueError:
            return

    def initializeUserInterface(self):
        '''
        self.master.title("Convex Hull 2D")
        self.pack(fill=tk.BOTH, expand=1)

        canvas = tk.Canvas(self)
        #canvas.grid(column=0, row=0,
        #    sticky=tk.W+tk.N)
        canvas.pack(fill=tk.BOTH, expand=1)
        '''
        self.w, self.h = self.root.winfo_screenwidth(), \
            self.root.winfo_screenheight()
        self.root.geometry("%dx%d+0+0" % (self.w, self.h))

        canvas = tk.Canvas(self.root, 
            width=self.w-200, height=self.h-200,
            borderwidth=2, relief='sunken')
        canvas.grid(column=0, row=0, 
            rowspan=10, sticky=tk.W)

        label = tk.Label(self.root, 
            text="ENTER COUNT \nOF POINTS \nTO RANDOMLY \nGENERATE")
        label.grid(column=1, row=0)

        self.inputCount = tk.StringVar()
        self.inputCount.set('50')
        entryPointCount = tk.Entry(self.root, 
            textvariable=self.inputCount)
        entryPointCount.grid(column=1, row=1,
            sticky=tk.W+tk.E)

        buttonSubmitInput = tk.Button(self.root,
            text='Generate New Points', 
            command=self.generateNewPoints)
        buttonSubmitInput.grid(column=1, row=2,
            rowspan=1,
            sticky=tk.W+tk.N+tk.E+tk.S)

        buttonDispAll = tk.Button(self.root,
            text='Display All Points',
            command=self.displayPoints)
        buttonDispAll.grid(column=1, row=3,
            rowspan=1, 
            sticky=tk.W+tk.N+tk.E+tk.S)

        buttonExJarvis = tk.Button(self.root,
            text='Execute Jarvis',
            command=self.executeJarvis)
        buttonExJarvis.grid(column=1, row=4,
            rowspan=1, 
            sticky=tk.W+tk.N+tk.E+tk.S)

        buttonExGraham = tk.Button(self.root,
            text='Execute Graham',
            command=self.executeGraham)
        buttonExGraham.grid(column=1, row=5,
            rowspan=1, 
            sticky=tk.W+tk.N+tk.E+tk.S)

        buttonStopAlgo = tk.Button(self.root,
            text='Stop Algorithm',
            command=self.interruptAlgorithm)
        buttonStopAlgo.grid(column=1,row=6,
            rowspan=1,
            sticky=tk.W+tk.N+tk.E+tk.S)

        return canvas


    def displayPoints(self):
        if isinstance(self.cvx, ConvexHull2D):   
            display = Display(self)
            display.displayAllPoints()
            del display


    def interruptAlgorithm(self):
        '''Method to kill thread running 
        algorithms prematurely
        '''
        self.killthread = True


    def updateCanvas(self, display, algo='jarvis'):
        start = time.time()
        if self.killthread:
            
            self.cvx.stopalgo = True
            self.clearCanvas()
            return

        if algo == 'jarvis':

            display.displayJarvis()
            if not self.threadjarvis.isAlive():
                # thread is no longer alive
                display.postAlgorithmStep()
                return

        elif algo == 'graham':

            display.displayGraham()
            
            if not self.threadgraham.isAlive():
                #self.postGrahamStep()
                display.postAlgorithmStep()
                return

        delta = time.time() - start
        if delta > self.delay/1000:
            print(delta)

        self.master.after(self.delay, 
            self.updateCanvas, display, algo
        )



    def executeJarvis(self):
        self.clearCanvas()
        display = DisplayJarvis(self)

        # if previously set True, set False
        self.killthread = False

        # create a thread for jarvis
        self.threadjarvis = threading.Thread(
            target=self.cvx.runJarvis,
            args=(True,)
        )
        self.threadjarvis.daemon = True
        self.threadjarvis.start()
        
        # allowing jarvis to be setup
        time.sleep(0.005)
        
        # call to update canvas
        self.updateCanvas(display, algo='jarvis')



    def executeGraham(self):
        self.clearCanvas()
        display = DisplayGraham(self)
        
        # if previously set True, set False
        self.killthread = False

        # create thread for Graham
        self.threadgraham = threading.Thread(
            target=self.cvx.runGraham,
            args=(True,)
        )
        self.threadgraham.daemon = True
        self.threadgraham.start()

        # allowing graham to be setup
        time.sleep(0.005)

        #call to update canvas
        self.updateCanvas(display, algo='graham')




if __name__ == '__main__':
    
    gui = GUI()