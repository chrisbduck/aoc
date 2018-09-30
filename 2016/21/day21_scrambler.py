def getInts(source, split_str):
	return [int(x) for x in source.split(split_str)]

def getInt(source, split_str):
	return int(source.split(split_str)[0])

def swapPos(command, input, in_reverse):
	x, y = getInts(command, " with position ")
	x, y = min(x, y), max(x, y)
	return input[:x] + input[y] + input[x + 1 : y] + input[x] + input[y + 1 :]

def swapLetter(command, input, in_reverse):
	x, y = command.split(" with letter ")
	TEMP_CHAR = '!'
	return input.replace(x, TEMP_CHAR).replace(y, x).replace(TEMP_CHAR, y)

def rotateLeft(command, input, in_reverse):
	if in_reverse:
		return rotateRight(command, input, in_reverse=False)
	x = getInt(command, " step")
	return rotateLeftBy(x, input)

def rotateLeftBy(num, input):
	num %= len(input)
	return input[num:] + input[:num]

def rotateRight(command, input, in_reverse):
	if in_reverse:
		return rotateLeft(command, input, in_reverse=False)
	x = getInt(command, " step")
	return rotateRightBy(x, input)

def rotateRightBy(num, input):
	num %= len(input)
	return input[-num:] + input[:-num]

def rotateBasedOnPos(command, input, in_reverse):
	x = command
	pos = input.index(x)
	if not in_reverse:
		if pos >= 4:
			pos += 1
		return rotateRightBy(pos + 1, input)
	
	source_pos_map = {
		1: 0,
		3: 1,
		5: 2,
		7: 3,
		10: 4,
		2: 4,
		4: 5,
		6: 6,
		0: 7,
		}
	if pos not in source_pos_map:
		raise RuntimeError("Unhandled rotation")
	source_pos = source_pos_map[pos]
	rotate_amount = pos - source_pos
	while rotate_amount < 0:
		rotate_amount += len(input)
	return rotateLeftBy(rotate_amount, input)
	

def reverseRange(command, input, in_reverse):
	x, y = getInts(command, " through ")
	x, y = min(x, y), max(x, y)
	return input[:x] + "".join(reversed(input[x : y + 1])) + input[y + 1:]

def movePos(command, input, in_reverse):
	x, y = getInts(command, " to position ")
	if in_reverse:
		x, y = y, x
	removed = input[x]
	remaining = input[:x] + input[x + 1 :]
	return remaining[:y] + removed + remaining[y:]

ALL_OPS = \
{
	"swap position ": swapPos,
	"swap letter ": swapLetter,
	"rotate left ": rotateLeft,
	"rotate right ": rotateRight,
	"rotate based on position of letter ": rotateBasedOnPos,
	"reverse positions ": reverseRange,
	"move position ": movePos,
}

def performOp(line, input, in_reverse):
	for op in ALL_OPS:
		if line.startswith(op):
			command = line[len(op):]
			func = ALL_OPS[op]
			return func(command, input, in_reverse)
	raise ValueError("Op not recognised: " + line)

def performAllOps(op_lines, input, in_reverse=False):
	#print("Start: " + input)
	if in_reverse:
		op_lines = reversed(op_lines)
	for line in op_lines:
		#print("       " + line)
		input = performOp(line, input, in_reverse)
		#print("-----: " + input)
	return input

def runRoundTripTest(op_lines, input):
	scrambled = performAllOps(op_lines, input, in_reverse=False)
	unscrambled = performAllOps(op_lines, scrambled, in_reverse=True)
	#print(scrambled, unscrambled)
	return unscrambled == input

def runSmokeTest(op_lines, input):
	for limit in range(3, len(op_lines)):
		limited_op_lines = op_lines[:limit]
		#print("Num lines: " + str(limit))
		if not runRoundTripTest(limited_op_lines, input):
			raise RuntimeError("Broke on line {0}: '{1}'".format(len(limited_op_lines), limited_op_lines[-1]))
	print("OK")

"""input = [
	"swap position 4 with position 0",
	"swap letter d with letter b",
	"reverse positions 0 through 4",
	"rotate left 1 step",
	"move position 1 to position 4",
	"move position 3 to position 0",
	"rotate based on position of letter b",
	"rotate based on position of letter d",
	]"""
input = [line.strip() for line in open("day21_input.txt").readlines()]
#input = ["swap position 7 with position 6"]

password1 = "abcdefgh"
#password2 = "agcedfbh"
password2 = "fbgdceah"

#scrambled = performAllOps(input, password1, in_reverse=False)
#print(scrambled)
#print(performAllOps(input, scrambled, in_reverse=True))
print(performAllOps(input, password2, in_reverse=True))

#runSmokeTest(input, password1)
