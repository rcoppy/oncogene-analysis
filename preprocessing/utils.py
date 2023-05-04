def format_csv_line(args: list): 
	line = ''
	for i in range(0, len(args)):
		line += str(args[i])
		if i != len(args) -1: 
			line += ','

	line += '\n'
	return line