import math
import csv

INPUT_PATH = "/Users/bkelly/Desktop/Advent/2019/aoc2019_1_1.csv"
#INPUT_PATH = "/Users/bkelly/Desktop/Advent/2019/aoc2019_1_2_test3.csv"

def fuelReq(mass):
    fuel = math.floor(int(mass) / 3) - 2
    #print(fuel)
    if fuel > 0:
    	fuel += fuelReq(fuel)
    else:
        fuel = 0
    return fuel

def allFuelReq(inputPath):
    totalFuelReq = 0
    fuelFuelReq = -1
    with open(inputPath, newline='') as input:
        reader = csv.reader(input)
        for row in reader:
            totalFuelReq += fuelReq(row[0])
    
    #fuelFuelReq = totalFuelReq
    #while fuelFuelReq > 0:
    #    fuelFuelReq = fuelReq(fuelFuelReq)
    #    totalFuelReq += fuelFuelReq
    print(totalFuelReq)

allFuelReq(INPUT_PATH)