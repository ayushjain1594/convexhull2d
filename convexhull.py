import random
import time
import threading

class ConvexHull2D:
	def __init__(self, n=None, points=None, delay=500,
		max_x=1250, max_y=900):
		self.count = 0
		if n:
			self.generatePoints(n, (50, max_x-50), (50, max_y-50))
			if n < 15:
				print(self.points)
		if points:
			self.points = points
			self.n = len(points)
		
		if delay:
			self.delayinsec = (delay-1)/1000


	def generatePoints(self, n_points, x_range=(50, 1200), y_range=(50, 850)):
		if n_points < 3:
			print("Minimum 3 points required.. Replacing n with 3")
			n_points = 3

		self.n = n_points

		self.points = [
			(random.randint(*x_range), random.randint(*y_range))
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
			Negative val = clockwise rotation from pq to pr
			Positve val = anticlockwise rotation from pq to pr
			Zero val = pq and pr are colinear
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


	def setupAlgoState(self):
		self.algo = {
			'ind_leftMostPoint': None,
			'ind_p': None,
			'ind_q': None,
			'ind_r': None,
			'result_hull': [],
		}
		self.stopalgo = False



	def runJarvis(self, trackstatus=False):
		if trackstatus:
			self.setupAlgoState()

		ind_leftMostPoint = self.findLeftMostPoint()
		ind_p = ind_leftMostPoint
		result_hull = [ind_p]
		
		if trackstatus:
			self.algo['ind_leftMostPoint'] = ind_leftMostPoint
			self.algo['ind_p'] = ind_p
			self.algo['result_hull'].append(ind_p)
			
		while (True):

			ind_q = (ind_p + 1) % self.n
			if trackstatus:
				self.algo['ind_q'] = ind_q

			for ind_r, point_r in enumerate(self.points):
				if trackstatus:
					
					if self.stopalgo:
						# check if a stop request is received
						return result_hull

					time.sleep(self.delayinsec)
					self.algo['ind_r'] = ind_r

				if ind_r == ind_q:
					continue

				orientation = self.orientation(ind_p, ind_q, ind_r)
				if orientation < 0:
					ind_q = ind_r
					if trackstatus:
						self.algo['ind_q'] = ind_q

				if orientation == 0:
					# for overlapping vectors, pick the farther point
					if self.squareDistance(ind_p, ind_r) > \
					self.squareDistance(ind_p, ind_q):
						ind_q = ind_r
						if trackstatus:
							self.algo['ind_q'] = ind_q
			ind_p = ind_q
			if trackstatus:
				self.algo['ind_p'] = ind_q

			if ind_p == ind_leftMostPoint:
				break

			result_hull.append(ind_p)
			if trackstatus:
				self.algo['result_hull'].append(ind_p)

		if not trackstatus:
			return result_hull
		else:
			return


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
				left_arr[i], right_arr[j], False) > 0:
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


	def runGraham(self, trackstatus=False):
		""" Graham's Scan Algorithm """
		
		if trackstatus:
			self.setupAlgoState()

		# find the left most point
		ind_leftMostPoint = self.findLeftMostPoint()

		# sort points around left most point in
		# anticlockwise order
		sorted_points = [self.points[ind_leftMostPoint]] \
			+ self.sortPointsAround(ind_leftMostPoint)

		# mapping of index of a point in sorted_points array to
		# index of the same point in original array of points
		# Assuming no degeneracy in terms of duplicate points
		index_match = {
			sorted_points[i]: self.points.index(sorted_points[i])
			for i in range(len(sorted_points))
		}

		# result contains indices of sorted_points
		result_hull = sorted_points[:3]

		if trackstatus:
			self.algo['result_hull'] = \
				[index_match.get(sorted_points[i])
				for i in range(3)]

		if len(sorted_points) > 3:
			p, q, r = sorted_points[1:4]
			ind_r = 3

			if trackstatus:
				self.algo['ind_p'] = index_match.get(p)
				self.algo['ind_q'] = index_match.get(q)
				self.algo['ind_r'] = index_match.get(r)

			while (ind_r < len(sorted_points)):
				
				if trackstatus:
					if self.stopalgo:
						# check if a stop request is received
						return result_hull

					time.sleep(self.delayinsec)

				orient = self.orientation(p, q, r, False)
				
				if orient > 0:
					# move forward
					result_hull.append(r)

					if trackstatus:
						self.algo['result_hull'].append(
							index_match.get(r)
						)

					p = q
					q = r
					ind_r = ind_r + 1

					if ind_r == len(sorted_points):
						break
					r = sorted_points[ind_r]

					if trackstatus:
						self.algo['ind_p'] = index_match.get(p)
						self.algo['ind_q'] = index_match.get(q)
						self.algo['ind_r'] = index_match.get(r)
					
				else:
					# remove the last point from result
					result_hull.pop()
					p, q = result_hull[-2:]

					if trackstatus:
						self.algo['result_hull'].pop()
						self.algo['ind_p'] = index_match.get(p)
						self.algo['ind_q'] = index_match.get(q)
		
		if not trackstatus:
			return [index_match.get(point) for point in result_hull]
		else:
			return


	def runChanAlgo(self):
		""" 
		Chan's Divide and Conquer Algo
		to find convex hull
		"""
		m = 4 # Must be at least 4

		# number of subsets to be created
		num_subsets = int(self.n/m)

		# List of list holding subsets of all points
		subsets = []
		i = 0
		for i in range(1, num_subsets):
			subsets.append(self.points[(i-1)*4:i*4])
		subsets.append(self.points[i*4:])

		# List of result points from running Graham on
		# all subsets
		cvxhull_subsets = []
		for subset in subsets:
			sub_cvx = ConvexHull2D(points=subset)
			for ind in sub_cvx.runGraham():
				cvxhull_subsets.append(subset[ind])
			del sub_cvx

		# Run jarvis on Graham result of subsets
		sub_cvx = ConvexHull2D(points=cvxhull_subsets)

		# Return result in original indices
		return [self.points.index(cvxhull_subsets[ind]) 
			for ind in sub_cvx.runJarvis()]


	def createHull(self, algo='jarvis'):
		""""""
		if algo == 'jarvis':
			return self.runJarvis()
		return []


def test(n=300):
	c = ConvexHull2D(n=300,
		#points=[(1, 1), (2, 5), (2, 3), (3, 3)]
	)

	ind_left = c.findLeftMostPoint()
	sorted_points = c.sortPointsAround(ind_left)
	"""
	for ind, point in enumerate(sorted_points[:-1]):
		args = (c.points[ind_left], sorted_points[ind], sorted_points[ind+1])
		print(*args,
			c.orientation(*args, False))
	"""

	jarvis_result = c.runJarvis()
	print("Jarvis: ", jarvis_result)

	graham_result = c.runGraham()
	print("Graham: ", graham_result)

	chan_result = c.runChanAlgo()
	print("Chan: ", chan_result)

	if jarvis_result != graham_result:
		c.runGraham(detail=True)

	print('\n\n')

if __name__ == '__main__':
	test()

	