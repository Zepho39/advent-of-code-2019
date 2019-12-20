import math
import csv

INPUT_PATH = "/Users/bkelly/Downloads/aoc2019_1_1.csv"

def fuelReq(mass):
    fuel = math.floor(int(mass) / 3) - 2
    return fuel

def allFuelReq(inputPath):
    totalFuelReq = 0
    with open(inputPath, newline='') as input:
        reader = csv.reader(input)
        for row in reader:
            totalFuelReq += fuelReq(row[0])
    print(totalFuelReq)

allFuelReq(INPUT_PATH)