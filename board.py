from utils import Point, Mark
from typing import List, Optional


class Board:
	"""
	Represents the game board.
	"""
	def __init__(self, size: int, end_count: int = 4) -> None:
		self.size = size
		self.tiles = []
		self.end_count = end_count

		for i in range(self.size):
			self.tiles.append([0]*self.size)

	def copy(self):
		"""
		Creates copy of the board to prevent slow deepcopy method unusable in minimax.
		:return: Copy of this Board object
		"""
		b = Board(self.size, self.end_count)
		for x in range(self.size):
			for y in range(self.size):
				b.tiles[x][y] = self.tiles[x][y]
		return b

	def is_valid_move(self, position: Point) -> bool:
		"""
		CHeck if the move is valid - is to the empty tile.
		:param position: Point with position of the move
		:return: True if move is valid, False otherwise
		"""
		if self.tiles[position.x][position.y] == 0:
			return True
		return False

	def check_end(self) -> Optional[List[Point]]:
		"""
		Check if the game ends meaning that one of the players 
		have `end_count` marks in row, column or diagonale
		:return: None if game can continue. Otherwies returns list of Points
				 with positions of winning marks or empty list when game ends in draw.
		"""
		for x in range(self.size):
			for y in range(self.size):
				if not self.tiles[x][y] == 0:
					result = self.check_around(x, y)
					if result is not None:
						return result
		if len(self.get_empty_tiles()) == 0:
			return []
		return None
	
	def check_around(self, x: int, y: int) -> Optional[List[str]]:
		"""
		Checks all 8 direction from given position for row, column or diagonale
		of marks that would mean end of game.
		:param x: x position on board from where to check around
		:param y: y position on board from where to check around
		:return: None if game can continue. Otherwies returns list of Points
				 with positions of winning marks.
		"""
		for direction in [[-1,0], [-1,-1], [0,-1], [1,-1]]:
			results = self.check_direction(x, y, direction[0], direction[1])
			if results is not None:
				return results
		return None

	def check_direction(self, x: int, y: int, dx: int, dy: int) -> Optional[List[Point]]:
		"""
		Check in direction [dx,dy] from point [x,y] for row, column or diagonale of
		`end_count` marks. Function expects that [x,y] is not empty.
		:param x: x position on board from where to check around
		:param y: y position on board from where to check around
		:return: None if game can continue. Otherwies returns list of Points
				 of winning marks.
		"""
		result = [Point(x,y)]
		mark = self.tiles[x][y]
		for i in range(self.end_count-1):
			x += dx
			y += dy
			if x >= 0 and y >= 0 and x < self.size and y < self.size:
				if not self.tiles[x][y] == mark:
					return None
				else:
					result.append(Point(x,y))
			else:
				return None
		return result

	def set_move(self, position: Point, mark: Mark) -> None:
		"""
		Setter for new move made by player.
		:param position: Point where the move was made
		:mark: Mark of the player that made the move (X or O)
		"""
		if mark == Mark.X:
			self.tiles[position.x][position.y] = 1
		else:
			self.tiles[position.x][position.y] = -1

	def get_empty_tiles(self) -> List[Point]:
		"""
		Returns list of empty tiles on board.
		:return: List of empty board tiles.
		"""
		empty_tiles = []
		for x in range(self.size):
			for y in range(self.size):
				if self.tiles[x][y] == 0:
					empty_tiles.append(Point(x,y))
		return empty_tiles

	def get_candidate_tiles(self) -> List[Point]:
		"""
		Returns list of all empty positions neighboring already placed marks
		:return: List of Points with empty position suitable for new mark
		"""
		empty_tiles = set()
		for x in range(self.size):
			for y in range(self.size):
				if not self.tiles[x][y] == 0:
					for d in [[0,1], [1,1], [1,0], [1,-1], [0,-1], [-1,-1], [-1,0], [-1,1]]:
						if x+d[0] >= 0 and y+d[1] >= 0 and x+d[0] < self.size and y+d[1] < self.size and self.tiles[x+d[0]][y+d[1]] == 0:
							empty_tiles.add(Point(x+d[0],y+d[1]))
		return list(empty_tiles)

	def get_hash_string(self) -> str:
		"""
		Computes hash string of the current board state
		:return: Unique string for current board state
		"""
		s = ''
		for i in range(self.size):
			s += ''.join(map(str,self.tiles[i]))
		return s

	def __eq__(self, other):
		return self.get_hash_string() == other.get_hash_string()

	def __hash__(self):
		return hash(self.get_hash_string())

	def __repr__(self):
		s = ''
		for x in range(self.size):
			for y in range(self.size):
				if self.tiles[x][y] == 0:
					s += '_ '
				elif self.tiles[x][y] == 1:
					s += 'x '
				else:
					s += 'o '
			s = s[:-1] + '\n'
		return s
