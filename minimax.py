from utils import Point, Mark
from typing import List, Callable, Optional
from board import BoardTile
from copy import deepcopy
import math

class MiniMaxMove():
	def __init__(self, position):
		self.position = position
		self.end_win = 0
		self.end_lose = 0
		self.end_draw = 0
		self.value = -99999

	def add_result(self, result):
		# print(f'Adding result {result} to {self.position}')
		if result == 1:
			self.end_win += 1
		elif result == -1:
			self.end_lose += 1
		else:
			self.end_draw += 1

	def always_win(self):
		if self.end_win > 0 and self.end_lose == 0 and self.end_draw == 0:
			return True
		return False

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

	def compute(self):
		n_empty = len(self.board.get_empty_tiles())
		for x in range(self.board.size):
			for y in range(self.board.size):
				if self.board.tiles[x][y].is_empty():
					child = deepcopy(self.board)
					child.set_move(Point(x,y), self.mark) 
					move = MiniMaxMove(Point(x,y))
					v = self.minimax(child, len(child.get_empty_tiles()), False, move)
					move.value = v
					self.moves.append(move)
					print(f'Done move {len(self.moves)} from {n_empty}')
					print(move, move.get_score())
					print(v)
					print('--------')

	def get_best_move(self):
		# Check if there is move that wins always
		for move in self.moves:
			if move.always_win():
				return move.position

		# Else find moste winnable move
		best_score = -99999
		best_move = None
		total_moves = 0
		for move in self.moves:
			total_moves += move.end_win + move.end_lose + move.end_draw
			if move.get_score() > best_score:
				best_score = move.get_score()
				best_move = move.position

		print('Total moves:', total_moves)
		return best_move


	def minimax(self, node: List[BoardTile], depth: int, is_maximizing: bool, move: MiniMaxMove) -> int:
		"""
		MiniMax algorithm search through all possible game states and finds the 
		best for the player.
		:param node: Currently serached board
		:param depth: Number of empty tiles - 1
		:param is_maximizing: True if currently serach move is 
							  maximizin (is played by this player), False otherwise
		:return: Value of currently serached node
		"""
		# print('------------------------------------------')
		# print(f'Minimax function starts in depth {depth}, is minimizing {is_maximizing}')
		# print(node)
		winner = self.get_board_result(node)
		# print(f'get_board_result = {winner}')
		if depth == 0 or winner is not None:
			move.add_result(winner)
			return winner

		if is_maximizing:
			value = -999999
			for child in self.get_child_nodes(node, True):
				value = max(value, self.minimax(child, depth -1, False, move))
			return value
		else:
			value = 999999
			for child in self.get_child_nodes(node, False):
				value = min(value, self.minimax(child, depth -1, True, move))
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
					child = deepcopy(board)
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
		# print('get_board_result ',result)

		if result is None:
			# Still some empty tiles -> Game can continue
			return None

		if len(result) == 0:
			#  Draw
			return 0

		if board.tiles[result[0].x][result[0].y].mark == self.mark:
			# There is a winner on board and it is the player -> +1
			return 1
		# There is a winner on board and it is not the player -> -1
		return -1
