def spin(command, progs):
	size = int(command)
	return progs[-size:] + progs[:-size]

def exchange(command, progs):
	pos_a, pos_b = (int(x) for x in command.split('/'))
	if pos_a > pos_b:
		pos_a, pos_b = pos_b, pos_a
	return progs[:pos_a] + progs[pos_b] + progs[pos_a + 1 : pos_b] + progs[pos_a] + progs[pos_b + 1:]

def partner(command, progs):
	prog_a, prog_b = command.split('/')
	pos_a, pos_b = progs.index(prog_a), progs.index(prog_b)
	if pos_a > pos_b:
		pos_a, pos_b = pos_b, pos_a
		prog_a, prog_b = prog_b, prog_a
	return progs[:pos_a] + prog_b + progs[pos_a + 1 : pos_b] + prog_a + progs[pos_b + 1:]


def applyMoveList(command_list, progs):
	MOVES = { 's': spin, 'x': exchange, 'p': partner }

	for command in command_list:
		progs = MOVES[command[0]](command[1:], progs)

	return progs


def getMappings(old, new):
	return [old.index(new[idx]) for idx in range(len(old))]

def applyMappings(progs, mappings, num_iterations):
	count = len(progs)
	#print(mappings)
	for itr in range(num_iterations):
		print(itr, ":", progs)
		progs = [progs[mappings[idx]] for idx in range(count)]
	#printProgs(progs)
	return progs

def printProgs(progs, prefix=""):
	print(prefix + "".join(progs))

progs = "abcdefghijklmnop"

#input = "s1,x3/4,pe/b"
input = open("2017day16_input.txt").read().strip()
move_list = input.split(',')
new_progs = applyMoveList(move_list, progs)
print(new_progs)

for itr in range(31):
	progs = applyMoveList(move_list, progs)
	printProgs(progs, "{0}: ".format(itr))

"""mappings = getMappings(progs, new_progs)
orig_mappings = mappings
print("Mappings for 1 iteration:", mappings)

applyMappings(progs, mappings, 31)"""

"""for factor in range(9):
	itr_count = 2
	new_progs = applyMappings(progs, mappings, itr_count)
	print("New: ", end='')
	printProgs(new_progs)
	alt_progs = applyMappings(progs, orig_mappings, pow(itr_count, (factor + 1)))
	print("Alt: ", end='')
	printProgs(alt_progs)
	if alt_progs != new_progs:
		raise RuntimeError("Mismatch")
	mappings = getMappings(progs, new_progs)
	print("mappings for {0} iterations:".format(pow(itr_count, factor + 1)), mappings)"""

printProgs(new_progs)

# NOT: abkjefdhcgilmnop