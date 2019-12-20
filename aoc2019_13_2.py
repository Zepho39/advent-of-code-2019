import math
import csv
import itertools
import logging

logging.basicConfig(filename='aoc2019_13_1.log',level=logging.DEBUG)

INPUT_PATH = ''
GRAV_VAL = 19690720

CSV_PATH = 'aoc2019_13_1.out.csv'
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
	#print("Opcode4: Diagnostic Output = {}".format(v))
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
	inputArray = [2,380,379,385,1008,2617,718741,381,1005,381,12,99,109,2618,1102,1,0,383,1102,0,1,382,20101,0,382,1,21001,383,0,2,21102,1,37,0,1105,1,578,4,382,4,383,204,1,1001,382,1,382,1007,382,43,381,1005,381,22,1001,383,1,383,1007,383,23,381,1005,381,18,1006,385,69,99,104,-1,104,0,4,386,3,384,1007,384,0,381,1005,381,94,107,0,384,381,1005,381,108,1105,1,161,107,1,392,381,1006,381,161,1101,0,-1,384,1105,1,119,1007,392,41,381,1006,381,161,1102,1,1,384,21002,392,1,1,21102,21,1,2,21101,0,0,3,21101,138,0,0,1105,1,549,1,392,384,392,20101,0,392,1,21101,21,0,2,21101,3,0,3,21102,161,1,0,1105,1,549,1101,0,0,384,20001,388,390,1,21001,389,0,2,21101,180,0,0,1105,1,578,1206,1,213,1208,1,2,381,1006,381,205,20001,388,390,1,20101,0,389,2,21101,0,205,0,1106,0,393,1002,390,-1,390,1101,0,1,384,20101,0,388,1,20001,389,391,2,21101,0,228,0,1105,1,578,1206,1,261,1208,1,2,381,1006,381,253,20101,0,388,1,20001,389,391,2,21101,253,0,0,1106,0,393,1002,391,-1,391,1101,1,0,384,1005,384,161,20001,388,390,1,20001,389,391,2,21101,0,279,0,1106,0,578,1206,1,316,1208,1,2,381,1006,381,304,20001,388,390,1,20001,389,391,2,21101,0,304,0,1105,1,393,1002,390,-1,390,1002,391,-1,391,1102,1,1,384,1005,384,161,20101,0,388,1,21001,389,0,2,21102,0,1,3,21101,0,338,0,1106,0,549,1,388,390,388,1,389,391,389,20101,0,388,1,20101,0,389,2,21102,4,1,3,21101,0,365,0,1106,0,549,1007,389,22,381,1005,381,75,104,-1,104,0,104,0,99,0,1,0,0,0,0,0,0,363,19,18,1,1,21,109,3,21201,-2,0,1,21202,-1,1,2,21102,1,0,3,21102,1,414,0,1105,1,549,21201,-2,0,1,21201,-1,0,2,21101,0,429,0,1105,1,601,1202,1,1,435,1,386,0,386,104,-1,104,0,4,386,1001,387,-1,387,1005,387,451,99,109,-3,2105,1,0,109,8,22202,-7,-6,-3,22201,-3,-5,-3,21202,-4,64,-2,2207,-3,-2,381,1005,381,492,21202,-2,-1,-1,22201,-3,-1,-3,2207,-3,-2,381,1006,381,481,21202,-4,8,-2,2207,-3,-2,381,1005,381,518,21202,-2,-1,-1,22201,-3,-1,-3,2207,-3,-2,381,1006,381,507,2207,-3,-4,381,1005,381,540,21202,-4,-1,-1,22201,-3,-1,-3,2207,-3,-4,381,1006,381,529,21202,-3,1,-7,109,-8,2105,1,0,109,4,1202,-2,43,566,201,-3,566,566,101,639,566,566,2102,1,-1,0,204,-3,204,-2,204,-1,109,-4,2105,1,0,109,3,1202,-1,43,593,201,-2,593,593,101,639,593,593,21001,0,0,-2,109,-3,2106,0,0,109,3,22102,23,-2,1,22201,1,-1,1,21102,1,499,2,21102,1,317,3,21102,989,1,4,21102,630,1,0,1105,1,456,21201,1,1628,-2,109,-3,2106,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,2,2,0,0,2,2,2,2,2,0,2,2,2,2,2,2,0,2,2,2,0,2,0,2,2,2,2,0,0,2,0,2,2,2,0,2,2,0,2,0,1,1,0,2,2,0,2,0,0,2,2,2,2,0,2,2,2,2,0,0,2,2,0,0,0,0,0,0,2,2,2,0,0,2,2,0,0,2,2,0,2,2,0,1,1,0,0,2,2,0,2,2,2,2,0,2,0,2,2,0,0,0,2,2,2,0,2,0,0,2,2,2,0,2,0,2,2,2,2,2,2,2,2,2,2,0,1,1,0,2,2,0,0,0,2,2,0,2,2,0,0,0,2,2,2,0,2,0,2,0,2,0,2,0,2,2,2,0,0,2,0,0,0,2,0,0,2,2,0,1,1,0,2,2,0,2,2,0,0,0,0,2,2,2,0,0,0,2,2,2,2,2,0,0,2,2,2,2,0,0,2,0,0,0,0,2,2,0,2,0,0,0,1,1,0,2,0,2,0,2,2,0,2,2,0,0,0,0,2,0,2,0,2,0,0,2,2,0,0,0,0,0,0,0,0,2,2,0,2,2,2,2,0,2,0,1,1,0,2,2,2,0,2,2,0,2,0,2,2,0,2,2,2,2,2,2,2,2,2,2,2,0,2,2,2,0,2,2,2,0,2,0,2,2,0,0,2,0,1,1,0,2,0,0,2,2,2,2,2,0,2,0,0,2,0,2,0,0,2,0,0,2,2,2,0,2,2,2,2,2,2,2,2,0,0,2,2,0,0,2,0,1,1,0,0,2,2,2,0,2,2,0,2,2,2,2,0,0,2,2,2,0,2,2,2,2,2,2,2,0,0,0,2,0,2,0,0,2,0,2,2,2,2,0,1,1,0,2,2,0,0,0,2,2,2,2,2,0,0,2,0,2,0,2,0,0,2,2,0,2,2,2,2,0,2,0,2,0,2,0,2,2,2,0,2,2,0,1,1,0,0,2,2,0,2,0,0,2,2,2,2,2,0,2,0,0,2,0,2,2,0,2,2,2,2,0,2,2,0,0,0,0,0,2,0,2,0,2,0,0,1,1,0,2,0,0,2,0,2,2,2,2,2,0,0,2,0,2,2,0,2,2,2,2,2,2,2,0,2,2,0,0,0,2,0,0,2,2,0,2,0,0,0,1,1,0,2,2,0,2,0,2,2,2,0,2,0,0,2,0,0,2,2,2,2,2,0,2,0,0,2,0,2,0,0,2,0,0,2,0,2,2,2,2,2,0,1,1,0,2,2,0,0,2,2,2,2,2,0,2,2,2,2,2,0,2,2,2,2,0,0,2,0,2,2,0,2,2,2,0,2,2,2,0,2,0,2,2,0,1,1,0,2,2,2,0,2,0,0,2,2,0,2,2,2,2,2,0,2,2,2,2,2,0,2,2,2,2,2,2,0,2,0,0,2,2,2,2,2,2,2,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,62,61,33,96,12,3,42,31,62,61,69,2,65,62,56,36,70,53,51,12,11,2,34,79,44,80,63,26,53,77,25,41,86,27,22,53,2,91,21,83,29,72,43,97,90,39,16,31,81,19,60,98,12,7,47,34,12,79,25,34,37,39,8,1,42,23,54,50,9,89,1,87,34,75,96,69,28,67,15,87,10,13,71,26,48,63,30,64,41,79,48,15,80,3,76,93,46,50,46,95,68,70,1,49,19,8,73,30,28,62,73,22,3,36,31,6,4,25,20,23,95,48,82,27,68,88,53,40,24,21,85,69,71,94,77,63,4,79,74,95,72,37,4,46,10,32,46,79,94,54,31,35,46,32,39,44,53,55,48,3,26,92,81,43,56,23,62,15,82,94,20,26,59,22,47,32,68,37,64,8,28,61,90,24,49,47,36,80,8,2,57,11,65,45,22,44,67,29,48,16,82,94,19,11,46,55,79,64,94,84,6,78,12,88,16,95,47,41,8,60,34,85,59,88,49,78,34,61,83,52,58,16,54,24,29,5,87,68,18,60,22,76,35,87,75,42,75,98,43,56,77,12,64,40,53,67,79,31,94,17,65,70,12,67,12,80,62,9,83,72,75,97,52,86,80,19,82,75,80,62,46,3,19,59,97,67,41,22,15,12,48,43,11,98,59,75,48,23,6,16,66,9,8,15,16,90,84,75,24,15,92,44,14,23,87,14,43,70,41,27,65,57,22,45,15,49,10,95,29,41,38,5,81,48,94,6,9,97,43,77,80,61,29,88,37,20,52,96,36,77,25,80,87,90,95,77,67,68,2,80,6,92,98,53,95,35,66,61,40,57,74,50,13,86,38,45,29,74,39,87,97,75,12,22,20,74,24,15,28,20,82,53,32,18,15,54,16,53,65,61,59,72,6,28,6,49,54,65,59,56,12,41,15,90,82,27,94,41,80,63,72,80,33,98,42,49,22,30,93,93,66,5,79,65,42,49,68,43,79,78,14,76,68,22,29,86,47,51,2,61,91,27,68,32,96,84,54,52,3,73,43,27,62,16,68,22,88,57,67,92,92,42,1,95,14,56,92,3,32,42,36,75,4,9,23,49,78,92,87,69,19,37,15,44,44,65,88,69,76,91,5,96,89,33,31,48,32,39,8,1,22,80,96,20,11,65,60,77,47,1,8,27,58,51,47,52,76,4,31,18,89,94,82,97,63,49,95,24,53,35,28,88,39,23,20,44,22,96,86,4,1,15,52,30,18,1,48,34,1,68,12,84,89,83,31,12,98,10,9,10,91,60,97,46,23,88,71,32,38,29,58,21,95,81,86,57,13,7,82,23,63,74,79,1,30,32,53,33,56,25,70,62,17,8,53,21,43,17,27,67,5,4,64,5,65,65,75,25,60,75,42,87,27,40,36,9,7,10,90,91,3,34,57,55,57,25,83,91,88,66,75,22,88,68,67,3,97,40,90,52,60,3,66,78,78,75,41,71,36,5,78,2,50,96,2,35,60,36,61,47,11,11,48,52,4,51,62,57,70,55,60,81,89,25,74,1,26,13,18,31,52,36,31,3,49,60,94,29,15,67,96,25,22,80,69,47,97,11,68,40,17,70,82,42,10,94,30,70,7,3,3,69,47,16,8,8,8,28,35,36,6,42,52,56,22,31,28,69,20,24,90,48,30,70,61,95,45,10,74,3,65,54,46,96,61,31,72,49,92,88,12,49,19,92,11,69,66,78,12,79,32,17,33,41,70,87,71,41,78,12,94,90,36,63,18,64,21,62,24,47,10,77,16,12,1,62,69,13,55,94,11,16,7,35,79,21,18,67,96,60,21,31,21,97,33,90,55,41,14,50,41,3,32,89,22,44,57,55,6,87,9,19,21,22,43,78,16,8,67,25,93,28,43,33,89,83,73,61,70,65,16,77,59,80,78,22,97,77,41,7,27,82,51,42,82,91,18,56,64,33,39,16,70,34,83,85,2,5,67,81,86,19,10,44,15,3,29,2,92,85,8,92,65,51,65,91,59,57,26,2,56,33,52,40,70,98,71,47,27,43,52,78,91,16,83,83,30,32,26,57,77,16,57,65,5,60,81,23,70,51,37,55,94,25,74,10,7,30,25,10,60,41,88,61,4,79,38,67,85,51,98,30,39,81,86,10,55,66,72,18,64,86,69,25,62,37,55,21,79,38,59,4,28,88,65,11,62,79,89,52,21,10,37,7,34,26,47,62,57,718741]
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
		#print('\nINFO: STEP {}, ROW {}'.format(stepCount, stepCount + 1))
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
		#print("DEBUG: opcodeAssist: opcode function = {}, length of input array = {}".format(opcodeFun, len(inputArray)))

		if int(v3) >= len(inputArray) and opcodeFun in (1, 2, 7, 8):
			print("DEBUG: opcodeAssist: Extending inputArray to support write to {}".format(v3))
			inputArray = extendArray(inputArray, v3)

		#print(inputArray)
		
		# OPCODE 1
		if opcodeFun == 1:
			#print("Opcode1 index {}: starting val = {} code = {}".format(i, inputArray[i], opcodeFun))
			#print("Opcode1 index {}: mode1 = {} mode2 = {} mode3 = {}".format(i, mode[0], mode[1], mode[2]))
			#print("Opcode1 index {}: v1 = {} v2 = {} v3 = {}".format(i, v1, v2, v3))
			inputArray = opcode1(v1, v2, v3, inputArray)
			i += 4

		# OPCODE 2
		elif opcodeFun == 2:
			#print("Opcode2 index {}: starting val = {} code = {}".format(i, inputArray[i], opcodeFun))
			#print("Opcode2 index {}: mode1 = {} mode2 = {} mode3 = {}".format(i, mode[0], mode[1], mode[2]))
			#print("Opcode2 index {}: v1 = {} v2 = {} v3 = {}".format(i, v1, v2, v3))
			inputArray = opcode2(v1, v2, v3, inputArray)
			i += 4

		# OPCODE 5
		elif opcodeFun == 5:
			#print("Opcode5 index {}: starting val = {} code = {}".format(i, inputArray[i], opcodeFun))
			#print("Opcode5 index {}: mode1 = {} mode2 = {} mode3 = {}".format(i, mode[0], mode[1], mode[2]))
			#print("Opcode5 index {}: v1 = {} v2 = {}".format(i, v1, v2))
			i = opcode5(i, v1, v2)

		# OPCODE 6
		elif opcodeFun == 6:
			#print("Opcode6 index {}: starting val = {} code = {}".format(i, inputArray[i], opcodeFun))
			#print("Opcode6 index {}: mode1 = {} mode2 = {} mode3 = {}".format(i, mode[0], mode[1], mode[2]))
			#print("Opcode6 index {}: v1 = {} v2 = {}".format(i, v1, v2))
			i = opcode6(i, v1, v2)

		# OPCODE 7
		elif opcodeFun == 7:
			#print("Opcode7 index {}: starting val = {} code = {}".format(i, inputArray[i], opcodeFun))
			#print("Opcode7 index {}: mode1 = {} mode2 = {} mode3 = {}".format(i, mode[0], mode[1], mode[2]))
			#print("Opcode7 index {}: v1 = {} v2 = {} v3 = {}".format(i, v1, v2, v3))
			inputArray = opcode7(v1, v2, v3, inputArray)
			i += 4

		# OPCODE 8
		elif opcodeFun == 8:
			#print("Opcode8 index {}: starting val = {} code = {}".format(i, inputArray[i], opcodeFun))
			#print("Opcode8 index {}: mode1 = {} mode2 = {} mode3 = {}".format(i, mode[0], mode[1], mode[2]))
			#print("Opcode8 index {}: v1 = {} v2 = {} v3 = {}".format(i, v1, v2, v3))
			inputArray = opcode8(v1, v2, v3, inputArray)
			i += 4

		# OPCODE 3
		elif opcodeFun == 3:
			#print("Opcode3 index {}: starting val = {} code = {}".format(i, inputArray[i], opcodeFun))
			#print("Opcode3 index {}: mode1 = {} mode2 = {} mode3 = {}".format(i, mode[0], mode[1], mode[2]))
			#print("Opcode3 index {}: v1 = {}".format(i, v1))
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
			#print("Opcode4 index {}: starting val = {} code = {}".format(i, inputArray[i], opcodeFun))
			#print("Opcode4 index {}: mode1 = {} mode2 = {} mode3 = {}".format(i, mode[0], mode[1], mode[2]))
			#print("Opcode4 index {}: v1 = {}".format(i, inputArray[i+1]))
			opcodeOutput = opcode4(v1, inputArray)
			i += 2
			#print("DEBUG: Opcode4 return index set to {}".format(i))
			return (opcodeOutput[0], 4, i, opcodeOutput[1], op3Counter, relativeBase)

		# OPCODE 9
		elif opcodeFun == 9:
			#print("Opcode9 index {}: starting val = {} code = {}".format(i, inputArray[i], opcodeFun))
			#print("Opcode9 index {}: mode1 = {} mode2 = {} mode3 = {}".format(i, mode[0], mode[1], mode[2]))
			#print("Opcode9 index {}: v1 = {}".format(i, v1))
			relativeBase = opcode9(v1, relativeBase)
			#print("Opcode9 index {}: new relativeBase = {}".format(i, relativeBase))
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

#print("INFO: {} bricks remaining".format(arcadeTester(seedInputArray)))
arcadePlayer(seedInputArray)

#50, 49, 35











