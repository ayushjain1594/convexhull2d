from tkinter import Tk, Canvas, Frame, BOTH
from convexhull import ConvexHull2D

class GUI(Frame):

	def __init__(self):
		super().__init__()

		self.canvas = self.initializeUserInterface()
		c = ConvexHull2D()
		c.generatePoints(50, (50, 700), (50, 450))
		#self.drawPoints(c.points, c.runJarvisAlgo())
		c.runJarvisAlgo(self)


	def initializeUserInterface(self):
		self.master.title("Lines")
		self.pack(fill=BOTH, expand=1)

		canvas = Canvas(self)
		#canvas.create_line(15, 25, 200, 25)
		#canvas.create_line(300, 35, 300, 200, dash=(4, 2))
		#canvas.create_line(55, 85, 155, 85, 105, 180, 55, 85)

		canvas.pack(fill=BOTH, expand=1)
		return canvas

	def drawPoints(self, points, hull_ind):
		for ind, point in enumerate(points):
			x1, y1 = (point[0] - 2), (point[1] - 2)
			x2, y2 = (point[0] + 2), (point[1] + 2)
			if ind in hull_ind:
				fill_col = "#008000"
			else:
				fill_col = "#000000"
			self.canvas.create_oval(
				x1, y1, x2, y2, fill=fill_col, width=2, outline=fill_col)
		'''
		if len(hull_ind) > 0:
			self.canvas.after(500, self.drawPoints, points, hull_ind[:-1])
		'''

def main():
	root = Tk()
	gui = GUI()
	root.geometry("750x500+300+300")
	root.mainloop()


if __name__ == '__main__':
	main()
