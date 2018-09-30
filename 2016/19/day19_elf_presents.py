NUM_ELVES = 3014387

def removeEverySecond(array, first_index_to_remove):
	if first_index_to_remove >= 2:
		raise ValueError("Invalid first index")
	return [val for index, val in enumerate(array) if index % 2 != first_index_to_remove]

def removeOpposite(array, index):
	array_len = len(array)
	opp_index = (index + array_len // 2) % array_len
	#print("Removing elf ", array[opp_index] + 1)
	del array[opp_index]
	if opp_index > index:
		index += 1
	return index % (array_len - 1)

def getLastElfPartOne():
	array = range(NUM_ELVES)
	first_index_to_remove = 1
	while len(array) > 1:
		next_first_index_to_remove = first_index_to_remove if len(array) % 2 == 0 else (1 - first_index_to_remove)
		array = removeEverySecond(array, first_index_to_remove)
		first_index_to_remove = next_first_index_to_remove
	return array[0] + 1

def getLastElfPartTwo():
	array = list(range(NUM_ELVES))
	index = 0
	rep = 0
	while len(array) > 1:
		index = removeOpposite(array, index)
		rep += 1
		if rep % 100 == 0:
			print(rep)
	return array[0] + 1

print("Last elf: " + str(getLastElfPartTwo()))
