from tkinter import Tk, Canvas, Frame, BOTH
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
        self.cvx = ConvexHull2D(n=100, delay=self.delay)
        self.displayInitialPoints()

        self.callJarvisAlgorithm()
        #self.callGrahamAlgorithm()


    def initializeUserInterface(self):
        self.master.title("Convex Hull 2D")
        self.pack(fill=BOTH, expand=1)

        canvas = Canvas(self)

        canvas.pack(fill=BOTH, expand=1)
        return canvas

    def displayInitialPoints(self):
        for ind, point in enumerate(self.cvx.points):
            x1, y1 = point
            x1, y1 = x1 - 2, y1 -2
            x2, y2 = point
            x2, y2 = x2 + 2, y2 + 2

            self.cvsobjects['points'][ind] = \
                self.canvas.create_oval(x1, y1, x2, y2, 
                    fill="#000000", width=2, outline="#000000"
                )

    def preJarvisGrahamStep(self):
        # GUI variables to track changes in algorithm params
        self.ind_p = None
        self.ind_q = None
        self.ind_r = None
        self.result_len = 0
        self.resultTupList = []
        self.firstRun = True
        self.counter = 0

    def displayJarvis(self):
        """ UPDATES CANVAS OBJECTS SHOWING JARVIS STEPS"""
        try:
            ind_p = self.cvx.algo['ind_p']
            ind_q = self.cvx.algo['ind_q']
            ind_r = self.cvx.algo['ind_r']

            result = self.cvx.algo['result_hull']

            try:
                if ind_p != self.ind_p:
                    # change in point p
                    if self.cvsobjects['texts'].get('p', 'NA') != 'NA':
                        self.canvas.delete(
                            self.cvsobjects['texts']['p']
                        )
                        
                    x, y = self.cvx.points[ind_p]
                    self.cvsobjects['texts']['p'] = self.canvas.create_text(
                        x, y+12, text='p '+str(ind_p))
                    self.ind_p = ind_p

                    if self.cvsobjects['lines'].get('pq', 'NA') != 'NA':
                        self.canvas.delete(self.cvsobjects['lines']['pq'])
                    if True or self.ind_q:
                        q_x, q_y = self.cvx.points[self.ind_q]
                        self.cvsobjects['lines']['pq'] = self.canvas.create_line(
                            x, y, q_x, q_y, width=3)

            except IndexError:
                print('IndexError occured updating p')
            except KeyError:
                print('KeyError occured updating p')
            except TypeError:
                print('TypeError occured updating p')

            try:
                if ind_q != self.ind_q:
                    # change in point q
                    if self.cvsobjects['texts'].get('q', 'NA') != 'NA':
                        self.canvas.delete(self.cvsobjects['texts']['q'])
                        
                    x, y = self.cvx.points[ind_q]
                    self.cvsobjects['texts']['q'] = self.canvas.create_text(
                        x, y+12, text='q '+str(ind_q))
                    self.ind_q = ind_q

                    if self.cvsobjects['lines'].get('pq', 'NA') != 'NA':
                        self.canvas.delete(self.cvsobjects['lines']['pq'])
                    if True or self.ind_p:
                        p_x, p_y = self.cvx.points[self.ind_p]
                        self.cvsobjects['lines']['pq'] = self.canvas.create_line(
                            p_x, p_y, x, y, width=3)
                    if self.cvsobjects['lines'].get('qr', 'NA') != 'NA':
                        self.canvas.delete(self.cvsobjects['lines']['qr'])
                    if True or self.ind_r:
                        r_x, r_y = self.cvx.points[self.ind_r]
                        self.cvsobjects['lines']['qr'] = self.canvas.create_line(
                            x, y, r_x, r_y, width=3)

            except IndexError:
                print('IndexError occured updating q')
            except KeyError:
                print('KeyError occured updating q')
            except TypeError:
                print('TypeError occured updating q')

            try:
                if ind_r != self.ind_r:
                    # Change in point r
                    if self.cvsobjects['texts'].get('r', 'NA') != 'NA':
                        self.canvas.delete(self.cvsobjects['texts']['r'])
                        
                    x, y = self.cvx.points[ind_r]
                    self.cvsobjects['texts']['r'] = self.canvas.create_text(
                        x, y+12, text='r '+str(ind_r))
                    self.ind_r = ind_r

                    if self.cvsobjects['lines'].get('qr', 'NA') != 'NA':
                        self.canvas.delete(self.cvsobjects['lines']['qr'])
                    if True or self.ind_q:
                        q_x, q_y = self.cvx.points[self.ind_q]
                        self.cvsobjects['lines']['qr'] = self.canvas.create_line(
                            q_x, q_y, x, y, width=3)

            except IndexError:
                print('IndexError occured updating r')
            except KeyError:
                print('KeyError occured updating r')
            except TypeError:
                print('TypeError occured updating r')

            if len(result) > 1:
                # if there are tentative result indices
                if self.cvsobjects['r_lines'].get(tuple(result[-2:]), None):
                    pass
                else:
                    x1, y1 = self.cvx.points[result[-2]]
                    x2, y2 = self.cvx.points[result[-1]]
                    self.cvsobjects['r_lines'][tuple(result[-2:])] = \
                        self.canvas.create_line(x1, y1, x2, y2, width=3)
        except AttributeError:
            pass
        #self.counter += 1
        #print('\t', self.counter)
        
    def postJarvisStep(self):
        """Method called when jarvis algorithm reach termination"""

        # Clear texts and intermediate jarvis step lines
        for key in self.cvsobjects['lines'].keys():
            self.canvas.delete(self.cvsobjects['lines'][key])
        for key in self.cvsobjects['texts'].keys():
            self.canvas.delete(self.cvsobjects['texts'][key])

        # Create final leg of results - joining last ind of result to first
        last_ind = self.cvx.algo['result_hull'][-1]
        first_ind = self.cvx.algo['result_hull'][0]
        x1, y1 = self.cvx.points[last_ind]
        x2, y2 = self.cvx.points[first_ind]
        self.cvsobjects['r_lines'][(last_ind, first_ind)] = \
            self.canvas.create_line(x1, y1, x2, y2, width=3)


    def displayGraham(self):
        try:
            ind_p = self.cvx.algo['ind_p']
            ind_q = self.cvx.algo['ind_q']
            ind_r = self.cvx.algo['ind_r']

            result = self.cvx.algo['result_hull']
            print(ind_p, ind_q, ind_r, result)

            if ind_p != self.ind_p:
                # change in point p
                if self.cvsobjects['texts'].get('p', 'NA') != 'NA':
                    self.canvas.delete(
                        self.cvsobjects['texts']['p']
                    )
                    
                x, y = self.cvx.points[ind_p]
                self.cvsobjects['texts']['p'] = self.canvas.create_text(
                    x, y+12, text='p '+str(ind_p))
                self.ind_p = ind_p

            if ind_q != self.ind_q:
                # change in point q
                if self.cvsobjects['texts'].get('q', 'NA') != 'NA':
                    self.canvas.delete(
                        self.cvsobjects['texts']['q']
                    )
                x, y = self.cvx.points[ind_q]
                self.cvsobjects['texts']['q'] = self.canvas.create_text(
                    x, y+12, text='q '+str(ind_q))
                self.ind_q = ind_q

            if ind_r != self.ind_r:
                # change in point r
                if self.cvsobjects['texts'].get('r', 'NA') != 'NA':
                    self.canvas.delete(
                        self.cvsobjects['texts']['r']
                    )
                x, y = self.cvx.points[ind_r]
                self.cvsobjects['texts']['r'] = self.canvas.create_text(
                    x, y+12, text='r '+str(ind_r))
                self.ind_r = ind_r

            if len(result) > 1:
                if self.firstRun:
                    for ind in range(len(result)-1):
                        x1, y1 = self.cvx.points[result[ind]]
                        x2, y2 = self.cvx.points[result[ind+1]]
                        self.cvsobjects['r_lines'][tuple(result[ind:ind+2])] = \
                            self.canvas.create_line(x1, y1, x2, y2, width=3)
                        self.resultTupList.append(tuple(result[ind:ind+2]))
                    self.result_len = len(result)
                    self.firstRun = False

                if len(result) > self.result_len:
                    # if there are tentative result indices
                    if self.cvsobjects['r_lines'].get(tuple(result[-2:]), None):
                        pass
                    else:
                        x1, y1 = self.cvx.points[result[-2]]
                        x2, y2 = self.cvx.points[result[-1]]
                        self.cvsobjects['r_lines'][tuple(result[-2:])] = \
                            self.canvas.create_line(x1, y1, x2, y2, width=3)
                        self.resultTupList.append(tuple(result[-2:]))
                    self.result_len = len(result)

            if len(result) < self.result_len:
                lastResultTup = self.resultTupList.pop()
                if self.cvsobjects['r_lines'].get(lastResultTup, None):
                    self.canvas.delete(
                        self.cvsobjects['r_lines'][lastResultTup]
                    )
                self.result_len = len(result)
                        
        except AttributeError:
            print("AttributeError")
        except IndexError:
            print("IndexError")
        except KeyError:
            print("KeyError")
        except TypeError:
            print("TypeError")


    def postGrahamStep(self):
        for key in self.cvsobjects['lines'].keys():
            self.canvas.delete(self.cvsobjects['lines'][key])
        for key in self.cvsobjects['texts'].keys():
            self.canvas.delete(self.cvsobjects['texts'][key])

        last_ind = self.cvx.algo['result_hull'][-1]
        first_ind = self.cvx.algo['result_hull'][0]
        x1, y1 = self.cvx.points[last_ind]
        x2, y2 = self.cvx.points[first_ind]
        self.cvsobjects['r_lines'][(last_ind, first_ind)] = \
            self.canvas.create_line(x1, y1, x2, y2, width=3)


    def updateCanvas(self, algo='jarvis'):
        start = time.time()
        if algo == 'jarvis':
            self.displayJarvis()
            if not self.threadjarvis.isAlive():
                self.postJarvisStep()
                return

        elif algo == 'graham':
            # setup code for updates in graham
            
            self.displayGraham()
            
            if not self.threadgraham.isAlive():
                self.postGrahamStep()
                return
        delta = time.time() - start
        if delta > self.delay/1000:
            print(delta)

        self.master.after(self.delay, 
            self.updateCanvas, algo
        )


    def callJarvisAlgorithm(self):
        self.preJarvisGrahamStep()

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
        self.updateCanvas(algo='jarvis')


    def callGrahamAlgorithm(self):
        self.preJarvisGrahamStep()

        self.threadgraham = threading.Thread(
            target=self.cvx.runGraham,
            args=(True,)
        )
        self.threadgraham.daemon = True
        self.threadgraham.start()

        # allowing graham to be setup
        time.sleep(0.005)

        #call to update canvas
        self.updateCanvas(algo='graham')


def main():
    root = Tk()
    gui = GUI()
    root.geometry("1250x900+300+300")
    root.mainloop()

if __name__ == '__main__':
    main()