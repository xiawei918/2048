from random import randint
import random

class game:
	board = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
	n = len(board)
	def __init__(self):
		self.generate_new_num()
		self.generate_new_num()


	def play(self):
		self.display_board()
		while not self.loose():
			move = self.user_input()
			valid = False
			if move == 'a':
				valid = self.shift_left()
			if move == 'd':
				valid = self.shift_right()
			if move == 'w':
				valid = self.shift_up()
			if move == 's':
				valid = self.shift_down()
			if valid:
				self.generate_new_num()
			self.display_board()
			if self.win():
				print 'You win!'
		print 'You loose!'

	def user_input(self):
		move = str(raw_input("Enter your next move ((a) for left, (d) for right, (w) for up, (s) for down: "))
		while move not in ['a','d','w','s']:
			print 'Invalid entry.'
			move = str(raw_input('Enter your next move ((a) for left, (d) for right, (w) for up, (s) for down: '))
		return move


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
		

	def display_board(self):
		print '-----------------'
		for i in range(len(self.board)):
			for j in range(len(self.board[0])):
				print '|',
				if self.board[i][j] == 0:
					print ' ',
				else:
					print self.board[i][j],
			print '|\n-----------------'

	def shift_left(self):
		valid = False
		for num in range(len(self.board)):
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
		return valid


	def shift_right(self):
		self.flip_board()
		valid = self.shift_left()
		self.flip_board()
		return valid

	def shift_up(self):
		self.transpose()
		valid = self.shift_left()
		self.transpose()
		return valid

	def shift_down(self):
		self.transpose()
		valid = self.shift_right()
		self.transpose()
		return valid

	def empty_cells(self):
		empty = []
		for i in range(len(self.board)):
			for j in range(len(self.board[0])):
				if self.board[i][j] == 0:
					empty.append((i,j))
		return empty

	def flip_board(self):
		temp = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
		for i in range(len(self.board)):
			for j in range(len(self.board[0])):
				temp[i][len(self.board)-j-1] = self.board[i][j]
		self.board = temp

	def transpose(self):
		temp = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
		for i in range(len(self.board)):
			for j in range(len(self.board[0])):
				temp[j][i] = self.board[i][j]
		self.board = temp

	def full(self):
		for i in range(len(self.board)):
			for j in range(len(self.board[0])):
				if self.board[i][j] == 0:
					return False
		return True

	def win(self):
		for i in range(len(self.board)):
			for j in range(len(self.board[0])):
				if self.board[i][j] == 2048:
					return True
		return False

	def loose(self):
		if self.full():
			for i in range(len(self.board)):
				for j in range(len(self.board[0])):
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
new_game.play()