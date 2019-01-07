#!/usr/bin/python3

import sys
import os

# ------------------------------------------------------------------------------
class Point:
	def __init__(self, x, y, z, t):
		self.x = x
		self.y = y
		self.z = z
		self.t = t

	def __str__(self):
		return "[{0}, {1}, {2}, {3}]".format(self.x, self.y, self.z, self.t)

	def distanceTo(self, other):
		return abs(self.x - other.x) + abs(self.y - other.y) + abs(self.z - other.z) + abs(self.t - other.t)

	@staticmethod
	def read(line):
		return Point(*[int(x) for x in line.split(',')])

# ------------------------------------------------------------------------------
def buildConstellations(points):
	constellations = list(range(len(points)))
	num_points = len(points)
	for p in range(num_points):
		for other in range(num_points):
			if other == p or constellations[other] == p or constellations[p] == other:
				continue
			dist = points[other].distanceTo(points[p])
			if dist <= 3:
				# Union-find: make the root of one constellation the parent of the root of the other
				root_p = p
				while constellations[root_p] != root_p:
					root_p = constellations[root_p]
				root_other = other
				while constellations[root_other] != root_other:
					root_other = constellations[root_other]
				# Indices might be the same, in which case the next line does nothing, so we don't bother checking
				constellations[root_other] = root_p
				print("Dist from", p, "to", other, "=", dist, "=> c of", root_other, ":=", constellations[root_other])

	# Flatten
	for p in range(num_points):
		current = p
		while constellations[current] != current:
			current = constellations[current]
		constellations[p] = current

	return constellations

# ------------------------------------------------------------------------------
def run(file_name):
	input_lines = [line.strip() for line in open(file_name).readlines()]
	points = [Point.read(line) for line in input_lines if len(line) > 0]
	print("\n".join([str(index) + ": " + str(p) for index, p in enumerate(points)]))

	constellations = buildConstellations(points)
	num_constellations = len(set(constellations))
	print("Num constellations:", num_constellations, " --> ", constellations)

# ------------------------------------------------------------------------------

if len(sys.argv) < 2:
	print("Usage: constellations <test_file_name>")
	sys.exit(1)

run(sys.argv[1])
