from tkinter import Tk, Canvas, Frame, BOTH
import threading
import time

from convexhull import ConvexHull2D

class GUI(Frame):

    def __init__(self, event, max_count=None):
        super().__init__()

        self.canvas = self.initializeUserInterface()

        self.cvxhull = ConvexHull2D()
        
        #c.generatePoints(10, (50, 700), (50, 450))
        #self.drawPoints(c.points, c.runJarvisAlgo())
        
        #result_j = self.cvxhull.runJarvisAlgo()
        #print(f"Jarvis: {result_j}")
        #result_g = self.cvxhull.runGrahamAlgo()
        #print(f"Graham: {result_g}")
        #self.drawPoints()

        #self.event = event
        self.max_count = max_count
        self.count = 0
        self.eventCheck()


    def initializeUserInterface(self):
        self.master.title("Convex Hull 2D")
        self.pack(fill=BOTH, expand=1)

        canvas = Canvas(self)
        #canvas.create_line(15, 25, 200, 25)
        #canvas.create_line(300, 35, 300, 200, dash=(4, 2))
        #canvas.create_line(55, 85, 155, 85, 105, 180, 55, 85)

        canvas.pack(fill=BOTH, expand=1)
        return canvas

    def drawPoints(self):
        self.cvxhull.generatePoints(10, (50, 700), (50, 450))
        jarvis_ind = self.cvxhull.runJarvisAlgo()
        graham_ind = self.cvxhull.runGrahamAlgo()
        points = self.cvxhull.points

        # clear canvas
        self.canvas.delete('all')
        for ind, point in enumerate(points):
            x1, y1 = (point[0] - 2), (point[1] - 2)
            x2, y2 = (point[0] + 2), (point[1] + 2)
            if ind in jarvis_ind:
                fill_col = "#008000"
            else:
                fill_col = "#000000"
            self.canvas.create_oval(
                x1, y1, x2, y2, fill=fill_col, width=2, outline=fill_col)
            self.canvas.create_text(
                x1, y1+12, text=str(ind)+str(point))

        for ind in graham_ind:
            x1, y1 = points[ind]

            outline_color = '#008000' if ind in jarvis_ind else '#ff0000'
            self.canvas.create_oval(
                x1-8, y1-8, x1+8, y1+8, 
                outline=outline_color, width=1
            )

        first_point = jarvis_ind[0]
        next_ind = 1
        while next_ind < len(jarvis_ind):
            x1, y1 = points[jarvis_ind[next_ind-1]]
            x2, y2 = points[jarvis_ind[next_ind]]
            self.canvas.create_line(x1, y1, x2, y2)
            next_ind += 1
        x1, y1 = points[jarvis_ind[next_ind-1]]
        x2, y2 = points[first_point]
        self.canvas.create_line(x1, y1, x2, y2)

        
    def eventCheck(self):
        #flag = self.event.is_set()

        #self.label['text'] = flag

        #if flag:
        #    self.drawPoints()
        #else:
        #    self.drawPoints()
        self.count += 1

        if self.max_count:
            if self.count > self.max_count:
                import sys
                sys.exit()

        self.drawPoints()

        self.master.after(4000, self.eventCheck)

def timingLoop(event):
    pass
    '''
    while True:
        event.set()
        time.sleep(2)
        event.clear()
        time.sleep(2)
    '''


def main():
    root = Tk()

    event = threading.Event()
    t = threading.Thread(target=timingLoop, args=(event,))
    t.daemon = True
    t.start()

    gui = GUI(event, 50)
    root.geometry("1250x900+300+300")
    root.mainloop()


if __name__ == '__main__':
    main()
