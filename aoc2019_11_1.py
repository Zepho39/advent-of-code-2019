import math
import csv
import itertools
import logging

logging.basicConfig(filename='aoc2019_11_1.log',level=logging.DEBUG)

INPUT_PATH = ''
GRAV_VAL = 19690720

CSV_PATH = 'aoc2019_11_1.out.csv'
#part 1 correct answer = 14522484

def opcode1(v1, v2, idest, inputArray):
	val = v1 + v2
	print('Opcode1 placing {} at index {}'.format(val, idest))
	inputArray[idest] = val
	return inputArray


def opcode2(v1, v2, idest, inputArray):
	val = v1 * v2
	print('Opcode2 placing {} at index {}'.format(val, idest))
	inputArray[idest] = val
	return inputArray

def opcode3(v, userInput, inputArray):
	inputArray[v] = userInput
	return inputArray

def opcode4(v, inputArray):
	print("Opcode4: Diagnostic Output = {}".format(v))
	return (v, inputArray)

# JUMP-IF-TRUE
# Assumes v2 is indexArray[indexArray[i+2]] or indexArray[i+2], depending on mode
# Returns the new instruction pointer
def opcode5(i, v1, v2):
	if v1 == 0:
		print("Opcode5 index {}: v1 = 0, not jumping".format(i))
		return i + 3
	else:
		print("Opcode5 index {}: v1 non-zero ({}), jumping to {}".format(i, v1, v2))
		return v2 

# JUMP-IF-FALSE
# Assumes v2 is indexArray[indexArray[i+2]] or indexArray[i+2], depending on mode
# Returns the new instruction pointer
def opcode6(i, v1, v2):
	if v1 == 0:
		print("Opcode6 index {}: v1 = 0, jumping to {}".format(i, v2))
		return v2
	else:
		return i + 3 
		print("Opcode6 index {}: v1 not 0 ({}), not jumping".format(i, v1))

# LESS THAN
#
def opcode7(v1, v2, idest, inputArray):
	if v1 < v2:
		inputArray[idest] = 1
	else:
		inputArray[idest] = 0
	return inputArray

# EQUALS
# 
def opcode8(v1, v2, idest, inputArray):
	if v1 == v2:
		inputArray[idest] = 1
	else:
		inputArray[idest] = 0
	return inputArray

# ADJUST RELATIVE BASE
# 
def opcode9(v, relativeBase):
	return v + relativeBase


def seedInputArray():
	inputArray = [3,8,1005,8,291,1106,0,11,0,0,0,104,1,104,0,3,8,1002,8,-1,10,101,1,10,10,4,10,108,0,8,10,4,10,1002,8,1,28,1,1003,20,10,2,1103,19,10,3,8,1002,8,-1,10,1001,10,1,10,4,10,1008,8,0,10,4,10,1001,8,0,59,1,1004,3,10,3,8,102,-1,8,10,1001,10,1,10,4,10,108,0,8,10,4,10,1001,8,0,84,1006,0,3,1,1102,12,10,3,8,1002,8,-1,10,101,1,10,10,4,10,1008,8,1,10,4,10,101,0,8,114,3,8,1002,8,-1,10,101,1,10,10,4,10,108,1,8,10,4,10,101,0,8,135,3,8,1002,8,-1,10,1001,10,1,10,4,10,1008,8,0,10,4,10,102,1,8,158,2,9,9,10,2,2,10,10,3,8,1002,8,-1,10,1001,10,1,10,4,10,1008,8,1,10,4,10,101,0,8,188,1006,0,56,3,8,1002,8,-1,10,1001,10,1,10,4,10,108,1,8,10,4,10,1001,8,0,212,1006,0,76,2,1005,8,10,3,8,102,-1,8,10,1001,10,1,10,4,10,108,1,8,10,4,10,1001,8,0,241,3,8,102,-1,8,10,101,1,10,10,4,10,1008,8,0,10,4,10,1002,8,1,264,1006,0,95,1,1001,12,10,101,1,9,9,1007,9,933,10,1005,10,15,99,109,613,104,0,104,1,21102,838484206484,1,1,21102,1,308,0,1106,0,412,21102,1,937267929116,1,21101,0,319,0,1105,1,412,3,10,104,0,104,1,3,10,104,0,104,0,3,10,104,0,104,1,3,10,104,0,104,1,3,10,104,0,104,0,3,10,104,0,104,1,21102,206312598619,1,1,21102,366,1,0,1105,1,412,21101,179410332867,0,1,21102,377,1,0,1105,1,412,3,10,104,0,104,0,3,10,104,0,104,0,21101,0,709580595968,1,21102,1,400,0,1106,0,412,21102,868389384552,1,1,21101,411,0,0,1106,0,412,99,109,2,21202,-1,1,1,21102,1,40,2,21102,1,443,3,21101,0,433,0,1106,0,476,109,-2,2105,1,0,0,1,0,0,1,109,2,3,10,204,-1,1001,438,439,454,4,0,1001,438,1,438,108,4,438,10,1006,10,470,1102,0,1,438,109,-2,2106,0,0,0,109,4,1202,-1,1,475,1207,-3,0,10,1006,10,493,21102,0,1,-3,21202,-3,1,1,21201,-2,0,2,21101,0,1,3,21102,1,512,0,1106,0,517,109,-4,2105,1,0,109,5,1207,-3,1,10,1006,10,540,2207,-4,-2,10,1006,10,540,22101,0,-4,-4,1106,0,608,21201,-4,0,1,21201,-3,-1,2,21202,-2,2,3,21101,0,559,0,1106,0,517,21201,1,0,-4,21102,1,1,-1,2207,-4,-2,10,1006,10,578,21101,0,0,-1,22202,-2,-1,-2,2107,0,-3,10,1006,10,600,21201,-1,0,1,21102,600,1,0,106,0,475,21202,-2,-1,-2,22201,-4,-2,-4,109,-5,2106,0,0]
	#inputArray[1] = 1
	#inputArray[2] = verb

	print("Input length is {}".format(len(inputArray)))
	header = []
	for i in range (0, len(inputArray)):
		header.append(i)
	with open(CSV_PATH, 'w') as file:
		writer = csv.writer(file)
		writer.writerow(header)

	return inputArray


def seedTestArray():
	inputArray = [104,1125899906842624,99]

	print("Input length is {}".format(len(inputArray)))
	header = []
	for i in range (0, len(inputArray)):
		header.append(i)
	with open(CSV_PATH, 'w') as file:
		writer = csv.writer(file)
		writer.writerow(header)

	return inputArray

# Returns nth digit of number, countin right to left
def get_digit(number, n):
    return number // 10**n % 10

def extendArray(inputArray, writeIndex):
	while writeIndex >= len(inputArray):
		inputArray.append('0')
	return inputArray

def opcodeAssist(inputs, inputArray, startingIndex, op3Start, relativeBaseStart):
	print("DEBUG: inputs = {}, inputArray = {}, startingIndex = {}, and op3Start = {}, relativeBaseStart = {}".format(inputs, inputArray, startingIndex, op3Start, relativeBaseStart))
	i = startingIndex
	op3Counter = op3Start
	relativeBase = relativeBaseStart

	opcodeOutputZero = inputs[op3Counter] if op3Counter < len(inputs) else inputs[len(inputs) - 1]
	opcodeOutput = (opcodeOutputZero, inputArray)
	stepCount = 0

	while (i < len(inputArray)) and (inputArray[i] != 99):
		stepCount += 1
		print('\nINFO: STEP {}, ROW {}'.format(stepCount, stepCount + 1))
		with open(CSV_PATH, 'a') as file:
			writer = csv.writer(file)
			writer.writerow(inputArray)

		opcode = str(inputArray[i])
		opcodeFun = (10 * get_digit(inputArray[i], 1)) + get_digit(inputArray[i], 0)

		mode = (get_digit(inputArray[i], 2), get_digit(inputArray[i], 3), get_digit(inputArray[i], 4))

		# Arg 1
		print("DEBUG: opcodeAssist: Trying to establish v1")
		if mode[0] == 0:
			if inputArray[i+1] > len(inputArray):
				v1 = 0
			else: 
				v1 = inputArray[inputArray[i+1]]
		elif mode[0] == 1:
			v1 = inputArray[i+1]
		elif mode[0] == 2:
			if inputArray[i+1] + relativeBase > len(inputArray):
				v1 = 0
			else:
				v1 = inputArray[inputArray[i+1] + relativeBase]
		print("DEBUG: opcodeAssist: v1 established, v1 = {}".format(v1))

		# Arg 2 TO DO
		print("DEBUG: opcodeAssist: Trying to establish v2")
		if mode[1] == 0:
			try:
				v2 = inputArray[inputArray[i+2]]
			except IndexError:
				v2 = 0
		elif mode[1] == 1:
			try:
				v2 = inputArray[i+2]
			except IndexError:
				v2 = 0
		elif mode[1] == 2:
			try:
				v2 = inputArray[inputArray[i+2] + relativeBase]
			except IndexError:
				v2 = 0
		print("DEBUG: opcodeAssist: v2 established, v2 = {}".format(v2))

		# Arg 3
		print("DEBUG: opcodeAssist: Trying to establish v3")
		if mode[2] == 0:
			try:
				v3 = inputArray[i+3]
			except IndexError:
				v3 = 0
		elif mode[2] == 1:
			v3 = i+3
		elif mode[2] == 2:
			try:
				v3 = inputArray[i+3] + relativeBase
			except IndexError:
				v3 = relativeBase
		print("DEBUG: opcodeAssist: v3 established, v3 = {}".format(v3))
		print("DEBUG: opcodeAssist: opcode function = {}, length of input array = {}".format(opcodeFun, len(inputArray)))

		if int(v3) >= len(inputArray) and opcodeFun in (1, 2, 7, 8):
			print("DEBUG: opcodeAssist: Extending inputArray to support write to {}".format(v3))
			inputArray = extendArray(inputArray, v3)

		print(inputArray)
		
		# OPCODE 1
		if opcodeFun == 1:
			print("Opcode1 index {}: starting val = {} code = {}".format(i, inputArray[i], opcodeFun))
			print("Opcode1 index {}: mode1 = {} mode2 = {} mode3 = {}".format(i, mode[0], mode[1], mode[2]))
			print("Opcode1 index {}: v1 = {} v2 = {} v3 = {}".format(i, v1, v2, v3))
			inputArray = opcode1(v1, v2, v3, inputArray)
			i += 4

		# OPCODE 2
		elif opcodeFun == 2:
			print("Opcode2 index {}: starting val = {} code = {}".format(i, inputArray[i], opcodeFun))
			print("Opcode2 index {}: mode1 = {} mode2 = {} mode3 = {}".format(i, mode[0], mode[1], mode[2]))
			print("Opcode2 index {}: v1 = {} v2 = {} v3 = {}".format(i, v1, v2, v3))
			inputArray = opcode2(v1, v2, v3, inputArray)
			i += 4

		# OPCODE 5
		elif opcodeFun == 5:
			print("Opcode5 index {}: starting val = {} code = {}".format(i, inputArray[i], opcodeFun))
			print("Opcode5 index {}: mode1 = {} mode2 = {} mode3 = {}".format(i, mode[0], mode[1], mode[2]))
			print("Opcode5 index {}: v1 = {} v2 = {}".format(i, v1, v2))
			i = opcode5(i, v1, v2)

		# OPCODE 6
		elif opcodeFun == 6:
			print("Opcode6 index {}: starting val = {} code = {}".format(i, inputArray[i], opcodeFun))
			print("Opcode6 index {}: mode1 = {} mode2 = {} mode3 = {}".format(i, mode[0], mode[1], mode[2]))
			print("Opcode6 index {}: v1 = {} v2 = {}".format(i, v1, v2))
			i = opcode6(i, v1, v2)

		# OPCODE 7
		elif opcodeFun == 7:
			print("Opcode7 index {}: starting val = {} code = {}".format(i, inputArray[i], opcodeFun))
			print("Opcode7 index {}: mode1 = {} mode2 = {} mode3 = {}".format(i, mode[0], mode[1], mode[2]))
			print("Opcode7 index {}: v1 = {} v2 = {} v3 = {}".format(i, v1, v2, v3))
			inputArray = opcode7(v1, v2, v3, inputArray)
			i += 4

		# OPCODE 8
		elif opcodeFun == 8:
			print("Opcode8 index {}: starting val = {} code = {}".format(i, inputArray[i], opcodeFun))
			print("Opcode8 index {}: mode1 = {} mode2 = {} mode3 = {}".format(i, mode[0], mode[1], mode[2]))
			print("Opcode8 index {}: v1 = {} v2 = {} v3 = {}".format(i, v1, v2, v3))
			inputArray = opcode8(v1, v2, v3, inputArray)
			i += 4

		# OPCODE 3
		elif opcodeFun == 3:
			print("Opcode3 index {}: starting val = {} code = {}".format(i, inputArray[i], opcodeFun))
			print("Opcode3 index {}: mode1 = {} mode2 = {} mode3 = {}".format(i, mode[0], mode[1], mode[2]))
			print("Opcode3 index {}: v1 = {}".format(i, v1))
			logging.debug("ops3Counter - {}".format(op3Counter))
			#opcode3(inputArray[i+1], inputs[0]) if op3Counter == 0 else opcode3(inputArray[i+1], inputs[1])
			if mode[0] == 0:
				inputArray = opcode3(inputArray[i+1], inputs[op3Counter], inputArray)
			elif mode[0] == 1:
				inputArray = opcode3(i+1, inputs[op3Counter], inputArray)
			elif mode[0] == 2:
				inputArray = opcode3(inputArray[i+1] + relativeBase, inputs[op3Counter], inputArray)
			op3Counter += 1
			i += 2

		# OPCODE 4
		elif opcodeFun == 4:
			print("Opcode4 index {}: starting val = {} code = {}".format(i, inputArray[i], opcodeFun))
			print("Opcode4 index {}: mode1 = {} mode2 = {} mode3 = {}".format(i, mode[0], mode[1], mode[2]))
			print("Opcode4 index {}: v1 = {}".format(i, inputArray[i+1]))
			opcodeOutput = opcode4(v1, inputArray)
			i += 2
			#print("DEBUG: Opcode4 return index set to {}".format(i))
			return (opcodeOutput[0], 4, i, opcodeOutput[1], op3Counter, relativeBase)

		# OPCODE 9
		elif opcodeFun == 9:
			print("Opcode9 index {}: starting val = {} code = {}".format(i, inputArray[i], opcodeFun))
			print("Opcode9 index {}: mode1 = {} mode2 = {} mode3 = {}".format(i, mode[0], mode[1], mode[2]))
			print("Opcode9 index {}: v1 = {}".format(i, v1))
			relativeBase = opcode9(v1, relativeBase)
			print("Opcode9 index {}: new relativeBase = {}".format(i, relativeBase))
			i += 2

		# OPCODE 99
		elif opcode[-2:] in ['99']:
			print("Opcode99 index {}: starting val = {} code = {}".format(i, inputArray[i], opcodeFun))
			return (opcodeOutput, 99, 1, inputArray, op3Counter, relativeBase)

		# UKNOWN OPCODE FOUND
		else:
			print("OpcodeUnknown index {}: starting val = {} code = {}".format(i, inputArray[i], opcodeFun))
			opcodeOutput = "ERROR: Unknown opcode found. Invalid input!"
			print("help!")
		#'''
	print("DEBUG: Exited While Loop, i = {},  len(inputArray)) = {}, and inputArray[i] = {}".format(i, len(inputArray), inputArray[i]))
	return (opcodeOutput, 99, 1, inputArray, op3Counter, relativeBase)


def gravAssistTester():
	for i in range(0, 100):
		for j in range(0, 100):
			seedInputArray(i, j)
			loc0 = opcodeAssist()
			if loc0 == GRAV_VAL:
				print("INFO: Found noun and verb. 100 * noun + verb = " + str((100 * i) + j))
				return "INFO: Success!"
	return "ERROR: No noun/verb combination found in the allowed value ranges."

# Generates a list of all lists of combinations of the input list
def generateCombinations(inputList):
	combos = (itertools.permutations(inputList, len(inputList)))
	print(list(combos))
	return list(combos)

# Probably already no longer works as of Day 7 pt 2
def ampRunner(phases, seedFunction):
	print("DEBUG: phases for this ampRunner run are {}".format(phases))
	A = opcodeAssist((phases[0], 0), seedFunction)
	B = opcodeAssist((phases[1], A), seedFunction)
	C = opcodeAssist((phases[2], B), seedFunction)
	D = opcodeAssist((phases[3], C), seedFunction)
	E = opcodeAssist((phases[4], D), seedFunction)
	return E

def ampFeedbackRunner(phases, seedFunction, userInput):
	maxFinalThrust = 0
	biggestPhase = []

	for idx, phase in enumerate(phases):
		print("DEBUG: Running phase {}: {}".format(idx, phase))
		# Initialize all amps
		#ampInit = seedFunction()
		amps = []
		opcodeInputArray = []
		opcodeIndexArray = []
		op3CounterArray = []
		ampIndex = 0
		while ampIndex < len(phase):
			amps.append(seedFunction())
			opcodeInputArray.append([phase[ampIndex]])
			opcodeIndexArray.append(0)
			op3CounterArray.append(0)
			ampIndex += 1

		print(amps)
		
		#print()
		ampIndex = 0
		returnCode = 0
		# Add user input to the input of the first amp
		opcodeInputArray[ampIndex].append(userInput)
		finalThrust = 0
		loop = 1

		while returnCode != 99:
			#opcodeAssist(inputs, inputArray, startingIndex, op3Starter)
			print("\nAt this time amp index = {}, loop = {}".format(ampIndex, loop))
			print("At this time opcodeIndexArray index = {}".format(opcodeIndexArray))
			print("At this time opcodeInputArray index = {}".format(opcodeInputArray))
			print("At this time amps = {}".format(amps))
			opcodeTuple = opcodeAssist(opcodeInputArray[ampIndex], amps[ampIndex], opcodeIndexArray[ampIndex], op3CounterArray[ampIndex])
			# return (opcodeOutput, 4, i, inputArray)
			finalThrust = opcodeTuple[0]
			returnCode = opcodeTuple[1]
			opcodeIndexArray[ampIndex] = opcodeTuple[2]
			amps[ampIndex] = opcodeTuple[3]
			op3CounterArray[ampIndex] = opcodeTuple[4]

			if (ampIndex + 1) == len(phase):
				opcodeInputArray[0].append(opcodeTuple[0])
				ampIndex = 0
				loop += 1
			else: 
				opcodeInputArray[ampIndex+1].append(opcodeTuple[0])
				ampIndex += 1


		if maxFinalThrust < finalThrust:
			maxFinalThrust = finalThrust
			biggestPhase = phase


	print("INFO: Maximum Thruster Output = {}".format(maxFinalThrust))
	print("INFO: Maximum Output Generated by Phase Sequence {}".format(biggestPhase))
	return maxFinalThrust


# 
def ampTester(seedFunction):
	maxThruster = 0
	maxPhaseOrder = []
	inputList = list(range(5,10))
	listOfCombinations = list(itertools.permutations(inputList, len(inputList)))
	#generateCombinations([0,1,2,3,4])
	print(listOfCombinations)
	for listOfPhases in listOfCombinations:
		thisThruster = ampRunner(listOfPhases, seedFunction)
		if maxThruster < thisThruster:
			maxThruster = thisThruster
			maxPhaseOrder = listOfPhases
	print("INFO: Maximum Thruster Output = {}".format(maxThruster))
	print("INFO: Maximum Output Generated by Phase Sequence {}".format(maxPhaseOrder))
	return (maxThruster, maxPhaseOrder)

# Assumes seedFunction returns a valid inputArray (array of integers)
# Assumes userInput is an array of all the initial userInput (in this case, [1])
def boostTester(seedFunction, userInput):
	boostArray = seedFunction()
	opcodeTuple = opcodeAssist(userInput, boostArray, 0, 0, 0)
	return(opcodeTuple[0])


# Assumes seedFunction returns a valid inputArray (array of integers)
# Assumes userInput is an array of all the initial userInput (in this case, [1])
def boostSensor(seedFunction, userInput):
	boostArray = seedFunction()
	opcodeTuple = opcodeAssist(userInput, boostArray, 0, 0, 0)
	return(opcodeTuple[1])

# Assumes turn is one of 0, 1
def rotate(turn, currentDir):
	# TURN LEFT
	if turn == 0:
		# FACING UP
		if currentDir == (0, 1):
			return (-1, 0)
		# FACING LEFT
		elif currentDir == (-1, 0):
			return (0, -1)
		# FACING DOWN
		elif currentDir == (0, -1):
			return (1, 0)
		# FACING RIGHT
		elif currentDir == (1, 0):
			return (0, 1)
	# TURN RIGHT
	elif turn == 1:
		# FACING UP
		if currentDir == (0, 1):
			return (1, 0)
		# FACING RIGHT
		elif currentDir == (1, 0):
			return (0, -1)
		# FACING DOWN
		elif currentDir == (0, -1):
			return (-1, 0)
		# FACING LEFT
		elif currentDir == (-1, 0):
			return (0, 1)



def hullPaintingRobot(seedFunction):
	robotBrain = seedFunction()
	# opcodeAssist(inputs, inputArray, startingIndex, op3Start, relativeBaseStart)
	# opcodeOutput = opcode4(v1, inputArray)
	# return (opcodeOutput[0], 4, i, opcodeOutput[1], op3Counter, relativeBase)
	# def opcode4(v, inputArray):
	# 	print("Opcode4: Diagnostic Output = {}".format(v))
	# 	return (v, inputArray)
	# First, it will output a value indicating the color to paint the panel the robot is over: 0 means to paint the panel black, and 1 means to paint the panel white.
	# Second, it will output a value indicating the direction the robot should turn: 0 means it should turn left 90 degrees, and 1 means it should turn right 90 degrees.
	output = 1
	robotLocation = (0, 0)
	hull = {}
	userInput = [0]
	currentDir = (0, 1)
	opcodeTuple = opcodeAssist(userInput, robotBrain, 0, 0, 0)
	paintCount = {}
	while opcodeTuple[1] != 99:
		if output == 1:
			if hull.get(robotLocation, 0) != opcodeTuple[0]:
				hull[robotLocation] = opcodeTuple[0]
				paintCount[robotLocation] = paintCount.get(robotLocation, 0) + 1
				output = 2
		elif output == 2:
			currentDir = rotate(opcodeTuple[0], currentDir)
			print("DEBUG: hullPaintingRobot current direction is {} and current robot location before moving is {}".format(currentDir, robotLocation))
			robotLocation = (robotLocation[0] + currentDir[0], robotLocation[1] + currentDir[1])
			userInput.append(hull.get(robotLocation, 0))
			output = 1
		opcodeTuple = opcodeAssist(userInput, opcodeTuple[3], opcodeTuple[2], opcodeTuple[4], opcodeTuple[5])
	return len(hull.keys())



print("Robot painting {} panels".format(hullPaintingRobot(seedInputArray)))













