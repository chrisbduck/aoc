import sys

# ------------------------------------------------------------------------------

class Prog:
	def __init__(self, instruction_lines):
		self._regs = {}
		self._instructions = [line.split() for line in instruction_lines]
		self._lastFreq = None
		self._pc = None
		self._iterations = 0

	def _getValue(self, text):
		if text.isdigit() or text[0] == "-":
			return int(text)
		return self._regs[text] if text in self._regs else 0

	def _trace(self, *args):
		print(self._pc, ":", " ".join(self._instructions[self._pc]), "\t=>", *args)

	def run(self):
		self._pc = 0
		while True:
			instr = self._instructions[self._pc]
			op = getattr(self, instr[0])
			if op(*instr[1:]):
				return
			self._pc += 1
			self._iterations += 1
			if self._iterations % 20 == 0:
				input()
	
	def snd(self, reg):
		self._lastFreq = self._getValue(reg)
		self._trace("playing sound with freq =", self._lastFreq)

	def set(self, dest, src):
		self._regs[dest] = self._getValue(src)
		self._trace(dest, ":=", self._regs[dest])

	def add(self, dest, src):
		self._regs[dest] = self._getValue(dest) + self._getValue(src)
		self._trace(dest, ":=", self._regs[dest])

	def mul(self, dest, src):
		self._regs[dest] = self._getValue(dest) * self._getValue(src)
		self._trace(dest, ":=", self._regs[dest])

	def mod(self, dest, src):
		self._regs[dest] = self._getValue(dest) % self._getValue(src)
		self._trace(dest, ":=", self._regs[dest])

	def rcv(self, reg):
		if self._getValue(reg) == 0:
			self._trace(reg, "is zero")
		else:
			print("recovered freq", self._lastFreq)
			return True		# terminate
		
	def jgz(self, test, offset):
		if self._getValue(test) <= 0:
			self._trace(test, "is not greater than zero")
		else:
			new_pc = self._pc + int(offset) - 1
			self._trace("jumping to", new_pc + 1)
			self._pc = new_pc

# ------------------------------------------------------------------------------

def main():
	if len(sys.argv) < 2:
		print("Usage: python duet.py <inputfile>")
		return

	input_lines = open(sys.argv[1]).readlines()
	Prog(input_lines).run()

# ------------------------------------------------------------------------------

main()