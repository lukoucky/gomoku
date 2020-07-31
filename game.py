from enum import Enum
from board import Board
from utils import Point, MouseState, Mark

class Game:
	"""
	Represents the game with is machanics.
	It suppose to be a Model in MVVM pattern.
	"""
	def __init__(self, view, end_count, player_x, player_o):
		self.board = Board(10, end_count)

		# TODO: Get rid of the view. It should not be in Model of MVVM
		self.view = view

		self.player_x = player_x
		self.player_x.bind_game_move(self.on_received_move)

		self.player_o = player_o
		self.player_o.bind_game_move(self.on_received_move)

		self.state = GameState.WAITING_FOR_X			

	def on_received_move(self, position, player):
		"""
		Callback function that is called by players. It receives new move
		and if the move is valid and player is expected to make a move it is set 
		on board.
		:param position: Point with position on board where the move should be made
		:param player: Player that is making the move
		"""
		if self.is_players_move(player):
			self.board.set_move(position, player.mark)
			result = self.board.check_end()
			self.view.draw_mark(position, player.mark, player.color)

			if result is not None:
				self.view.draw_end_game(result, player.mark)
				self.state = GameState.END
			else:
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
