class Display():
	""" Class to track algorithm progress and display on canvas """

	def __init__(self, gui):
		self.gui = gui
		self.pointcolor = "#000000"


	def displayAllPoints(self):
		'''Method to initially display all points on canvas'''
		for ind, point in enumerate(self.gui.cvx.points):
			# creating circle of diameter 4
			x1, y1 = point
			x1, y1 = x1 - 2, y1 -2
			x2, y2 = point
			x2, y2 = x2 + 2, y2 + 2

			self.createElement('points', ind, 
				x1, y1, x2, y2, 
				fill=self.pointcolor,
				width=2, 
				outline=self.pointcolor
			)


	def preAlgorithmDisplaySetup(self):
		'''Method to setup variables tracking progress''' 
		self.ind_p = None
		self.ind_q = None
		self.ind_r = None
		self.result_len = 0
		self.resultTupList = []
		self.firstRun = True
		self.counter = 0


	def deleteElement(self, elementtype, key):
		'''Method to delete elements from canvas
		param:
			elementtype: str
				This has to be one of the keys 
				of cvsobjects of class GUI.
			key: int/tuple/str
				Depending on the element type,
				this is a unique key to identify
				elements created on canvas
		'''
		try:
			if self.gui.cvsobjects[elementtype].get(key, None):
				self.gui.canvas.delete(
					self.gui.cvsobjects[elementtype][key]
				)
		except KeyError:
			print("Invalid key or element type")
			pass
		except AttributeError:
			print("Possibly missing attribute in GUI object")
			pass


	def createElement(self, elementtype, key, *args, **kwargs):
		'''Method to create elements on canvas
		param:
			elementtype, key : same as method deleteElement
			*args, **kwargs: arguments to be passed in respective
			methods of class Canvas
		'''
		try:
			if elementtype == 'lines' or elementtype == 'r_lines':
				self.gui.cvsobjects[elementtype][key] = \
					self.gui.canvas.create_line(*args, **kwargs)

			elif elementtype == 'texts':
				self.gui.cvsobjects[elementtype][key] = \
					self.gui.canvas.create_text(*args, **kwargs)

			elif elementtype == 'points':
				self.gui.cvsobjects[elementtype][key] = \
					self.gui.canvas.create_oval(*args, **kwargs)

		except KeyError:
			print("Invalid element type")


	def updatePoint(self, ind, point='p', updateLines=True):
		'''Method to update points identifying current state of
		algorithm
		param:
			ind: int
				This has to be an index of points of 
				ConvexHull2D object
			point: str
				Unique identifier for state of algorithm.
				Can only be p/q/r
			updateLines: bool
				If true, canvas will update and display 
				tentative lines between pq and qr.
		'''
		# delete old point text if exists
		self.deleteElement('texts', point)

		# get new point coordinates and create new text
		x, y = self.gui.cvx.points[ind]
		self.createElement('texts', point, 
			x, y+12, text=point+' '+str(ind)
		)
		
		if updateLines:
			if point == 'p':
				# Only pq needs to be updated
				# delete previous pq
				self.deleteElement('lines', 'pq')

				if self.ind_q:
					# point q exists, create new pq
					q_x, q_y = self.gui.cvx.points[self.ind_q]
					self.createElement('lines', 'pq', 
						x, y, q_x, q_y, width=3
					)

			if point == 'q':
				# Both pq and qr needs to be updated
				self.deleteElement('lines', 'pq')

				if self.ind_p:
					# point p exists, create new pq
					p_x, p_y = self.gui.cvx.points[self.ind_p]
					self.createElement('lines', 'pq', 
						p_x, p_y, x, y, width=3
					)

				self.deleteElement('lines', 'qr')

				if self.ind_r:
					# point r exists, create new qr
					r_x, r_y = self.gui.cvx.points[self.ind_r]
					self.createElement('lines', 'qr', 
						x, y, r_x, r_y, width=3
					)

			if point == 'r':
				# Only qr needs to be updated
				self.deleteElement('lines', 'qr')

				if self.ind_q:
					# point q exists, create new qr
					q_x, q_y = self.gui.cvx.points[self.ind_q]
					self.createElement('lines', 'qr',
						q_x, q_y, x, y, width=3
					)



	def displayAlgorithm(self, return_state=False):
		'''Method extracting current algo state and comparing
		with its own record to check and call for updating
		canvas
		param: 
			return_state: bool
				If true, method to be return exatracted 
				state of algorithm
		'''
		try:
			ind_p = self.gui.cvx.algo['ind_p']
			ind_q = self.gui.cvx.algo['ind_q']
			ind_r = self.gui.cvx.algo['ind_r']

			result = self.gui.cvx.algo['result_hull']

			if ind_p != self.ind_p:
				# change in point p, update Point P
				self.updatePoint(ind_p, 'p', updateLines=True)
				self.ind_p = ind_p

			if ind_q != self.ind_q:
				# change in point q, update Point q
				self.updatePoint(ind_q, 'q', updateLines=True)
				self.ind_q = ind_q

			if ind_r != self.ind_r:
				# change in point r, update Point r
				self.updatePoint(ind_r, 'r', updateLines=True)
				self.ind_r = ind_r

			if return_state:
				return ind_p, ind_q, ind_r, result
			else:
				return
		except AttributeError:
			print("AttributeError")
		except IndexError:
			print("IndexError")
		except KeyError:
			print("KeyError")
		except TypeError:
			print("TypeError")



	def postAlgorithmStep(self):
		# clear lines and text showing intemediate algo steps
		for key in self.gui.cvsobjects['lines'].keys():
			self.deleteElement('lines', key)
		for key in self.gui.cvsobjects['texts'].keys():
			self.deleteElement('texts', key)

		# connect last and first points in result to show
		# complete hull
		try:
			last_ind = self.gui.cvx.algo['result_hull'][-1]
			first_ind = self.gui.cvx.algo['result_hull'][0]
			x1, y1 = self.gui.cvx.points[last_ind]
			x2, y2 = self.gui.cvx.points[first_ind]
			self.createElement('r_lines', (last_ind, first_ind),
				x1, y1, x2, y2, width=3
			)
		except IndexError:
			pass
			


class DisplayJarvis(Display):
	def __init__(self, gui):
		super().__init__(gui)
		super().preAlgorithmDisplaySetup()
		if len(self.gui.cvsobjects['points']) == 0:
			super().displayAllPoints()


	def displayJarvis(self):
		ind_p, ind_q, ind_r, result = \
			super().displayAlgorithm(return_state=True)
		try:
			if len(result) > 1:
				# there are tentaive results
				key = tuple(result[-2:])
				if self.gui.cvsobjects['r_lines'].get(
					key, None):
					pass
				else:
					x1, y1 = self.gui.cvx.points[result[-2]]
					x2, y2 = self.gui.cvx.points[result[-1]]
					super().createElement('r_lines', key, 
						x1, y1, x2, y2, width=3
					)
		except KeyError:
			print("KeyError raised while displaying Jarvis")
		except AttributeError:
			print("AttributeError raised while displaying Jarvis")



class DisplayGraham(Display):
	def __init__(self, gui):
		super().__init__(gui)
		super().preAlgorithmDisplaySetup()
		if len(self.gui.cvsobjects['points']) == 0:
			super().displayAllPoints()


	def displayGraham(self):
		ind_p, ind_q, ind_r, result = \
			super().displayAlgorithm(return_state=True)

		try:
			if len(result) > 1:
				# there are tentative results
				if self.firstRun:
					# display all available result lines
					for ind in range(len(result)-1):
						x1, y1 = self.gui.cvx.points[result[ind]]
						x2, y2 = self.gui.cvx.points[result[ind+1]]
						key = tuple(result[ind:ind+2])
						super().createElement('r_lines', key,
							x1, y1, x2, y2, width=3
						)
						self.resultTupList.append(key)
					self.result_len = len(result)
					self.firstRun = False

				if len(result) > self.result_len:
					# new result indices were added
					key = tuple(result[-2:])

					if self.gui.cvsobjects['r_lines'].get(key, None):
						pass
					else:
						x1, y1 = self.gui.cvx.points[result[-2]]
						x2, y2 = self.gui.cvx.points[result[-1]]
						super().createElement('r_lines', key,
							x1, y1, x2, y2, width=3
						)
						self.resultTupList.append(key)

					self.result_len = len(result)
			if len(result) < self.result_len:
				# assuming concurrency of GUI and algorithm, only
				# one element (result line) to be removed
				lastResultTup = self.resultTupList.pop()
				super().deleteElement('r_lines',  lastResultTup)
				self.result_len = len(result)
		except AttributeError:
			print("AttributeError raised while displaying Graham")
		except KeyError:
			print("KeyError raised while displaying Graham")
		except IndexError:
			print("IndexError raised while displaying Graham")
		except TypeError:
			print("TypeError raised while displaying Graham")
