import _functools

def generateHash(block_counts):
	return _functools.reduce(lambda x, y: x * 100 + y, block_counts)

def realloc(block_counts):
	known_states = {}
	iterations = 0
	while True:
		#print(block_counts)
		hash = generateHash(block_counts)
		if hash in known_states:
			return iterations - known_states[hash]
		known_states[hash] = iterations
		reallocStep(block_counts)
		iterations += 1

def reallocStep(block_counts):
	count = max(block_counts)
	index = block_counts.index(count)
	block_counts[index] = 0
	while count > 0:
		index = (index + 1) % len(block_counts)
		block_counts[index] += 1
		count -= 1
	return block_counts

input = [int(x) for x in open("2017day6_input.txt").read().split()]
#input = [0, 2, 7, 0]
print(realloc(input))
