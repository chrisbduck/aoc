class Node:
	def __init__(self, id, connections):
		self.id = id
		self.connections = connections
		self.group = None

	def resolve(self, graph):
		self.connections = [graph[x] for x in self.connections]

def parseGraph(input_lines):
	graph = {}
	for line in input_lines:
		id, remainder = line.split(" <-> ")
		graph[id] = Node(id, remainder.split(", "))
	[x.resolve(graph) for x in graph.values()]
	return graph

def getConnectedNodes(graph, id):
	root = graph[id]
	visited = set()
	upcoming = [root]
	while len(upcoming) > 0:
		node = upcoming.pop()
		if node in visited:
			continue
		visited.add(node)

		[upcoming.append(conn) for conn in node.connections]
		
	return visited

def tagConnectedNodesInGroup(group, graph, id):
	for node in getConnectedNodes(graph, id):
		if node.group is not None:
			raise RuntimeError("Already in a group")
		node.group = group

def tagAllGroupsInGraph(graph):
	group = 0
	for node in graph.values():
		if node.group is None:
			tagConnectedNodesInGroup(group, graph, node.id)
			group += 1
	return group

test_input = """
0 <-> 2
1 <-> 1
2 <-> 0, 3, 4
3 <-> 2, 4
4 <-> 2, 3, 6
5 <-> 6
6 <-> 4, 5
""".strip().split("\n")

input = [line.strip() for line in open("2017day12_input.txt").readlines()]

graph = parseGraph(input)
#print("\n".join(["{0}: {1}".format(x, ", ".join([conn.id for conn in graph[x].connections])) for x in graph]))
connected = getConnectedNodes(graph, "0")
#print(", ".join([conn.id for conn in getConnectedNodes(graph, "0")]))
print(len(connected))

num_groups = tagAllGroupsInGraph(graph)
print(num_groups)
