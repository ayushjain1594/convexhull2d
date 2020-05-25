from tkinter import Tk, Canvas, Frame, BOTH, Button
import threading
import time

from convexhull import ConvexHull2D

class GUI(Frame):
    def __init__(self):
        super().__init__()

        self.canvas = self.initializeUserInterface()
        self.cvsobjects = {
            'points': {},
            'r_lines': {},
            'circles': {},
            'texts': {},
            'lines': {},
        }
        
        self.delay = 200 # in miliseconds
        self.cvx = ConvexHull2D(n=50, delay=self.delay)

        #self.executeJarvis()
        self.executeGraham()


    def initializeUserInterface(self):
        self.master.title("Convex Hull 2D")
        self.pack(fill=BOTH, expand=1)

        canvas = Canvas(self)

        canvas.pack(fill=BOTH, expand=1)
        return canvas


    def updateCanvas(self, display, algo='jarvis'):
        start = time.time()
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
        from display import Display
        from display import DisplayJarvis
        display = DisplayJarvis(self)

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
        from display import DisplayGraham
        display = DisplayGraham(self)
        
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



def main():
    root = Tk()
    gui = GUI()
    
    w, h = root.winfo_screenwidth(), root.winfo_screenheight()
    root.geometry("%dx%d" % (w, h))
    
    root.mainloop()

if __name__ == '__main__':
    main()