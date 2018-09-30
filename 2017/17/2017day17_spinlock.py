def createBuffer(step_size, num_iterations):
	buffer = [0]
	pos = 0
	count = 1
	while count <= num_iterations:
		pos = (pos + step_size) % count + 1
		if pos == count:
			buffer.append(count)
		else:
			buffer.insert(pos, count)
		if count % 100000 == 0:
			print('.', end='', flush=True)
		if count == num_iterations:
			arr = [str(buffer[x]) for x in range(count)]
			arr[pos] = '({0})'.format(arr[pos])
			print('[' + ", ".join(arr) + ']')
			print("**", buffer[(buffer.index(0) + 1) % len(buffer)])
		count += 1

createBuffer(337, 50000000)
