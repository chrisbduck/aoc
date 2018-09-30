import _functools

def getHashList(list_length, input_lengths, reps=1):
	list = [x for x in range(list_length)]
	#print("Start:", list)
	curr_pos = 0
	skip_size = 0
	for rep_index in range(reps):
		for length in input_lengths:
			#print("* Length:", length)
			if length > 1:
				# Get reversed sublist
				end_pos = min(curr_pos + length, list_length)
				sublist = list[curr_pos : end_pos]
				used_length = end_pos - curr_pos
				wrapped_length = length - used_length
				sublist.extend(list[0 : wrapped_length])
				sublist.reverse()

				# Replace existing elements
				#print("sublist:", sublist)
				#print("curr_pos:", curr_pos, "used:", used_length, "wrapped:", wrapped_length)
				new_list = sublist[used_length:]
				#print("->", new_list)
				new_list.extend(list[wrapped_length : curr_pos])
				#print("->", new_list)
				new_list.extend(sublist[:used_length])
				#print("->", new_list)
				new_list.extend(list[end_pos:])
				#print("->", new_list)
				list = new_list

			curr_pos = (curr_pos + length + skip_size) % list_length
			skip_size += 1
			#print(list)
	#print("Finish:", list)
	return list

def getAsciiList(string):
	list = [ord(char) for char in string]
	list.extend([17, 31, 73, 47, 23])
	return list

def getSparseHash(list_length, input_lengths):
	return getHashList(list_length, input_lengths, reps=64)

def xor(seq):
	return _functools.reduce(lambda x, y: x ^ y, seq)

def getDenseHash(list_length, input_lengths):
	sparse = getSparseHash(list_length, input_lengths)
	dense_digits = len(sparse) // 16
	dense_numbers = [xor(sparse[digit * 16 : (digit + 1) * 16]) for digit in range(dense_digits)]
	return "".join(["%02x" % num for num in dense_numbers])

#print(getSparseHash(5, [3, 4, 1, 5]))
#input = [int(x) for x in open("2017day10_input.txt").read().split(',')]
#print(getHashList(256, input))

input = open("2017day10_input.txt").read()
#for input in ["", "AoC 2017", "1,2,3", "1,2,4"]:
print(getDenseHash(256, getAsciiList(input)))

#print(xor([65, 27, 9, 1, 4, 3, 40, 50, 91, 7, 6, 0, 2, 5, 68, 22]))
