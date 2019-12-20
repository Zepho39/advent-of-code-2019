import math
import csv

INPUT_PATH = ''
GRAV_VAL = 19690720
USER_INPUT = 1

CSV_PATH = 'aoc2019_5_1.out.csv'

inputArray = []

def opcode1(v1, v2, idest):
	global inputArray
	val = v1 + v2
	print('Opcode1 placing {} at index {}'.format(val, idest))
	inputArray[idest] = val
	#print(inputArray)


def opcode2(v1, v2, idest):
	global inputArray
	val = v1 * v2
	print('Opcode2 placing {} at index {}'.format(val, idest))
	inputArray[idest] = val
	#print(inputArray)

def opcode3(v):
	global inputArray
	global USER_INPUT
	inputArray[v] = USER_INPUT

def opcode4(v):
	global inputArray
	print("Opcode4: Diagnostic Output = {}".format(inputArray[v]))


def seedInputArray():
	global inputArray
	inputArray = [3,225,1,225,6,6,1100,1,238,225,104,0,1101,65,73,225,1101,37,7,225,1101,42,58,225,1102,62,44,224,101,-2728,224,224,4,224,102,8,223,223,101,6,224,224,1,223,224,223,1,69,126,224,101,-92,224,224,4,224,1002,223,8,223,101,7,224,224,1,223,224,223,1102,41,84,225,1001,22,92,224,101,-150,224,224,4,224,102,8,223,223,101,3,224,224,1,224,223,223,1101,80,65,225,1101,32,13,224,101,-45,224,224,4,224,102,8,223,223,101,1,224,224,1,224,223,223,1101,21,18,225,1102,5,51,225,2,17,14,224,1001,224,-2701,224,4,224,1002,223,8,223,101,4,224,224,1,223,224,223,101,68,95,224,101,-148,224,224,4,224,1002,223,8,223,101,1,224,224,1,223,224,223,1102,12,22,225,102,58,173,224,1001,224,-696,224,4,224,1002,223,8,223,1001,224,6,224,1,223,224,223,1002,121,62,224,1001,224,-1302,224,4,224,1002,223,8,223,101,4,224,224,1,223,224,223,4,223,99,0,0,0,677,0,0,0,0,0,0,0,0,0,0,0,1105,0,99999,1105,227,247,1105,1,99999,1005,227,99999,1005,0,256,1105,1,99999,1106,227,99999,1106,0,265,1105,1,99999,1006,0,99999,1006,227,274,1105,1,99999,1105,1,280,1105,1,99999,1,225,225,225,1101,294,0,0,105,1,0,1105,1,99999,1106,0,300,1105,1,99999,1,225,225,225,1101,314,0,0,106,0,0,1105,1,99999,1008,226,677,224,102,2,223,223,1005,224,329,1001,223,1,223,7,677,226,224,102,2,223,223,1006,224,344,1001,223,1,223,1007,226,677,224,1002,223,2,223,1006,224,359,1001,223,1,223,1007,677,677,224,102,2,223,223,1005,224,374,1001,223,1,223,108,677,677,224,102,2,223,223,1006,224,389,101,1,223,223,8,226,677,224,102,2,223,223,1005,224,404,101,1,223,223,7,226,677,224,1002,223,2,223,1005,224,419,101,1,223,223,8,677,226,224,1002,223,2,223,1005,224,434,101,1,223,223,107,677,677,224,1002,223,2,223,1006,224,449,101,1,223,223,7,677,677,224,1002,223,2,223,1006,224,464,101,1,223,223,1107,226,226,224,102,2,223,223,1006,224,479,1001,223,1,223,1007,226,226,224,102,2,223,223,1006,224,494,101,1,223,223,108,226,677,224,1002,223,2,223,1006,224,509,101,1,223,223,1108,226,677,224,102,2,223,223,1006,224,524,1001,223,1,223,1008,226,226,224,1002,223,2,223,1005,224,539,101,1,223,223,107,226,226,224,102,2,223,223,1006,224,554,101,1,223,223,8,677,677,224,102,2,223,223,1005,224,569,101,1,223,223,107,226,677,224,102,2,223,223,1005,224,584,101,1,223,223,1108,226,226,224,1002,223,2,223,1005,224,599,1001,223,1,223,1008,677,677,224,1002,223,2,223,1005,224,614,101,1,223,223,1107,226,677,224,102,2,223,223,1005,224,629,101,1,223,223,1108,677,226,224,1002,223,2,223,1005,224,644,1001,223,1,223,1107,677,226,224,1002,223,2,223,1006,224,659,1001,223,1,223,108,226,226,224,102,2,223,223,1006,224,674,101,1,223,223,4,223,99,226]
	#inputArray[1] = 1
	#inputArray[2] = verb
	#print(inputArray)
	print(len(inputArray))
	header = []
	for i in range (0, len(inputArray)):
		header.append(i)
	with open(CSV_PATH, 'a') as file:
		writer = csv.writer(file)
		writer.writerow(header)


def seedTestArray():
	global inputArray
	inputArray = [1,9,10,3,2,3,11,0,99,30,40,50]
	#print(inputArray)

def gravAssist():
	global inputArray
	i = 0
	#print(len(inputArray))
	loc0 = "ERROR: Shouldn't have returned yet."
	stepCount = 0

	while (i < len(inputArray)) and (inputArray[i] != 99):
		stepCount += 1
		print('\nSTEP {}, ROW {}'.format(stepCount, stepCount + 1))
		with open(CSV_PATH, 'a') as file:
			writer = csv.writer(file)
			writer.writerow(inputArray)

		opcode = str(inputArray[i])
		mode1 = -1
		mode2 = -1
		mode3 = -1

		if len(opcode) < 3:
			mode1 = 0
			mode2 = 0
			mode3 = 0
		elif len(opcode) < 4:
			mode1 = opcode[0]
			mode2 = 0
			mode3 = 0
		elif len(opcode) < 5:
			mode1 = opcode[1]
			mode2 = opcode[0]
			mode3 = 0
		elif len(opcode) == 5:
			mode1 = opcode[2]
			mode2 = opcode[1]
			mode3 = opcode[0]

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
			print("Opcode1 index {}: mode1 = {} mode2 = {} mode3 = {}".format(i, mode1, mode2, mode3))
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
			print("Opcode2 index {}: mode1 = {} mode2 = {} mode3 = {}".format(i, mode1, mode2, mode3))
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
			print("Opcode3 index {}: mode1 = {} mode2 = {} mode3 = {}".format(i, mode1, mode2, mode3))
			print("Opcode3 index {}: v1 = {}".format(i, inputArray[i+1]))
			opcode3(inputArray[i+1])
			i += 2
		elif code == 4:
			print("Opcode4 index {}: starting val = {} code = {}".format(i, inputArray[i], code))
			print("Opcode4 index {}: mode1 = {} mode2 = {} mode3 = {}".format(i, mode1, mode2, mode3))
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
		if opcode in ['1','01','001','0001','00001']:
			print("Opcode1 index {}: starting val = {} code = {}".format(i, inputArray[i], code))
			print("Opcode1 index {}: mode1 = {} mode2 = {} mode3 = {}".format(i, mode1, mode2, mode3))
			print("Opcode1 index {}: v1 = {} v2 = {} v3 = {}".format(i, inputArray[inputArray[i+1]], inputArray[inputArray[i+2]], inputArray[i+3]))
			opcode1(inputArray[inputArray[i+1]], inputArray[inputArray[i+2]], inputArray[i+3])
			i += 4
		elif opcode in ['1101', '01101']:
			print("Opcode1 index {}: starting val = {} code = {}".format(i, inputArray[i], code))
			print("Opcode1 index {}: mode1 = {} mode2 = {} mode3 = {}".format(i, mode1, mode2, mode3))
			print("Opcode1 index {}: v1 = {} v2 = {} v3 = {}".format(i, inputArray[i+1], inputArray[i+2], inputArray[i+3]))
			opcode1(inputArray[i+1], inputArray[i+2], inputArray[i+3])
			i += 4
		elif opcode in ['1001', '01001']:
			print("Opcode1 index {}: starting val = {} code = {}".format(i, inputArray[i], code))
			print("Opcode1 index {}: mode1 = {} mode2 = {} mode3 = {}".format(i, mode1, mode2, mode3))
			print("Opcode1 index {}: v1 = {} v2 = {} v3 = {}".format(i, inputArray[inputArray[i+1]], inputArray[i+2], inputArray[i+3]))
			opcode1(inputArray[inputArray[i+1]], inputArray[i+2], inputArray[i+3])
			i += 4
		elif opcode in ['101', '0101', '00101']:
			print("Opcode1 index {}: starting val = {} code = {}".format(i, inputArray[i], code))
			print("Opcode1 index {}: mode1 = {} mode2 = {} mode3 = {}".format(i, mode1, mode2, mode3))
			print("Opcode1 index {}: v1 = {} v2 = {} v3 = {}".format(i, inputArray[i+1], inputArray[inputArray[i+2]], inputArray[i+3]))
			opcode1(inputArray[i+1], inputArray[inputArray[i+2]], inputArray[i+3])
			i += 4
		elif opcode in ['2','02','002','0002','00002']:
			print("Opcode2 index {}: starting val = {} code = {}".format(i, inputArray[i], code))
			print("Opcode2 index {}: mode1 = {} mode2 = {} mode3 = {}".format(i, mode1, mode2, mode3))
			print("Opcode2 index {}: v1 = {} v2 = {} v3 = {}".format(i, inputArray[inputArray[i+1]], inputArray[inputArray[i+2]], inputArray[i+3]))
			opcode2(inputArray[inputArray[i+1]], inputArray[inputArray[i+2]], inputArray[i+3])
			i += 4
		elif opcode in ['1102', '01102']:
			print("Opcode2 index {}: starting val = {} code = {}".format(i, inputArray[i], code))
			print("Opcode2 index {}: mode1 = {} mode2 = {} mode3 = {}".format(i, mode1, mode2, mode3))
			print("Opcode2 index {}: v1 = {} v2 = {} v3 = {}".format(i, inputArray[i+1], inputArray[i+2], inputArray[i+3]))
			opcode2(inputArray[i+1], inputArray[i+2], inputArray[i+3])
			i += 4
		elif opcode in ['1002', '01002']:
			print("Opcode2 index {}: starting val = {} code = {}".format(i, inputArray[i], code))
			print("Opcode2 index {}: mode1 = {} mode2 = {} mode3 = {}".format(i, mode1, mode2, mode3))
			print("Opcode2 index {}: v1 = {} v2 = {} v3 = {}".format(i, inputArray[inputArray[i+1]], inputArray[i+2], inputArray[i+3]))
			opcode2(inputArray[inputArray[i+1]], inputArray[i+2], inputArray[i+3])
			i += 4
		elif opcode in ['102', '0102', '00102']:
			print("Opcode2 index {}: starting val = {} code = {}".format(i, inputArray[i], code))
			print("Opcode2 index {}: mode1 = {} mode2 = {} mode3 = {}".format(i, mode1, mode2, mode3))
			print("Opcode2 index {}: v1 = {} v2 = {} v3 = {}".format(i, inputArray[i+1], inputArray[inputArray[i+2]], inputArray[i+3]))
			opcode2(inputArray[i+1], inputArray[inputArray[i+2]], inputArray[i+3])
			i += 4
		elif opcode[-1:] in ['3']:
			print("Opcode3 index {}: starting val = {} code = {}".format(i, inputArray[i], code))
			print("Opcode3 index {}: mode1 = {} mode2 = {} mode3 = {}".format(i, mode1, mode2, mode3))
			print("Opcode3 index {}: v1 = {}".format(i, inputArray[i+1]))
			opcode3(inputArray[i+1])
			i += 2
		elif opcode[-1:] in ['4']:
			print("Opcode4 index {}: starting val = {} code = {}".format(i, inputArray[i], code))
			print("Opcode4 index {}: mode1 = {} mode2 = {} mode3 = {}".format(i, mode1, mode2, mode3))
			print("Opcode4 index {}: v1 = {}".format(i, inputArray[i+1]))
			opcode4(inputArray[i+1])
			i += 2
		elif opcode[-2:] in ['99']:
			print("Opcode99 index {}: starting val = {} code = {}".format(i, inputArray[i], code))
			loc0 = inputArray[0]
		else:
			print("OpcodeUnknown index {}: starting val = {} code = {}".format(i, inputArray[i], code))
			loc0 = "ERROR: Unknown opcode found. Invalid input!"
			#print("help!")
		#'''

	loc0 = inputArray[0]
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


seedInputArray()
print(gravAssist())













