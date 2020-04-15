import random

class ConvexHull2D:
	def __init__(self, n=None):
		self.count = 0
		if n:
			self.generatePoints(n)
			print(self.points)

	def generatePoints(self, n_points, xrange=(0, 50), yrange=(0, 50)):
		if n_points < 3:
			print("Minimum 3 points required.. Replacing n with 3")
			n_points = 3

		self.n = n_points

		self.points = [
			(random.randint(*xrange), random.randint(*yrange))
			for _ in range(self.n)]


	def squareDistance(self, ind_p, ind_q):
		try:
			x1, y1 = self.points[ind_p]
			x2, y2 = self.points[ind_q]
		except IndexError:
			return 0
		return (x1 - x2)**2 + (y1 - y2)**2


	def orientation(self, p, q, r, as_index=True):
		""" Calculate and return orientation
			either based on indices or generic 
			2D points
		args - 
			p, q, r: int or tuple/list
				indices of 2D points p, q, r or
				the points itself if as_index is False
			as_index: Bool
				Boolean the type of input - indices
				or points
		return - 
			type: numeric (float/int)
		"""
		try:
			if as_index:
				px, py = self.points[p]
				qx, qy = self.points[q]
				rx, ry = self.points[r]
			else:
				px, py = p
				qx, qy = q
				rx, ry = r
		except IndexError:
			print("Invalid indices provided")
			return 0
		except (ValueError, TypeError):
			print("Invalid points provided")
			return 0
		return (qy - py)*(rx - qx) - (ry - qy)*(qx - px)


	def findLeftMostPoint(self):
		""" Finds left most point 
			among all points
			return : int
				index of left most point
		"""
		ind_leftMostPoint = None
		x_min = 999999999
		for ind, point in enumerate(self.points):
			point_x, point_y = point
			if point_x < x_min:
				x_min = point_x
				ind_leftMostPoint = ind
		return ind_leftMostPoint

	def runJarvisAlgo(self):
		""" Jarvis Algorithm """

		ind_leftMostPoint = self.findLeftMostPoint()

		ind_p = ind_leftMostPoint

		result_hull = [ind_p]


		while (True):
			ind_q = (ind_p + 1) % self.n

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

	def sortPointsAround(self, pivot_ind, points_override=None):
		"""
		Sort points around pivot point
		in anticlockwise direction such that
		orientation(pivot, i, i+1) > 0 for 
		every consecutive points

		Sorting using mergesort, O(nlogn)
		args - 
			pivot_ind: int
				index of pivot point
			points_override: None or list of tuple
				if not None, use these points instead
		return - 
			sorted_points: list of tuples
		"""
		if points_override:
			points = points_override
		else:
			points = [self.points[ind] 
				for ind in range(self.n)
				if ind != pivot_ind]
		self.count += 1
		if len(points) > 1:
			mid = len(points)//2
			left_arr = points[:mid]
			right_arr = points[mid:]
			left_arr = self.sortPointsAround(pivot_ind, left_arr)
			right_arr = self.sortPointsAround(pivot_ind, right_arr)

			i, j, k = 0, 0, 0
			while i < len(left_arr) and j < len(right_arr):
				if self.orientation(
				self.points[pivot_ind],
				left_arr[i], right_arr[j], False) < 0:
					points[k] = left_arr[i]
					i += 1
					k += 1
				else:
					points[k] = right_arr[j]
					j += 1
					k += 1

			while i < len(left_arr):
				points[k] = left_arr[i]
				i += 1
				k += 1

			while j < len(right_arr):
				points[k] = right_arr[j]
				j += 1
				k += 1

		return points


	def runGrahamAlgo(self, detail=False):
		""" Graham's Scan Algorithm """
		
		# find the left most point
		ind_leftMostPoint = self.findLeftMostPoint()

		# sort points around left most point in
		# anticlockwise order
		sorted_points = [self.points[ind_leftMostPoint]] \
			+ self.sortPointsAround(ind_leftMostPoint)

		# result contains indices of sorted_points
		result_hull = [0, 1, 2]

		p, q, r = 1, 2, 3
		while (r < len(sorted_points)):
			if detail:
				print(f'p = {p} q = {q} r = {r}, result_hull = {[self.points.index(sorted_points[ind]) for ind in result_hull]}')
				num = input('Continue ?')
			orient = self.orientation(
				sorted_points[p], 
				sorted_points[q],
				sorted_points[r], False)
			if detail:
				print(orient)
			if orient < 0:
				# move forward
				result_hull.append(r)
				p = q
				q = r
				r = r + 1

			else:
				# remove the last point from result
				result_hull = result_hull[:-1]
				q = p
				p = p - 1
		
		return [self.points.index(sorted_points[ind])
			for ind in result_hull]


	def createHull(self, algo='jarvis'):
		""""""
		if algo == 'jarvis':
			return self.runJarvisAlgo()
		return []

def test(n=10):
	c = ConvexHull2D(n)

	ind_left = c.findLeftMostPoint()
	sorted_points = c.sortPointsAround(ind_left)
	for ind, point in enumerate(sorted_points[:-1]):
		args = (c.points[ind_left], sorted_points[ind], sorted_points[ind+1])
		print(*args,
			c.orientation(*args, False))

	jarvis_result = c.runJarvisAlgo()
	print("Jarvis: ", jarvis_result)

	graham_result = c.runGrahamAlgo()
	print("Graham: ", graham_result)

	if jarvis_result != graham_result:
		c.runGrahamAlgo(detail=True)

	print('\n\n')

if __name__ == '__main__':
	test()
	