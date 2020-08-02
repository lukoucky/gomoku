from utils import Point, Mark
from typing import List, Callable, Optional
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
		return self.end_win - self.end_lose
		# return self.value

	def __repr__(self):
		return f'{self.position} - W:{self.end_win}, L:{self.end_lose}, D:{self.end_draw}'

class MiniMax():
	def __init__(self, board, mark, max_depth):
		self.board = board
		self.mark = mark
		self.moves = []
		self.max_depth = max_depth

	def compute(self):
		candidates = self.board.get_candidate_tiles()
		for p in candidates:
			if self.board.tiles[p.x][p.y] == 0:
				child = self.board.copy()
				child.set_move(p, self.mark) 
				move = MiniMaxMove(p)
				depth = min(len(child.get_candidate_tiles()), self.max_depth)
				v = self.minimax(child, depth, False, move, -math.inf, math.inf)
				move.value = v
				self.moves.append(move)
				print(f'Done move {len(self.moves)} from {len(candidates)}')
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


	def minimax(self, node: List[Point], depth: int, is_maximizing: bool, move: MiniMaxMove, alpha: int, beta: int) -> int:
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


	def get_child_nodes(self, board: List[Point], this_players_move: bool) -> List[List[Point]]:
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
				if board.tiles[x][y] == 0:
					child = board.copy()
					child.set_move(Point(x,y), mark) 
					child_nodes.append(child)
		return child_nodes

	def get_board_result(self, board: List[Point]) -> Optional[int]:
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

		if board.tiles[result[0].x][result[0].y] == 1 and self.mark == Mark.X:
			return 1
		elif board.tiles[result[0].x][result[0].y] == -1 and self.mark == Mark.O:
			return 1
		return -1
