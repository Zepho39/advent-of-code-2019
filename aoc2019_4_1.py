

MIN = 240920
MAX = 789857


def passConsDups(num):
	nString = str(num)
	for i in range(len(nString)):
		if (i + 1) == len(nString):
			return False
		if nString[i] == nString[i+1] and nString[i] != nString[i+2]:
			return True 
	return False

def passIncreasing(num):
	nString = str(num)
	for i in range(len(nString)):
		if (i + 1) == len(nString):
			return True
		if int(nString[i]) > int(nString[i+1]):
			return False
	return True


def passAllChecks(num):
	return (passIncreasing(num) and passConsDups(num))


def passwordsInRange():
	global MIN
	global MAX
	passwords = []
	for i in range(MIN, MAX + 1):
		if passAllChecks(i):
			passwords.append(i)
	return passwords

#print(len(passwordsInRange()))

print(passAllChecks(112233))