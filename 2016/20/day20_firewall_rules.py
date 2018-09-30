def findStartIndex(all_ranges, start):
	if len(all_ranges) == 0:
		return 0
	start_index = 0
	end_index = len(all_ranges)
	while start_index < end_index:
		mid_index = (start_index + end_index) // 2
		if all_ranges[mid_index][0] <= start:
			if start_index == mid_index:
				return start_index + 1
			start_index = mid_index
		else:
			if end_index == mid_index:
				return end_index - 1
			end_index = mid_index
	return (start_index + 1) if all_ranges[start_index][0] < start else start_index

def addRange(all_ranges, line):
	start, end = [int(x) for x in line.split('-')]
	start = int(start)
	end = int(end) + 1
	"""# Find the start of the range
	index = bisect(all_ranges, start)
	if index > 0:
		if all_ranges[index - 1][0] == start:
			# Start overlaps exactly with an existing start.  Find the max of the ends
			end = max(end, all_ranges[index - 1][1])
			# If the end overlaps the start of the next range, replace the previous one with the max end and remove the next entry;
			# otherwise just replace the previous one with the max
			if index < len(all_ranges) and end >= all_ranges[index][0]:
				end = max(end, all_ranges[index][1])
				del all_ranges[index]
			index -= 1
		elif all_ranges[index - 1][1] >= start:
			# Start overlaps with previous end.  Replace the previous one with the max end
			end = max(end, all_ranges[index - 1][1])
	# else no overlap; just insert
	all_ranges.insert(index, (start, end))"""
	
	# Insert at the right position for the start of the range
	#index = bisect(all_ranges, start)
	index = findStartIndex(all_ranges, start)
	
	# If there is a previous overlapping range (there is at most one), replace it; otherwise insert
	if index > 0 and all_ranges[index - 1][1] >= start:
		index -= 1
		start = all_ranges[index][0]
		end = max(all_ranges[index][1], end)
		all_ranges[index] = (start, end)
	else:
		all_ranges.insert(index, (start, end))

	# On all subsequent ranges, if their start overlaps the end of this range, replace this range with the max end and delete the next entry
	while index < len(all_ranges) - 1 and end >= all_ranges[index + 1][0]:
		end = max(end, all_ranges[index + 1][1])
		all_ranges[index] = (start, end)
		del all_ranges[index + 1]


def buildRangeList(input_lines):
	all_ranges = []
	[addRange(all_ranges, line) for line in input_lines]
	return all_ranges

def getSmallestValNotInRange(all_ranges):
	if len(all_ranges) == 0:
		return 0
	if all_ranges[0][0] > 0:
		return 0
	return all_ranges[0][1]

def countValuesInRanges(all_ranges):
	return sum([end - start for start, end in all_ranges])

def countValuesNotInRanges(all_ranges, total_values=4294967296):
	print(countValuesInRanges(all_ranges))
	return total_values - countValuesInRanges(all_ranges)

#input_lines = """5-8
#0-0
#8-9""".split("\n")
input_lines = open("day20_input.txt").readlines()

#print(getSmallestValNotInRange(buildRangeList(input_lines)))
#print(countValuesNotInRanges(buildRangeList(input_lines), total_values=10))
print(countValuesNotInRanges(buildRangeList(input_lines)))
