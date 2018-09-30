from queue import Queue

# ------------------------------------------------------------------------------
class Map:

	SPACE = '.'
	WALL = '#'
	VISITED = '*'

	def __init__(self, input_lines):
		self.build(input_lines)

	def build(self, input_lines):
		self.x_size = len(input_lines[0].strip())
		self.y_size = len(input_lines)
		self.map = [[Map.SPACE for y in range(self.y_size)] for x in range(self.x_size)]
		self.points = []
		for y in range(self.y_size):
			line = input_lines[y].strip()
			for x in range(self.x_size):
				char = line[x]
				if char.isdigit():
					digit = ord(char) - ord('0')
					while len(self.points) <= digit:
						self.points.append(None)
					self.points[digit] = (x, y)
				self.map[x][y] = char

	def print(self):
		file = open('c:\\temp\\map.txt', 'w')
		for y in range(self.y_size):
			for x in range(self.x_size):
				print(self.map[x][y], end='', file=file)
			print('', file=file)
		print('Points: ' + str(self.points), file=file)

	def getDistancesBetweenAllPoints(self):
		return [self._getDistanceFromPointToOthers(index) for index in range(len(self.points))]

	def _getDistanceFromPointToOthers(self, point_index):
		temp_map = [[self.map[x][y] for y in range(self.y_size)] for x in range(self.x_size)]
		pending_locs = Queue()
		pending_locs.put((self.points[point_index], 0))
		num_pending_points = len(self.points)
		point_distances = [None for point in self.points]

		while not pending_locs.empty():
			(x, y), dist = pending_locs.get()
			char = temp_map[x][y]
			if char == Map.WALL or char == Map.VISITED:
				continue

			temp_map[x][y] = Map.VISITED
			for point_index in range(len(point_distances)):
				if point_distances[point_index] is None and self.points[point_index] == (x, y):
					point_distances[point_index] = dist
					num_pending_points -= 1
					if num_pending_points == 0:
						if any([dist is None for dist in point_distances]):
							raise RuntimeError("Not all points were found")
						return point_distances

			for adj_x, adj_y in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
				if adj_x >= 0 and adj_x < self.x_size and adj_y >= 0 and adj_y < self.y_size:
					char = temp_map[adj_x][adj_y]
					if char != Map.WALL and char != Map.VISITED:
						pending_locs.put(((adj_x, adj_y), dist + 1))

		raise RuntimeError("Not all points were accessible")

	def _printTempMap(self, temp_map):
		orig_map = self.map
		self.map = temp_map
		self.print()
		self.map = orig_map

# ------------------------------------------------------------------------------
class Graph:

	NO_MIN_STEPS = 100000000

	def __init__(self, map):
		self.distances = map.getDistancesBetweenAllPoints()
		self.num_points = len(self.distances)
		self.checkMatch()

	def checkMatch(self):
		for first_index in range(self.num_points):
			for second_index in range(self.num_points):
				dist_one_way = self.distances[first_index][second_index]
				dist_other_way = self.distances[second_index][first_index]
				if dist_one_way != dist_other_way:
					raise RuntimeError("Distance mismatch")

	def print(self):
		for first_index in range(self.num_points):
			for second_index in range(self.num_points):
				print('%3d ' % self.distances[first_index][second_index], end='')
			print('')

	def getFewestStepsToVisitAll(self, start_index, return_to_index=-1):
		visited = [False for x in range(self.num_points)]
		visited[start_index] = True
		return self._getFewestStepsToVisit(visited, start_index, return_to_index)

	def _getFewestStepsToVisit(self, visited, start_index, return_to_index):
		min_steps = Graph.NO_MIN_STEPS
		for index in range(self.num_points):
			if not visited[index]:
				visited[index] = True
				steps = self.distances[start_index][index] + self._getFewestStepsToVisit(visited, index, return_to_index)
				min_steps = min(min_steps, steps)
				visited[index] = False
		
		if min_steps != Graph.NO_MIN_STEPS:
			return min_steps
		if return_to_index == -1:
			return 0
		return self.distances[start_index][0]

# ------------------------------------------------------------------------------

input_lines = open('day24_input.txt').readlines()
map = Map(input_lines)
graph = Graph(map)
map.print()
print('')
print(graph.getFewestStepsToVisitAll(start_index=0, return_to_index=0))
