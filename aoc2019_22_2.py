

def newStack(stack):
	return stack[::-1]

def cutStack(stack, depth):
	toBack = stack[:depth]
	toFront = stack[(len(stack)-depth)*-1:]
	#newStack1 = stack[(len(stack)-depth)*-1:]
	#newStack1 += stack[:depth]
	#toFront += toBack
	stack = toFront + toBack
	return stack

def cutNegativeStack(stack, depth):
	stack.reverse()
	stack = cutStack(stack, abs(depth))
	stack.reverse()
	return stack

def dealWithInc(stack, inc):
	newStack = stack.copy()
	pos = 0
	for i in range(len(stack)):
		newStack[pos%len(stack)] = stack[i]
		pos += inc
	return newStack

def createFactoryOrderDeck(size):
	deck = []
	for i in range(size):
		deck.append(i)
	return deck 

def parseInstructions(file, deck):
	with open(file) as shuffling:
		instruction = shuffling.readline().strip('\n')
		while instruction:
			if instruction == 'deal into new stack':
				deck = newStack(deck)
			elif dWI in instruction:
				deck = dealWithInc(deck, int(instruction[len(dWI):]))
			elif cut in instruction:
				inst = int(instruction.strip(cut))
				if inst < 0:
					deck = cutNegativeStack(deck, inst)
				else:
					deck = cutStack(deck, inst)
			instruction = shuffling.readline().strip('\n')
	return deck 

def findCard(deck, value):
	res_list = [i for i, val in enumerate(deck) if val == value] 
	return res_list

def shuffleMultipleTimes(deck, times, file):
	time = 0
	while time < times:
		print("Shuffling for the {}th time".format(time))
		deck = parseInstructions(file, deck)
		time += 1
	return deck 

#deck = [0,1,2,3,4,5,6,7,8,9]
#print(cutStack(deck, 3))
#print(cutNegativeStack(deck, -4))
#print(dealWithInc(deck, 3))
#print(parseInstructions('aoc2019_22.test1.txt', 10))
#deck = parseInstructions('aoc2019_22.input.txt', 10007)
#print(findCard(deck))

deck = createFactoryOrderDeck(119315717514047)
deck = shuffleMultipleTimes(deck, 101741582076661, 'aoc2019_22.input.txt')
print(deck[2020])




