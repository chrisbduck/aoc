#!/usr/bin/python3

import os
import re
import sys

#INPUT_FILE = "test_input.txt"
INPUT_FILE = "puzzle_input.txt"

# ------------------------------------------------------------------------------

class Network:
	def __init__(self, input_file):
		full_file_name = os.path.dirname(sys.argv[0]) + '/' + input_file
		# Use self._coords[y][x] with y = 0 at the top
		self._coords = [line[:-1] for line in open(full_file_name).readlines() if len(line) > 1]
		self._traceCoords(self._coords)
		self._outCoords = [list(line) for line in self._coords]
		self._outChar = '0'
		self._pos = None
		self._max = [len(self._coords[0]), len(self._coords)]
		self._dir = [0, 1]

	def _traceCoords(self, coords):
		for line in coords:
			print("".join(line))

	def _setOutCoord(self):
		self._outCoords[self._pos[1]][self._pos[0]] = self._outChar
		self._outChar = 'a' if self._outChar == '9' else '0' if self._outChar == 'z' else chr(ord(self._outChar) + 1)

	def run(self):
		self._pos = self._getStartPos()
		sequence = ""
		num_steps = 0
		while True:
			#print(self._pos, end=" ")
			if not self._coordExists(self._pos[0], self._pos[1]):
				break
			
			self._setOutCoord()

			char = self._getCurrentChar()
			if not self._charMatchesCurrentDir(char):
				if char == '+':
					new_dir = self._getNewDir()
					if new_dir is not None:
						self._dir = new_dir
						print(self._pos, ": Turned to new dir", self._dir)
				elif re.match("[A-Z]", char):
					print(self._pos, ": Adding char", char)
					sequence += char
				elif char == ' ':
					# Stop on an empty space.  Count the last step to make up for the first step onto the board
					break
			
			self._pos = [self._pos[0] + self._dir[0], self._pos[1] + self._dir[1]]
			num_steps += 1

		print("")
		self._traceCoords(self._outCoords)
		return (sequence, num_steps)
		
	def _getStartPos(self):
		for index, char in enumerate(self._coords[0]):
			if char == "|":
				return [index, 0]
		raise RuntimeError("No starting position found")

	def _coordExists(self, x, y):
		return x >= 0 and x < self._max[0] and y >= 0 and y < self._max[1]

	def _getCheckedCharAt(self, x, y):
		return self._getCharAt(x, y) if self._coordExists(x, y) else " "

	def _getCharAt(self, x, y):
		return self._coords[y][x]

	def _getCurrentChar(self):
		return self._getCharAt(self._pos[0], self._pos[1])

	def _charMatchesCurrentDir(self, char):
		return char == ("-" if self._dir[0] != 0 else "|")

	def _getNewDir(self):
		# If going horizontally, choose a vertical move if possible
		if self._dir[0] != 0:
			for y_offset in (-1, +1):
				if re.match(r"[A-Z\+\|]", self._getCheckedCharAt(self._pos[0], self._pos[1] + y_offset)):
					return [0, y_offset]
		# Otherwise choose a horizontal move if possible
		else:
			for x_offset in (-1, +1):
				if re.match(r"[A-Z\+\-]", self._getCheckedCharAt(self._pos[0] + x_offset, self._pos[1])):
					return [x_offset, 0]
		return None

# ------------------------------------------------------------------------------

def main():
	network = Network(INPUT_FILE)
	print(network.run())

# ------------------------------------------------------------------------------

main()
