from game import Game
from view import View
from utils import Mark
from player import RandomPlayer, HumanPlayer

class ViewModel():
	"""
	Class that connects Game with View and runs the game.
	It suppose to be a View Model in MVVM pattern.
	"""
	def __init__(self):
		# Number of marks in a row, column or diagonale to end game
		end_count = 4

		self.view = View()
		self.view.bind_tile_click_listener(self.on_tile_click)

		self.px = HumanPlayer(end_count, Mark.X, '#32a852')
		self.po = RandomPlayer(end_count, Mark.O, 'black')

		self.game = Game(self.view, end_count, self.px, self.po)

	def on_tile_click(self, position):
		"""
		Bind View's callback of new click on tile with Human Players
		send_move() method.
		:param position: Point with position of the move on board
		"""
		self.px.send_move(position)

	def run(self):
		"""
		Runs the game
		"""
		self.view.canvas.pack()
		self.view.frame.pack()
		self.view.root.mainloop()

if __name__ == '__main__':
	vm = ViewModel()
	vm.run()
