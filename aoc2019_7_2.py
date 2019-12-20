import math
import csv
import itertools
import logging

'''
From https://www.reddit.com/r/adventofcode/comments/e7aqcb/2019_day_7_part_2_confused_with_the_question/


However, the output from amplifier E is now connected into amplifier A's input. This creates the feedback loop: the signal will be sent through the amplifiers many times.

I've read the question a few times and I am still quite confused with exactly how it is supposed to work.

Does this mean:

Amp A reaches opcode 4, outputs, but has yet to halt (99), pauses execution

Amp B starts, takes in phase as input, then takes in Amp A's output as input, then runs until it reaches opcode 4, outputs, has yet to halt, but pauses execution

and so on...

after Amp E outputs, pauses executions

Amp A restarts execution from where it left off, taking in Amp E's output as input the next time it sees opcode 3?

(or does Amp A start again from the start, taking in Amp E's output as input?)

And... exactly when does the whole feedback loop stop?

UPDATE:

Solved!

All your 5 amps should have their own individual memory array that persists in the current feedback loop, until the final thruster value is generated from Amp E.

The phase is only fed to the Amps exactly once (i.e. when the Amps are first "initialised" or "started"). To quote /u/overdue123 "More concretely, A's first inputs are {phase setting}, 0 (as specified in the problem), {Amp E's first output}, {Amp E's second output} ... "

When an individual Amp meets opcode 4 (output), they output a signal to be taken in by the next amp, and then they PAUSE EXECUTION to be resumed again when the loop goes back to the same particular amp (that is, you have to keep track of the instruction pointer for each individual amp). Another example, when Amp E meets opcode 4, Amp E outputs a signal for Amp A, pauses execution, then Amp A begins from where it stopped previously. The next input Amp A takes in IS NOT the phase (since it has already taken in the phase once), but is Amp E's output signal.

One minor correction from /u/Aneurysm9: an Amp doesn't need to pause execution at opcode 4. If there is a buffer or the next amplifier is able to immediately take the output as input then the first amplifier can proceed. The only place that amplifiers must block is when receiving input via opcode 3. Because opcode 3 results in changes in memory which may change the result of the next instruction, the machine cannot proceed until it has received and processed the input.

The whole feedback loop stops when Amp E meets opcode 99 (halt), this is where you should take the last seen output signal as the thrust value.

Quoting /u/sophiebits "For each permutation of phase values, you initialize the 5 amps and their instruction pointers and their memory arrays from scratch, but then they each maintain state (i.e. their memory arrays) through that permutation of phase values (until the next set of phase values).
'''

logging.basicConfig(filename='aoc2019_7_2.log',level=logging.DEBUG)

INPUT_PATH = ''
GRAV_VAL = 19690720

CSV_PATH = 'aoc2019_7_2.out.csv'
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
	print("Opcode4: Diagnostic Output = {}".format(inputArray[v]))
	return (inputArray[v], inputArray)

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


def seedInputArray():
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

	return inputArray


def seedTestArray():
	inputArray = [3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10]

	print("Input length is {}".format(len(inputArray)))
	header = []
	for i in range (0, len(inputArray)):
		header.append(i)
	with open(CSV_PATH, 'w') as file:
		writer = csv.writer(file)
		writer.writerow(header)

	return inputArray

def opcodeAssist(inputs, inputArray, startingIndex, op3Start):
	print("DEBUG: inputs = {}, inputArray = {}, startingIndex = {}, and op3Start = {}".format(inputs, inputArray, startingIndex, op3Start))
	i = startingIndex
	op3Counter = op3Start

	opcodeOutput = inputs[op3Counter]
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

		print(inputArray)
		
		## Before
		# OPCODE 1
		if opcode in ['1','01','001','0001','00001']:
			print("Opcode1 index {}: starting val = {} code = {}".format(i, inputArray[i], code))
			print("Opcode1 index {}: mode1 = {} mode2 = {} mode3 = {}".format(i, mode[0], mode[1], mode[2]))
			print("Opcode1 index {}: v1 = {} v2 = {} v3 = {}".format(i, inputArray[inputArray[i+1]], inputArray[inputArray[i+2]], inputArray[i+3]))
			inputArray = opcode1(inputArray[inputArray[i+1]], inputArray[inputArray[i+2]], inputArray[i+3], inputArray)
			i += 4
		elif opcode in ['1101', '01101']:
			print("Opcode1 index {}: starting val = {} code = {}".format(i, inputArray[i], code))
			print("Opcode1 index {}: mode1 = {} mode2 = {} mode3 = {}".format(i, mode[0], mode[1], mode[2]))
			print("Opcode1 index {}: v1 = {} v2 = {} v3 = {}".format(i, inputArray[i+1], inputArray[i+2], inputArray[i+3]))
			inputArray = opcode1(inputArray[i+1], inputArray[i+2], inputArray[i+3], inputArray)
			i += 4
		elif opcode in ['1001', '01001']:
			print("Opcode1 index {}: starting val = {} code = {}".format(i, inputArray[i], code))
			print("Opcode1 index {}: mode1 = {} mode2 = {} mode3 = {}".format(i, mode[0], mode[1], mode[2]))
			print("Opcode1 index {}: v1 = {} v2 = {} v3 = {}".format(i, inputArray[inputArray[i+1]], inputArray[i+2], inputArray[i+3]))
			inputArray = opcode1(inputArray[inputArray[i+1]], inputArray[i+2], inputArray[i+3], inputArray)
			i += 4
		elif opcode in ['101', '0101', '00101']:
			print("Opcode1 index {}: starting val = {} code = {}".format(i, inputArray[i], code))
			print("Opcode1 index {}: mode1 = {} mode2 = {} mode3 = {}".format(i, mode[0], mode[1], mode[2]))
			print("Opcode1 index {}: v1 = {} v2 = {} v3 = {}".format(i, inputArray[i+1], inputArray[inputArray[i+2]], inputArray[i+3]))
			inputArray = opcode1(inputArray[i+1], inputArray[inputArray[i+2]], inputArray[i+3], inputArray)
			i += 4

		# OPCODE 2
		elif opcode in ['2','02','002','0002','00002']:
			print("Opcode2 index {}: starting val = {} code = {}".format(i, inputArray[i], code))
			print("Opcode2 index {}: mode1 = {} mode2 = {} mode3 = {}".format(i, mode[0], mode[1], mode[2]))
			print("Opcode2 index {}: v1 = {} v2 = {} v3 = {}".format(i, inputArray[inputArray[i+1]], inputArray[inputArray[i+2]], inputArray[i+3]))
			inputArray = opcode2(inputArray[inputArray[i+1]], inputArray[inputArray[i+2]], inputArray[i+3], inputArray)
			i += 4
		elif opcode in ['1102', '01102']:
			print("Opcode2 index {}: starting val = {} code = {}".format(i, inputArray[i], code))
			print("Opcode2 index {}: mode1 = {} mode2 = {} mode3 = {}".format(i, mode[0], mode[1], mode[2]))
			print("Opcode2 index {}: v1 = {} v2 = {} v3 = {}".format(i, inputArray[i+1], inputArray[i+2], inputArray[i+3]))
			inputArray = opcode2(inputArray[i+1], inputArray[i+2], inputArray[i+3], inputArray)
			i += 4
		elif opcode in ['1002', '01002']:
			print("Opcode2 index {}: starting val = {} code = {}".format(i, inputArray[i], code))
			print("Opcode2 index {}: mode1 = {} mode2 = {} mode3 = {}".format(i, mode[0], mode[1], mode[2]))
			print("Opcode2 index {}: v1 = {} v2 = {} v3 = {}".format(i, inputArray[inputArray[i+1]], inputArray[i+2], inputArray[i+3]))
			inputArray = opcode2(inputArray[inputArray[i+1]], inputArray[i+2], inputArray[i+3], inputArray)
			i += 4
		elif opcode in ['102', '0102', '00102']:
			print("Opcode2 index {}: starting val = {} code = {}".format(i, inputArray[i], code))
			print("Opcode2 index {}: mode1 = {} mode2 = {} mode3 = {}".format(i, mode[0], mode[1], mode[2]))
			print("Opcode2 index {}: v1 = {} v2 = {} v3 = {}".format(i, inputArray[i+1], inputArray[inputArray[i+2]], inputArray[i+3]))
			inputArray = opcode2(inputArray[i+1], inputArray[inputArray[i+2]], inputArray[i+3], inputArray)
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
			inputArray = opcode7(inputArray[inputArray[i+1]], inputArray[inputArray[i+2]], inputArray[i+3], inputArray)
			i += 4
		elif opcode in ['1107', '01107']:
			print("Opcode7 index {}: starting val = {} code = {}".format(i, inputArray[i], code))
			print("Opcode7 index {}: mode1 = {} mode2 = {} mode3 = {}".format(i, mode[0], mode[1], mode[2]))
			print("Opcode7 index {}: v1 = {} v2 = {} v3 = {}".format(i, inputArray[i+1], inputArray[i+2], inputArray[i+3]))
			inputArray = opcode7(inputArray[i+1], inputArray[i+2], inputArray[i+3], inputArray)
			i += 4
		elif opcode in ['1007', '01007']:
			print("Opcode7 index {}: starting val = {} code = {}".format(i, inputArray[i], code))
			print("Opcode7 index {}: mode1 = {} mode2 = {} mode3 = {}".format(i, mode[0], mode[1], mode[2]))
			print("Opcode7 index {}: v1 = {} v2 = {} v3 = {}".format(i, inputArray[inputArray[i+1]], inputArray[i+2], inputArray[i+3]))
			inputArray = opcode7(inputArray[inputArray[i+1]], inputArray[i+2], inputArray[i+3], inputArray)
			i += 4
		elif opcode in ['107', '0107', '00107']:
			print("Opcode7 index {}: starting val = {} code = {}".format(i, inputArray[i], code))
			print("Opcode7 index {}: mode1 = {} mode2 = {} mode3 = {}".format(i, mode[0], mode[1], mode[2]))
			print("Opcode7 index {}: v1 = {} v2 = {} v3 = {}".format(i, inputArray[i+1], inputArray[inputArray[i+2]], inputArray[i+3]))
			inputArray = opcode7(inputArray[i+1], inputArray[inputArray[i+2]], inputArray[i+3], inputArray)
			i += 4

		# OPCODE 8
		elif opcode in ['8','08','008','0008','00008']:
			print("Opcode8 index {}: starting val = {} code = {}".format(i, inputArray[i], code))
			print("Opcode8 index {}: mode1 = {} mode2 = {} mode3 = {}".format(i, mode[0], mode[1], mode[2]))
			print("Opcode8 index {}: v1 = {} v2 = {} v3 = {}".format(i, inputArray[inputArray[i+1]], inputArray[inputArray[i+2]], inputArray[i+3]))
			inputArray = opcode8(inputArray[inputArray[i+1]], inputArray[inputArray[i+2]], inputArray[i+3], inputArray)
			i += 4
		elif opcode in ['1108', '01108']:
			print("Opcode8 index {}: starting val = {} code = {}".format(i, inputArray[i], code))
			print("Opcode8 index {}: mode1 = {} mode2 = {} mode3 = {}".format(i, mode[0], mode[1], mode[2]))
			print("Opcode8 index {}: v1 = {} v2 = {} v3 = {}".format(i, inputArray[i+1], inputArray[i+2], inputArray[i+3]))
			inputArray = opcode8(inputArray[i+1], inputArray[i+2], inputArray[i+3], inputArray)
			i += 4
		elif opcode in ['1008', '01008']:
			print("Opcode8 index {}: starting val = {} code = {}".format(i, inputArray[i], code))
			print("Opcode8 index {}: mode1 = {} mode2 = {} mode3 = {}".format(i, mode[0], mode[1], mode[2]))
			print("Opcode8 index {}: v1 = {} v2 = {} v3 = {}".format(i, inputArray[inputArray[i+1]], inputArray[i+2], inputArray[i+3]))
			inputArray = opcode8(inputArray[inputArray[i+1]], inputArray[i+2], inputArray[i+3], inputArray)
			i += 4
		elif opcode in ['108', '0108', '00108']:
			print("Opcode8 index {}: starting val = {} code = {}".format(i, inputArray[i], code))
			print("Opcode8 index {}: mode1 = {} mode2 = {} mode3 = {}".format(i, mode[0], mode[1], mode[2]))
			print("Opcode8 index {}: v1 = {} v2 = {} v3 = {}".format(i, inputArray[i+1], inputArray[inputArray[i+2]], inputArray[i+3]))
			inputArray = opcode8(inputArray[i+1], inputArray[inputArray[i+2]], inputArray[i+3], inputArray)
			i += 4

		# OPCODE 3
		elif opcode[-1:] in ['3']:
			print("Opcode3 index {}: starting val = {} code = {}".format(i, inputArray[i], code))
			print("Opcode3 index {}: mode1 = {} mode2 = {} mode3 = {}".format(i, mode[0], mode[1], mode[2]))
			print("Opcode3 index {}: v1 = {}".format(i, inputArray[i+1]))
			logging.debug("ops3Counter - {}".format(op3Counter))
			#opcode3(inputArray[i+1], inputs[0]) if op3Counter == 0 else opcode3(inputArray[i+1], inputs[1])
			inputArray = opcode3(inputArray[i+1], inputs[op3Counter], inputArray)
			op3Counter += 1
			i += 2

		# OPCODE 4
		elif opcode[-1:] in ['4']:
			print("Opcode4 index {}: starting val = {} code = {}".format(i, inputArray[i], code))
			print("Opcode4 index {}: mode1 = {} mode2 = {} mode3 = {}".format(i, mode[0], mode[1], mode[2]))
			print("Opcode4 index {}: v1 = {}".format(i, inputArray[i+1]))
			if mode[0] == 0:
				opcodeOutput = opcode4(inputArray[i+1], inputArray)
			else:
				opcodeOutput = opcode4(i+1, inputArray)
			i += 2
			print("DEBUG: Opcode4 return index set to {}".format(i))
			return (opcodeOutput[0], 4, i, opcodeOutput[1], op3Counter)

		# OPCODE 99
		elif opcode[-2:] in ['99']:
			print("Opcode99 index {}: starting val = {} code = {}".format(i, inputArray[i], code))
			return (opcodeOutput, 99, 1, inputArray, op3Counter)

		# UKNOWN OPCODE FOUND
		else:
			print("OpcodeUnknown index {}: starting val = {} code = {}".format(i, inputArray[i], code))
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


#seedTestArray()
#seedInputArray()
#ampTester(seedTestArray)
inputList = list(range(5,10))
listOfCombinations = list(itertools.permutations(inputList, len(inputList)))
#ampFeedbackRunner(phases, seedFunction, userInput)
print(listOfCombinations)
print(ampFeedbackRunner(listOfCombinations, seedInputArray, 0))

#print("\nMaximum Thruster Output = {}".format(amped[0])

#print("\nMax Output generated by phase order {}".format(amped[1]))













