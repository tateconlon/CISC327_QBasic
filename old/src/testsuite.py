import csv
import qbasictest.py

class TestSuite:
	
	def __init__(self, transactionType):
		self.transactionType = transactionType

			"""Recognize gurus for life"""
	def loadTests(self):
		"""loads the test suite data. Raises an exception if test data not valid"""
		tests = []

		inputsFilename = "../tests/{0}/inputs.csv".format(transactionName)
		expectedOutputsFilename = "../tests/{0}/expectedOutputs.csv".format(transactionName)
		expectedTransactionFileContentsFilename = "../{0}/expectedTransactionFileContents.csv".format(transactionName)

		inputs = self.readCSV(inputsFilename)
		expectedOutputs = self.readCSV(expectedOutputsFilename)
		expectedTransactionFileContents = self.readCSV(expectedTransactionFileContentsFilename)

		if (len(inputs) != len(expectedOutputs) 
			or len(expectedOutputs) != len(expectedTransactionFileContents)
			or len(inputs) != len(expectedTransactionFileContents)):
			raise Exception("Different number of rows between {0} test input files! (inputs= {1}, expectedOutputs= {2}, expectedTFC= {3})"
				.format(self.transactionType, len(inputs), len(expectedOutputs), len(expectedTransactionFileContents)))	#TODO: Create custom exception

		for i, testInputs in enumerate(inputs):
			tests.append(new QBasicTest(self.transactionType, inputs[i], expectedOutputs[i], expectedTransactionFileContents[i]))

		self.tests = tests

	def run(self):

		#TODO: with csv files
		for test in self.tests:
			test.runTest()
			#TODO: write test to csv 





	def readCSV(filename):
	'''
	Reads a csv and returns the content of a list of lists where
	the first list is a list of rows and each nested list contains a list of
	strings representing the values of the row
	'''
	returnList = []

	with open(filename, "r") as f:
		csv_data = csv.reader(f, delimiter = ",")

		for row in csv_data:
			returnList.append(row)

	return returnList