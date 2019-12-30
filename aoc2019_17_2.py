import math
import csv
import itertools
import logging
from collections import defaultdict

logging.basicConfig(filename='aoc2019_17_2.log',level=logging.DEBUG)

INPUT_PATH = ''
GRAV_VAL = 19690720

CSV_PATH = 'aoc2019_17_2.out.csv'
#part 1 correct answer = 14522484

MANUAL_ENTRY = False

def opcode1(v1, v2, idest, inputArray):
	val = v1 + v2
	#logging.debug("Opcode1 placing {} at index {}".format(val, idest))
	inputArray[idest] = val
	return inputArray


def opcode2(v1, v2, idest, inputArray):
	val = v1 * v2
	#logging.debug("Opcode2 placing {} at index {}".format(val, idest))
	inputArray[idest] = val
	return inputArray

def opcode3(v, userInput, inputArray):
	inputArray[v] = userInput
	return inputArray

def opcode4(v, inputArray):
	logging.debug("Opcode4: Diagnostic Output = {}".format(v))
	return (v, inputArray)

# JUMP-IF-TRUE
# Assumes v2 is indexArray[indexArray[i+2]] or indexArray[i+2], depending on mode
# Returns the new instruction pointer
def opcode5(i, v1, v2):
	if v1 == 0:
		#logging.debug("Opcode5 index {}: v1 = 0, not jumping".format(i))
		return i + 3
	else:
		#logging.debug("Opcode5 index {}: v1 non-zero ({}), jumping to {}".format(i, v1, v2))
		return v2 

# JUMP-IF-FALSE
# Assumes v2 is indexArray[indexArray[i+2]] or indexArray[i+2], depending on mode
# Returns the new instruction pointer
def opcode6(i, v1, v2):
	if v1 == 0:
		#logging.debug("Opcode6 index {}: v1 = 0, jumping to {}".format(i, v2))
		return v2
	else:
		return i + 3 
		#logging.debug("Opcode6 index {}: v1 not 0 ({}), not jumping".format(i, v1))

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
	inputArray = [2,330,331,332,109,3612,1102,1182,1,16,1102,1,1477,24,101,0,0,570,1006,570,36,1001,571,0,0,1001,570,-1,570,1001,24,1,24,1106,0,18,1008,571,0,571,1001,16,1,16,1008,16,1477,570,1006,570,14,21101,0,58,0,1105,1,786,1006,332,62,99,21101,0,333,1,21102,1,73,0,1105,1,579,1102,0,1,572,1102,0,1,573,3,574,101,1,573,573,1007,574,65,570,1005,570,151,107,67,574,570,1005,570,151,1001,574,-64,574,1002,574,-1,574,1001,572,1,572,1007,572,11,570,1006,570,165,101,1182,572,127,1001,574,0,0,3,574,101,1,573,573,1008,574,10,570,1005,570,189,1008,574,44,570,1006,570,158,1106,0,81,21101,0,340,1,1105,1,177,21101,477,0,1,1105,1,177,21102,1,514,1,21102,1,176,0,1105,1,579,99,21102,184,1,0,1105,1,579,4,574,104,10,99,1007,573,22,570,1006,570,165,102,1,572,1182,21101,0,375,1,21102,1,211,0,1106,0,579,21101,1182,11,1,21102,222,1,0,1105,1,979,21102,388,1,1,21101,0,233,0,1105,1,579,21101,1182,22,1,21102,244,1,0,1105,1,979,21101,401,0,1,21101,0,255,0,1106,0,579,21101,1182,33,1,21101,0,266,0,1106,0,979,21101,0,414,1,21102,277,1,0,1105,1,579,3,575,1008,575,89,570,1008,575,121,575,1,575,570,575,3,574,1008,574,10,570,1006,570,291,104,10,21102,1182,1,1,21102,313,1,0,1106,0,622,1005,575,327,1102,1,1,575,21102,327,1,0,1105,1,786,4,438,99,0,1,1,6,77,97,105,110,58,10,33,10,69,120,112,101,99,116,101,100,32,102,117,110,99,116,105,111,110,32,110,97,109,101,32,98,117,116,32,103,111,116,58,32,0,12,70,117,110,99,116,105,111,110,32,65,58,10,12,70,117,110,99,116,105,111,110,32,66,58,10,12,70,117,110,99,116,105,111,110,32,67,58,10,23,67,111,110,116,105,110,117,111,117,115,32,118,105,100,101,111,32,102,101,101,100,63,10,0,37,10,69,120,112,101,99,116,101,100,32,82,44,32,76,44,32,111,114,32,100,105,115,116,97,110,99,101,32,98,117,116,32,103,111,116,58,32,36,10,69,120,112,101,99,116,101,100,32,99,111,109,109,97,32,111,114,32,110,101,119,108,105,110,101,32,98,117,116,32,103,111,116,58,32,43,10,68,101,102,105,110,105,116,105,111,110,115,32,109,97,121,32,98,101,32,97,116,32,109,111,115,116,32,50,48,32,99,104,97,114,97,99,116,101,114,115,33,10,94,62,118,60,0,1,0,-1,-1,0,1,0,0,0,0,0,0,1,2,0,0,109,4,1201,-3,0,587,20102,1,0,-1,22101,1,-3,-3,21102,1,0,-2,2208,-2,-1,570,1005,570,617,2201,-3,-2,609,4,0,21201,-2,1,-2,1106,0,597,109,-4,2105,1,0,109,5,1201,-4,0,629,21002,0,1,-2,22101,1,-4,-4,21102,0,1,-3,2208,-3,-2,570,1005,570,781,2201,-4,-3,652,21001,0,0,-1,1208,-1,-4,570,1005,570,709,1208,-1,-5,570,1005,570,734,1207,-1,0,570,1005,570,759,1206,-1,774,1001,578,562,684,1,0,576,576,1001,578,566,692,1,0,577,577,21101,702,0,0,1106,0,786,21201,-1,-1,-1,1105,1,676,1001,578,1,578,1008,578,4,570,1006,570,724,1001,578,-4,578,21101,731,0,0,1106,0,786,1105,1,774,1001,578,-1,578,1008,578,-1,570,1006,570,749,1001,578,4,578,21101,0,756,0,1106,0,786,1105,1,774,21202,-1,-11,1,22101,1182,1,1,21101,774,0,0,1106,0,622,21201,-3,1,-3,1105,1,640,109,-5,2106,0,0,109,7,1005,575,802,20102,1,576,-6,20101,0,577,-5,1105,1,814,21101,0,0,-1,21101,0,0,-5,21101,0,0,-6,20208,-6,576,-2,208,-5,577,570,22002,570,-2,-2,21202,-5,35,-3,22201,-6,-3,-3,22101,1477,-3,-3,1202,-3,1,843,1005,0,863,21202,-2,42,-4,22101,46,-4,-4,1206,-2,924,21102,1,1,-1,1105,1,924,1205,-2,873,21102,35,1,-4,1105,1,924,2102,1,-3,878,1008,0,1,570,1006,570,916,1001,374,1,374,1201,-3,0,895,1101,2,0,0,1201,-3,0,902,1001,438,0,438,2202,-6,-5,570,1,570,374,570,1,570,438,438,1001,578,558,921,21001,0,0,-4,1006,575,959,204,-4,22101,1,-6,-6,1208,-6,35,570,1006,570,814,104,10,22101,1,-5,-5,1208,-5,61,570,1006,570,810,104,10,1206,-1,974,99,1206,-1,974,1101,0,1,575,21101,973,0,0,1105,1,786,99,109,-7,2105,1,0,109,6,21102,0,1,-4,21101,0,0,-3,203,-2,22101,1,-3,-3,21208,-2,82,-1,1205,-1,1030,21208,-2,76,-1,1205,-1,1037,21207,-2,48,-1,1205,-1,1124,22107,57,-2,-1,1205,-1,1124,21201,-2,-48,-2,1105,1,1041,21102,1,-4,-2,1105,1,1041,21102,-5,1,-2,21201,-4,1,-4,21207,-4,11,-1,1206,-1,1138,2201,-5,-4,1059,1202,-2,1,0,203,-2,22101,1,-3,-3,21207,-2,48,-1,1205,-1,1107,22107,57,-2,-1,1205,-1,1107,21201,-2,-48,-2,2201,-5,-4,1090,20102,10,0,-1,22201,-2,-1,-2,2201,-5,-4,1103,2101,0,-2,0,1106,0,1060,21208,-2,10,-1,1205,-1,1162,21208,-2,44,-1,1206,-1,1131,1106,0,989,21101,0,439,1,1105,1,1150,21102,477,1,1,1105,1,1150,21101,0,514,1,21102,1,1149,0,1105,1,579,99,21102,1157,1,0,1105,1,579,204,-2,104,10,99,21207,-3,22,-1,1206,-1,1138,2101,0,-5,1176,2102,1,-4,0,109,-6,2106,0,0,2,7,34,1,34,1,34,1,34,1,34,1,26,9,26,1,34,1,34,1,34,1,34,1,34,1,34,1,34,1,34,1,34,5,34,1,34,1,34,1,34,1,34,1,34,11,34,1,34,1,11,9,14,1,11,1,22,1,11,1,22,1,11,1,22,1,11,1,22,1,11,1,16,7,11,1,16,1,17,1,16,1,17,1,16,1,17,1,8,7,1,1,11,7,8,1,5,1,1,1,11,1,14,1,5,1,1,1,11,1,14,1,5,1,1,1,11,1,14,1,5,1,1,1,3,5,3,1,14,1,5,1,1,1,3,1,3,1,3,1,14,9,3,1,3,1,3,1,20,1,5,1,3,1,3,1,20,11,3,1,26,1,7,1,18,5,3,1,1,7,18,1,3,1,3,1,1,1,24,1,3,1,3,1,1,1,24,1,3,1,3,1,1,1,24,13,26,1,3,1,1,1,1,1,24,7,1,1,1,1,24,1,1,1,5,1,1,1,24,1,1,1,1,11,20,1,1,1,1,1,3,1,1,1,3,1,14,9,1,1,3,1,1,11,8,1,5,1,3,1,3,1,5,1,5,1,8,1,5,1,3,5,5,1,5,1,8,1,5,1,13,1,5,1,8,1,5,1,13,1,5,1,8,1,5,1,13,1,5,1,8,7,13,7,8]
	#inputArray[1] = 1
	#inputArray[2] = verb

	print("Input length is {}".format(len(inputArray)))
	header = []
	for i in range (0, len(inputArray)):
		header.append(i)
	'''
	with open(CSV_PATH, 'w') as file:
		writer = csv.writer(file)
		writer.writerow(header)
	'''
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
	#logging.debug("inputs = {}, inputArray = {}, startingIndex = {}, and op3Start = {}, relativeBaseStart = {}".format(inputs, inputArray, startingIndex, op3Start, relativeBaseStart))
	i = startingIndex
	op3Counter = op3Start
	relativeBase = relativeBaseStart

	#opcodeOutputZero = inputs[op3Counter] if op3Counter < len(inputs) else inputs[len(inputs) - 1]
	#opcodeOutput = (opcodeOutputZero, inputArray)
	stepCount = 0

	while (i < len(inputArray)) and (inputArray[i] != 99):
		stepCount += 1
		logging.debug("STEP {}, ROW {}".format(stepCount, stepCount + 1))
		'''
		with open(CSV_PATH, 'a') as file:
			writer = csv.writer(file)
			writer.writerow(inputArray)
		'''
		opcode = str(inputArray[i])
		opcodeFun = (10 * get_digit(inputArray[i], 1)) + get_digit(inputArray[i], 0)

		mode = (get_digit(inputArray[i], 2), get_digit(inputArray[i], 3), get_digit(inputArray[i], 4))

		if inputArray[i+1] > len(inputArray):
			inputArray = extendArray(inputArray, inputArray[i+1])
		elif inputArray[i+2] > len(inputArray):
			inputArray = extendArray(inputArray, inputArray[i+2])

		# Arg 1
		#logging.debug("opcodeAssist: Trying to establish v1")
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
		#logging.debug("opcodeAssist: v1 established, v1 = {}".format(v1))

		# Arg 2 TO DO
		#logging.debug("opcodeAssist: Trying to establish v2")
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
		#logging.debug("opcodeAssist: v2 established, v2 = {}".format(v2))

		# Arg 3
		#logging.debug("opcodeAssist: Trying to establish v3")
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
		#logging.debug("opcodeAssist: v3 established, v3 = {}".format(v3))
		logging.debug("opcodeAssist: opcode function = {}, length of input array = {}".format(opcodeFun, len(inputArray)))

		if int(v3) >= len(inputArray) and opcodeFun in (1, 2, 7, 8):
			logging.debug("opcodeAssist: Extending inputArray to support write to {}".format(v3))
			inputArray = extendArray(inputArray, v3)

		#print(inputArray)
		
		# OPCODE 1
		if opcodeFun == 1:
			logging.debug("Opcode1 index {}: starting val = {} code = {}".format(i, inputArray[i], opcodeFun))
			logging.debug("Opcode1 index {}: mode1 = {} mode2 = {} mode3 = {}".format(i, mode[0], mode[1], mode[2]))
			logging.debug("Opcode1 index {}: v1 = {} v2 = {} v3 = {}".format(i, v1, v2, v3))
			inputArray = opcode1(v1, v2, v3, inputArray)
			i += 4

		# OPCODE 2
		elif opcodeFun == 2:
			logging.debug("Opcode2 index {}: starting val = {} code = {}".format(i, inputArray[i], opcodeFun))
			logging.debug("Opcode2 index {}: mode1 = {} mode2 = {} mode3 = {}".format(i, mode[0], mode[1], mode[2]))
			logging.debug("Opcode2 index {}: v1 = {} v2 = {} v3 = {}".format(i, v1, v2, v3))
			inputArray = opcode2(v1, v2, v3, inputArray)
			i += 4

		# OPCODE 5
		elif opcodeFun == 5:
			logging.debug("Opcode5 index {}: starting val = {} code = {}".format(i, inputArray[i], opcodeFun))
			logging.debug("Opcode5 index {}: mode1 = {} mode2 = {} mode3 = {}".format(i, mode[0], mode[1], mode[2]))
			logging.debug("Opcode5 index {}: v1 = {} v2 = {}".format(i, v1, v2))
			i = opcode5(i, v1, v2)

		# OPCODE 6
		elif opcodeFun == 6:
			logging.debug("Opcode6 index {}: starting val = {} code = {}".format(i, inputArray[i], opcodeFun))
			logging.debug("Opcode6 index {}: mode1 = {} mode2 = {} mode3 = {}".format(i, mode[0], mode[1], mode[2]))
			logging.debug("Opcode6 index {}: v1 = {} v2 = {}".format(i, v1, v2))
			i = opcode6(i, v1, v2)

		# OPCODE 7
		elif opcodeFun == 7:
			logging.debug("Opcode7 index {}: starting val = {} code = {}".format(i, inputArray[i], opcodeFun))
			logging.debug("Opcode7 index {}: mode1 = {} mode2 = {} mode3 = {}".format(i, mode[0], mode[1], mode[2]))
			logging.debug("Opcode7 index {}: v1 = {} v2 = {} v3 = {}".format(i, v1, v2, v3))
			inputArray = opcode7(v1, v2, v3, inputArray)
			i += 4

		# OPCODE 8
		elif opcodeFun == 8:
			logging.debug("Opcode8 index {}: starting val = {} code = {}".format(i, inputArray[i], opcodeFun))
			logging.debug("Opcode8 index {}: mode1 = {} mode2 = {} mode3 = {}".format(i, mode[0], mode[1], mode[2]))
			logging.debug("Opcode8 index {}: v1 = {} v2 = {} v3 = {}".format(i, v1, v2, v3))
			inputArray = opcode8(v1, v2, v3, inputArray)
			i += 4

		# OPCODE 3
		elif opcodeFun == 3:
			logging.debug("Opcode3 index {}: starting val = {} code = {}".format(i, inputArray[i], opcodeFun))
			logging.debug("Opcode3 index {}: mode1 = {} mode2 = {} mode3 = {}".format(i, mode[0], mode[1], mode[2]))
			logging.debug("Opcode3 index {}: v1 = {}".format(i, v1))
			logging.debug("ops3Counter - {}".format(op3Counter))
			#opcode3(inputArray[i+1], inputs[0]) if op3Counter == 0 else opcode3(inputArray[i+1], inputs[1])
			global MANUAL_ENTRY
			if MANUAL_ENTRY:
				print("Enter User Input")
				commandLineInput = input()
				inputs.append(int(commandLineInput))

			if mode[0] == 0:
				inputArray = opcode3(inputArray[i+1], inputs[op3Counter], inputArray)
			elif mode[0] == 1:
				inputArray = opcode3(i+1, inputs[op3Counter], inputArray)
			elif mode[0] == 2:
				inputArray = opcode3(inputArray[i+1] + relativeBase, inputs[op3Counter], inputArray)
			logging.debug("Opcode3 index {}: using value {}".format(i, inputs[op3Counter]))
			op3Counter += 1
			i += 2

		# OPCODE 4
		elif opcodeFun == 4:
			logging.debug("Opcode4 index {}: starting val = {} code = {}".format(i, inputArray[i], opcodeFun))
			logging.debug("Opcode4 index {}: mode1 = {} mode2 = {} mode3 = {}".format(i, mode[0], mode[1], mode[2]))
			logging.debug("Opcode4 index {}: v1 = {}".format(i, inputArray[i+1]))
			opcodeOutput = opcode4(v1, inputArray)
			i += 2
			logging.debug("Opcode4 return index set to {}".format(i))
			return (opcodeOutput[0], 4, i, opcodeOutput[1], op3Counter, relativeBase)

		# OPCODE 9
		elif opcodeFun == 9:
			logging.debug("Opcode9 index {}: starting val = {} code = {}".format(i, inputArray[i], opcodeFun))
			logging.debug("Opcode9 index {}: mode1 = {} mode2 = {} mode3 = {}".format(i, mode[0], mode[1], mode[2]))
			logging.debug("Opcode9 index {}: v1 = {}".format(i, v1))
			relativeBase = opcode9(v1, relativeBase)
			logging.debug("Opcode9 index {}: new relativeBase = {}".format(i, relativeBase))
			i += 2

		# OPCODE 99
		elif opcode[-2:] in ['99']:
			#logging.debug("Opcode99 index {}: starting val = {} code = {}".format(i, inputArray[i], opcodeFun))
			return (opcodeOutput, 99, 1, inputArray, op3Counter, relativeBase)

		# UKNOWN OPCODE FOUND
		else:
			#logging.debug("OpcodeUnknown index {}: starting val = {} code = {}".format(i, inputArray[i], opcodeFun))
			opcodeOutput = "ERROR: Unknown opcode found. Invalid input!"
			print("help!")
		#'''
	#logging.debug("Exited While Loop, i = {},  len(inputArray)) = {}, and inputArray[i] = {}".format(i, len(inputArray), inputArray[i]))
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
	logging.debug("phases for this ampRunner run are {}".format(phases))
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
		logging.debug("Running phase {}: {}".format(idx, phase))
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
	# 	#logging.debug("Opcode4: Diagnostic Output = {}".format(v))
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
			logging.debug("hullPaintingRobot robot's location {} is currently {}, was painted {}".format(robotLocation, hull.get(robotLocation, 0), opcodeTuple[0]))
			if hull.get(robotLocation, 0) != opcodeTuple[0]:
				hull[robotLocation] = opcodeTuple[0]
				paintCount[robotLocation] = paintCount.get(robotLocation, 0) + 1
			output = 2
		elif output == 2:
			currentDir = rotate(opcodeTuple[0], currentDir)
			logging.debug("hullPaintingRobot current direction is {} and current robot location before moving is {}".format(currentDir, robotLocation))
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
			#logging.debug("arcadeRunner: board = {} after adding {} at ({}, {})".format(board, opcodeTuple[0], currX, currY))
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
				#logging.debug("arcadeRunner: screen = {}".format(screen))
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
	#logging.debug("arcadeRunner: screen = {}".format(screen))
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
		logging.debug("repairDroneFindOxegynTank: toExplore = {} and oxygenControl = {}".format(toExplore, oxygenControl))
		attemptedDroidLocation = newDroidLocation(droid, lastDir)
		#logging.debug("repairDroneFindOxegynTank: opcodeTuple = {}".format(opcodeTuple))
		#print("Droid at {}, last direction = {}, and board = {}".format(droid, lastDir, board))
		# Hit Wall Case
		if opcodeTuple[0] == 0:
			board[attemptedDroidLocation] = '#'
			logging.debug("repairDroneFindOxegynTank: found wall at {}, last direction was {} and current direction is {}".format(attemptedDroidLocation, lastDir, cycleDir(lastDir, 1)))
			lastDir = cycleDir(lastDir, 1)
			toExplore.discard(attemptedDroidLocation)
		#logging.debug("arcadeRunner: board = {} after adding {} at ({}, {})".format(board, opcodeTuple[0], currX, currY))
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
	#logging.debug("drawOxygenRoom: minX = {}, maxX = {}, minY = {}, maxY = {}, board = {}".format(minX, maxX, minY, maxY, board))
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

def buildScaffoldingView(seedFunction):
	scaffold = seedFunction()
	global MANUAL_ENTRY
	board = []
	boardGraph = {}
	userInput = []
	opcodeTuple = opcodeAssist(userInput, scaffold, 0, 0, 0)
	maxX = 0
	minX = 0
	maxY = 0
	minY = 0
	count = 0
	start = (0, 0)
	line = ""
	main = "A,C,C,A,B,A,B,A,B,C\n"
	A = "R,6,R,6,R,8,L,10,L,4\n"
	B = "L,4,L,12,R,6,L,10\n"
	C = "R,6,L,10,R,8\n"
	video = 'n\n'
	inputs = main + A + B + C + video
	for c in inputs:
		userInput.append(ord(c))
	while opcodeTuple[1] != 99:
		if opcodeTuple[0] == 35:
			logging.debug("buildScaffoldingView: adding # to line")
			boardGraph[(count, len(line))] = '#'
			line += '#'
		elif opcodeTuple[0] == 46:
			logging.debug("buildScaffoldingView: adding . to line")
			boardGraph[(count, len(line))] = '.'
			line += '.'
		elif opcodeTuple[0] == 10:
			logging.debug("buildScaffoldingView: found end of line")
			board.append(line)
			line = ""
			count += 1
		elif opcodeTuple[0] == 60:
			logging.debug("buildScaffoldingView: adding < to line")
			boardGraph[(count, len(line))] = '<'
			line += '<'
		elif opcodeTuple[0] == 62:
			logging.debug("buildScaffoldingView: adding > to line")
			boardGraph[(count, len(line))] = '>'
			line += '>'
		elif opcodeTuple[0] == 94:
			logging.debug("buildScaffoldingView: adding ^ to line")
			boardGraph[(count, len(line))] = '^'
			line += '^'
		elif opcodeTuple[0] == 118:
			logging.debug("buildScaffoldingView: adding v to line")
			boardGraph[(count, len(line))] = 'v'
			line += 'v'
		elif opcodeTuple[0] in [88, 120]:
			logging.debug("buildScaffoldingView: adding X to line")
			boardGraph[(count, len(line))] = 'X'
			line += 'X'
		else:
			print("ERROR: buildScaffoldingView: uknown return code found {}".format(opcodeTuple[0]))
		opcodeTuple = opcodeAssist(userInput, scaffold, opcodeTuple[2], opcodeTuple[4], opcodeTuple[5])
		logging.debug("buildScaffoldingView: Current line = {}".format(line))
		print(board)
	return (board, boardGraph)

def findAlignmentParams(boardGraph, lenX, lenY):
	params = {}
	for y in range(lenY):
		for x in range(lenX):
			if boardGraph.get((x, y), '?') == '#' and boardGraph.get((x-1, y), '?') == '#' and boardGraph.get((x+1, y), '?') == '#' and boardGraph.get((x, y-1), '?') == '#' and boardGraph.get((x, y+1), '?') == '#':
				params[(x, y)] = x * y
	return params

scaffTuple = buildScaffoldingView(seedInputArray)
print(scaffTuple[0])

params = findAlignmentParams(scaffTuple[1], len(scaffTuple[0]), len(scaffTuple[0][0]))

totalParams = 0
for k, v in params.items():
	totalParams += v 

print(totalParams)

'''
Inputs, counted visually:

A,C,C,A,B,A,B,A,B,C
R,6,R,6,R,8,L,10,L,4
L,4,L,12,R,6,L,10,
R,6,L,10,R,8

video = 'y\n'

As commands
65 44 67 44 67 44 65 44 66 44 65 44 66 44 65 44 66 44 67 10
76 44 6 44 4 44 |76 44 4 44 76 44 4 44 76 44 6 44 6 44 |82 44 6 44 76 44 6 44 4 44 82 4 46 10
76446444448244810
824464482446448244810

Y = 89, y = 121
N = 78, n = 110
L = 76
R = 82
, = 44

65  A         97  a
66  B         98  b
67  C 		  99  c

52  4 
54  6 
56  8
48  0
49  1
50  2
'''







