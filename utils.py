from enum import Enum
import math

class Point:
	"""
	Represents simple 2D point.
	"""
	def __init__(self, x = 0, y = 0):
		self.x = x
		self.y = y

	def distance_to(self, other):
		"""
		Computes distance to another point.
		:param other: Another Point
		:return: Distance to other Point
		"""
		return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)

	def __repr__(self):
		return f'[{self.x}:{self.y}]'


class MouseState(Enum):
	"""
	Represents state of mouse click - clicked or released.
	"""
	CLICKED = 0
	RELEASED = 1

class Mark(Enum):
	"""
	Represents X and O mark of Tic Tac Toe game
	"""
	X = 0
	O = 1
