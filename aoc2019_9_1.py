import math
import csv
import itertools
import logging

logging.basicConfig(filename='aoc2019_9_1.log',level=logging.DEBUG)

INPUT_PATH = ''
GRAV_VAL = 19690720

CSV_PATH = 'aoc2019_9_1.out.csv'
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
	inputArray = [1102,34463338,34463338,63,1007,63,34463338,63,1005,63,53,1101,0,3,1000,109,988,209,12,9,1000,209,6,209,3,203,0,1008,1000,1,63,1005,63,65,1008,1000,2,63,1005,63,904,1008,1000,0,63,1005,63,58,4,25,104,0,99,4,0,104,0,99,4,17,104,0,99,0,0,1102,1,24,1017,1101,0,36,1006,1101,0,30,1011,1101,26,0,1018,1101,32,0,1015,1101,34,0,1004,1101,0,37,1002,1101,25,0,1012,1102,38,1,1010,1101,29,0,1019,1101,308,0,1029,1102,1,696,1027,1102,1,429,1022,1102,1,21,1005,1102,1,33,1013,1101,39,0,1008,1102,20,1,1009,1101,0,652,1025,1102,313,1,1028,1101,0,31,1003,1102,661,1,1024,1101,35,0,1016,1101,0,23,1000,1102,28,1,1014,1102,0,1,1020,1102,27,1,1007,1101,0,1,1021,1102,22,1,1001,1101,703,0,1026,1101,0,422,1023,109,-5,2101,0,9,63,1008,63,31,63,1005,63,205,1001,64,1,64,1105,1,207,4,187,1002,64,2,64,109,6,2102,1,3,63,1008,63,37,63,1005,63,227,1105,1,233,4,213,1001,64,1,64,1002,64,2,64,109,11,21108,40,40,3,1005,1015,255,4,239,1001,64,1,64,1106,0,255,1002,64,2,64,109,-3,21107,41,40,2,1005,1011,275,1001,64,1,64,1105,1,277,4,261,1002,64,2,64,109,4,2107,28,-6,63,1005,63,297,1001,64,1,64,1106,0,299,4,283,1002,64,2,64,109,15,2106,0,0,4,305,1106,0,317,1001,64,1,64,1002,64,2,64,109,-23,2108,22,4,63,1005,63,337,1001,64,1,64,1105,1,339,4,323,1002,64,2,64,109,6,21101,42,0,0,1008,1011,40,63,1005,63,363,1001,64,1,64,1105,1,365,4,345,1002,64,2,64,109,-17,1207,7,21,63,1005,63,381,1105,1,387,4,371,1001,64,1,64,1002,64,2,64,109,14,1201,-1,0,63,1008,63,25,63,1005,63,407,1105,1,413,4,393,1001,64,1,64,1002,64,2,64,109,15,2105,1,0,1001,64,1,64,1105,1,431,4,419,1002,64,2,64,109,-23,2101,0,6,63,1008,63,36,63,1005,63,453,4,437,1106,0,457,1001,64,1,64,1002,64,2,64,109,10,2108,21,-5,63,1005,63,475,4,463,1106,0,479,1001,64,1,64,1002,64,2,64,109,-3,1201,2,0,63,1008,63,20,63,1005,63,505,4,485,1001,64,1,64,1105,1,505,1002,64,2,64,109,4,2107,35,-5,63,1005,63,527,4,511,1001,64,1,64,1105,1,527,1002,64,2,64,109,15,1206,-5,543,1001,64,1,64,1105,1,545,4,533,1002,64,2,64,109,-8,1205,3,563,4,551,1001,64,1,64,1106,0,563,1002,64,2,64,109,-5,1206,7,581,4,569,1001,64,1,64,1105,1,581,1002,64,2,64,109,-8,1207,-3,38,63,1005,63,599,4,587,1105,1,603,1001,64,1,64,1002,64,2,64,109,19,1205,-4,619,1001,64,1,64,1105,1,621,4,609,1002,64,2,64,109,-13,1208,-4,27,63,1005,63,639,4,627,1105,1,643,1001,64,1,64,1002,64,2,64,109,5,2105,1,8,4,649,1001,64,1,64,1106,0,661,1002,64,2,64,109,-16,1202,4,1,63,1008,63,34,63,1005,63,683,4,667,1106,0,687,1001,64,1,64,1002,64,2,64,109,26,2106,0,1,1001,64,1,64,1105,1,705,4,693,1002,64,2,64,109,-9,21102,43,1,-7,1008,1010,46,63,1005,63,725,1105,1,731,4,711,1001,64,1,64,1002,64,2,64,109,-26,1202,9,1,63,1008,63,26,63,1005,63,755,1001,64,1,64,1105,1,757,4,737,1002,64,2,64,109,34,21108,44,43,-8,1005,1017,773,1106,0,779,4,763,1001,64,1,64,1002,64,2,64,109,-15,21102,45,1,1,1008,1011,45,63,1005,63,801,4,785,1106,0,805,1001,64,1,64,1002,64,2,64,109,-14,1208,10,35,63,1005,63,821,1106,0,827,4,811,1001,64,1,64,1002,64,2,64,109,17,2102,1,-4,63,1008,63,20,63,1005,63,853,4,833,1001,64,1,64,1106,0,853,1002,64,2,64,109,6,21107,46,47,-4,1005,1015,871,4,859,1105,1,875,1001,64,1,64,1002,64,2,64,109,-10,21101,47,0,4,1008,1013,47,63,1005,63,901,4,881,1001,64,1,64,1105,1,901,4,64,99,21102,27,1,1,21102,1,915,0,1106,0,922,21201,1,37790,1,204,1,99,109,3,1207,-2,3,63,1005,63,964,21201,-2,-1,1,21102,1,942,0,1106,0,922,22102,1,1,-1,21201,-2,-3,1,21102,957,1,0,1105,1,922,22201,1,-1,-2,1105,1,968,21201,-2,0,-2,109,-3,2105,1,0]
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

	opcodeOutput = inputs[op3Counter]
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

		'''
		if len(opcode) < 3:
			mode = (0, 0, 0)
		elif len(opcode) < 4:
			mode = (opcode[0], 0, 0)
		elif len(opcode) < 5:
			mode = (opcode[1], opcode[0], 0)
		elif len(opcode) == 5:
			mode = (opcode[2], opcode[1], opcode[0])
		'''

		# code = int(opcode[-2:] if len(opcode) > 2 else int(opopcodeFun))

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

		if v3 >= len(inputArray) and opcodeFun in (1, 2, 7, 8):
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
			#return (opcodeOutput[0], 4, i, opcodeOutput[1], op3Counter)

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
			return (opcodeOutput, 99, 1, inputArray, op3Counter)

		# UKNOWN OPCODE FOUND
		else:
			print("OpcodeUnknown index {}: starting val = {} code = {}".format(i, inputArray[i], opcodeFun))
			opcodeOutput = "ERROR: Unknown opcode found. Invalid input!"
			print("help!")
		#'''
	print("DEBUG: Exited While Loop, i = {},  len(inputArray)) = {}, and inputArray[i] = {}".format(i, len(inputArray), inputArray[i]))
	return (opcodeOutput, 99, 1, inputArray, op3Counter)


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

#seedTestArray()
#seedInputArray()
#ampTester(seedTestArray)
#inputList = list(range(5,10))
#listOfCombinations = list(itertools.permutations(inputList, len(inputList)))
#ampFeedbackRunner(phases, seedFunction, userInput)
#print(listOfCombinations)
#print(ampFeedbackRunner(listOfCombinations, seedInputArray, 0))

#print("\nMaximum Thruster Output = {}".format(amped[0])

#print("\nMax Output generated by phase order {}".format(amped[1]))

print(boostTester(seedInputArray, [1]))













