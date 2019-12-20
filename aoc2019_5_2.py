import math
import csv

INPUT_PATH = ''
GRAV_VAL = 19690720
USER_INPUT = 5

CSV_PATH = 'aoc2019_5_2.out.csv'
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

def opcode3(v):
	global inputArray
	global USER_INPUT
	inputArray[v] = USER_INPUT

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
	inputArray = [3,225,1,225,6,6,1100,1,238,225,104,0,1101,65,73,225,1101,37,7,225,1101,42,58,225,1102,62,44,224,101,-2728,224,224,4,224,102,8,223,223,101,6,224,224,1,223,224,223,1,69,126,224,101,-92,224,224,4,224,1002,223,8,223,101,7,224,224,1,223,224,223,1102,41,84,225,1001,22,92,224,101,-150,224,224,4,224,102,8,223,223,101,3,224,224,1,224,223,223,1101,80,65,225,1101,32,13,224,101,-45,224,224,4,224,102,8,223,223,101,1,224,224,1,224,223,223,1101,21,18,225,1102,5,51,225,2,17,14,224,1001,224,-2701,224,4,224,1002,223,8,223,101,4,224,224,1,223,224,223,101,68,95,224,101,-148,224,224,4,224,1002,223,8,223,101,1,224,224,1,223,224,223,1102,12,22,225,102,58,173,224,1001,224,-696,224,4,224,1002,223,8,223,1001,224,6,224,1,223,224,223,1002,121,62,224,1001,224,-1302,224,4,224,1002,223,8,223,101,4,224,224,1,223,224,223,4,223,99,0,0,0,677,0,0,0,0,0,0,0,0,0,0,0,1105,0,99999,1105,227,247,1105,1,99999,1005,227,99999,1005,0,256,1105,1,99999,1106,227,99999,1106,0,265,1105,1,99999,1006,0,99999,1006,227,274,1105,1,99999,1105,1,280,1105,1,99999,1,225,225,225,1101,294,0,0,105,1,0,1105,1,99999,1106,0,300,1105,1,99999,1,225,225,225,1101,314,0,0,106,0,0,1105,1,99999,1008,226,677,224,102,2,223,223,1005,224,329,1001,223,1,223,7,677,226,224,102,2,223,223,1006,224,344,1001,223,1,223,1007,226,677,224,1002,223,2,223,1006,224,359,1001,223,1,223,1007,677,677,224,102,2,223,223,1005,224,374,1001,223,1,223,108,677,677,224,102,2,223,223,1006,224,389,101,1,223,223,8,226,677,224,102,2,223,223,1005,224,404,101,1,223,223,7,226,677,224,1002,223,2,223,1005,224,419,101,1,223,223,8,677,226,224,1002,223,2,223,1005,224,434,101,1,223,223,107,677,677,224,1002,223,2,223,1006,224,449,101,1,223,223,7,677,677,224,1002,223,2,223,1006,224,464,101,1,223,223,1107,226,226,224,102,2,223,223,1006,224,479,1001,223,1,223,1007,226,226,224,102,2,223,223,1006,224,494,101,1,223,223,108,226,677,224,1002,223,2,223,1006,224,509,101,1,223,223,1108,226,677,224,102,2,223,223,1006,224,524,1001,223,1,223,1008,226,226,224,1002,223,2,223,1005,224,539,101,1,223,223,107,226,226,224,102,2,223,223,1006,224,554,101,1,223,223,8,677,677,224,102,2,223,223,1005,224,569,101,1,223,223,107,226,677,224,102,2,223,223,1005,224,584,101,1,223,223,1108,226,226,224,1002,223,2,223,1005,224,599,1001,223,1,223,1008,677,677,224,1002,223,2,223,1005,224,614,101,1,223,223,1107,226,677,224,102,2,223,223,1005,224,629,101,1,223,223,1108,677,226,224,1002,223,2,223,1005,224,644,1001,223,1,223,1107,677,226,224,1002,223,2,223,1006,224,659,1001,223,1,223,108,226,226,224,102,2,223,223,1006,224,674,101,1,223,223,4,223,99,226]
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
	inputArray = [3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99]

	print("Input length is {}".format(len(inputArray)))
	header = []
	for i in range (0, len(inputArray)):
		header.append(i)
	with open(CSV_PATH, 'w') as file:
		writer = csv.writer(file)
		writer.writerow(header)

def gravAssist():
	global inputArray
	i = 0

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
		#v1 = -9999
		#v2 = -9999
		#v3 = -9999
		'''
		if code == 1:
			v1 = inputArray[inputArray[i+1]] if mode1 == 0 else inputArray[i+1]
			v2 = inputArray[inputArray[i+2]] if mode2 == 0 else inputArray[i+2]
			v3 = inputArray[i+3] if mode3 == 0 else (i + 3)
			#v1_0 = inputArray[inputArray[i+1]]
			#v1_1 = inputArray[i+1]
			#v2_0 = inputArray[inputArray[i+2]]
			#v2_1 = inputArray[i+2]
			#v3_0 = inputArray[i+3]
			#v3_1 = (i + 3)
			print("Opcode1 index {}: starting val = {} code = {}".format(i, inputArray[i], code))
			print("Opcode1 index {}: mode1 = {} mode2 = {} mode3 = {}".format(i, mode[0], mode[1], mode[2]))
			#print("Opcode1 index {}: Positional v1 = {} positional v2 = {} positional v3 = {}".format(i, v1_0, v2_0, v3_0))
			#print("Opcode1 index {}: Immediate v1 = {} immediate v2 = {} immediate v3 = {}".format(i, v1_1, v2_1, v3_1))
			#v1 = v1_0 if mode1 == 0 else v1_1
			#v2 = v2_0 if mode2 == 0 else v2_1
			#v3 = v3_0 if mode3 == 0 else v3_1
			print("Opcode1 index {}: v1 = {} v2 = {} v3 = {}".format(i, v1, v2, v3))
			opcode1(v1, v2, v3)
			i += 4
		elif code == 2:
			v1 = inputArray[inputArray[i+1]] if mode1 == 0 else inputArray[i+1]
			v2 = inputArray[inputArray[i+2]] if mode2 == 0 else inputArray[i+2]
			v3 = inputArray[i+3] if mode3 == 0 else (i + 3)
			#v1_0 = inputArray[inputArray[i+1]]
			#v1_1 = inputArray[i+1]
			#v2_0 = inputArray[inputArray[i+2]]
			#v2_1 = inputArray[i+2]
			#v3_0 = inputArray[i+3]
			#v3_1 = (i + 3)
			print("Opcode2 index {}: starting val = {} code = {}".format(i, inputArray[i], code))
			print("Opcode2 index {}: mode1 = {} mode2 = {} mode3 = {}".format(i, mode[0], mode[1], mode[2]))
			#print("Opcode2 index {}: Positional v1 = {} positional v2 = {} positional v3 = {}".format(i, v1_0, v2_0, v3_0))
			#print("Opcode2 index {}: Immediate v1 = {} immediate v2 = {} immediate v3 = {}".format(i, v1_1, v2_1, v3_1))
			#v1 = v1_0 if mode1 == 0 else v1_1
			#v2 = v2_0 if mode2 == 0 else v2_1
			#v3 = v3_0 if mode3 == 0 else v3_1
			print("Opcode2 index {}: v1 = {} v2 = {} v3 = {}".format(i, v1, v2, v3))
			opcode2(v1, v2, v3)
			i += 4
		elif code == 3:
			print("Opcode3 index {}: starting val = {} code = {}".format(i, inputArray[i], code))
			print("Opcode3 index {}: mode1 = {} mode2 = {} mode3 = {}".format(i, mode[0], mode[1], mode[2]))
			print("Opcode3 index {}: v1 = {}".format(i, inputArray[i+1]))
			opcode3(inputArray[i+1])
			i += 2
		elif code == 4:
			print("Opcode4 index {}: starting val = {} code = {}".format(i, inputArray[i], code))
			print("Opcode4 index {}: mode1 = {} mode2 = {} mode3 = {}".format(i, mode[0], mode[1], mode[2]))
			print("Opcode4 index {}: v1 = {}".format(i, inputArray[i+1]))
			opcode4(inputArray[i+1])
			i += 2
		elif code == 99:
			print("Opcode99 index {}: starting val = {} code = {}".format(i, inputArray[i], code))
			loc0 = inputArray[0]
		else:
			print("OpcodeUnknown index {}: starting val = {} code = {}".format(i, inputArray[i], code))
			loc0 = "ERROR: Unknown opcode found. Invalid input!"
			#print("help!")
		'''

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
			opcode3(inputArray[i+1])
			i += 2

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

'''
def gravAssistTester():
	for i in range(0, 100):
		for j in range(0, 100):
			seedInputArray(i, j)
			loc0 = gravAssist()
			if loc0 == GRAV_VAL:
				print("INFO: Found noun and verb. 100 * noun + verb = " + str((100 * i) + j))
				return "INFO: Success!"
	return "ERROR: No noun/verb combination found in the allowed value ranges."
'''

#seedTestArray()
seedInputArray()
print("\nFinal Code = {}".format(gravAssist()))













