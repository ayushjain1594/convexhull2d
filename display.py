class Display():
	""" Class to track algorithm progress and display on canvas """

	def __init__(self, gui, algo='jarvis'):
		self.gui = gui
		self.pointcolor = "#000000"
		self.algo = algo


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


	def deleteElement(self, elementtype='texts', key):
		try:
			self.gui.cvsobjects.delete(
				self.gui.cvsobjects[elementtype][key]
			)
		except KeyError:
			print("Invalid key or element type")
			pass


	def createElement(self, elementtype, key, *args, **kwargs):
		try:
			if elementtype == 'lines':
				self.gui.cvsobjects[elementtype][key] = \
					self.gui.canvas.create_line(*args, **kwargs)

			elif elementtype == 'texts':
				self.gui.cvsobjects[elementtype][key] = \
					self.gui.canvas.create_text(*args, **kwargs)

			elif elementtype == 'r_lines':
				self.gui.cvsobjects[elementtype][key] = \
					self.gui.canvas.create_line(*args, **kwargs)

			elif elementtype == 'points':
				self.gui.cvsobjects[elementtype][key] = \
					self.gui.canvas.create_oval(*args, **kwargs)

		except KeyError:
			print("Invalid element type")


	def updatePoint(self, ind, point='p', updateLines=True):
		# delete old point text if exists
		if self.gui.cvsobjects['texts'].get(point, None):
			self.deleteElement('texts', point)

		# get new point coordinates and create new text
		x, y = self.gui.cvx.points[ind]
		self.createElement('texts', point, 
			x, y+12, text=point+' '+str(ind)
		)
		
		if updateLines:
			if point == 'p':
				# Only pq needs to be updated
				if self.gui.cvsobjects['lines'].get('pq', None):
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
				if self.gui.cvsobjects['lines'].get('pq', None):
					self.deleteElement('lines', 'pq')

				if self.ind_p:
					# point p exists, create new pq
					p_x, p_y = self.gui.cvx.points[self.ind_p]
					self.createElement('lines', 'pq', 
						p_x, p_y, x, y, width=3
					)

				if self.gui.cvsobjects['lines'].get('qr', None):
					self.deleteElement('lines', 'qr')

				if self.ind_r:
					# point r exists, create new qr
					r_x, r_y = self.gui.cvx.points[self.ind_r]
					self.createElement('lines', 'qr', 
						x, y, r_x, r_y, width=3
					)

			if point == 'r':
				# Only qr needs to be updated
				if self.gui.cvsobjects['lines'].get('qr', None):
					self.deleteElement('lines', 'qr')

				if self.ind_q:
					# point q exists, create new qr
					q_x, q_y = self.gui.cvx.points[self.ind_q]
					self.createElement('lines', 'qr',
						q_x, q_y, x, y, width=3
					)



	def displayAlgorithm(self):
		try:
			ind_p = self.cvx.algo['ind_p']
            ind_q = self.cvx.algo['ind_q']
            ind_r = self.cvx.algo['ind_r']

            result = self.cvx.algo['result_hull']

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
