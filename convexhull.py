import random

class ConvexHull2D:
	def __init__(self):
		pass

	def generatePoints(self, n_points, xrange=(0, 50), yrange=(0, 50)):
		if n_points < 3:
			print("Minimum 3 points required.. Replacing n with 3")
			n_points = 3

		self.points = [
			(random.randint(*xrange), random.randint(*yrange))
			for _ in range(n_points)]


	def squareDistance(self, ind_p, ind_q):
		try:
			x1, y1 = self.points[ind_p]
			x2, y2 = self.points[ind_q]
		except IndexError:
			return 0
		return (x1 - x2)**2 + (y1 - y2)**2


	def orientation(self, ind_p, ind_q, ind_r):
		""" Calculate and return orientation
		: param p/q/r: tuple/list of length 2 with num
			numeric argument
		: return : float/int
		"""
		try:
			px, py = self.points[ind_p]
			qx, qy = self.points[ind_q]
			rx, ry = self.points[ind_r]
		except IndexError:
			print("Invalid indices provided")
			return 0
		return (qy - py)*(rx - qx) - (ry - qy)*(qx - px)


	def createHull(self, algo='jarvis'):
		""""""
		if algo == 'jarvis':
			return self.runJarvisAlgo()
		return []


	def runJarvisAlgo(self):
		""" Jarvis Algorithm """

		ind_leftMostPoint = None
		x_min = 999999999
		for ind, point in enumerate(self.points):
			point_x, point_y = point
			if point_x < x_min:
				x_min = point_x
				ind_leftMostPoint = ind

		ind_p = ind_leftMostPoint

		result_hull = [ind_p]


		while (True):
			ind_q = (ind_p + 1) % len(self.points)

			for ind_r, point_r in enumerate(self.points):
				if ind_r == ind_q:
					continue

				orientation = self.orientation(ind_p, ind_q, ind_r)
				if orientation > 0:
					ind_q = ind_r
				if orientation == 0:
					# for overlapping vectors, pick the farther point
					if self.squareDistance(ind_p, ind_r) > \
					self.squareDistance(ind_p, ind_q):
						ind_q = ind_r

			ind_p = ind_q

			if ind_p == ind_leftMostPoint:
				break

			result_hull.append(ind_p)

		return result_hull


if __name__ == '__main__':
	c = ConvexHull2D()
	c.generatePoints(20)
	print([c.points[ind] for ind in c.runJarvisAlgo()])
	