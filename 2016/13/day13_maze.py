PUZZLE_INPUT = 1364
#PUZZLE_INPUT = 10

def generateMaze(width, height):
	return [[generateCoord(x, y) for y in range(height)] for x in range(width)]

def generateCoord(x, y):
	val = x*x + 3*x + 2*x*y + y + y*y + PUZZLE_INPUT
	num_1_bits = bin(val).count("1")
	return '.' if num_1_bits % 2 == 0 else '#'

def showMaze(maze):
	width = len(maze)
	height = len(maze[0])
	for y in range(height):
		for x in range(width):
			print(maze[x][y], end='')
		print('')

def traverseMaze(maze, start_x, start_y, target_x, target_y):
	width = len(maze)
	height = len(maze[0])
	if maze[start_x][start_y] != '.':
		raise RuntimeError("Can't start on a wall")

	distinct_count = 0
	pending = [(start_x, start_y, -1)]
	while len(pending) > 0:
		x, y, dist = pending.pop()
		if maze[x][y] != '.':
			continue
		maze[x][y] = 'O'
		dist += 1
		distinct_count += 1
		if dist == 50:
			continue
		"""if x == target_x and y == target_y:
			showMaze(maze)
			print("dist = " + str(dist))
			return"""
		if x > 0:
			pending.insert(0, (x - 1, y, dist))
		if x < width - 1:
			pending.insert(0, (x + 1, y, dist))
		if y > 0:
			pending.insert(0, (x, y - 1, dist))
		if y < height - 1:
			pending.insert(0, (x, y + 1, dist))
	showMaze(maze)
	print("Distinct: " + str(distinct_count))

maze = generateMaze(40, 50)
#showMaze(maze)
traverseMaze(maze, 1, 1, 31, 39)
