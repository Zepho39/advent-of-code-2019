import math

INPUT_PATH = ''
GRAV_VAL = 19690720

inputArray = []

def opcode1(i1, i2, idest):
	global inputArray
	val = inputArray[i1] + inputArray[i2]
	inputArray[idest] = val
	#print(inputArray)


def opcode2(i1, i2, idest):
	global inputArray
	val = inputArray[i1] * inputArray[i2]
	inputArray[idest] = val
	#print(inputArray)


def seedInputArray(noun, verb):
	global inputArray
	inputArray = [1,0,0,3,1,1,2,3,1,3,4,3,1,5,0,3,2,9,1,19,1,19,5,23,1,23,6,27,2,9,27,31,1,5,31,35,1,35,10,39,1,39,10,43,2,43,9,47,1,6,47,51,2,51,6,55,1,5,55,59,2,59,10,63,1,9,63,67,1,9,67,71,2,71,6,75,1,5,75,79,1,5,79,83,1,9,83,87,2,87,10,91,2,10,91,95,1,95,9,99,2,99,9,103,2,10,103,107,2,9,107,111,1,111,5,115,1,115,2,119,1,119,6,0,99,2,0,14,0]
	inputArray[1] = noun
	inputArray[2] = verb
	#print(inputArray)

def seedTestArray():
	global inputArray
	inputArray = [1,9,10,3,2,3,11,0,99,30,40,50]
	#print(inputArray)

def gravAssist():
	global inputArray
	i = 0
	#print(len(inputArray))
	loc0 = "ERROR: Shouldn't have returned yet."
	while (i < len(inputArray)) and (inputArray[i] != 99):
		if inputArray[i] == 1:
			opcode1(inputArray[i+1], inputArray[i+2], inputArray[i+3])
			i += 4
		elif inputArray[i] == 2:
			opcode2(inputArray[i+1], inputArray[i+2], inputArray[i+3])
			i += 4
		elif inputArray[i] == 99:
			loc0 = inputArray[0]
		else:
			loc0 = "ERROR: Unknown opcode found. Invalid input!"
	loc0 = inputArray[0]
	return loc0

def gravAssistTester():
	for i in range(0, 100):
		for j in range(0, 100):
			seedInputArray(i, j)
			loc0 = gravAssist()
			if loc0 == GRAV_VAL:
				print("INFO: Found noun and verb. 100 * noun + verb = " + str((100 * i) + j))
				return "INFO: Success!"
	return "ERROR: No noun/verb combination found in the allowed value ranges."

print(gravAssistTester())













