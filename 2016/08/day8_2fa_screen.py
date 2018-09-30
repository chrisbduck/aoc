WIDTH = 50
HEIGHT = 6

screen = [[False for y in range(HEIGHT)] for x in range(WIDTH)]

#input = ["rect 3x2", "rotate column x=1 by 1", "rotate row y=0 by 4", "rotate column x=1 by 1"]
input = open('day8_input.txt').readlines()

def rect(scr, width, height):
	for x in range(width):
		for y in range(height):
			scr[x][y] = True

def rotateRow(scr, y, amount):
	source = [scr[x][y] for x in range(WIDTH)]
	for x in range(WIDTH):
		source_x = (x - amount) % WIDTH
		scr[x][y] = source[source_x]

def rotateCol(scr, x, amount):
	source = [scr[x][y] for y in range(HEIGHT)]
	for y in range(HEIGHT):
		source_y = (y - amount) % HEIGHT
		scr[x][y] = source[source_y]

def consume(source, str):
	return source[len(str):] if source.startswith(str) else None

def apply(scr, line):
	rect_str = consume(line, "rect ")
	if rect_str is not None:
		width, height = rect_str.split('x')
		rect(scr, int(width), int(height))
		return
	col_str = consume(line, "rotate column x=")
	if col_str is not None:
		x, amount = col_str.split(' by ')
		rotateCol(scr, int(x), int(amount))
		return
	row_str = consume(line, "rotate row y=")
	if row_str is not None:
		y, amount = row_str.split(' by ')
		rotateRow(scr, int(y), int(amount))
		return
	print("Unknown input: " + line)

def show(scr):
	for y in range(HEIGHT):
		for x in range(WIDTH):
			print('#' if scr[x][y] else '.', end = '')
		print('')

def countPixels(scr):
	return sum([sum(scr[x]) for x in range(WIDTH)])

[apply(screen, line) for line in input]
show(screen)
print("Total: " + str(countPixels(screen)))