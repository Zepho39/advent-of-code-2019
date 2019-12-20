import math
import csv
import itertools

INPUT_PATH = ''
GRAV_VAL = 19690720

CSV_PATH = 'aoc2019_7_1.out.csv'
#part 1 correct answer = 14522484

inputArray = []

def opcode1(v1, v2, idest):
	global inputArray
	val = v1 + v2
	print('Opcode1 placing {} at index {}'.format(val, idest))
	inputArray[idest] = val


def opcode2(v1, v2, idest):
	global inputArray
	val = v1 * v2
	print('Opcode2 placing {} at index {}'.format(val, idest))
	inputArray[idest] = val

def opcode3(v, userInput):
	global inputArray
	global phase
	inputArray[v] = userInput

def opcode4(v):
	global inputArray
	print("Opcode4: Diagnostic Output = {}".format(inputArray[v]))
	return inputArray[v]

# JUMP-IF-TRUE
# Assumes v2 is indexArray[indexArray[i+2]] or indexArray[i+2], depending on mode
# Returns the new instruction pointer
def opcode5(i, v1, v2):
	if v1 == 0:
		return i + 3
	else:
		return v2 

# JUMP-IF-FALSE
# Assumes v2 is indexArray[indexArray[i+2]] or indexArray[i+2], depending on mode
# Returns the new instruction pointer
def opcode6(i, v1, v2):
	if v1 == 0:
		return v2
	else:
		return i + 3 

# LESS THAN
#
def opcode7(v1, v2, idest):
	if v1 < v2:
		inputArray[idest] = 1
	else:
		inputArray[idest] = 0

# EQUALS
# 
def opcode8(v1, v2, idest):
	if v1 == v2:
		inputArray[idest] = 1
	else:
		inputArray[idest] = 0


def seedInputArray():
	global inputArray
	inputArray = [3,8,1001,8,10,8,105,1,0,0,21,46,67,88,101,126,207,288,369,450,99999,3,9,1001,9,5,9,1002,9,5,9,1001,9,5,9,102,3,9,9,101,2,9,9,4,9,99,3,9,102,4,9,9,101,5,9,9,102,5,9,9,101,3,9,9,4,9,99,3,9,1001,9,3,9,102,2,9,9,1001,9,5,9,102,4,9,9,4,9,99,3,9,102,3,9,9,1001,9,4,9,4,9,99,3,9,102,3,9,9,1001,9,3,9,1002,9,2,9,101,4,9,9,102,3,9,9,4,9,99,3,9,101,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,99,3,9,101,1,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,99,3,9,101,1,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,1,9,4,9,99,3,9,101,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,101,1,9,9,4,9,3,9,101,1,9,9,4,9,99,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,99]
	#inputArray[1] = 1
	#inputArray[2] = verb

	print("Input length is {}".format(len(inputArray)))
	header = []
	for i in range (0, len(inputArray)):
		header.append(i)
	with open(CSV_PATH, 'w') as file:
		writer = csv.writer(file)
		writer.writerow(header)


def seedTestArray():
	global inputArray
	inputArray = [3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0]

	print("Input length is {}".format(len(inputArray)))
	header = []
	for i in range (0, len(inputArray)):
		header.append(i)
	with open(CSV_PATH, 'w') as file:
		writer = csv.writer(file)
		writer.writerow(header)

def opcodeAssist(inputs, seedFunction):
	global inputArray
	seedFunction()
	i = 0
	op3Counter = 0

	loc0 = "ERROR: Shouldn't have returned yet."
	stepCount = 0

	while (i < len(inputArray)) and (inputArray[i] != 99):
		stepCount += 1
		print('\nSTEP {}, ROW {}'.format(stepCount, stepCount + 1))
		with open(CSV_PATH, 'a') as file:
			writer = csv.writer(file)
			writer.writerow(inputArray)

		opcode = str(inputArray[i])

		if len(opcode) < 3:
			mode = (0, 0, 0)
		elif len(opcode) < 4:
			mode = (opcode[0], 0, 0)
		elif len(opcode) < 5:
			mode = (opcode[1], opcode[0], 0)
		elif len(opcode) == 5:
			mode = (opcode[2], opcode[1], opcode[0])

		code = int(opcode[-2:] if len(opcode) > 2 else int(opcode))

		# OPCODE 1
		if opcode in ['1','01','001','0001','00001']:
			print("Opcode1 index {}: starting val = {} code = {}".format(i, inputArray[i], code))
			print("Opcode1 index {}: mode1 = {} mode2 = {} mode3 = {}".format(i, mode[0], mode[1], mode[2]))
			print("Opcode1 index {}: v1 = {} v2 = {} v3 = {}".format(i, inputArray[inputArray[i+1]], inputArray[inputArray[i+2]], inputArray[i+3]))
			opcode1(inputArray[inputArray[i+1]], inputArray[inputArray[i+2]], inputArray[i+3])
			i += 4
		elif opcode in ['1101', '01101']:
			print("Opcode1 index {}: starting val = {} code = {}".format(i, inputArray[i], code))
			print("Opcode1 index {}: mode1 = {} mode2 = {} mode3 = {}".format(i, mode[0], mode[1], mode[2]))
			print("Opcode1 index {}: v1 = {} v2 = {} v3 = {}".format(i, inputArray[i+1], inputArray[i+2], inputArray[i+3]))
			opcode1(inputArray[i+1], inputArray[i+2], inputArray[i+3])
			i += 4
		elif opcode in ['1001', '01001']:
			print("Opcode1 index {}: starting val = {} code = {}".format(i, inputArray[i], code))
			print("Opcode1 index {}: mode1 = {} mode2 = {} mode3 = {}".format(i, mode[0], mode[1], mode[2]))
			print("Opcode1 index {}: v1 = {} v2 = {} v3 = {}".format(i, inputArray[inputArray[i+1]], inputArray[i+2], inputArray[i+3]))
			opcode1(inputArray[inputArray[i+1]], inputArray[i+2], inputArray[i+3])
			i += 4
		elif opcode in ['101', '0101', '00101']:
			print("Opcode1 index {}: starting val = {} code = {}".format(i, inputArray[i], code))
			print("Opcode1 index {}: mode1 = {} mode2 = {} mode3 = {}".format(i, mode[0], mode[1], mode[2]))
			print("Opcode1 index {}: v1 = {} v2 = {} v3 = {}".format(i, inputArray[i+1], inputArray[inputArray[i+2]], inputArray[i+3]))
			opcode1(inputArray[i+1], inputArray[inputArray[i+2]], inputArray[i+3])
			i += 4

		# OPCODE 2
		elif opcode in ['2','02','002','0002','00002']:
			print("Opcode2 index {}: starting val = {} code = {}".format(i, inputArray[i], code))
			print("Opcode2 index {}: mode1 = {} mode2 = {} mode3 = {}".format(i, mode[0], mode[1], mode[2]))
			print("Opcode2 index {}: v1 = {} v2 = {} v3 = {}".format(i, inputArray[inputArray[i+1]], inputArray[inputArray[i+2]], inputArray[i+3]))
			opcode2(inputArray[inputArray[i+1]], inputArray[inputArray[i+2]], inputArray[i+3])
			i += 4
		elif opcode in ['1102', '01102']:
			print("Opcode2 index {}: starting val = {} code = {}".format(i, inputArray[i], code))
			print("Opcode2 index {}: mode1 = {} mode2 = {} mode3 = {}".format(i, mode[0], mode[1], mode[2]))
			print("Opcode2 index {}: v1 = {} v2 = {} v3 = {}".format(i, inputArray[i+1], inputArray[i+2], inputArray[i+3]))
			opcode2(inputArray[i+1], inputArray[i+2], inputArray[i+3])
			i += 4
		elif opcode in ['1002', '01002']:
			print("Opcode2 index {}: starting val = {} code = {}".format(i, inputArray[i], code))
			print("Opcode2 index {}: mode1 = {} mode2 = {} mode3 = {}".format(i, mode[0], mode[1], mode[2]))
			print("Opcode2 index {}: v1 = {} v2 = {} v3 = {}".format(i, inputArray[inputArray[i+1]], inputArray[i+2], inputArray[i+3]))
			opcode2(inputArray[inputArray[i+1]], inputArray[i+2], inputArray[i+3])
			i += 4
		elif opcode in ['102', '0102', '00102']:
			print("Opcode2 index {}: starting val = {} code = {}".format(i, inputArray[i], code))
			print("Opcode2 index {}: mode1 = {} mode2 = {} mode3 = {}".format(i, mode[0], mode[1], mode[2]))
			print("Opcode2 index {}: v1 = {} v2 = {} v3 = {}".format(i, inputArray[i+1], inputArray[inputArray[i+2]], inputArray[i+3]))
			opcode2(inputArray[i+1], inputArray[inputArray[i+2]], inputArray[i+3])
			i += 4

		# OPCODE 5
		elif opcode in ['5','05','005','0005']:
			print("Opcode5 index {}: starting val = {} code = {}".format(i, inputArray[i], code))
			print("Opcode5 index {}: mode1 = {} mode2 = {} mode3 = {}".format(i, mode[0], mode[1], mode[2]))
			print("Opcode5 index {}: v1 = {} v2 = {}".format(i, inputArray[inputArray[i+1]], inputArray[inputArray[i+2]]))
			i = opcode5(i, inputArray[inputArray[i+1]], inputArray[inputArray[i+2]])
		elif opcode in ['1105']:
			print("Opcode5 index {}: starting val = {} code = {}".format(i, inputArray[i], code))
			print("Opcode5 index {}: mode1 = {} mode2 = {} mode3 = {}".format(i, mode[0], mode[1], mode[2]))
			print("Opcode5 index {}: v1 = {} v2 = {}".format(i, inputArray[i+1], inputArray[i+2]))
			i = opcode5(i, inputArray[i+1], inputArray[i+2])
		elif opcode in ['105','0105']:
			print("Opcode5 index {}: starting val = {} code = {}".format(i, inputArray[i], code))
			print("Opcode5 index {}: mode1 = {} mode2 = {} mode3 = {}".format(i, mode[0], mode[1], mode[2]))
			print("Opcode5 index {}: v1 = {} v2 = {}".format(i, inputArray[i+1], inputArray[inputArray[i+2]]))
			i = opcode5(i, inputArray[i+1], inputArray[inputArray[i+2]])
		elif opcode in ['1005']:
			print("Opcode5 index {}: starting val = {} code = {}".format(i, inputArray[i], code))
			print("Opcode5 index {}: mode1 = {} mode2 = {} mode3 = {}".format(i, mode[0], mode[1], mode[2]))
			print("Opcode5 index {}: v1 = {} v2 = {}".format(i, inputArray[inputArray[i+1]], inputArray[i+2]))
			i = opcode5(i, inputArray[inputArray[i+1]], inputArray[i+2])

		# OPCODE 6
		elif opcode in ['6','06','006','0006']:
			print("Opcode6 index {}: starting val = {} code = {}".format(i, inputArray[i], code))
			print("Opcode6 index {}: mode1 = {} mode2 = {} mode3 = {}".format(i, mode[0], mode[1], mode[2]))
			print("Opcode6 index {}: v1 = {} v2 = {}".format(i, inputArray[inputArray[i+1]], inputArray[inputArray[i+2]]))
			i = opcode6(i, inputArray[inputArray[i+1]], inputArray[inputArray[i+2]])
		elif opcode in ['1106']:
			print("Opcode6 index {}: starting val = {} code = {}".format(i, inputArray[i], code))
			print("Opcode6 index {}: mode1 = {} mode2 = {} mode3 = {}".format(i, mode[0], mode[1], mode[2]))
			print("Opcode6 index {}: v1 = {} v2 = {}".format(i, inputArray[i+1], inputArray[i+2]))
			i = opcode6(i, inputArray[i+1], inputArray[i+2])
		elif opcode in ['106','0106']:
			print("Opcode6 index {}: starting val = {} code = {}".format(i, inputArray[i], code))
			print("Opcode6 index {}: mode1 = {} mode2 = {} mode3 = {}".format(i, mode[0], mode[1], mode[2]))
			print("Opcode6 index {}: v1 = {} v2 = {}".format(i, inputArray[i+1], inputArray[inputArray[i+2]]))
			i = opcode6(i, inputArray[i+1], inputArray[inputArray[i+2]])
		elif opcode in ['1006']:
			print("Opcode6 index {}: starting val = {} code = {}".format(i, inputArray[i], code))
			print("Opcode6 index {}: mode1 = {} mode2 = {} mode3 = {}".format(i, mode[0], mode[1], mode[2]))
			print("Opcode6 index {}: v1 = {} v2 = {}".format(i, inputArray[inputArray[i+1]], inputArray[i+2]))
			i = opcode6(i, inputArray[inputArray[i+1]], inputArray[i+2])

		# OPCODE 7
		elif opcode in ['7','07','007','0007','00007']:
			print("Opcode7 index {}: starting val = {} code = {}".format(i, inputArray[i], code))
			print("Opcode7 index {}: mode1 = {} mode2 = {} mode3 = {}".format(i, mode[0], mode[1], mode[2]))
			print("Opcode7 index {}: v1 = {} v2 = {} v3 = {}".format(i, inputArray[inputArray[i+1]], inputArray[inputArray[i+2]], inputArray[i+3]))
			opcode7(inputArray[inputArray[i+1]], inputArray[inputArray[i+2]], inputArray[i+3])
			i += 4
		elif opcode in ['1107', '01107']:
			print("Opcode7 index {}: starting val = {} code = {}".format(i, inputArray[i], code))
			print("Opcode7 index {}: mode1 = {} mode2 = {} mode3 = {}".format(i, mode[0], mode[1], mode[2]))
			print("Opcode7 index {}: v1 = {} v2 = {} v3 = {}".format(i, inputArray[i+1], inputArray[i+2], inputArray[i+3]))
			opcode7(inputArray[i+1], inputArray[i+2], inputArray[i+3])
			i += 4
		elif opcode in ['1007', '01007']:
			print("Opcode7 index {}: starting val = {} code = {}".format(i, inputArray[i], code))
			print("Opcode7 index {}: mode1 = {} mode2 = {} mode3 = {}".format(i, mode[0], mode[1], mode[2]))
			print("Opcode7 index {}: v1 = {} v2 = {} v3 = {}".format(i, inputArray[inputArray[i+1]], inputArray[i+2], inputArray[i+3]))
			opcode7(inputArray[inputArray[i+1]], inputArray[i+2], inputArray[i+3])
			i += 4
		elif opcode in ['107', '0107', '00107']:
			print("Opcode7 index {}: starting val = {} code = {}".format(i, inputArray[i], code))
			print("Opcode7 index {}: mode1 = {} mode2 = {} mode3 = {}".format(i, mode[0], mode[1], mode[2]))
			print("Opcode7 index {}: v1 = {} v2 = {} v3 = {}".format(i, inputArray[i+1], inputArray[inputArray[i+2]], inputArray[i+3]))
			opcode7(inputArray[i+1], inputArray[inputArray[i+2]], inputArray[i+3])
			i += 4

		# OPCODE 8
		elif opcode in ['8','08','008','0008','00008']:
			print("Opcode8 index {}: starting val = {} code = {}".format(i, inputArray[i], code))
			print("Opcode8 index {}: mode1 = {} mode2 = {} mode3 = {}".format(i, mode[0], mode[1], mode[2]))
			print("Opcode8 index {}: v1 = {} v2 = {} v3 = {}".format(i, inputArray[inputArray[i+1]], inputArray[inputArray[i+2]], inputArray[i+3]))
			opcode8(inputArray[inputArray[i+1]], inputArray[inputArray[i+2]], inputArray[i+3])
			i += 4
		elif opcode in ['1108', '01108']:
			print("Opcode8 index {}: starting val = {} code = {}".format(i, inputArray[i], code))
			print("Opcode8 index {}: mode1 = {} mode2 = {} mode3 = {}".format(i, mode[0], mode[1], mode[2]))
			print("Opcode8 index {}: v1 = {} v2 = {} v3 = {}".format(i, inputArray[i+1], inputArray[i+2], inputArray[i+3]))
			opcode8(inputArray[i+1], inputArray[i+2], inputArray[i+3])
			i += 4
		elif opcode in ['1008', '01008']:
			print("Opcode8 index {}: starting val = {} code = {}".format(i, inputArray[i], code))
			print("Opcode8 index {}: mode1 = {} mode2 = {} mode3 = {}".format(i, mode[0], mode[1], mode[2]))
			print("Opcode8 index {}: v1 = {} v2 = {} v3 = {}".format(i, inputArray[inputArray[i+1]], inputArray[i+2], inputArray[i+3]))
			opcode8(inputArray[inputArray[i+1]], inputArray[i+2], inputArray[i+3])
			i += 4
		elif opcode in ['108', '0108', '00108']:
			print("Opcode8 index {}: starting val = {} code = {}".format(i, inputArray[i], code))
			print("Opcode8 index {}: mode1 = {} mode2 = {} mode3 = {}".format(i, mode[0], mode[1], mode[2]))
			print("Opcode8 index {}: v1 = {} v2 = {} v3 = {}".format(i, inputArray[i+1], inputArray[inputArray[i+2]], inputArray[i+3]))
			opcode8(inputArray[i+1], inputArray[inputArray[i+2]], inputArray[i+3])
			i += 4

		# OPCODE 3
		elif opcode[-1:] in ['3']:
			print("Opcode3 index {}: starting val = {} code = {}".format(i, inputArray[i], code))
			print("Opcode3 index {}: mode1 = {} mode2 = {} mode3 = {}".format(i, mode[0], mode[1], mode[2]))
			print("Opcode3 index {}: v1 = {}".format(i, inputArray[i+1]))
			opcode3(inputArray[i+1], inputs[op3Counter])
			i += 2
			op3Counter += 1

		# OPCODE 4
		elif opcode[-1:] in ['4']:
			print("Opcode4 index {}: starting val = {} code = {}".format(i, inputArray[i], code))
			print("Opcode4 index {}: mode1 = {} mode2 = {} mode3 = {}".format(i, mode[0], mode[1], mode[2]))
			print("Opcode4 index {}: v1 = {}".format(i, inputArray[i+1]))
			if mode[0] == 0:
				loc0 = opcode4(inputArray[i+1])
			else:
				loc0 = opcode4(i+1)
			i += 2

		# OPCODE 99
		elif opcode[-2:] in ['99']:
			print("Opcode99 index {}: starting val = {} code = {}".format(i, inputArray[i], code))
			#loc0 = inputArray[0]

		# UKNOWN OPCODE FOUND
		else:
			print("OpcodeUnknown index {}: starting val = {} code = {}".format(i, inputArray[i], code))
			loc0 = "ERROR: Unknown opcode found. Invalid input!"
			#print("help!")
		#'''

	#loc0 = inputArray[0]
	return loc0


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

#
def ampRunner(phases, seedFunction):
	print("DEBUG: phases for this ampRunner run are {}".format(phases))
	A = opcodeAssist((phases[0], 0), seedFunction)
	B = opcodeAssist((phases[1], A), seedFunction)
	C = opcodeAssist((phases[2], B), seedFunction)
	D = opcodeAssist((phases[3], C), seedFunction)
	E = opcodeAssist((phases[4], D), seedFunction)
	return E

# 
def ampTester(seedFunction):
	maxThruster = 0
	maxPhaseOrder = []
	inputList = [0,1,2,3,4]
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


#seedTestArray()
#seedInputArray()
ampTester(seedInputArray)
#print("\nMaximum Thruster Output = {}".format(amped[0])

#print("\nMax Output generated by phase order {}".format(amped[1]))













