import curses
import random
 
# Please note that curses uses a y,x coordination system.
# In the code you see here, I'll be using x,y
 
# If any of the code seems inconsistent, it's because I took
# some of the things from my current project out and replaced
# for the purposes of this article
 
# Also, some of this was poorly converted. If you want to clean
# it up, go for it. Otherwise, I might get around to it eventually ;)
 
# I have not included placing up/down stairs or any of that business
 
# TODO: COMMENT THINGS BETTER!
 
# This is just the basic dungeon tile. It holds a shape.
class dungeon_tile:
	_shape = ''
 
	def __init__(self, shape):
		self._shape = shape
 
	def get_shape(self):
		return self._shape
 
	def set_shape(self, shape):
		self._shape = shape
 
# Our randomly generated dungeon
class dungeon:
	_map_size = (0, 0)
	_tiles = []
 
	# max_features - how many rooms/corridors will be generated at the most
	# room_chance - the % chance that the generated feature will be a room
	def __init__(self, map_size_x, map_size_y, max_features, room_chance):
		# seed the psuedo-random number generator
		random.seed()
 
		# set the map size
		self._map_size = (map_size_x, map_size_y)
 
		# fill the map with blank tiles
		for x in range (0, self._map_size[0]):
			self._tiles.append([])
			for y in range (0,  self._map_size[1]):
				self._tiles[x].append(dungeon_tile(''))
 
		current_features = 1
		self._make_room(self._map_size[0]/2, self._map_size[1]/2, 5, 5, random.randint(0, 3))
 
		for i in range (0, 1000):
			if current_features == max_features: break
 
			newx = 0
			xmod = 0
			newy = 0
			ymod = 0
			direction = -1
 
			for j in range (0, 1000):
				newx = random.randint(1, self._map_size[0]-2)
				newy = random.randint(1, self._map_size[1]-2)
				direction = -1
 
				shape = self._tiles[newx][newy].get_shape()
 
				if shape == '#' or shape == 'c':
					if self._tiles[newx][newy+1].get_shape() == '.' or self._tiles[newx][newy+1].get_shape() == 'c':
						xmod = 0
						ymod = -1
						direction = 0
					elif self._tiles[newx-1][newy].get_shape() == '.' or self._tiles[newx-1][newy].get_shape() == 'c':
						xmod = 1
						ymod = 0
						direction = 1
					elif self._tiles[newx][newy-1].get_shape() == '.' or self._tiles[newx][newy-1].get_shape() == 'c':
						xmod = 0
						ymod = 1
						direction = 2
					elif self._tiles[newx+1][newy].get_shape() == '.' or self._tiles[newx+1][newy].get_shape() == 'c':
						xmod = -1
						ymod = 0
						direction = 3
 
					if direction > -1: break
 
			if direction > -1:
				feature = random.randint(0, 100)
 
				if feature <= room_chance:
					if self._make_room(newx+xmod, newy+ymod, 10, 10, direction):
						current_features += 1
						self._tiles[newx][newy].set_shape('+')
						self._tiles[newx+xmod][newy+ymod].set_shape('.')
				elif feature > room_chance:
					if self._make_corridor(newx+xmod, newy+ymod, 6, direction):
						current_features += 1
						self._tiles[newx][newy].set_shape('+')
 
	# this shows the map. we're not doing a scrolling map for this article, so it's easier
	def draw(self, stdscr):
		for x in range (0, self._map_size[0]):
			for y in range (0, self._map_size[1]):
				stdscr.addstr(y, x, self._tiles[x][y].get_shape())
		stdscr.refresh()
 
	# this makes a corridor at x,y in a direction
	def _make_corridor(self, x, y, length, direction):
		len = random.randint(2, length)
 
		dir = 0
		if direction > 0 and direction < 4: dir = direction
 
		if dir == 0:
			if x < 0 or x > self._map_size[0]-1: return False
 
			for i in range (y, y-len, -1):
				if i < 0 or i > self._map_size[1]-1: return False
				if self._tiles[x][i].get_shape() != '':return False
 
			for i in range (y, y-len, -1):
				self._tiles[x][i].set_shape('c')
		elif dir == 1:
			if y < 0 or y > self._map_size[1]-1: return False
 
			for i in range (x, x+len):
				if i < 0 or i > self._map_size[1]-1: return False
				if self._tiles[i][y].get_shape() != '': return False
 
			for i in range (x, x+len):
				self._tiles[i][y].set_shape('c')
		elif dir == 2:
			if x < 0 or x > self._map_size[0]-1: return False
 
			for i in range (y, y+len):
				if i < 0 or i > self._map_size[1]-1: return False
				if self._tiles[x][i].get_shape() != '': return False
 
			for i in range (y, y+len):
				self._tiles[x][i].set_shape('c')
		elif dir == 3:
			if y < 0 or y > self._map_size[1]-1: return False
 
			for i in range (x, x-len, -1):
				if i < 0 or i > self._map_size[1]-1: return False
				if self._tiles[i][y].get_shape() != '': return False
 
			for i in range (x, x-len, -1):
				self._tiles[i][y].set_shape('c')
 
		return True
 
	# this makes a room at x,y with the width,height and in a direction
	def _make_room(self, x, y, width, height, direction):
		rand_width = random.randint(4, width)
		rand_height = random.randint(4, height)
 
		dir = 0
		if direction > 0 and direction < 4: dir = direction
 
		if dir == 0:
			for i in range (y, y-rand_height, -1):
				if i < 0 or i > self._map_size[1]-1: return False
				for j in range (x-rand_width/2, (x+(rand_width+1)/2)):
					if j < 0 or j > self._map_size[0]-1: return False
					if self._tiles[j][i].get_shape() != '': return False
 
			for i in range (y, y-rand_height, -1):
				for j in range (x-rand_width/2, (x+(rand_width+1)/2)):
					if j == x-rand_width/2: self._tiles[j][i].set_shape('#')
					elif j == x+(rand_width-1)/2: self._tiles[j][i].set_shape('#')
					elif i == y: self._tiles[j][i].set_shape('#')
					elif i == y-rand_height+1: self._tiles[j][i].set_shape('#')
					else: self._tiles[j][i].set_shape('.')
		elif dir == 1:
			for i in range (y-rand_height/2, y+(rand_height+1)/2):
				if i < 0 or i > self._map_size[1]-1: return False
				for j in range (x, x+rand_width):
					if j < 0 or j > self._map_size[0]-1: return False
					if self._tiles[j][i].get_shape() != '': return False
 
			for i in range (y-rand_height/2, y+(rand_height+1)/2):
				for j in range (x, x+rand_width):
					if j == x: self._tiles[j][i].set_shape('#')
					elif j == x+(rand_width-1): self._tiles[j][i].set_shape('#')
					elif i == y-rand_height/2: self._tiles[j][i].set_shape('#')
					elif i == y+(rand_height-1)/2: self._tiles[j][i].set_shape('#')
					else: self._tiles[j][i].set_shape('.')
		elif dir == 2:
			for i in range (y, y+rand_height):
				if i < 0 or i > self._map_size[1]-1: return False
				for j in range (x-rand_width/2, x+(rand_width+1)/2):
					if j < 0 or j > self._map_size[0]-1: return False
					if self._tiles[j][i].get_shape() != '': return False
 
			for i in range (y, y+rand_height):
				for j in range (x-rand_width/2, x+(rand_width+1)/2):
					if j == x-rand_width/2: self._tiles[j][i].set_shape('#')
					elif j == x+(rand_width-1)/2: self._tiles[j][i].set_shape('#')
					elif i == y: self._tiles[j][i].set_shape('#')
					elif i == y+(rand_height-1): self._tiles[j][i].set_shape('#')
					else: self._tiles[j][i].set_shape('.')
		elif dir == 3:
			for i in range (y-rand_height/2, y+(rand_height+1)/2):
				if i < 0 or i > self._map_size[1]-1: return False
				for j in range (x, x-rand_width, -1):
					if j < 0 or j > self._map_size[0]-1: return False
					if self._tiles[j][i].get_shape() != '': return False
 
			for i in range (y-rand_height/2, y+(rand_height+1)/2):
				for j in range (x, x-rand_width-1, -1):
					if j == x: self._tiles[j][i].set_shape('#')
					elif j == x-rand_width: self._tiles[j][i].set_shape('#')
					elif i == y-rand_height/2: self._tiles[j][i].set_shape('#')
					elif i == y+(rand_height-1)/2: self._tiles[j][i].set_shape('#')
					else: self._tiles[j][i].set_shape('.')
 
		return True
 
def main(stdscr):
	screen_y, screen_x = stdscr.getmaxyx()
 
	this_dungeon = dungeon(screen_x, screen_y, 5, 50)
	this_dungeon.draw(stdscr)
 
	stdscr.getch()
 
if __name__ == '__main__':
	curses.wrapper(main)
