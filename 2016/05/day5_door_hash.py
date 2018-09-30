from hashlib import md5
import unicodedata

def calculateMD5(str):
	source = unicodedata.normalize("NFKD", str).encode('ascii', 'ignore')
	return md5(source).hexdigest()

def findPassword(baseStr):
	index = 0
	password = ""
	while True:
		indexed_str = baseStr + str(index)
		hash = calculateMD5(indexed_str)
		if hash[:5] == "00000":
			password += hash[5]
			if len(password) == 8:
				return password
		if index % 1000 == 0:
			print(str(index) + "... " + password)
		index += 1


def findComplexPassword(baseStr):
	index = 0
	password = "        "
	while True:
		indexed_str = baseStr + str(index)
		hash = calculateMD5(indexed_str)
		if hash[:5] == "00000" and hash[5] >= '0' and hash[5] <= '7':
			position = int(hash[5])
			if password[position] == ' ':
				password = password[:position] + hash[6] + password[position + 1:]
				if password.find(" ") == -1:
					return password
		if index % 1000 == 0:
			print(str(index) + "... " + password)
		index += 1


print(findComplexPassword("ffykfhsq"))
