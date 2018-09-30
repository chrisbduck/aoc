# Hex grid: represent as square grid for simplicity:
# 
# ---+-+---
# |  |N|  |
# ---+-+---
# |NW| |NE|
# ---+-+---
# |  |X|  |
# ---+-+---
# |SW| |SE|
# ---+-+---
# |  |S|  |
# ---------
# 

class Coord:
	def __init__(self, x=0, y=0):
		self.x = x
		self.y = y

	def move(self, dx, dy):
		self.x += dx
		self.y += dy

	def moveCombined(self, offset):
		self.x += offset[0]
		self.y += offset[1]

	def __str__(self):
		return "({0}, {1})".format(self.x, self.y)

OFFSETS = { "n": (0, 2), "s": (0, -2), "nw": (-1, 1), "sw": (-1, -1), "ne": (1, 1), "se": (1, -1) }

def followPath(path, start_pos):
	pos = Coord(start_pos.x, start_pos.y)
	max_offset = 0
	for dir in path.split(','):
		pos.moveCombined(OFFSETS[dir])
		current_offset = getShortestPathLength(start_pos, pos)
		max_offset = max(max_offset, current_offset)
	return (pos, max_offset)

def getShortestPathLength(start_pos, end_pos):
	dx = abs(end_pos.x - start_pos.x)
	dy = abs(end_pos.y - start_pos.y)
	# Each x step is required, and can subtract at least one y step, so if dx > dy, return dx;
	# otherwise one y step remains for every 2 difference after subtracting dx
	extra_y_steps = max(dy - dx, 0) // 2
	return dx + extra_y_steps

"""for input in [
		"ne,ne,ne",
		"ne,ne,sw,sw",
		"ne,ne,s,s",
		"se,sw,se,sw,sw"
	]:"""
for input in [open("2017day11_input.txt").read()]:
	pos = Coord(0, 0)
	moved_pos, max_offset = followPath(input, pos)
	num_steps = getShortestPathLength(pos, moved_pos)
	print(moved_pos, ":", num_steps, "; max:", max_offset)
