import math
import csv
import itertools
import logging
from collections import defaultdict

logging.basicConfig(filename='aoc2019_15_1.log',level=logging.DEBUG)

INPUT_PATH = ''
GRAV_VAL = 19690720

CSV_PATH = 'aoc2019_15_1.out.csv'
#part 1 correct answer = 14522484

MANUAL_ENTRY = False

def opcode1(v1, v2, idest, inputArray):
	val = v1 + v2
	#print("Opcode1 placing {} at index {}".format(val, idest))
	inputArray[idest] = val
	return inputArray


def opcode2(v1, v2, idest, inputArray):
	val = v1 * v2
	#print("Opcode2 placing {} at index {}".format(val, idest))
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
		#print("Opcode5 index {}: v1 = 0, not jumping".format(i))
		return i + 3
	else:
		#print("Opcode5 index {}: v1 non-zero ({}), jumping to {}".format(i, v1, v2))
		return v2 

# JUMP-IF-FALSE
# Assumes v2 is indexArray[indexArray[i+2]] or indexArray[i+2], depending on mode
# Returns the new instruction pointer
def opcode6(i, v1, v2):
	if v1 == 0:
		#print("Opcode6 index {}: v1 = 0, jumping to {}".format(i, v2))
		return v2
	else:
		return i + 3 
		#print("Opcode6 index {}: v1 not 0 ({}), not jumping".format(i, v1))

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
	inputArray = [3,1033,1008,1033,1,1032,1005,1032,31,1008,1033,2,1032,1005,1032,58,1008,1033,3,1032,1005,1032,81,1008,1033,4,1032,1005,1032,104,99,1001,1034,0,1039,1002,1036,1,1041,1001,1035,-1,1040,1008,1038,0,1043,102,-1,1043,1032,1,1037,1032,1042,1105,1,124,1001,1034,0,1039,1001,1036,0,1041,1001,1035,1,1040,1008,1038,0,1043,1,1037,1038,1042,1106,0,124,1001,1034,-1,1039,1008,1036,0,1041,101,0,1035,1040,1001,1038,0,1043,102,1,1037,1042,1105,1,124,1001,1034,1,1039,1008,1036,0,1041,1002,1035,1,1040,101,0,1038,1043,101,0,1037,1042,1006,1039,217,1006,1040,217,1008,1039,40,1032,1005,1032,217,1008,1040,40,1032,1005,1032,217,1008,1039,5,1032,1006,1032,165,1008,1040,35,1032,1006,1032,165,1102,1,2,1044,1106,0,224,2,1041,1043,1032,1006,1032,179,1102,1,1,1044,1105,1,224,1,1041,1043,1032,1006,1032,217,1,1042,1043,1032,1001,1032,-1,1032,1002,1032,39,1032,1,1032,1039,1032,101,-1,1032,1032,101,252,1032,211,1007,0,44,1044,1105,1,224,1102,0,1,1044,1106,0,224,1006,1044,247,1002,1039,1,1034,1001,1040,0,1035,1001,1041,0,1036,1002,1043,1,1038,102,1,1042,1037,4,1044,1105,1,0,5,26,24,17,68,40,71,9,36,46,67,39,48,8,20,23,12,47,28,13,47,2,68,17,71,31,63,31,83,14,78,31,8,33,30,63,30,5,7,11,91,97,17,84,23,37,46,6,14,59,1,76,41,63,85,83,86,63,33,13,50,17,37,16,59,8,7,35,71,9,23,67,46,62,58,38,76,3,71,43,17,64,29,30,72,91,17,70,21,15,76,31,89,20,38,27,65,53,60,34,90,99,56,15,45,57,8,52,70,36,15,79,32,35,83,78,10,3,90,16,74,14,84,43,20,81,91,25,71,83,24,31,92,72,34,59,27,78,6,31,14,31,76,9,80,63,35,40,92,12,84,65,41,27,82,10,7,56,25,70,4,98,16,37,65,46,78,11,97,20,16,95,98,24,31,3,57,74,42,99,36,34,74,10,81,46,43,97,2,24,61,55,13,96,41,41,46,14,64,2,46,94,53,3,3,81,37,85,7,54,29,90,22,75,47,20,26,86,69,53,89,17,2,55,13,85,99,90,2,48,29,66,55,31,19,39,59,56,98,28,38,10,46,10,62,20,63,18,53,97,9,32,6,46,3,91,24,6,62,30,73,26,24,50,3,16,78,3,34,50,8,18,40,65,64,21,28,30,87,45,99,8,21,77,40,73,38,56,12,86,64,43,61,89,4,55,47,28,14,8,99,52,51,40,82,26,19,68,17,53,70,5,14,22,64,69,84,14,69,2,80,18,79,5,66,18,34,48,31,34,54,50,8,33,73,38,52,94,71,7,31,94,31,93,66,82,39,40,42,80,91,70,10,6,50,35,96,13,7,89,22,58,30,24,85,81,88,55,7,58,38,91,55,11,35,84,28,87,26,78,48,66,11,88,8,18,68,55,38,6,1,57,60,1,8,99,58,21,29,88,32,32,57,72,8,20,45,5,91,39,51,59,82,29,52,37,33,49,5,28,38,17,6,58,67,11,72,51,42,4,3,12,94,84,25,31,72,32,89,49,4,23,57,49,27,38,50,30,23,15,80,4,12,67,14,48,76,91,58,11,63,37,95,1,15,22,84,8,23,87,61,32,78,87,7,47,1,81,31,84,91,21,19,68,6,87,3,72,43,60,23,67,42,40,62,9,86,33,84,69,24,97,37,49,24,67,2,16,52,3,42,49,3,95,84,61,8,40,79,10,74,51,6,77,63,1,66,7,55,24,80,68,17,30,47,54,30,77,40,99,18,85,99,85,2,27,18,33,54,99,27,5,64,39,22,66,12,71,29,26,35,49,13,41,22,76,30,70,30,75,34,7,5,62,1,23,61,43,90,24,91,40,42,75,48,40,91,39,46,38,56,17,28,51,56,7,51,40,56,22,87,43,99,6,58,93,35,47,83,10,57,55,68,34,68,93,28,55,11,3,53,80,9,41,42,50,95,7,4,84,10,91,33,12,99,98,60,76,73,24,70,46,72,27,36,62,27,25,43,59,39,9,95,72,9,17,79,36,52,52,22,4,55,57,16,19,65,62,83,11,76,73,37,89,21,86,6,88,17,93,1,59,8,48,73,90,96,10,85,46,12,99,16,16,76,4,2,2,45,62,30,12,14,72,60,9,19,71,43,41,36,99,69,38,1,1,48,32,33,83,26,15,51,19,31,71,92,8,49,34,87,32,80,73,28,65,95,7,8,85,12,63,22,83,8,70,1,82,96,59,29,95,43,59,72,68,38,48,11,87,54,90,11,93,30,63,12,96,41,64,21,89,24,94,73,79,18,55,40,95,0,0,21,21,1,10,1,0,0,0,0,0,0]
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
	#print("DEBUG: inputs = {}, inputArray = {}, startingIndex = {}, and op3Start = {}, relativeBaseStart = {}".format(inputs, inputArray, startingIndex, op3Start, relativeBaseStart))
	i = startingIndex
	op3Counter = op3Start
	relativeBase = relativeBaseStart

	#opcodeOutputZero = inputs[op3Counter] if op3Counter < len(inputs) else inputs[len(inputs) - 1]
	#opcodeOutput = (opcodeOutputZero, inputArray)
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
		#print("DEBUG: opcodeAssist: Trying to establish v1")
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
		#print("DEBUG: opcodeAssist: v1 established, v1 = {}".format(v1))

		# Arg 2 TO DO
		#print("DEBUG: opcodeAssist: Trying to establish v2")
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
		#print("DEBUG: opcodeAssist: v2 established, v2 = {}".format(v2))

		# Arg 3
		#print("DEBUG: opcodeAssist: Trying to establish v3")
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
		#print("DEBUG: opcodeAssist: v3 established, v3 = {}".format(v3))
		print("DEBUG: opcodeAssist: opcode function = {}, length of input array = {}".format(opcodeFun, len(inputArray)))

		if int(v3) >= len(inputArray) and opcodeFun in (1, 2, 7, 8):
			print("DEBUG: opcodeAssist: Extending inputArray to support write to {}".format(v3))
			inputArray = extendArray(inputArray, v3)

		#print(inputArray)
		
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
			global MANUAL_ENTRY
			if MANUAL_ENTRY:
				print("Enter JoyStick direction (-1 for left, 1 for right, 0 for don't move)")
				commandLineInput = input()
				while commandLineInput not in ['-1', '0', '1']:
					print("ERROR: Input not one of -1, 0, or 1. Please enter new input")
					commandLineInput = input()
				inputs.append(int(commandLineInput))

			if mode[0] == 0:
				inputArray = opcode3(inputArray[i+1], inputs[op3Counter], inputArray)
			elif mode[0] == 1:
				inputArray = opcode3(i+1, inputs[op3Counter], inputArray)
			elif mode[0] == 2:
				inputArray = opcode3(inputArray[i+1] + relativeBase, inputs[op3Counter], inputArray)
			print("Opcode3 index {}: using value {}".format(i, inputs[op3Counter]))
			op3Counter += 1
			i += 2

		# OPCODE 4
		elif opcodeFun == 4:
			print("Opcode4 index {}: starting val = {} code = {}".format(i, inputArray[i], opcodeFun))
			print("Opcode4 index {}: mode1 = {} mode2 = {} mode3 = {}".format(i, mode[0], mode[1], mode[2]))
			print("Opcode4 index {}: v1 = {}".format(i, inputArray[i+1]))
			opcodeOutput = opcode4(v1, inputArray)
			i += 2
			print("DEBUG: Opcode4 return index set to {}".format(i))
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
			#print("Opcode99 index {}: starting val = {} code = {}".format(i, inputArray[i], opcodeFun))
			return (opcodeOutput, 99, 1, inputArray, op3Counter, relativeBase)

		# UKNOWN OPCODE FOUND
		else:
			#print("OpcodeUnknown index {}: starting val = {} code = {}".format(i, inputArray[i], opcodeFun))
			opcodeOutput = "ERROR: Unknown opcode found. Invalid input!"
			print("help!")
		#'''
	#print("DEBUG: Exited While Loop, i = {},  len(inputArray)) = {}, and inputArray[i] = {}".format(i, len(inputArray), inputArray[i]))
	return ("Exit", 99, 1, inputArray, op3Counter, relativeBase)


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



def hullPaintingRobot(seedFunction, startColor):
	robotBrain = seedFunction()
	# opcodeAssist(inputs, inputArray, startingIndex, op3Start, relativeBaseStart)
	# opcodeOutput = opcode4(v1, inputArray)
	# return (opcodeOutput[0], 4, i, opcodeOutput[1], op3Counter, relativeBase)
	# def opcode4(v, inputArray):
	# 	#print("Opcode4: Diagnostic Output = {}".format(v))
	# 	return (v, inputArray)
	# First, it will output a value indicating the color to paint the panel the robot is over: 0 means to paint the panel black, and 1 means to paint the panel white.
	# Second, it will output a value indicating the direction the robot should turn: 0 means it should turn left 90 degrees, and 1 means it should turn right 90 degrees.
	output = 1
	robotLocation = (0, 0)
	hull = {robotLocation : 1}
	userInput = [startColor]
	currentDir = (0, 1)
	opcodeTuple = opcodeAssist(userInput, robotBrain, 0, 0, 0)
	paintCount = {}
	maxX = 0
	minX = 0
	maxY = 0
	minY = 0
	while opcodeTuple[1] != 99:
		if output == 1:
			print("DEBUG: hullPaintingRobot robot's location {} is currently {}, was painted {}".format(robotLocation, hull.get(robotLocation, 0), opcodeTuple[0]))
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
		if robotLocation[0] > maxX:
			maxX = robotLocation[0]
		if robotLocation[0] < minX:
			minX = robotLocation[0]
		if robotLocation[1] > maxY:
			maxY = robotLocation[1]
		if robotLocation[1] < minY:
			minY = robotLocation[1]
		opcodeTuple = opcodeAssist(userInput, opcodeTuple[3], opcodeTuple[2], opcodeTuple[4], opcodeTuple[5])
	width = abs(maxX) + abs(minX)
	height = abs(maxY) + abs(minY)
	return (hull, minX, maxX, minY, maxY)

def drawHullMessage(seedFunction):
	hullTuple = hullPaintingRobot(seedFunction, 1)
	hullPicture = []
	hIndex = 0
	wIndex = 0
	for h in range(hullTuple[3], hullTuple[4]):
		hullPicture.append([])
		wIndex = 0
		for w in range(hullTuple[1], hullTuple[2]):
			paint = '#' if hullTuple[0].get((w, h), 0) == 1 else ' '
			hullPicture[hIndex].append(paint)
			wIndex += 1
		hIndex += 1
	hullPicture.reverse()
	return hullPicture

# seedFunction is the function that builds a valid memory array. printAtTile is a boolean flag dictating whether or not to print the screen when a tile has be created or updated
def arcadeRunner(seedFunction, printAtTile):
	global MANUAL_ENTRY
	board = {}
	game = seedFunction()
	userInput = []
	opcodeTuple = opcodeAssist(userInput, game, 0, 0, 0)
	paintCount = {}
	maxX = 0
	currX = 0
	maxY = 0
	currY = 0
	count = 1
	ball = (0, 0)
	paddle = 0
	paddleDir = 0
	while opcodeTuple[1] != 99:
		if count == 1:
			currX = opcodeTuple[0]
			if opcodeTuple[0] > maxX:
				maxX = opcodeTuple[0]
			count = 2
		elif count == 2:
			currY = opcodeTuple[0]
			if opcodeTuple[0] > maxY:
				maxY = opcodeTuple[0]
			count = 3
		elif count == 3:
			board[(currX, currY)] = opcodeTuple[0]
			#print("DEBUG: arcadeRunner: board = {} after adding {} at ({}, {})".format(board, opcodeTuple[0], currX, currY))
			count = 1
			if opcodeTuple[0] == 3:
				paddle = currX
			if opcodeTuple[0] == 4:
				ball = (currX, currY)
				if not MANUAL_ENTRY:
					if ball[0] > paddle:
						paddleDir = 1
					elif ball[0] < paddle:
						paddleDir = -1
					elif ball[0] == paddle:
						paddleDir = 0
					userInput.append(paddleDir)
			if printAtTile and opcodeTuple[4] > 0:
				screen = []
				for i in range (0, maxY+1):
					row = ''
					for j in range (0, maxX+1):
						row += str(board.get((j, i), 0))
					screen.append(row)
				#print("DEBUG: arcadeRunner: screen = {}".format(screen))
				drawScreen(screen)
				print("Current Score = {}".format(board.get((-1, 0), 0)))
		game = opcodeTuple[3]

		opcodeTuple = opcodeAssist(userInput, game, opcodeTuple[2], opcodeTuple[4], opcodeTuple[5])
	screen = []
	for i in range (0, maxY+1):
		row = ''
		for j in range (0, maxX+1):
			row += str(board.get((j, i), 0))
		screen.append(row)
	#print("DEBUG: arcadeRunner: screen = {}".format(screen))
	print("Final Score = {}".format(board.get((-1, 0), 0)))
	return (screen, board.get((-1, 0), 0))


def drawScreen(screen):
	for row in screen:
		print(row.replace('0', ' ').replace('1', '\\').replace('2', '#').replace('3', '_').replace('4', 'o'))

def arcadeTester(seedFunction):
	screen = arcadeRunner(seedFunction, False)[0]
	drawScreen(screen)
	bricks = 0
	for row in screen:
		bricks += row.count('2')
	return bricks

def arcadePlayer(seedFunction):
	arcadeResult = arcadeRunner(seedFunction, True)
	return arcadeResult[1]

def cycleDirClockwise(currentDir):
	if currentDir == 1:
		return 4
	elif currentDir == 2:
		return 3
	elif currentDir == 3:
		return 1
	elif currentDir == 4:
		return 2
	else:
		return 0

def cycleDirCounterClockwise(currentDir):
	if currentDir == 1:
		return 3
	elif currentDir == 2:
		return 4
	elif currentDir == 3:
		return 2
	elif currentDir == 4:
		return 1
	else:
		return 0

def cycleDir(currentDir, rotation):
	if rotation == 0:
		return cycleDirClockwise(currentDir)
	elif rotation == 1:
		return cycleDirCounterClockwise(currentDir)
	else:
		return 0
		
def newDroidLocation(currentDroidLocation, dir):
	if dir == 1:
		return (currentDroidLocation[0], currentDroidLocation[1] + 1)
	elif dir == 2:
		return (currentDroidLocation[0], currentDroidLocation[1] - 1)
	elif dir == 3:
		return (currentDroidLocation[0] - 1, currentDroidLocation[1])
	elif dir == 4:
		return (currentDroidLocation[0] + 1, currentDroidLocation[1])
	else:
		return (0, 0)

def buildGraph(board, minX, maxX, minY, maxY):
	graph = defaultdict(set)
	for y in range (minY, maxY+1):
		for x in range(minX, maxX+1):
			if board.get((x-1, y), '?') not in ['#', '?']:
				graph[(x, y)].add((x-1, y))
			if board.get((x+1, y), '?') not in ['#', '?']:
				graph[(x, y)].add((x+1, y))
			if board.get((x, y-1), '?') not in ['#', '?']:
				graph[(x, y)].add((x, y-1))
			if board.get((x, y+1), '?') not in ['#', '?']:
				graph[(x, y)].add((x, y+1))
	return graph 

def djikstraPath(start, end, graph):
    # shortest paths is a dict of nodes
    # whose value is a tuple of (previous node, weight)
    shortest_paths = {start: (None, 0)}
    current_node = start
    visited = set()
    
    while current_node != end:
        visited.add(current_node)
        destinations = graph[current_node]
        weight_to_current_node = shortest_paths[current_node][1]

        for next_node in destinations:
            weight = 1 + weight_to_current_node
            if next_node not in shortest_paths:
                shortest_paths[next_node] = (current_node, weight)
            else:
                current_shortest_weight = shortest_paths[next_node][1]
                if current_shortest_weight > weight:
                    shortest_paths[next_node] = (current_node, weight)
        
        next_destinations = {node: shortest_paths[node] for node in shortest_paths if node not in visited}
        if not next_destinations:
            return "Route Not Possible"
        # next node is the destination with the lowest weight
        current_node = min(next_destinations, key=lambda k: next_destinations[k][1])
    
    # Work back through destinations in shortest path
    path = []
    while current_node is not None:
        path.append(current_node)
        next_node = shortest_paths[current_node][0]
        current_node = next_node
    # Reverse path
    path = path[::-1]
    return path

def inaccessible(board, minX, maxX, minY, maxY, coord):
	if board.get((coord[0] - 1, coord[1]), '?') == '#' and board.get((coord[0] + 1, coord[1]), '?') == '#' and board.get((coord[0], coord[1] - 1), '?') == '#' and board.get((coord[0], coord[1] + 1), '?') == '#':
		return True
	if coord == (minX, minY) or coord == (minX, maxY) or coord == (maxX, minY) or coord == (maxX, maxY):
		return True 
	elif coord[0] == minX and board.get((coord[0] + 1, coord[1]), '?') == '#' and board.get((coord[0], coord[1] - 1), '?') == '#' and board.get((coord[0], coord[1] + 1), '?') == '#':
		return True 
	elif coord[0] == maxX and board.get((coord[0] - 1, coord[1]), '?') == '#' and board.get((coord[0], coord[1] - 1), '?') == '#' and board.get((coord[0], coord[1] + 1), '?') == '#':
		return True 
	elif coord[1] == minY and board.get((coord[0], coord[1] + 1), '?') == '#' and board.get((coord[0] - 1, coord[1]), '?') == '#' and board.get((cord[0] + 1, coord[1]), '?') == '#':
		return True 
	elif coord[1] == maxY and board.get((coord[0], coord[1] - 1), '?') == '#' and board.get((coord[0] - 1, coord[1]), '?') == '#' and board.get((cord[0] + 1, coord[1]), '?') == '#':
		return True 
	else:
		return False 

def unexplored(board, minX, maxX, minY, maxY):
	unexp = set([])
	for y in range(minY+1, maxY):
		for x in range(minX+1, maxX):
			if board.get((x, y), '?') == '?' and not inaccessible(board, minX, maxX, minY, maxY, (x, y)):
				unexp.add((x, y))
	return unexp 


# Solves as if its a maze, always taking the right-most open path
def repairDroneFindOxegynTank(seedFunction):
	global MANUAL_ENTRY
	board = {}
	sealedSection = seedFunction()
	userInput = [4]
	opcodeTuple = opcodeAssist(userInput, sealedSection, 0, 0, 0)
	paintCount = {}
	maxX = 0
	minX = 0
	maxY = 0
	minY = 0
	count = 1
	droid = (0, 0)
	lastDroid = (0, 0)
	board[droid] = 'D'
	# 1 = north, 2 = south, 3 = west, 4 = east
	# Always taking the rightest path, should start at 4 and cycle 4, 1, 3, 2, 4, ...etc
	lastDir = 4
	djikstra = defaultdict(set)
	toExplore = set([])
	oxygenControl = False
	while opcodeTuple[1] != 99 and (len(toExplore) > 0 or not oxygenControl):
		print("DEBUG: repairDroneFindOxegynTank: toExplore = {} and oxygenControl = {}".format(toExplore, oxygenControl))
		attemptedDroidLocation = newDroidLocation(droid, lastDir)
		#print("DEBUG: repairDroneFindOxegynTank: opcodeTuple = {}".format(opcodeTuple))
		#print("Droid at {}, last direction = {}, and board = {}".format(droid, lastDir, board))
		# Hit Wall Case
		if opcodeTuple[0] == 0:
			board[attemptedDroidLocation] = '#'
			print("DEBUG: repairDroneFindOxegynTank: found wall at {}, last direction was {} and current direction is {}".format(attemptedDroidLocation, lastDir, cycleDir(lastDir, 1)))
			lastDir = cycleDir(lastDir, 1)
			toExplore.discard(attemptedDroidLocation)
		#print("DEBUG: arcadeRunner: board = {} after adding {} at ({}, {})".format(board, opcodeTuple[0], currX, currY))
		elif opcodeTuple[0] == 1:
			board[droid] = ' '
			board[attemptedDroidLocation] = 'D'
			#djikstra[droid].add(attemptedDroidLocation)
			#djikstra[attemptedDroidLocation].add(droid)
			toExplore.discard(attemptedDroidLocation)
			lastDroid = droid
			droid = attemptedDroidLocation
			lastDir = cycleDir(lastDir, 0)
		
		elif opcodeTuple[0] == 2:
			print("INFO: repairDroneFindOxegynTank: Oxygen control found at {}".format(attemptedDroidLocation))
			board[droid] = ' '
			board[attemptedDroidLocation] = 'O'
			#djikstra[droid].add(attemptedDroidLocation)
			#djikstra[attemptedDroidLocation].add(droid)
			toExplore.discard(attemptedDroidLocation)
			droid = attemptedDroidLocation
			lastDir = cycleDir(lastDir, 0)
			drawOxygenRoom(board, minX, maxX, minY, maxY)
			oxygenControl = attemptedDroidLocation
			toExplore = unexplored(board, minX, maxX, minY, maxY)
		else:
			logging.error("Unexpected return code {} from remote droid operation".format(opcodeTuple[1]))
		
		if attemptedDroidLocation[0] > maxX:
			maxX = attemptedDroidLocation[0]
		if attemptedDroidLocation[0] < minX:
			minX = attemptedDroidLocation[0]
		if attemptedDroidLocation[1] > maxY:
			maxY = attemptedDroidLocation[1]
		if attemptedDroidLocation[1] < minY:
			minY = attemptedDroidLocation[1]
			
		sealedSection = opcodeTuple[3]
		userInput.append(lastDir)
		opcodeTuple = opcodeAssist(userInput, sealedSection, opcodeTuple[2], opcodeTuple[4], opcodeTuple[5])
		drawOxygenRoom(board, minX, maxX, minY, maxY)

	return (board, minX, maxX, minY, maxY, oxygenControl)
	
def drawOxygenRoom(board, minX, maxX, minY, maxY):
	#print("DEBUG: drawOxygenRoom: minX = {}, maxX = {}, minY = {}, maxY = {}, board = {}".format(minX, maxX, minY, maxY, board))
	screen = []
	yInd = 0
	xInd = 0
	for y in range(minY, maxY+1):
		screen.append("")
		for x in range(minX, maxX+1):
			screen[yInd] = screen[yInd] + board.get((x, y), '?')
			xInd += 1
		yInd += 1
		xInd = 0
	for s in screen:
		print(s)
	#print(screen)
	return screen 

# Returns the furthest distance the oxygen needs to travel
def oxygenate(graph, oxygen):
	furthestPoint = (0, 0)
	furthestDist = 0
	for k in graph.keys():
		path = djikstraPath(k, oxygen, graph)
		if len(path) - 1 > furthestDist:
			furthestDist = len(path) - 1
			furthestPoint = k 
	return furthestDist - 1
#drawOxygenRoom(repairDroneFindOxegynTank(seedInputArray))

droneTuple = repairDroneFindOxegynTank(seedInputArray)

djikstra = buildGraph(droneTuple[0], droneTuple[1], droneTuple[2], droneTuple[3], droneTuple[4])

#path = djikstraPath((0, 0), droneTuple[5], djikstra)
#print("DEBUG: length of shortest path = {}, path = {}".format(len(path) - 1, path))
print(oxygenate(djikstra, droneTuple[5]))







