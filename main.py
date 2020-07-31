from game import Game
from view import View
from utils import Mark, Point
from player import Player, RandomPlayer, HumanPlayer
from typing import List


class ViewModel():
	"""
	Class that connects Game with View and runs the game.
	It suppose to be a View Model in MVVM pattern.
	"""
	def __init__(self) -> None:
		# Number of marks in a row, column or diagonale to end game
		end_count = 4

		# Number of tiles on the board in each dimension
		board_size = 10

		# Size of GUI window in pixels
		window_size = 500

		self.view = View(window_size, board_size)
		self.view.bind_tile_click_listener(self.on_tile_click)

		self.px = HumanPlayer(end_count, Mark.X, '#32a852')
		self.po = RandomPlayer(end_count, Mark.O, 'black')

		self.game = Game(self.px, self.po, end_count, board_size)
		self.game.bind_draw_mark_listener(self.on_new_mark)
		self.game.bind_end_game_listener(self.on_end_game)

	def on_tile_click(self, position: Point) -> None:
		"""
		Bind View's callback of new click on tile with Human Players
		send_move() method.
		:param position: Point with position of the move on board
		"""
		self.px.send_move(position)

	def on_new_mark(self, position: Point, player: Player):
		"""
		Binds View's callback of new mark with new mark action in Game.
		:param position: Point with position of the new mark on board
		:param player: Player that made the mark
		"""
		self.view.draw_mark(position, player.mark, player.color)

	def on_end_game(self, positions: List[Point], player: Player):
		"""
		Binds View's callback of end game with end game action in Game.
		:param positions: List of Points with positions of the winning marks
		:param player: Player that wins
		"""
		self.view.draw_end_game(positions, player.mark)

	def run(self) -> None:
		"""
		Runs the game
		"""
		self.view.canvas.pack()
		self.view.frame.pack()
		self.view.root.mainloop()

if __name__ == '__main__':
	vm = ViewModel()
	vm.run()
