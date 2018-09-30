# ------------------------------------------------------------------------------
class Prog:

	TGL_REPLACEMENTS = {
		'inc': 'dec',
		'dec': 'inc',
		'tgl': 'inc',
		'out': 'inc',
		'jmp': 'inc',
		'jnz': 'cpy',
		'cpy': 'jnz',
		'jz':  'cpy',
		'div': 'jnz',
		'mod': 'jnz',
	}

	def __init__(self, instruction_list, a=0, b=0, c=0, d=0, max_output_length=-1):
		self.instruction_list = instruction_list
		self.setRegs(a, b, c, d)
		self.reg = {}
		self.pc = 0
		self.output = ''
		self.max_output_length = max_output_length
		self._halt = False

	def getVal(self, src):
		return self.reg[src] if src in self.reg else int(src)

	def _getInstruction(self, index):
		instr = self.instruction_list[index].strip()
		comment_index = instr.find(';')
		if comment_index < 0:
			return instr
		return instr[:comment_index].strip()
	
	def execInstruction(self):
		segments = self._getInstruction(self.pc).split()
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
		self.initRegs()
		self.pc = 0
		self.output = ''
		self._halt = False
		while not self._halt and self.pc < len(self.instruction_list):
			self.pc += self.execInstruction()

	def setRegs(self, a=0, b=0, c=0, d=0):
		self.initial_reg_values = { 'a': a, 'b': b, 'c': c, 'd': d }
		self.initRegs()

	def initRegs(self):
		self.reg = { key: self.initial_reg_values[key] for key in self.initial_reg_values }

	def traceRegs(self):
		print("; ".join(["{0} = {1}".format(key, self.reg[key]) for key in self.reg]))

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
			return self.jmp(offset)

	def tgl(self, offset):
		other_pc = self.pc + self.getVal(offset)
		if other_pc >= 0 and other_pc < len(self.instruction_list):
			orig = self.instruction_list[other_pc].strip()
			modified = self._toggleInstruction(orig)
			self.instruction_list[other_pc] = modified
			#print("Toggled instruction %d from '%s' to '%s'" % (other_pc, orig, modified))

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

	def out(self, src):
		self.output += str(self.getVal(src))
		if self.max_output_length >= 0 and len(self.output) >= self.max_output_length:
			self.output = self.output[:self.max_output_length]
			self._halt = True

	def jz(self, test, offset):
		if self.getVal(test) == 0:
			return self.jmp(offset)

	def jmp(self, offset):
		offset_val = self.getVal(offset)
		if offset_val != 0:
			return offset_val

	def div(self, divisor, dest):
		self.reg[dest] = self.getVal(dest) // self.getVal(divisor)

	def mod(self, divisor, dest):
		self.reg[dest] = self.getVal(dest) % self.getVal(divisor)

	def _toggleInstruction(self, instr):
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

def runTest(test_name, instruction_list, max_output_length):
	print(test_name, end=": ")
	prog = Prog(instruction_list, max_output_length=max_output_length)
	prog.run()
	return prog

def checkInputResult(test_name, expected_result_in_a, instruction_list):
	prog = runTest(test_name, instruction_list, max_output_length=-1)
	if prog.reg['a'] != expected_result_in_a:
		print("FAIL.  Expected: {0}; actual: {1}".format(expected_result_in_a, self.reg['a']))
	else:
		print('OK')

def checkOutputResult(test_name, expected_result_in_output, instruction_list, max_output_length=-1):
	prog = runTest(test_name, instruction_list, max_output_length)
	if prog.output != expected_result_in_output:
		print("FAIL.  Expected: '{0}'; actual: '{1}'".format(expected_result_in_output, prog.output))
	else:
		print("OK")

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
checkInputResult("jz1", 1, ["jz 1 2", "cpy 1 a"])
checkInputResult("jz2", 0, ["jz 0 2", "cpy 1 a"])
checkInputResult("jz3", 1, ["cpy 2 b", "jz b 2", "cpy 1 a"])
checkInputResult("jz4", 0, ["cpy 0 b", "jz b 2", "cpy 1 a"])
checkInputResult("jmp1", 0, ["jmp 2", "cpy 3 a"])
checkInputResult("jmp2", 1, ["jnz a 4", "inc a", "jmp -2", "cpy 4 a"])
checkInputResult("tgl1", 1, ["tgl 1", "dec a"])
checkInputResult("tgl2", -1, ["tgl 1", "inc a"])
checkInputResult("tgl3", 1, ["tgl 1", "tgl a"])
checkInputResult("tgl4", 0, ["tgl 1", "tgl 1"])
checkInputResult("tgl5", 1, ["tgl 1", "jnz 1 a"])
checkInputResult("tgl6", 0, ["tgl 1", "cpy 1 a"])
checkInputResult("tgl7", 0, ["tgl 10"])
checkInputResult("tgl8", 0, ["cpy -1 b", "tgl a", "inc b", "jnz b -2"])
checkInputResult("tgl9", 1, ["tgl 1", "out a"])
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
checkInputResult("div1", 3, ["cpy 9 a", "div 3 a"])
checkInputResult("div2", 2, ["cpy 2 b", "cpy 4 a", "div b a"])
checkInputResult("div3", 2, ["cpy 2 b", "cpy 5 a", "div b a"])
checkInputResult("mod1", 0, ["cpy 0 a", "mod 2 a"])
checkInputResult("mod2", 1, ["cpy 1 a", "mod 2 a"])
checkInputResult("mod3", 0, ["cpy 2 a", "mod 2 a"])
checkInputResult("mod4", 1, ["cpy 7 a", "cpy 3 b", "mod b a"])
checkInputResult("nop1", 0, ["nop"])
checkOutputResult("out1", '3', ["cpy 3 a", "out a"])
checkOutputResult("out2", '24', ["cpy 4 b", "out 2", "out b"])

puzzle_input = open("day25_opt_input.txt").readlines()

puzzle_output1 = '0101011110010101011110010101011110010101011110010101011110010101011110010101011110010101011110010101'
checkOutputResult("puzzle", puzzle_output1, puzzle_input, max_output_length=len(puzzle_output1))

desired_output = "01" * 50
prog = Prog(puzzle_input, max_output_length=len(desired_output))

for a in range(10000):
	print("%d = " % a, end='')
	prog.setRegs(a=a)
	prog.run()
	print("'%s'" % prog.output)
	if prog.output == desired_output:
		print("Desired output achieved with a = %d" % a)
		break

print("Done.")

