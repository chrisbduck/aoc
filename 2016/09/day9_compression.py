def decompress(source):
	pos = 0
	end_pos = pos + len(source)
	output = ""

	while pos < end_pos:
		if source[pos] != '(':
			if not source[pos].isspace():
				output += source[pos]
			pos += 1
			continue
		
		end_bracket_pos = source.find(')', pos + 1)
		compression_seq = source[pos + 1 : end_bracket_pos]
		pos = end_bracket_pos + 1

		num_chars, num_repeats = [int(x) for x in compression_seq.split('x')]
		repeat_seq = source[pos : pos + num_chars]
		pos += num_chars

		output += repeat_seq * num_repeats

	return output

def getDecompressedLength(source):
	out_length = 0
	pos = 0
	end_pos = pos + len(source)
	while pos < end_pos:
		if source[pos] != '(':
			if not source[pos].isspace():
				out_length += 1
			pos += 1
			continue
		
		end_bracket_pos = source.find(')', pos + 1)
		compression_seq = source[pos + 1 : end_bracket_pos]
		pos = end_bracket_pos + 1

		num_chars, num_repeats = [int(x) for x in compression_seq.split('x')]
		repeat_seq = source[pos : pos + num_chars]
		repeat_seq_len = getDecompressedLength(repeat_seq)
		pos += num_chars

		out_length += repeat_seq_len * num_repeats

	return out_length


input = "".join(open("day9_input.txt").readlines())
print(getDecompressedLength(input))
