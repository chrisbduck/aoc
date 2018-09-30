TRAP_CHAR = '^'
SAFE_CHAR = '.'

def isTrap(x, row_above_is_trap):
	left_is_trap = False if x == 0 else row_above_is_trap[x - 1]
	right_is_trap = False if x >= len(row_above_is_trap) - 1 else row_above_is_trap[x + 1]
	return left_is_trap != right_is_trap

def generateNextRow(row_above_is_trap):
	return [isTrap(x, row_above_is_trap) for x in range(len(row_above_is_trap))]

def readInput(line):
	return [c == TRAP_CHAR for c in line]

def writeLine(row_is_trap):
	print("".join([TRAP_CHAR if is_trap else SAFE_CHAR for is_trap in row_is_trap]))

def countSafeTilesInLine(row_is_trap):
	return len([1 for is_trap in row_is_trap if not is_trap])

input = "......^.^^.....^^^^^^^^^...^.^..^^.^^^..^.^..^.^^^.^^^^..^^.^.^.....^^^^^..^..^^^..^^.^.^..^^..^^^.."
num_safe_tiles = 0
row = readInput(input)
for row_num in range(400000):
	#writeLine(row)
	num_safe_tiles += countSafeTilesInLine(row)
	row = generateNextRow(row)
	if row_num % 1000 == 0:
		print(row_num)

print(num_safe_tiles)
