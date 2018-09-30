reg = { 'a': 0, 'b': 0, 'c': 1, 'd': 0 }

def consume(source, str, outarr):
	if source.startswith(str):
		outarr[0] = source[len(str):]
		return True
	return False

def getVal(src):
	return reg[src] if src in ('a', 'b', 'c', 'd') else int(src)

remainder = [None]
"""def execInstruction(line):
	print("** " + line)
	val = execInstr(line)
	print("   ", end='')
	traceRegs()
	return val"""

def execInstruction(line):
	if consume(line, "cpy ", remainder):
		src, dest = remainder[0].split(' ')
		reg[dest] = getVal(src)
	elif consume(line, "inc ", remainder):
		dest = remainder[0]
		reg[dest] += 1
	elif consume(line, "dec ", remainder):
		dest = remainder[0]
		reg[dest] -= 1
	elif consume(line, "jnz ", remainder):
		check, offset = remainder[0].split(' ')
		if getVal(check) != 0:
			return pc + int(offset)
	else:
		raise RuntimeError("Invalid instruction: " + line)
	return pc + 1

def traceRegs():
	print("a = {0}; b = {1}; c = {2}; d = {3}".format(reg['a'], reg['b'], reg['c'], reg['d']))

"""input = [
	"cpy 41 a",
	"inc a",
	"inc a",
	"dec a",
	"jnz a 2",
	"dec a"
]"""
input = open("day12_input.txt").readlines()

pc = 0
while pc < len(input):
	pc = execInstruction(input[pc].strip())

traceRegs()
