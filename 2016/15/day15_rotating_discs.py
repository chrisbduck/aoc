import re

def require(str, input):
	if not input.startswith(str):
		raise ValueError("input does not start with " + str)
	return input[len(str):]

def getInt(input):
	match_str = re.match("[0-9]+", input).group(0)
	return int(match_str), input[len(match_str):]

def getIntAfterStr(str, input):
	input = require(str, input)
	return getInt(input)

def parseDiscs(input):
	discs = []
	for line in input:
		src = line
		disc_num, src = getIntAfterStr("Disc #", src)
		if disc_num != len(discs) + 1:
			raise RuntimeError("Unexpected disc number: " + line)
		num_pos, src = getIntAfterStr(" has ", src)
		start_pos, src = getIntAfterStr(" positions; at time=0, it is at position ", src)
		discs.append((num_pos, start_pos))
	return discs

def isAtPosZero(disc_info, time):
	num_pos, start_pos = disc_info
	pos = (start_pos + time) % num_pos
	return pos == 0

def getFirstOpenTime(input):
	discs = parseDiscs(input)	# num_pos, start_pos
	base_time = 0
	while True:
		if all([isAtPosZero(discs[disc_index], base_time + disc_index + 1) for disc_index in range(0, len(discs))]):
			return base_time
		base_time += 1

"""input = [
	"Disc #1 has 5 positions; at time=0, it is at position 4.",
	"Disc #2 has 2 positions; at time=0, it is at position 1."
]"""
input = open("day15_input.txt").readlines()
input.append("Disc #7 has 11 positions; at time=0, it is at position 0.")

print(getFirstOpenTime(input))
