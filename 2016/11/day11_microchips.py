import re
import queue

BOTTOM_FLOOR = 1
TOP_FLOOR = 4

def readInput(input_lines):
	floor = 1
	obj_descs = {}
	obj_floors = []
	for line in input_lines:
		for str in re.findall("([a-z]+)-compatible microchip", line):
			if str not in obj_descs:
				obj_descs[str] = len(obj_floors)
				obj_floors.append(floor)
				obj_floors.append(None)
			else:
				index = obj_descs[str]
				obj_floors[index] = floor
		for str in re.findall("([a-z]+) generator", line):
			if str not in obj_descs:
				obj_descs[str] = len(obj_floors)
				obj_floors.append(None)
				obj_floors.append(floor)
			else:
				index = obj_descs[str]
				obj_floors[index + 1] = floor
		floor += 1

	if len(obj_floors) % 2 != 0:
		raise RuntimeError("Should have an even number of floors")
	for floor in obj_floors:
		if floor is None:
			raise ValueError("Should have no entries with None")

	return obj_descs, obj_floors

def isFinished(obj_floors):
	return all([floor == TOP_FLOOR for floor in obj_floors])

def isSafe(obj_floors):
	num_types = len(obj_floors) // 2
	for type_index in range(num_types):
		chip_floor = obj_floors[type_index * 2]
		gen_floor = obj_floors[type_index * 2 + 1]
		if gen_floor == chip_floor:
			continue
		if any((obj_floors[t2_index * 2 + 1] == chip_floor for t2_index in range(num_types) if t2_index != type_index)):
			return False
	return True

def getObjectMovePossibilities(object_indices):
	num = len(object_indices)
	if num >= 1:
		for index in range(num):
			yield (object_indices[index], None)
	if num >= 2:
		for index1 in range(num):
			for index2 in range(index1 + 1, num):
				yield (object_indices[index1], object_indices[index2])

def generateMove(obj_floors, elevator_floor, num_steps, obj_index1, obj_index2, floor_offset):
	obj_floors = list(obj_floors)
	if obj_index1 is not None:
		obj_floors[obj_index1] += floor_offset
	if obj_index2 is not None:
		obj_floors[obj_index2] += floor_offset
	return (obj_floors, elevator_floor + floor_offset, num_steps + 1)

def getPossibleMoves(obj_floors, elevator_floor, num_steps):
	indices_on_floor = [index for index in range(len(obj_floors)) if obj_floors[index] == elevator_floor]
	for obj_index1, obj_index2 in getObjectMovePossibilities(indices_on_floor):
		if elevator_floor > 1:
			#print("Can move", entities[obj_index1] if obj_index1 is not None else None, entities[obj_index2] if obj_index2 is not None else None, "down")
			# Can move down
			yield generateMove(obj_floors, elevator_floor, num_steps, obj_index1, obj_index2, -1)
		if elevator_floor < 4:
			#print("Can move", entities[obj_index1] if obj_index1 is not None else None, entities[obj_index2] if obj_index2 is not None else None, "up")
			# Can move up
			yield generateMove(obj_floors, elevator_floor, num_steps, obj_index1, obj_index2, +1)

def getObjFloorsHash(obj_floors, elevator_floor):
	return elevator_floor - 1 + sum([(obj_floors[index] - 1) << ((index + 1) * 2) for index in range(len(obj_floors))])

def moveToFourthFloor(obj_descs, obj_floors):
	elevator_floor = 1
	num_steps = 0
	pending = queue.Queue()
	pending.put((obj_floors, elevator_floor, num_steps))
	visited_states = set()
	while not pending.empty():
		obj_floors, elevator_floor, num_steps = pending.get()
		#state = getStateString(obj_descs, obj_floors, elevator_floor)
		#state_hash = hash(state)
		state_hash = getObjFloorsHash(obj_floors, elevator_floor)
		if state_hash in visited_states or not isSafe(obj_floors):
			continue
		if len(visited_states) == 0:
			print(getStateString(obj_descs, obj_floors, elevator_floor))
		elif len(visited_states) % 100 == 0:
			print(str(len(visited_states)) + "...")
		visited_states.add(state_hash)
		#print(state)
		if isFinished(obj_floors):
			print(getStateString(obj_descs, obj_floors, elevator_floor))
			return num_steps
		[pending.put(move) for move in getPossibleMoves(obj_floors, elevator_floor, num_steps)]
	raise RuntimeError("No acceptable sequence")

def getDesc(obj_descs, index):
	for key in obj_descs:
		if obj_descs[key] // 2 == index // 2:
			desc = key[:2]
			return desc.upper() if index % 2 != 0 else desc
	raise ValueError("No description")

def getStateString(obj_descs, obj_floors, elevator_floor):
	state = ""
	for floor in reversed(range(BOTTOM_FLOOR, TOP_FLOOR + 1)):
		state += ("*" if elevator_floor == floor else "F") + str(floor) + ": "
		state += " ".join([getDesc(obj_descs, index) for index in range(len(obj_floors)) if obj_floors[index] == floor])
		state += "\n"
	return state + "\n"

test_input_lines = """The first floor contains a hydrogen-compatible microchip and a lithium-compatible microchip.
The second floor contains a hydrogen generator.
The third floor contains a lithium generator.
The fourth floor contains nothing relevant.""".split('\n')

input_lines_part1 = """The first floor contains a polonium generator, a thulium generator, a thulium-compatible microchip, a promethium generator, a ruthenium generator, a ruthenium-compatible microchip, a cobalt generator, and a cobalt-compatible microchip.
The second floor contains a polonium-compatible microchip and a promethium-compatible microchip.
The third floor contains nothing relevant.
The fourth floor contains nothing relevant.""".split('\n')

input_lines_part2 = """The first floor contains a polonium generator, a thulium generator, a thulium-compatible microchip, a promethium generator, a ruthenium generator, a ruthenium-compatible microchip, a cobalt generator, a cobalt-compatible microchip, an elerium generator, an elerium-compatible microchip, a dilithium generator, and a dilithium-compatible microchip.
The second floor contains a polonium-compatible microchip and a promethium-compatible microchip.
The third floor contains nothing relevant.
The fourth floor contains nothing relevant.""".split('\n')

obj_descs, obj_floors = readInput(input_lines_part2)
print(moveToFourthFloor(obj_descs, obj_floors))
