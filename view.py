from tkinter import Tk, Frame, Canvas, Event
from utils import Point, MouseState, Mark
from typing import List, Callable, Optional


class View:
	"""
	Class for drawing game state to canvas. 
	It suppose to be a View in MVVM pattern.
	"""
	def __init__(self, window_size: int = 500, board_size:int  = 10) -> None:
		self.canvas_width = window_size 
		self.canvas_height = window_size 
		self.board_size = board_size
		self.root = Tk()
		self.root.title('Tic Tac Toe')
		self.frame = Frame(self.root, width=window_size, height=window_size)
		self.canvas = Canvas(self.frame, width=window_size, height=window_size)
		self.mouse_state = MouseHandler()
		self.tile_click_listener = None

		# Colors and fonts
		self.color_tile_border = '#d8d8d8'
		self.color_background = 'white'
		self.color_winning = 'red'
		scale = window_size // board_size
		self.mark_font = f'Times {scale} bold'

		# Constants
		self.tile_size = self.canvas_height / self.board_size
		self.mark_offset = self.tile_size / 2
		self.winning_line_width = 4

		# Mouse binds
		self.canvas.focus_set()
		self.canvas.bind("<Button-1>", self.on_left_mouse_click)
		self.canvas.bind("<ButtonRelease-1>", self.on_left_mouse_release)

		self.init_board()

	def init_board(self) -> None:
		"""
		Draws empty board to canvas.
		"""
		self.canvas.create_rectangle(0, 0, self.canvas_width, self.canvas_height, fill=self.color_background)
		for x in range(0, self.canvas_width, self.canvas_width//self.board_size):
			self.canvas.create_line(x, 0, x, self.canvas_width, fill=self.color_tile_border)

		for y in range(0, self.canvas_width, self.canvas_height//self.board_size):
			self.canvas.create_line(0, y, self.canvas_height, y, fill=self.color_tile_border)

	def draw_mark(self, position: Point, mark: Mark, color: str) -> None:
		"""
		Draws mark on given position.
		:param position: Point where to make the mark. Point as a tile on board not the pixel.
		:param mark: Marker that should be draw
		:param color: Color string
		"""
		if mark == Mark.O:
			mark_text = 'o'
		else:
			mark_text = 'x'
		px = position.x * self.tile_size + self.mark_offset
		py = position.y * self.tile_size + self.mark_offset
		self.canvas.create_text(px, py, fill=color, font=self.mark_font, text=mark_text)

	def draw_end_game(self, positions: List[Point], mark: Mark) -> None:
		"""
		Draws end game marks and cross them with a line.
		:param positions: List of Points where with wininng row, column or diagonale. Points as a tiles on board not the pixels.
		:param mark: Marker that should be draw
		"""
		for position in positions:
			self.draw_mark(position, mark, self.color_winning)

		x0 = positions[0].x * self.tile_size + self.mark_offset
		y0 = positions[0].y * self.tile_size + self.mark_offset
		x1 = positions[-1].x * self.tile_size + self.mark_offset
		y1 = positions[-1].y * self.tile_size + self.mark_offset
		self.canvas.create_line(x0, y0, x1, y1, fill=self.color_winning, width=self.winning_line_width)

	def bind_tile_click_listener(self, listener: Callable) -> None:
		"""
		Method binds lister of clicks on game board with event of clicking.
		:param listener: Method that can listen to event of clicking on board. 
						 Method must accept one parameter that conations Point 
						 where the click was made.
		"""
		self.tile_click_listener = listener

	def get_clicked_tile(self, x: int, y: int) -> Optional[Point]:
		"""
		Finds the tile on board where the mouse click was made.
		:param x: X position of pixel of the click
		:param y: Y position of pixel of the click
		:return: None if the click is outside of the board. Point with the tiles position otherwise
		"""
		tile_x = x//(self.canvas_width//self.board_size)
		tile_y = y//(self.canvas_height//self.board_size)

		if tile_x < 0 or tile_x >= self.board_size or tile_y < 0 or tile_y >= self.board_size:
			return None
		else:
			return Point(tile_x, tile_y)

	def on_left_mouse_click(self, event: Event) -> None:
		"""
		Lister of mouse click.
		:param event: Tkinter click event
		"""
		self.mouse_state.set_click(event.x, event.y)

	def on_left_mouse_release(self, event: Event) -> None:
		"""
		Lister of mouse click release.
		:param event: Tkinter click release event
		"""
		is_click_valid = self.mouse_state.set_release(event.x, event.y)
		position = self.get_clicked_tile(event.x, event.y)
		if is_click_valid and position is not None:
			self.tile_click_listener(position)


class MouseHandler:
	"""
	Handles mouse click. If the distance between mouse button release and mouse 
	button click is larger than `eps` the mouse click is not valid.
	"""
	def __init__(self, eps: int = 1) -> None:
		self.eps = eps
		self.state = MouseState.CLICKED
		self.click_position = Point(-eps*10,-eps*10)

	def set_click(self, x: int, y: int) -> None:
		"""
		Sets new mouse click position
		:param x: X position of pixel of the click
		:param y: Y position of pixel of the click
		"""
		self.state = MouseState.CLICKED
		self.click_position = Point(x, y)

	def set_release(self, x: int, y: int) -> bool:
		"""
		Sets new mouse click release position. Serves to the purpouse 
		when player click on one position but release on another position. This is 
		considered as not valid click.
		:param x: X position of pixel of the click
		:param y: Y position of pixel of the click
		"""
		is_click_valid = False
		release_position = Point(x, y)
		if self.state == MouseState.CLICKED:
			self.state = MouseState.RELEASED
			if self.click_position.distance_to(release_position) <= self.eps:
				is_click_valid = True
		return is_click_valid


