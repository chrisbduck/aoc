from hashlib import md5
import unicodedata

def calculateMD5(str):
	source = unicodedata.normalize("NFKD", str).encode('ascii', 'ignore')
	return md5(source).hexdigest()

# x = 0-3; y = 0-3
# start = 0, 0; end = 3, 3

MIN = 0
MAX = 3

def isDoorOpen(code):
	return "bcdef".find(code) >= 0

def getPossibleMoves(pos, seq, puzzle_input):
	moves = []
	hash = calculateMD5(puzzle_input + seq)
	if pos[1] > MIN and isDoorOpen(hash[0]):
		moves.append(('U', (pos[0], pos[1] - 1)))
	if pos[1] < MAX and isDoorOpen(hash[1]):
		moves.append(('D', (pos[0], pos[1] + 1)))
	if pos[0] > MIN and isDoorOpen(hash[2]):
		moves.append(('L', (pos[0] - 1, pos[1])))
	if pos[0] < MAX and isDoorOpen(hash[3]):
		moves.append(('R', (pos[0] + 1, pos[1])))
	return moves

def findShortestPath(start_pos, puzzle_input):
	states = []
	states.insert(0, (start_pos, ""))
	while len(states) > 0:
		pos, move_sequence = states.pop()
		if pos[0] == MAX and pos[1] == MAX:
			return move_sequence
		for move in getPossibleMoves(pos, move_sequence, puzzle_input):
			states.insert(0, (move[1], move_sequence + move[0]))
	raise RuntimeError("No valid path")

def findLongestPath(start_pos, puzzle_input):
	path = None
	states = []
	states.insert(0, (start_pos, ""))
	while len(states) > 0:
		pos, move_sequence = states.pop()
		if pos[0] == MAX and pos[1] == MAX:
			path = move_sequence
			continue
		for move in getPossibleMoves(pos, move_sequence, puzzle_input):
			states.insert(0, (move[1], move_sequence + move[0]))
	return path

#print(findShortestPath((MIN, MIN), "pgflpeqp"))
print(len(findLongestPath((MIN, MIN), "pgflpeqp")))