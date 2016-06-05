from random import randint
import random
from Tkinter import *


SIZE = 500
GRID_LEN = 4
GRID_PADDING = 10

BACKGROUND_COLOR_GAME = "#92877d"
BACKGROUND_COLOR_CELL_EMPTY = "#9e948a"
BACKGROUND_COLOR_DICT = {   2:"#eee4da", 4:"#ede0c8", 8:"#f2b179", 16:"#f59563", \
                            32:"#f67c5f", 64:"#f65e3b", 128:"#edcf72", 256:"#edcc61", \
                            512:"#edc850", 1024:"#edc53f", 2048:"#edc22e" }
CELL_COLOR_DICT = { 2:"#776e65", 4:"#776e65", 8:"#f9f6f2", 16:"#f9f6f2", \
                    32:"#f9f6f2", 64:"#f9f6f2", 128:"#f9f6f2", 256:"#f9f6f2", \
                    512:"#f9f6f2", 1024:"#f9f6f2", 2048:"#f9f6f2" }
FONT = ("Verdana", 40, "bold")

KEY_UP_ALT = "\'\\uf700\'"
KEY_DOWN_ALT = "\'\\uf701\'"
KEY_LEFT_ALT = "\'\\uf702\'"
KEY_RIGHT_ALT = "\'\\uf703\'"

KEY_UP = "'w'"
KEY_DOWN = "'s'"
KEY_LEFT = "'a'"
KEY_RIGHT = "'d'"



class game(Frame):
	board = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
	def __init__(self):
		Frame.__init__(self)
		self.grid()
		self.master.title('2048')
		self.master.bind("<Left>", self.shift_left)
		self.master.bind("<Right>", self.shift_right)
		self.master.bind("<Up>", self.shift_up)
		self.master.bind("<Down>", self.shift_down)
		self.grid_cells=[]
		self.init_grid()

		self.generate_new_num()
		self.generate_new_num()
		self.update_grid_cells()
		self.mainloop()
		#self.play()
	
	def update_grid_cells(self):
		for i in range(GRID_LEN):
			for j in range(GRID_LEN):
				new_number = self.board[i][j]
				if new_number == 0:
					self.grid_cells[i][j].configure(text="", bg=BACKGROUND_COLOR_CELL_EMPTY)
				else:
					self.grid_cells[i][j].configure(text=str(new_number), bg=BACKGROUND_COLOR_DICT[new_number], fg=CELL_COLOR_DICT[new_number])
		self.update_idletasks()


	def init_grid(self):
		background = Frame(self, bg=BACKGROUND_COLOR_GAME, width=SIZE, height=SIZE)
		background.grid()
		for i in range(GRID_LEN):
			grid_row = []
			for j in range(GRID_LEN):
				cell = Frame(background, bg=BACKGROUND_COLOR_CELL_EMPTY, width=SIZE/GRID_LEN, height=SIZE/GRID_LEN)
				cell.grid(row=i, column=j, padx=GRID_PADDING, pady=GRID_PADDING)
				t = Label(master=cell, text="", bg=BACKGROUND_COLOR_CELL_EMPTY, justify=CENTER, font=FONT, width=4, height=2)
				t.grid()
				grid_row.append(t)

			self.grid_cells.append(grid_row)


	def after_press(self, valid):
		if valid:
			self.generate_new_num()
			self.update_grid_cells()
			if self.win():
				self.grid_cells[1][1].configure(text="You",bg=BACKGROUND_COLOR_CELL_EMPTY)
				self.grid_cells[1][2].configure(text="Win!",bg=BACKGROUND_COLOR_CELL_EMPTY)
			if self.loose():
		       		self.grid_cells[1][1].configure(text="You",bg=BACKGROUND_COLOR_CELL_EMPTY)
		       		self.grid_cells[1][2].configure(text="Lose!",bg=BACKGROUND_COLOR_CELL_EMPTY)


	def rand_position(self):
		a = randint(0,len(self.empty_cells())-1)
		return list(self.empty_cells())[a]

	def two_or_four(self):
		r = randint(0,9)
		if r == 4:
			return 4
		else: 
			return 2

	def generate_new_num(self):
		x,y = self.rand_position()
		self.board[x][y] = self.two_or_four()

	def shift_left(self,event,aux=True):
		valid = False
		for num in range(GRID_LEN):
			line = self.board[num]
			temp = []
			result = []
			if sum(line) == 0:
				self.board[num] = line
			for i in range(len(line)):
				if line[i] != 0:
					temp.append(line[i])
			for i in range(len(temp)-1):
				if temp[i] == temp[i+1]:
					temp[i] += temp[i]
					temp[i+1] = 0
			for i in range(len(temp)):
				if temp[i] != 0:
					result.append(temp[i])
			for i in range(len(result),len(line)):
				result.append(0)
			self.board[num] = result
			if line != result:
				valid = True
		if aux:
			self.after_press(valid)
		return valid


	def shift_right(self,event):
		self.flip_board()
		valid = self.shift_left(event,False)
		self.flip_board()
		self.after_press(valid)

	def shift_up(self,event):
		self.transpose()
		valid = self.shift_left(event,False)
		self.transpose()
		self.after_press(valid)

	def shift_down(self,event):
		self.transpose()
		valid = self.shift_right(event,False)
		self.transpose()
		self.after_press(valid)

	def empty_cells(self):
		empty = []
		for i in range(GRID_LEN):
			for j in range(GRID_LEN):
				if self.board[i][j] == 0:
					empty.append((i,j))
		return empty

	def flip_board(self):
		temp = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
		for i in range(GRID_LEN):
			for j in range(GRID_LEN):
				temp[i][len(self.board)-j-1] = self.board[i][j]
		self.board = temp

	def transpose(self):
		temp = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
		for i in range(GRID_LEN):
			for j in range(GRID_LEN):
				temp[j][i] = self.board[i][j]
		self.board = temp

	def full(self):
		for i in range(GRID_LEN):
			for j in range(GRID_LEN):
				if self.board[i][j] == 0:
					return False
		return True

	def win(self):
		for i in range(GRID_LEN):
			for j in range(GRID_LEN):
				if self.board[i][j] == 2048:
					return True
		return False

	def loose(self):
		if self.full():
			for i in range(GRID_LEN):
				for j in range(GRID_LEN):
					print i,j
					for cell in self.neighbor(i,j):
						print i,j,cell[0],cell[1],self.board[i][j] == self.board[cell[0]][cell[1]]
						if self.board[i][j] == self.board[cell[0]][cell[1]]:
							return False
			return True
		return False


	def neighbor(self,i,j):
		n = len(self.board)
		directions = [(1,0),(-1,0),(0,1),(0,-1)]
		result = []
		for item in directions:
			if i+item[0] >= 0 and i+item[0] < n and j+item[1] >= 0 and j+item[1] < n:
				result.append((i+item[0],j+item[1]))
		return result


###########start###########
new_game = game()
