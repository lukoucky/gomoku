from abc import ABC, abstractmethod
from random import randrange
from utils import Point, Mark
from typing import List, Callable, Optional
from minimax import MiniMax


class Player(ABC):
	"""
	Base class for all players of Tic Tac Toe game
	"""
	def __init__(self, name: str, end_count: int, mark: Mark, color: str) -> None:
		self.name = name
		self.end_count = end_count
		self.mark = mark
		self.color = color

		self.move_listener = None

	# TODO: Change from board to some safe copy of board that cannot alter game state
	@abstractmethod
	def move(self, board: List[Point]) -> None:
		"""
		Command from game to make a move. After the move is computed it should call send_move().
		:param board: 2D list with current board
		"""
		pass

	def send_move(self, move: Point) -> None:
		"""
		Notifies move_listener with new move.
		:param move: Point with position of move on board.
		"""
		self.move_listener(move, self)

	def bind_game_move(self, move_listener: Callable) -> None:
		"""
		Binds listener of new move.
		:param move_listener: Method that will be called when new move is made. 
							  Method must accept one parameter with Point.
		"""
		self.move_listener = move_listener


class HumanPlayer(Player):
	"""
	Human player. Does nothing, just empty class to be haned to Game.
	Move is send from View via ViewModel that calls send_move() of this class.
	"""
	def __init__(self, end_count: int, mark: Mark, color: str) -> None:
		Player.__init__(self, 'Human player', end_count, mark, color)

	def move(self, board: List[Point]) -> None:
		"""
		Nothing to do here, just wait for View's callback with clicked tile
		that will call send_move() directly.
		:param board: 2D list with current board.
		"""
		pass


class RandomPlayer(Player):
	"""
	Random Player just selects random empty tile and move there.
	"""
	def __init__(self, end_count: int, mark: Mark, color: str) -> None:
		Player.__init__(self, 'Random player', end_count, mark, color)

	def move(self, board: List[Point]) -> None:
		"""
		Selects random empty tile and move there.
		:param board: 2D list with current board.
		"""
		empty_tiles = board.get_empty_tiles()
		tile_id = randrange(len(empty_tiles))
		self.send_move(empty_tiles[tile_id])


class MiniMaxPlayer(Player):
	"""
	Player is using MiniMax algorthm to find the best move.
	"""
	def __init__(self, end_count: int, mark: Mark, color: str) -> None:
		Player.__init__(self, 'MiniMax player', end_count, mark, color)

	def move(self, board: List[Point]) -> None:
		"""
		Selects best move using minimax algorithm. Some special cases
		like first move, one move from winning are hardcoded.
		:param board: 2D list with current board.
		"""
		mm = MiniMax(board, self.mark)
		mm.compute()
		self.send_move(mm.get_best_move())
