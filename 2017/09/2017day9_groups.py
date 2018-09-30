import re

def getScore(input):
	initial = input
	# Remove escape sequences
	input = re.sub("!(.)", "", input)
	# Remove garbage
	input = re.sub("<[^>]*>", "", input)
	# Remove commas for simplicity
	input = re.sub(",", "", input)
	# For each open brace, inc the active count
	# For each close brace, add the active count to the score, and dec the active count
	active = 0
	score = 0
	for char in input:
		if char == '{':
			active += 1
		elif char == '}':
			score += active
			active -= 1
	print("\t{0}: {1}".format(initial, score))
	return score

def countNonCancelled(input):
	initial = input
	# Remove escape sequences
	input = re.sub("!(.)", "", input)
	# Count garbage
	count = sum([len(matchstr) - 2 for matchstr in re.findall("<[^>]*>", input)])
	print("\t{0}: {1}".format(initial, count))
	return count

"""
test_input_lines = {
	"{}": 1,
	"{{{}}}": 6,
	"{{},{}}": 5,
	"{{{},{},{{}}}}": 16,
	"{<a>,<a>,<a>,<a>}": 1,
	"{{<ab>},{<ab>},{<ab>},{<ab>}}": 9,
	"{{<!!>},{<!!>},{<!!>},{<!!>}}": 9,
	"{{<a!>},{<a!>},{<a!>},{<ab>}}": 3
}

for line in test_input_lines:
	score = getScore(line)
	if score != test_input_lines[line]:
		raise RuntimeError("Mismatched score: expected {0}; got {1}".format(test_input_lines[line], score))

print(getScore(open("2017day9_input.txt").read()))
"""

test_input_lines = {
	'<>': 0,
	'<random characters>': 17,
	'<<<<>': 3,
	'<{!>}>': 2,
	'<!!>': 0,
	'<!!!>>': 0,
	'<{o"i!a,<{i<a>': 10
}

for line in test_input_lines:
	count = countNonCancelled(line)
	if count != test_input_lines[line]:
		raise RuntimeError("Mismatched count: expected {0}; got {1}".format(test_input_lines[line], score))

print(countNonCancelled(open("2017day9_input.txt").read()))