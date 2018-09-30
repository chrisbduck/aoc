from hashlib import md5
import unicodedata
import re

#SALT = "abc"
SALT = "jlmsuwbz"
triple = re.compile(r"(.)\1\1")

def calculateMD5(str):
	source = unicodedata.normalize("NFKD", str).encode('ascii', 'ignore')
	return md5(source).hexdigest()

def calculateStretchMD5(str):
	for itr in range(2017):
		str = calculateMD5(str)
	return str

_all_hashes = []
def getMD5(index):
	while len(_all_hashes) <= index:
		_all_hashes.append(calculateStretchMD5(SALT + str(len(_all_hashes))))
	return _all_hashes[index]

def indexIsKey(index):
	match = triple.search(getMD5(index))
	if not match:
		return False
	quin = match.group(1) * 5
	for next_index in range(index + 1, index + 1000):
		if getMD5(next_index).find(quin) >= 0:
			return True
	return False

def printNthKey(n):
	key_count = 0
	index = 0
	while True:
		if indexIsKey(index):
			key_count += 1
			print(key_count, "th key: ", index)
			if key_count == n:
				return
		index += 1

printNthKey(64)
