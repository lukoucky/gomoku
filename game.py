from enum import Enum
from board import Board
from utils import Point, MouseState, Mark

class Game:
	"""
	Represents the game machanics.
	It suppose to be a Model in MVVM pattern.
	"""
	def __init__(self, player_x, player_o, end_count, board_size):
		self.board = Board(board_size, end_count)

		self.player_x = player_x
		self.player_x.bind_game_move(self.on_received_move)

		self.player_o = player_o
		self.player_o.bind_game_move(self.on_received_move)

		self.draw_mark_listener = None
		self.end_game_listener = None

		self.state = GameState.WAITING_FOR_X		

	def bind_draw_mark_listener(self, listener):
		"""
		Binds listener for new mark update
		:param listener: Method that must accept Point and Player and notifiy
						 View to draw new mark from Player
		"""
		self.draw_mark_listener = listener

	def bind_end_game_listener(self, listener):
		"""
		Binds listener for end game
		:param listener: Method that must accept list of winning Points and Player and 
						 notifiy View to draw end game screen
		"""
		self.end_game_listener = listener

	def on_received_move(self, position, player):
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

	def is_players_move(self, player):
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

	def switch_players_and_move(self):
		"""
		Switch game state to next player and send command to the player to make move.
		"""
		if self.state == GameState.WAITING_FOR_O:
			self.state = GameState.WAITING_FOR_X
			self.player_x.move(self.board)
		else:
			self.state = GameState.WAITING_FOR_O
			self.player_o.move(self.board)

class GameState(Enum):
	"""
	Represents possible states of game
	"""
	WAITING_FOR_X = 0
	WAITING_FOR_O = 1
	END = 2
