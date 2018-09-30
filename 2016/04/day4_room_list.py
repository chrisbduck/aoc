import itertools

def getSectorIfRealRoom(str):
	sector, name, is_real = getRoomData(str)
	return sector if is_real else 0

def getRoomData(str):
	segments = str.split('[')
	checksum = segments[1].split(']')[0]
	segments = segments[0].split('-')
	sector = int(segments.pop())
	name_source = "-".join(segments)
	name = decodeName(name_source, sector)
	most_common_letters = getMostCommonLetters(itertools.chain(*segments))
	key = "".join(most_common_letters)
	return sector, name, checksum == key

def decodeName(name_source, sector):
	count = sector % 26
	table = buildRotationTable(count)
	return "".join([rotateLetter(x, table) for x in name_source])

def rotateLetter(letter, table):
	if letter >= 'a' and letter <= 'z':
		return table[ord(letter) - ord('a')]
	return letter

def buildRotationTable(count):
	num_table = [chr(x) for x in range(ord('a'), ord('z') + 1)]
	for x in range(count):
		num_table = num_table[1:] + [num_table[0]]
	return num_table

def getMostCommonLetters(all_letters):
	letters_count = {}
	for letter in all_letters:
		if letter in letters_count:
			letters_count[letter] += 1
		else:
			letters_count[letter] = 1
	
	most_common_letters = [x for x in letters_count.keys()]
	most_common_letters.sort(key = lambda x: letters_count[x] * 1000 - ord(x), reverse = True)
	return most_common_letters[:5]

def getSectorIDSum(str_list):
	return sum([getSectorIfRealRoom(x) for x in str_list])

def appendNameIfReal(str, out_list):
	sector, name, is_real = getRoomData(str)
	if is_real:
		out_list.append(name + "\n")
		if name == "northpole-object-storage":
			print(sector)

"""print(getSectorIDSum([
	"aaaaa-bbb-z-y-x-123[abxyz]",
	"a-b-c-d-e-f-g-h-987[abcde]",
	"not-a-real-room-404[oarel]",
	"totally-real-room-200[decoy]"
]))"""

input = open("day4_input.txt").readlines()
#input = ["qzmt-zixmtkozy-ivhz-343[zxcv]"]
#print(getSectorIDSum(input))
#print(getRoomData("qzmt-zixmtkozy-ivhz-343[zxcv]"))
output = []
[appendNameIfReal(line, output) for line in input]

output_file = open("c:\\temp\\output.txt", "w")
output_file.writelines(output)
