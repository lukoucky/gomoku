from utils import Point

class Board:
	"""
	Represents the game board.
	"""

	def __init__(self, size, end_count=4):
		self.size = size
		self.tiles = []
		self.end_count = end_count

		for x in range(self.size):
			self.tiles.append([0]*self.size)
			for y in range(self.size):
				self.tiles[x][y] = BoardTile(x, y)

	def check_end(self):
		"""
		Check if the game ends meaning that one of the players 
		have `end_count` marks in row, column or diagonale
		:return: None if game can continue. Otherwies returns list of Points
				 with positions of winning marks.
		"""
		for x in range(self.size):
			for y in range(self.size):
				if not self.tiles[x][y].is_empty():
					result = self.check_around(x, y)
					if result is not None:
						return result
		return None
	
	def check_around(self, x, y):
		"""
		Checks all 8 direction from given position for row, column or diagonale
		of marks that would mean end of game.
		:param x: x position on board from where to check around
		:param y: y position on board from where to check around
		:return: None if game can continue. Otherwies returns list of Points
				 with positions of winning marks.
		"""
		for direction in [[0,1], [1,1], [1,0], [1,-1], [0,-1], [-1,-1], [-1,0], [-1,1]]:
			results = self.check_direction(x, y, direction[0], direction[1])
			if results is not None:
				points = []
				for result in results:
					points.append(Point(result.position_x, result.position_y))
				return points
		return None

	def check_direction(self, x, y, dx, dy):
		"""
		Check in direction [dx,dy] from point [x,y] for row, column or diagonale of
		`end_count` marks. Function expects that [x,y] is not empty.
		:param x: x position on board from where to check around
		:param y: y position on board from where to check around
		:return: None if game can continue. Otherwies returns list of BoardTile
				 of winning marks.
		"""
		result = [self.tiles[x][y]]
		mark = self.tiles[x][y].mark
		for i in range(self.end_count-1):
			x += dx
			y += dy
			if x >= 0 and y >= 0 and x < self.size and y < self.size:
				if not self.tiles[x][y].mark == mark:
					return None
				else:
					result.append(self.tiles[x][y])
			else:
				return None
		return result

	def set_move(self, position, mark):
		"""
		Setter for new move made by player.
		:param position: Point where the move was made
		:mark: Mark of the player that made the move (X or O)
		"""
		self.tiles[position.x][position.y].mark = mark


	def __repr__(self):
		s = ''
		for x in range(self.size):
			for y in range(self.size):
				s += str(self.tiles[x][y]) + ', '
			s = s[:-2] + '\n'
		return s


class BoardTile:
	"""
	Represents one tile (box) on the game board.
	"""
	def __init__(self, position_x, position_y):
		self.position_x = position_x
		self.position_y = position_y
		self.mark = None

	def __repr__(self):
		return f'[{self.position_x}:{self.position_y}]'

	def is_empty(self):
		"""
		Check if tile is empty (no mark have been set)
		:return: True if tile is empty, False otherwies
		"""
		if self.mark is None:
			return True
		return False
