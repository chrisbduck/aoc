test_input = """
b inc 5 if a > 1
a inc 1 if b < 5
c dec -10 if a >= 1
c inc -20 if c == 10""".strip().split('\n')

file_input = open("2017day8_input.txt").readlines()

input = file_input


def processInstructions(input_lines):
	regs = {}
	for line in input_lines:
		set_reg, cmd, diff, if_token, cmp_reg, cmp_op, cmp_val = line.split()
		diff = int(diff)
		cmp_val = int(cmp_val)
		if conditionPasses(cmp_reg, cmp_op, cmp_val, regs):
			applyCommand(set_reg, cmd, diff, regs)
	return regs

def getReg(reg, all_regs):
	return 0 if not reg in all_regs else all_regs[reg]

OPS = \
{
	">": lambda x, y: x > y,
	"<": lambda x, y: x < y,
	">=": lambda x, y: x >= y,
	"<=": lambda x, y: x <= y,
	"==": lambda x, y: x == y,
	"!=": lambda x, y: x != y
}

def conditionPasses(reg, op, cmp_val, all_regs):
	reg_val = getReg(reg, all_regs)
	op_func = OPS[op]
	return op_func(reg_val, cmp_val)

def applyCommand(reg, cmd, diff, all_regs):
	reg_val = getReg(reg, all_regs)
	new_val = reg_val + (-diff if cmd == "dec" else diff)
	all_regs[reg] = new_val
	all_regs["highest"] = max(all_regs["highest"], new_val) if "highest" in all_regs else new_val

def getLargestVal(all_regs):
	return max([all_regs[key] for key in all_regs if key != "highest"])


regs = processInstructions(input)
print(regs)
largest_val = getLargestVal(regs)
print("largest:", largest_val)
highest_val = regs["highest"]
print("highest:", highest_val)

