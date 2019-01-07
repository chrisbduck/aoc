#!/usr/bin/python3

import os
import sys

# ------------------------------------------------------------------------------
def addPort(port, port_map, index):
	if not port in port_map:
		port_map[port] = [index]
	else:
		port_map[port].append(index)

# ------------------------------------------------------------------------------
def parseComponents(input_lines):
	components = [[int(val) for val in line.split('/')] for line in input_lines]
	port_map = {}
	for index, comp in enumerate(components):
		addPort(comp[0], port_map, index)
		if comp[1] != comp[0]:
			addPort(comp[1], port_map, index)
	return components, port_map

# ------------------------------------------------------------------------------
def getAllStrengths(components, port_map, next_port, current_strength, in_use):
	if next_port in port_map:
		for index in port_map[next_port]:
			if not in_use[index]:
				in_use[index] = True
				comp = components[index]
				other_port = comp[1 if next_port == comp[0] else 0]
				new_strength = current_strength + comp[0] + comp[1]
				for strength in getAllStrengths(components, port_map, other_port, new_strength, in_use):
					yield strength
				in_use[index] = False

	yield current_strength

# ------------------------------------------------------------------------------
def getMaxStrength(components, port_map):
	in_use = [False for x in range(len(components))]
	return max(getAllStrengths(components, port_map, 0, 0, in_use))

# ------------------------------------------------------------------------------
def getLongestBridges(components, port_map, next_port, components_so_far, in_use):
	if next_port in port_map:
		for index in port_map[next_port]:
			if not in_use[index]:
				in_use[index] = True
				comp = components[index]
				other_port = comp[1 if next_port == comp[0] else 0]
				components_so_far.append(comp)
				for bridge in getLongestBridges(components, port_map, other_port, components_so_far, in_use):
					yield bridge
				components_so_far.pop()
				in_use[index] = False

	yield list(components_so_far)

# ------------------------------------------------------------------------------
def getStrength(bridge):
	return sum([comp[0] + comp[1] for comp in bridge])

# ------------------------------------------------------------------------------
def getStrengthOfLongest(components, port_map):
	in_use = [False for x in range(len(components))]
	candidates = list(getLongestBridges(components, port_map, 0, [], in_use))
	longest_length = max([len(bridge) for bridge in candidates])
	candidates = [bridge for bridge in candidates if len(bridge) == longest_length]
	return max([getStrength(bridge) for bridge in candidates])

# ------------------------------------------------------------------------------
def run(input_file_name):
	input_lines = [line for line in open(input_file_name).readlines() if line != ""]
	components, port_map = parseComponents(input_lines)
	print("Max strength:", getMaxStrength(components, port_map))
	print("Strength of longest bridge:", getStrengthOfLongest(components, port_map))

# ------------------------------------------------------------------------------

if len(sys.argv) < 2:
	raise RuntimeError("Usage: bridges.py <input_file_name>")
run(sys.argv[1])
