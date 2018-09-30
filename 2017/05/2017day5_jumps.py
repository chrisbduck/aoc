def processJumps(jump_list):
	index = 0
	jump_count = 0
	while index >= 0 and index < len(jump_list):
		#print(jump_count, jump_list)
		next_index = index + jump_list[index]
		adjustment = -1 if jump_list[index] >= 3 else +1
		jump_list[index] += adjustment
		index = next_index
		jump_count += 1
	return jump_count

test_input = """
0
3
0
1
-3"""
main_input = open("2017day5_input.txt").read()

input = [int(x) for x in main_input.strip().split("\n")]
print(processJumps(input))
