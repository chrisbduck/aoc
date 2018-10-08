import sys
import threading

#
# Part 1 is in duet_part_1.py.  This is part 2.  I copied and modified the code since there's no real need to
# maintain it anyway.
#

# ------------------------------------------------------------------------------

class Prog:
	def __init__(self, instruction_lines, prog_num):
		self._regs = {}
		self._instructions = [line.split() for line in instruction_lines]
		self._pc = None
		self._prog_num = prog_num
		self._regs['p'] = prog_num
		self._other = None
		self._rcv_queue = []
		self._is_waiting = False
		self._terminate = False
		self._send_count = 0

	def _getValue(self, text):
		if text.isdigit() or text[0] == "-":
			return int(text)
		return self._regs[text] if text in self._regs else 0

	def _trace(self, *args):
		print("[{0}] {1:>2}:  {2:10} =>".format(self._prog_num, self._pc, " ".join(self._instructions[self._pc])), *args)

	def setOtherProg(self, other_prog):
		self._other = other_prog

	def postMessage(self, value):
		self._other.receiveMessage(value)
		self._send_count += 1

	def receiveMessage(self, value):
		self._rcv_queue.append(value)

	def isWaiting(self):
		return self._is_waiting

	def terminate(self):
		self._terminate = True

	def getSendCount(self):
		return self._send_count

	def run(self):
		self._pc = 0
		while not self._terminate:
			instr = self._instructions[self._pc]
			op = getattr(self, instr[0])
			op(*instr[1:])
			self._pc += 1
	
	def snd(self, reg):
		value = self._getValue(reg)
		self.postMessage(value)
		self._trace("posted value", value)

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
		if len(self._rcv_queue) == 0:
			self._is_waiting = True
			if self._other.isWaiting():
				self._trace("deadlock")
				self._other.terminate()
				self.terminate()
				return
			self._trace("waiting for data")
			# Busy wait; non-optimal but no need to optimize here
			while len(self._rcv_queue) == 0:
				if self._terminate:
					return
			self._is_waiting = False
		value = self._rcv_queue[0]
		del self._rcv_queue[0]
		self._regs[reg] = value
		self._trace(reg, ":=", value)
		
	def jgz(self, test, offset):
		if self._getValue(test) <= 0:
			self._trace(test, "is not greater than zero")
		else:
			new_pc = self._pc + self._getValue(offset) - 1
			self._trace("jumping to", new_pc + 1)
			self._pc = new_pc

# ------------------------------------------------------------------------------

def main():
	if len(sys.argv) < 2:
		print("Usage: python duet.py <inputfile>")
		return

	input_lines = open(sys.argv[1]).readlines()
	prog0 = Prog(input_lines, prog_num=0)
	prog1 = Prog(input_lines, prog_num=1)
	prog0.setOtherProg(prog1)
	prog1.setOtherProg(prog0)
	thread = threading.Thread(target=lambda: prog1.run())
	thread.start()
	prog0.run()
	thread.join()
	print("Prog 1 send count:", prog1.getSendCount())

# ------------------------------------------------------------------------------

main()
