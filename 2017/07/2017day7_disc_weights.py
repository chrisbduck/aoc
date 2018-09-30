class Prog:
	def __init__(self, line):
		segments = line.split()
		self.name = segments[0]
		self.weight = int(segments[1][1:-1])
		self.tree_weight = 0
		self.next_ids = [id.replace(',', '') for id in segments[3:]]
		self.next = []
		self.prev = []

	def resolve(self, map):
		self.next = [map[id] for id in self.next_ids]
		[next.addPrev(self) for next in self.next]

	def addPrev(self, prev):
		self.prev.append(prev)

	def calculateTreeWeight(self):
		self.tree_weight = self.weight + sum([next.calculateTreeWeight() for next in self.next])
		return self.tree_weight

	def findUnbalancedSubtreeIntendedWeight(self):
		print(self.name, self.tree_weight)
		if self.next == []:
			return None
		for next in self.next:
			result = next.findUnbalancedSubtreeIntendedWeight()
			if result is not None:
				return result
		first_weight = self.next[0].tree_weight
		for index in range(1, len(self.next)):
			next_weight = self.next[index].tree_weight
			if next_weight != first_weight:
				# if index is 1 and val 2 == val 1, val 0 is the odd one out; otherwise this index is
				mismatch_index = 0 if index == 1 and self.next[1].tree_weight == self.next[2].tree_weight else index
				match_index = 1 if mismatch_index == 0 else 0
				diff = self.next[match_index].tree_weight - self.next[mismatch_index].tree_weight
				return self.next[mismatch_index].weight + diff

	def __str__(self):
		return "name = {0}; weight = {1}; next = {2}; prev = {3}".format(self.name, self.weight, ", ".join([next.name for next in self.next]), ", ".join([prev.name for prev in self.prev]))

def buildGraph(all_lines):
	all_progs = [Prog(line) for line in all_lines]
	prog_map = {prog.name: prog for prog in all_progs}
	[prog.resolve(prog_map) for prog in all_progs]
	root = [prog for prog in all_progs if prog.prev == []][0]
	root.calculateTreeWeight()
	return root


# test input
input = """pbga (66)
xhth (57)
ebii (61)
havc (66)
ktlj (57)
fwft (72) -> ktlj, cntj, xhth
qoyq (66)
padx (45) -> pbga, havc, qoyq
tknk (41) -> ugml, padx, fwft
jptl (61)
ugml (68) -> gyxo, ebii, jptl
gyxo (61)
cntj (57)""".split("\n")

input = open("2017day7_input.txt").readlines()
root = buildGraph(input)
weight = root.findUnbalancedSubtreeIntendedWeight()
print(weight)
