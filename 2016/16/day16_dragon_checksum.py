input = "10011111011011001"

def buildData(data, length):
	while len(data) < length:
		data = buildIteration(data)
		print("len = " + str(len(data)))
	return data[:length]

def flip(data):
	return "".join(reversed(['1' if x == '0' else '0' for x in data]))

def buildIteration(data):
	return data + "0" + flip(data)

def getChecksum(data):
	while len(data) % 2 == 0:
		pairs = [data[x * 2] + data[x * 2 + 1] for x in range(len(data) // 2)]
		data = "".join(["1" if x == "00" or x == "11" else "0" for x in pairs])
	return data

"""def getSmartChecksum(input, length, checksum=""):
	while len(input) < length:
		checksum += getChecksum(input)
		return getChecksum(input[:length])
	return getChecksum(input) + getSmartChecksum("0" + flip(input))"""

print(getChecksum(buildData(input, 35651584)))
