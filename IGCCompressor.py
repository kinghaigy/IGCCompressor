import sys, getopt, math

def main(argv):
	inputFileName = ''
	units = ''
	height = -1

	try:
		opts, args = getopt.getopt(argv, "h",["file=", "height=", "units="])
	except getopt.GetoptError:
		errAndQuit();

	# Start parsing command line options	
	for opt, arg in opts:
		if opt == "-h":
			errAndQuit()
		elif opt == "--units":
			units = arg

		elif opt == "--file":
			inputFileName = arg

		elif opt == "--height":
			height = int(arg)
		
	# Was there enough parameters entered?
	if len(inputFileName) == 0:
		print("ERROR: No file name provided")
		errAndQuit()

	if not (units == "feet" or units == "metres"):
		print("ERROR: No units specified")
		errAndQuit()

	if height < 0:
		print("ERROR: No height specified")
		errAndQuit()


	# Convert feet to meters if need be
	if units == "feet":
		height = feetToMeters(height)

	# Time to compress
	compressIGC(inputFileName, height)


def feetToMeters(feet):
	return feet * 0.3048

def metresToFeet(metres):
	return metres/0.3048

def errAndQuit():
	print("Usage:\n   IGCCompress.py --file <file_name> --height 10000 --units feet\n   IGCCompress.py --file <file_name> --height 3300 --units metres")
	sys.exit()

def compressIGC(fileName, height):
	try:
		igcFile = open(fileName, 'r', newline='')
	except IOError as e:
		print("Failed to open", fileName,": ", e.strerror)
		sys.exit()

	# Find the maximum gps and pressure altitude
	maxGPSAlt = -1
	maxPressAlt = -1

	for line in igcFile:
		if line[0] == 'B':
			# This line stores a tracklog point
			GPSAlt = int(line[30:35])
			pressAlt = int(line[25:30])

			if GPSAlt > maxGPSAlt:
				maxGPSAlt = GPSAlt

			if pressAlt > maxPressAlt:
				maxPressAlt = pressAlt

	print("Maximum recorded GPS altitude:", maxGPSAlt, "metres (", metresToFeet(maxGPSAlt), "feet)")
	print("Maximum recorded pressure altitude:", maxPressAlt, "metres (", metresToFeet(maxPressAlt), "feet)")

	if max(maxGPSAlt, maxPressAlt) < height:
		# The highest point recorded is under our ceiling - do nothing
		print("These heights are under the imposed ceiling of ", height, "metres (", metresToFeet(height), "feet). Nothing needs to change")
		sys.exit()

	# Work out how much to scale by
	scalar = height/max(maxGPSAlt, maxPressAlt)
	print("Scaling all heights by ", scalar,"...")

	# Iterate through and fix all heights
	outputIGCFile = open("Compressed " + fileName, 'w')

	# Bring iterator back to the top
	igcFile.seek(0)
	for line in igcFile:
		if line[0] == 'B':
			# Modify the heights
			line = line[0:25] + "{0:05d}".format(int(scalar * int(line[25:30]))) + "{0:05d}".format(int(scalar * int(line[30:35]))) + line[35:]
		
		# Write to the file
		outputIGCFile.write(line)

	# Save and close the file
	outputIGCFile.close()





# If the name of this instance is the main one (the first one called) then pass the command line args into the main function
if __name__ == "__main__":
   main(sys.argv[1:])