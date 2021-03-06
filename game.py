from enum import Enum
from board import Board
from utils import Point, MouseState, Mark
from player import Player
from typing import List, Callable, Optional

class Game:
	"""
	Represents the game machanics.
	It suppose to be a Model in MVVM pattern.
	"""
	def __init__(self, player_x: Player, player_o: Player, end_count: int, board_size: int) -> None:
		self.state = GameState.INIT	
		self.board_size = board_size
		self.end_count = end_count
		self.board = Board(self.board_size, self.end_count)

		self.player_x = player_x
		self.player_x.bind_game_move(self.on_received_move)

		self.player_o = player_o
		self.player_o.bind_game_move(self.on_received_move)

		self.draw_mark_listener = None
		self.end_game_listener = None

	def bind_draw_mark_listener(self, listener: Callable) -> None:
		"""
		Binds listener for new mark update
		:param listener: Method that must accept Point and Player and notifiy
						 View to draw new mark from Player
		"""
		self.draw_mark_listener = listener
		self.start_if_initialized()

	def bind_end_game_listener(self, listener: Callable) -> None:
		"""
		Binds listener for end game
		:param listener: Method that must accept list of winning Points and Player and 
						 notifiy View to draw end game screen
		"""
		self.end_game_listener = listener
		self.start_if_initialized()

	def start_if_initialized(self) -> None:
		"""
		Starts the game if it is properly initialized. That means that 
		draw_mark_listener and end_game_listener is set.
		"""
		if not self.end_game_listener is None and not self.draw_mark_listener is None:
			self.state = GameState.WAITING_FOR_X
			self.player_x.move(self.board)

	def on_received_move(self, position: Point, player: Player) -> None:
		"""
		Callback function that is called by players. It receives new move
		and if the move is valid and player is expected to make a move it is set 
		on board.
		:param position: Point with position on board where the move should be made
		:param player: Player that is making the move
		"""
		if self.is_players_move(player) and self.board.is_valid_move(position):
			self.board.set_move(position, player.mark)
			result = self.board.check_end()

			if result is not None:
				self.state = GameState.END
				self.end_game_listener(result, player)
			else:
				self.draw_mark_listener(position, player)
				self.switch_players_and_move()

	def is_players_move(self, player: Player) -> bool:
		"""
		Check if the player that is making the move is entitled to do so.
		:param player: Player that is making the move
		:return: True if player is expected to make the move, False otherwise.
		"""
		if player.mark == Mark.O and self.state == GameState.WAITING_FOR_O:
			return True
		elif player.mark == Mark.X and self.state == GameState.WAITING_FOR_X:
			return True
		return False

	def switch_players_and_move(self) -> None:
		"""
		Switch game state to next player and send command to the player to make move.
		"""
		if self.state == GameState.WAITING_FOR_O:
			self.state = GameState.WAITING_FOR_X
			self.player_x.move(self.board)
		else:
			self.state = GameState.WAITING_FOR_O
			self.player_o.move(self.board)

	def restart(self):
		"""
		Restarts the game
		"""
		self.board = Board(self.board_size, self.end_count)
		self.state = GameState.WAITING_FOR_X
		self.player_x.move(self.board)


class GameState(Enum):
	"""
	Represents possible states of game
	"""
	INIT = 0
	WAITING_FOR_X = 1
	WAITING_FOR_O = 2
	END = 3
