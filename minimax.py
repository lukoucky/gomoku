from utils import Point, Mark
from typing import List, Callable, Optional
from board import BoardTile
import math

class MiniMaxMove():
	def __init__(self, position):
		self.position = position
		self.end_win = 0
		self.end_lose = 0
		self.end_draw = 0
		self.value = -99999

	def add_result(self, result):
		if result == 1:
			self.end_win += 1
		elif result == -1:
			self.end_lose += 1
		else:
			self.end_draw += 1

	def get_score(self):
		# return self.end_win - self.end_lose
		return self.value

	def __repr__(self):
		return f'{self.position} - W:{self.end_win}, L:{self.end_lose}, D:{self.end_draw}'

class MiniMax():
	def __init__(self, board, mark):
		self.board = board
		self.mark = mark
		self.moves = []
		self.max_depth = 3

	def compute(self):
		n_empty = len(self.board.get_empty_tiles())
		for x in range(self.board.size):
			for y in range(self.board.size):
				if self.board.tiles[x][y].is_empty():
					child = self.board.copy()
					child.set_move(Point(x,y), self.mark) 
					move = MiniMaxMove(Point(x,y))
					depth = min(len(child.get_empty_tiles()), self.max_depth)
					v = self.minimax(child, depth, False, move, -math.inf, math.inf)
					move.value = v
					self.moves.append(move)
					print(f'Done move {len(self.moves)} from {n_empty}')
					print(move, move.get_score())
					print(v)
					print('--------')

	def get_best_move(self):
		best_score = -math.inf
		best_move = None
		total_moves = 0
		for move in self.moves:
			total_moves += move.end_win + move.end_lose + move.end_draw
			if move.get_score() > best_score:
				best_score = move.get_score()
				best_move = move.position

		return best_move


	def minimax(self, node: List[BoardTile], depth: int, is_maximizing: bool, move: MiniMaxMove, alpha: int, beta: int) -> int:
		"""
		MiniMax algorithm search through all possible game states and finds the 
		best for the player.
		:param node: Currently serached board
		:param depth: Number of empty tiles - 1
		:param is_maximizing: True if currently serach move is 
							  maximizin (is played by this player), False otherwise
		:return: Value of currently serached node
		"""
		winner = self.get_board_result(node)
		if depth == 0 or winner is not None:
			move.add_result(winner)
			if winner is None:
				return 0
			return winner

		if is_maximizing:
			value = -math.inf
			for child in self.get_child_nodes(node, True):
				value = max(value, self.minimax(child, depth -1, False, move, alpha, beta))
				alpha = max(alpha, value)
				if beta <= alpha:
					break
			return value
		else:
			value = math.inf
			for child in self.get_child_nodes(node, False):
				value = min(value, self.minimax(child, depth -1, True, move, alpha, beta))
				beta = min(beta, value)
				if beta <= alpha:
					break
			return value


	def get_child_nodes(self, board: List[BoardTile], this_players_move: bool) -> List[List[BoardTile]]:
		"""
		For currently serached board prepares all possible next moves
		:param board: Currently serached board
		:param this_players_move: True if currently serach move is played by this 
								  player, False otherwise
		:return: List with all possible boards in next move
		"""
		mark = self.mark
		if not this_players_move:
			if self.mark == Mark.O:
				mark = Mark.X
			else:
				mark = Mark.O

		child_nodes = []
		for x in range(board.size):
			for y in range(board.size):
				if board.tiles[x][y].is_empty():
					child = board.copy()
					child.set_move(Point(x,y), mark) 
					child_nodes.append(child)
		return child_nodes

	def get_board_result(self, board: List[BoardTile]) -> Optional[int]:
		"""
		Checks if the board represents finnished game.
		:param board: 2D list with board.
		:return: None if game is not finnished. -1 if player lost, 1 if player won and 0 for draw.
		"""
		result = board.check_end()
		if result is None:
			return None

		if len(result) == 0:
			return 0

		if board.tiles[result[0].x][result[0].y].mark == self.mark:
			return 1
		return -1
