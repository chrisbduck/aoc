def countValidPassphrases(all_phrases):
	return len([phrase for phrase in all_phrases if isValidPassphrase(phrase)])

def isValidPassphrase(phrase):
	segments = ["".join(sorted(word)) for word in phrase.split()]
	set_segments = set(segments)
	return len(segments) == len(set_segments)

test_input = """
abcde fghij
abcde xyz ecdab
a ab abc abd abf abj
iiii oiii ooii oooi oooo
oiii ioii iioi iiio
"""
main_input = open("2017day4_input.txt").read()
print(countValidPassphrases(main_input.strip().split("\n")))
