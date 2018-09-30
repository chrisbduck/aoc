# ------------------------------------------------------------------------------
class Prog:

	INITIAL_REGS = { 'a': 12, 'b': 0, 'c': 0, 'd': 0 }
	ZERO_REGS = { 'a': 0, 'b': 0, 'c': 0, 'd': 0 }
	TGL_REPLACEMENTS = {
		'inc': 'dec',
		'dec': 'inc',
		'tgl': 'inc',
		'jnz': 'cpy',
		'cpy': 'jnz'
	}

	def __init__(self, instruction_list, initial_reg_values):
		self.instruction_list = instruction_list
		self.initial_reg_values = initial_reg_values
		self.reg = {}
		self.pc = 0

	def getVal(self, src):
		return self.reg[src] if src in self.reg else int(src)

	def execInstruction(self):
		segments = self.instruction_list[self.pc].strip().split()
		op = getattr(self, segments[0])
		if op is None:
			raise RuntimeError("Invalid instruction: " + line)
		pc_offset = op(*segments[1:])
		return pc_offset if pc_offset is not None else 1

	def debugExecInstruction(self):
		print("** " + self.instruction_list[self.pc])
		pc_offset = self.execInstruction()
		print("   ", end='')
		traceRegs()
		return pc_offset

	def run(self):
		self.reg = { key: self.initial_reg_values[key] for key in self.initial_reg_values }
		self.pc = 0
		while self.pc < len(self.instruction_list):
			self.pc += self.execInstruction()

	def traceRegs(self):
		print("a = {0}; b = {1}; c = {2}; d = {3}".format(self.reg['a'], self.reg['b'], self.reg['c'], self.reg['d']))

	def cpy(self, src, dest):
		if dest in self.reg:
			self.reg[dest] = self.getVal(src)

	def inc(self, dest):
		if dest in self.reg:
			self.reg[dest] += 1

	def dec(self, dest):
		if dest in self.reg:
			self.reg[dest] -= 1

	def jnz(self, test, offset):
		if self.getVal(test) != 0:
			offset_val = self.getVal(offset)
			if offset_val != 0:
				return offset_val

	def tgl(self, offset):
		other_pc = self.pc + self.getVal(offset)
		if other_pc >= 0 and other_pc < len(self.instruction_list):
			orig = self.instruction_list[other_pc].strip()
			modified = self.toggleInstruction(orig)
			self.instruction_list[other_pc] = modified
			print("Toggled instruction %d from '%s' to '%s'" % (other_pc, orig, modified))

	def add(self, src, dest):
		if dest in self.reg:
			self.reg[dest] += self.getVal(src)

	def sub(self, src, dest):
		if dest in self.reg:
			self.reg[dest] -= self.getVal(src)

	def mul(self, src, dest):
		if dest in self.reg:
			self.reg[dest] *= self.getVal(src)

	def nop(self):
		pass

	def toggleInstruction(self, instr):
		for tgl in Prog.TGL_REPLACEMENTS:
			if instr.startswith(tgl):
				return instr.replace(tgl, Prog.TGL_REPLACEMENTS[tgl])
		raise RuntimeError("Toggle failed on instruction: " + instr)

# ------------------------------------------------------------------------------

def getInt(src):
	try:
		return int(src)
	except ValueError:
		return None

def checkInputResult(test_name, expected_result_in_a, instruction_list):
	print(test_name, end=": ")
	prog = Prog(instruction_list, Prog.ZERO_REGS)
	prog.run()
	if prog.reg['a'] != expected_result_in_a:
		print("FAIL.  Expected: {0}; actual: {1}".format(expected_result_in_a, self.reg['a']))
	else:
		print('OK')

# ------------------------------------------------------------------------------

checkInputResult("cpy1", 1, ["cpy 1 a"])
checkInputResult("cpy2", -1, ["cpy -1 a"])
checkInputResult("cpy3", 3, ["cpy 3 b", "cpy b a"])
checkInputResult("inc1", 1, ["cpy 0 a", "inc a"])
checkInputResult("inc2", 0, ["cpy -1 a", "inc a"])
checkInputResult("dec1", 0, ["cpy 1 a", "dec a"])
checkInputResult("dec2", -1, ["cpy 0 a", "dec a"])
checkInputResult("jnz1", 3, ["cpy 3 a", "jnz a 2", "cpy 4 a"])
checkInputResult("jnz2", 4, ["cpy 0 a", "jnz a 2", "cpy 4 a"])
checkInputResult("jnz3", 4, ["cpy 2 a", "jnz a 0", "cpy 4 a"])
checkInputResult("jnz4", 2, ["cpy 2 a", "jnz 1 2", "cpy 4 a"])
checkInputResult("tgl1", 1, ["tgl 1", "dec a"])
checkInputResult("tgl2", -1, ["tgl 1", "inc a"])
checkInputResult("tgl3", 1, ["tgl 1", "tgl a"])
checkInputResult("tgl4", 0, ["tgl 1", "tgl 1"])
checkInputResult("tgl5", 1, ["tgl 1", "jnz 1 a"])
checkInputResult("tgl6", 0, ["tgl 1", "cpy 1 a"])
checkInputResult("tgl7", 0, ["tgl 10"])
checkInputResult("tgl8", 0, ["cpy -1 b", "tgl a", "inc b", "jnz b -2"])
checkInputResult("test", 3, ["cpy 2 a", "tgl a", "tgl a", "tgl a", "cpy 1 a", "dec a", "dec a"])
checkInputResult("add1", -3, ["add -3 a"])
checkInputResult("add2", 3, ["cpy 3 b", "add b a"])
checkInputResult("add3", 15, ["cpy 10 a", "cpy 5 b", "add b a"])
checkInputResult("sub1", 2, ["sub -2 a"])
checkInputResult("sub2", -3, ["cpy 3 b", "sub b a"])
checkInputResult("sub3", 3, ["cpy 10 a", "cpy 7 b", "sub b a"])
checkInputResult("mul1", 0, ["mul 5 a"])
checkInputResult("mul2", 15, ["cpy 3 a", "mul 5 a"])
checkInputResult("mul3", -4, ["cpy 2 a", "cpy -2 b", "mul b a"])
checkInputResult("nop1", 0, ["nop"])

puzzle_input = open("day23_opt_input.txt").readlines()

prog = Prog(puzzle_input, Prog.INITIAL_REGS)
prog.run()
prog.traceRegs()
