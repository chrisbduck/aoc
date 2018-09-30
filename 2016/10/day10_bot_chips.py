class Manager:
	def __init__(self, constructor):
		self.members = []
		self.member_constructor = constructor

	def getMember(self, index):
		while len(self.members) <= index:
			self.members.append(None)
		if self.members[index] is None:
			self.members[index] = self.member_constructor(index)
		return self.members[index]

class Bot:
	def __init__(self, index):
		self.values = []
		self.index = index
		self.low_out = None
		self.high_out = None

	def addValue(self, value):
		if len(self.values) >= 2:
			raise RuntimeError("Too many values on bot " + str(index))
		self.values.append(value)
		if self.canSend():
			self.sendValues()

	def setOutputs(self, low_out, high_out):
		self.low_out = low_out
		self.high_out = high_out
		if self.canSend():
			self.sendValues()

	def canSend(self):
		return len(self.values) == 2 and self.low_out is not None and self.high_out is not None

	def sendValues(self):
		low_val = min(self.values)
		high_val = max(self.values)
		if low_val == 17 and high_val == 61:
			print("** BOT INDEX: " + str(self.index))
		self.low_out.addValue(low_val)
		self.high_out.addValue(high_val)

	@staticmethod
	def a(cls):
		pass

class Output:
	def __init__(self, index):
		self.index = index

	def addValue(self, value):
		print("Output " + str(self.index) + " = " + str(value))

def consume(source, str):
	return source[len(str):] if source.startswith(str) else None

def parseOutput(source):
	bot_line = consume(source, "bot ")
	if bot_line is not None:
		return bot_mgr.getMember(int(bot_line))
	output_line = consume(source, "output ")
	if output_line is not None:
		return out_mgr.getMember(int(output_line))

def handleInstruction(line):
	value_line = consume(line, "value ")
	if value_line is not None:
		value, bot_index = [int(x) for x in value_line.split(" goes to bot ")]
		bot = bot_mgr.getMember(bot_index)
		bot.addValue(value)
		return

	bot_line = consume(line, "bot ")
	if bot_line is not None:
		bot_index_str, remainder = bot_line.split(" gives low to ")
		bot = bot_mgr.getMember(int(bot_index_str))
		low, high = [parseOutput(x) for x in remainder.split(" and high to ")]
		bot.setOutputs(low, high)




bot_mgr = Manager(Bot)
out_mgr = Manager(Output)

"""input = [
	"value 5 goes to bot 2",
	"bot 2 gives low to bot 1 and high to bot 0",
	"value 3 goes to bot 1",
	"bot 1 gives low to output 1 and high to bot 0",
	"bot 0 gives low to output 2 and high to output 0",
	"value 2 goes to bot 2"
]"""
input = open("day10_input.txt").readlines()

[handleInstruction(line) for line in input]
