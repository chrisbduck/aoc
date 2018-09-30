
def isValidTriangle(sides):
	if len(sides) != 3:
		raise RuntimeError("Need three sides")
	if not all([type(x) is int for x in sides]):
		raise RuntimeError("Should be integers")
	largest = max(sides)
	sides.remove(largest)
	if sides[0] + sides[1] > largest:
		return True
	return False

def parseTriangleFromLine(line):
	return [int(x) for x in line.split()]

all_lines = open("day3_input.txt").readlines()
num_valid_triangles = [isValidTriangle(parseTriangleFromLine(line)) for line in all_lines].count(True)

print("Part 1: " + str(num_valid_triangles))

start_line = 0
num_valid_triangles = 0
while start_line < len(all_lines):
	triangles = [parseTriangleFromLine(all_lines[start_line + x]) for x in range(3)]
	transposed_triangles = [[triangles[y][x] for y in range(3)] for x in range(3)]
	num_valid_triangles += [isValidTriangle(triangle) for triangle in transposed_triangles].count(True)
	start_line += 3

print("Part 2: " + str(num_valid_triangles))
