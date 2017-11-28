class QBasicTest:
	"""A class which represents a single test, each with it's set of inputs,
	expected outputs and various other properties
	"""

	def __init__(self, transactionType, inputList, expectedOutputList, expectedTransactionFileList):
		self.transactionType = transactionType
		self.inputs = inputList
		self.expectedOutput = expectedOutput
		self.expectedTransactionFile = self.expectedTransactionFile

	def runTest():
		"""Run test"""
		#start QBasic
		#load valid AccountsFile
		#run the inputs
		#gather output from terminal
		#when finished read transaction Summary

	def readTransactionFile(self):
		filename = "../test/{0}/transactionSummary.txt".format(transactionType)
		with open(filename, "r") as f:
			self.outputTransactionFile = [line.strip() for line in f]

	def generateActualOutputsRow(self):
		"""Returns a list representation of the row to put in the test's actualOutputs.csv row"""
		row = self.terminalOutput[:] #slice operator copies the list

		if self.expectedOutput == self.terminalOutput:
			row.append("match")
		else
			row.append("nomatch")

		return row

	def generateResultsRow(self):
		"""Returns a list representation of the row to put in the test's results.csv row"""
		row = self.outputTransactionFile[:] #slice operator copies the list

		if self.expectedTransactionFileList == self.outputTransactionFile:
			row.append("match")
		else
			row.append("nomatch")

		return row