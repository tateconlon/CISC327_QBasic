#!/usr/bin/env python3
import csv



def readTestInputCsv(transactionName):
	'''

	Reads the inputs for a transactions test suite and returns
	a list of tests, each which contains a list of input for that test
	'''
	filename = "../tests/{0}/inputs.csv".format(transactionName)
	testInputList = []

	with open(filename, "r") as f:
		csv_data = csv.reader(f, delimiter = ",")

		for row in csv_data:
			testInputList.append(row)

	return testInputList

def main():
	print(readTestInputCsv("createacct"))

if __name__ == "__main__":
	main()
