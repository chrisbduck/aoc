import collections
from bisect import bisect_left

NODE_START = "/dev/grid/node-x"

Node = collections.namedtuple('Node', ['x', 'y', 'used', 'avail'])

def readNodes(input_lines):
	all_nodes = []
	for line in input_lines:
		if not line.startswith(NODE_START):
			continue
		line = line[len(NODE_START):]
		segments = line.split()
		x, y = [int(val) for val in segments[0].split('-y')]
		used = int(segments[2].split('T')[0])
		avail = int(segments[3].split('T')[0])
		all_nodes.append(Node(x, y, used, avail))
	
	max_x = max(all_nodes, key = lambda node: node.x).x
	empty = [node for node in all_nodes if node.used == 0][0]
	goal = [node for node in all_nodes if node.x == max_x and node.y == 0][0]
	return all_nodes, empty, goal

def buildNodeArray(all_nodes):
	max_x = max(all_nodes, key = lambda node: node.x).x
	max_y = max(all_nodes, key = lambda node: node.y).y
	array = [[None for y in range(max_y + 1)] for x in range(max_x + 1)]
	for node in all_nodes:
		array[node.x][node.y] = node
	return array

def sortNodesByIncreasingAvail(all_nodes):
	return sorted(all_nodes, key=lambda node: node[3])

def getAllAvails(all_nodes):
	return [node.avail for node in all_nodes]

def countNodesWithAtLeastGivenAvail(required_avail, all_avails):
	index_for_avail = bisect_left(all_avails, required_avail)
	return len(all_avails) - index_for_avail

def countViablePairs(all_nodes):
	sorted_nodes = sortNodesByIncreasingAvail(all_nodes)
	all_avails = getAllAvails(sorted_nodes)
	num_pairs = 0
	for node in sorted_nodes:
		if node.used == 0:
			continue
		nodes_with_min_avail = countNodesWithAtLeastGivenAvail(node.used, all_avails)
		if node.avail >= node.used:
			nodes_with_min_avail -= 1
		num_pairs += nodes_with_min_avail
	return num_pairs

def plotNodes(array, empty, goal):
	for y in range(len(array[0])):
		for x in range(len(array)):
			node = array[x][y]
			sym = 'G' if node is goal else '_' if node is empty else '#' if node.used > empty.avail else '.'
			print(sym, end='')
		print('')

def plotSpace(array, empty, goal):
	for y in range(len(array[0])):
		for x in range(len(array)):
			node = array[x][y]
			print("%2d/%2d " % (node.used, (node.avail + node.used)), end='')
			#sym = 'G' if node is goal else '_' if node is empty else '#' if node.used / node.avail > 0.5 else '*'
			#print(sym, end='')
		print('')

def moveEmptyToLeftOfGoal(array, empty, goal):
	empty = Node(7, 4, empty.used, empty.avail)
	start_moves = 12
	target_x = goal.x - 1
	target_y = 0
	x_dist = abs(target_x - empty.x)
	y_dist = abs(target_y - empty.y)
	empty = Node(target_x, target_y, empty.used, empty.avail)
	return x_dist + y_dist + start_moves, empty

def moveGoalToLeft(array, empty, goal):
	if empty.x != goal.x - 1 or empty.y != goal.y:
		raise ValueError("Empty in wrong spot")
	goal = Node(empty.x, goal.y, goal.used, goal.avail)
	if goal.x == 0:
		return 1, empty, goal
	empty = Node(goal.x - 1, empty.y, empty.used, empty.avail)
	return 5, empty, goal

def moveGoalToTopLeft(array, empty, goal):
	num_moves, empty = moveEmptyToLeftOfGoal(array, empty, goal)
	while goal.x != 0:
		extra_moves, empty, goal = moveGoalToLeft(array, empty, goal)
		num_moves += extra_moves
	return num_moves

input = open("day22_input.txt").readlines()
#input = ["/dev/grid/node-x0-y0     93T   71T    22T   76%"]

all_nodes, empty, goal = readNodes(input)
array = buildNodeArray(all_nodes)
plotNodes(array, empty, goal)
print('')
print("Empty:", empty)
print("Goal:", goal)
#print(countViablePairs(all_nodes))
print(moveGoalToTopLeft(array, empty, goal))
