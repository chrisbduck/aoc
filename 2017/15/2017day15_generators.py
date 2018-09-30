def getNextValueA(current):
	while True:
		current = (current * 16807) % 0x7FFFFFFF
		if (current & 3) == 0:
			return current

def getNextValueB(current):
	while True:
		current = (current * 48271) % 0x7FFFFFFF
		if (current & 7) == 0:
			return current

def checkNextValues(a, b, itr_count):
	match_count = 0
	for itr in range(itr_count):
		a = getNextValueA(a)
		b = getNextValueB(b)
		match = (a & 0xFFFF) == (b & 0xFFFF)
		#print(a, b, match)
		if match:
			match_count += 1
		if itr % 1000000 == 0 and itr > 0:
			print(".", end='', flush=True)
	return match_count

# test input
"""
a = 65
b = 8921
match_count = checkNextValues(a, b, itr_count=5)
print(match_count)
"""

# puzzle input

a = 618
b = 814
match_count = checkNextValues(a, b, itr_count=5000000)
print(match_count)
