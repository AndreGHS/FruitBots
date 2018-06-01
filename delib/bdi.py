import random
import numpy as np
from react.react import React

import pathFinding

DESIRE_CLOSEST_FRUIT = 0

# actions
CATCH_UP = 0
CATCH_LEFT = 1
CATCH_DOWN = 2
CATCH_RIGHT = 3
MOVE_UP = 4
MOVE_LEFT = 5
MOVE_DOWN = 6
MOVE_RIGHT = 7


WALL = -3

class B:

	def __init__(self):
		self.grid = []
		self.row = None
		self.col = None
		self.fruits_count = []
		self.fruits_left = []
		self.fruits_pos = []
		self.grid_size = None

	def get_fruit_pos(self):
		return np.asarray(np.where(self.grid >0)).T

	def update_beliefs(self, perception):
		self.grid = perception.get("grid")
		self.grid_size = len(perception.get("grid"))
		self.row = perception.get("row")
		self.col = perception.get("col")
		self.fruits_count = perception.get("fruits_count")
		self.fruits_left = perception.get("fruits_left")
		self.fruits_pos = self.get_fruit_pos()

class BDI:

	def __init__(self, grid_size):
		self.P = []
		self.I = None
		self.B = B()

		self.graph = pathFinding.Graph()
		self.graph.constructGraphFromGrid(grid_size)

	def updateGraph(self, grid_size):	
		self.graph = pathFinding.Graph()
		self.graph.constructGraphFromGrid(grid_size)

	def execute(self, perception):
		self.B.update_beliefs(perception)
		
		if not(not self.P or self.impossible(self.B,self.I) or self.succeeded(self.B,self.I)):

			action = self.get_action(self.P)

		else:
			# in this case the desire is always to catch the closest fruit
			D = self.option(self.B)
			print("D VALUE", D)
			if D != None:
				print("D")
				self.I = self.filter(self.B, D)
				self.P = self.build_plan(self.B,self.I)
				if self.P:
					print("DELIB")
					action = self.get_action(self.P)
				else:
					print("REACT")
					# if no desire or if empty plan behave as reactive agent
					action = React().execute(self.get_neighbor_cells(self.B.grid, self.B.row, self.B.col)) 
			else:
				print("REACT")
				# if no desire or if empty plan behave as reactive agent
				action = React().execute(self.get_neighbor_cells(self.B.grid, self.B.row, self.B.col))
		return action

	def get_neighbor_cells(self, grid, row,col):
		global grid_size

		cells = [
					grid[row-1][col] if row-1 >= 0 else WALL, # up
					grid[row][col-1] if col-1 >= 0 else WALL, # left
					grid[row+1][col] if row+1 < len(grid) else WALL, # down
					grid[row][col+1] if col+1 < len(grid) else WALL # right
				]
		return cells

	# returns next action in plan
	def get_action(self, P):
		action = P.pop(0)
		return action

	# returns desire
	# according to the current beliefs, selects agent desires
	def option(self, B):

		# if fruits left
		if sum(b[1] for b in B.fruits_left) > 0:
			desire = DESIRE_CLOSEST_FRUIT
		else:
			desire = None

		print(B.fruits_left)
		print("DESIRE", sum(b[1] for b in B.fruits_left) )
		return desire

	def find_closest_fruits(self, B):
		fruit_dist = []
		
		for fruit in B.fruits_pos:
			x = fruit[0] - B.row
			y = fruit[1] - B.col
			d = abs(x) + abs(y) # manhattan distance
			#d = math.sqrt(pow(x, 2) + pow(y, 2)) # euclidian
			fruit_dist.append((fruit, d, B.grid[fruit[0]][fruit[1]]))
		closest_fruits = sorted(fruit_dist, key=lambda x:x[1])
		print("closest_fruits sorted", closest_fruits)
		closest_fruits = [(f[0],f[2]) for f in closest_fruits if f[1] == closest_fruits[0][1]]
		return closest_fruits

	# returns intention
	def filter(self, B, D):
		if D == DESIRE_CLOSEST_FRUIT:

			# closest fruits to bot
			closest_fruits = self.find_closest_fruits(B)
			print("my pos", (B.row, B.col))
			print("CLOSEST FRUITS", closest_fruits)
			# fruits that exist on board
			"""print(B.fruits_left)
			fruits_on_board = [f for f in B.fruits_left if f != 0]
			print(fruits_on_board)
			fruits_on_board = dict(fruits_on_board)
			print("dict", fruits_on_board)"""


			fruits_count_dict = dict(B.fruits_count)
			# fruits that the bot needs (has less quantity) and that are close to him
			closest_fruits = [(f[0],f[1], fruits_count_dict.get(f[1])) for f in closest_fruits]
			closest_fruits = sorted(closest_fruits, key=lambda x:x[2])
			closest_fruits = [f for f in closest_fruits if f[2] == closest_fruits[0][2]]

			fruit_type = random.choice(closest_fruits)
			valid_fruits = [f[0] for f in closest_fruits if B.grid[f[0][0]][f[0][1]] == fruit_type[1]]

			I = random.choice(valid_fruits)

			return I
			
	# convert list of tuples (x,y) to actions
	def convert_mov(self, B, movement):
		plan = []
		size = len(movement)

		for m in range(size):
			new = movement[m]
			if m == 0:
				before = (B.row, B.col)
			else: 
				before = movement[m-1]

			if before[0]+1 == new[0]:
				action = MOVE_DOWN if m != size-1 else CATCH_DOWN
			elif before[0]-1 == new[0]:
				action = MOVE_UP if m != size-1 else CATCH_UP
			elif before[1]+1 == new[1]:
				action = MOVE_RIGHT if m != size-1 else CATCH_RIGHT
			elif before[1]-1 == new[1]:
				action = MOVE_LEFT if m != size-1 else CATCH_LEFT

			plan.append(action)

		return plan

	def build_plan(self, B,I):
		startNode = str(B.row)+str(B.col)
		endNode = str(I[0])+str(I[1])
		movement = self.graph.getPathForMovement(self.graph.bfs_short_path(startNode, endNode))
		P = self.convert_mov(B, movement)
		return P

    # if the fruit in no longer in position
	def impossible(self, B, I):
		if B.grid[I[0]][I[1]] < 1:
			return False

	def succeeded(self, B, I):
		return False