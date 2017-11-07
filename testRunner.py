import os
import difflib
from pprint import pprint

qbasicProgramPath = "src/qbasic.py"
testInputPath = "test/inputs"
testExpectedOutputPath = "test/expectedOutput"
testExpectedTFPath = "test/expectedTF"
testValidAccountsPath = "test/validAccounts"
actualOutputTFPath = "test/actualOutputTF"
actualOutputPath = "test/actualOutput"
reportFN = "report.txt"

commandString = "python src/qbasic-interactive.py {va} {tf} < {input} "#"> {output}" #ValidAccount, outputTransactionFile, inputs, outputs

def runTransactionTests(transactionName):
	
	directory = os.fsencode(testInputPath + "/{0}".format(transactionName))

	for file in os.listdir(directory):
		filename = os.fsdecode(file)

		if not filename.endswith(".txt"): 
		    continue

		
		
		validAccountsFile = testValidAccountsPath + "/{0}/validAccounts.txt".format(transactionName)
		outputTFFile = "\"" + actualOutputTFPath + "/{0}/{1}".format(transactionName, filename) + "\""
		inputFile = "\"" + testInputPath + "/{0}/{1}".format(transactionName, filename) + "\""
		outputFile = "\"" + actualOutputPath + "/{0}/{1}".format(transactionName, filename) +"\""

		os.makedirs(actualOutputTFPath + "/{0}".format(transactionName), exist_ok=True)
		os.makedirs(actualOutputPath + "/{0}".format(transactionName), exist_ok=True)			


		# print(validAccountsFile)
		#print(outputTFFile)
		print("-"*30 + inputFile + "-"*15)
		# print(outputFile)

		os.system(commandString.format(va=validAccountsFile, tf=outputTFFile, input=inputFile)) #, output=outputFile))

def compareAndGenerateReport(transactionName):

	directory = os.fsencode(testInputPath + "/{0}".format(transactionName))

	for file in os.listdir(directory):
		filename = os.fsdecode(file)

		if not filename.endswith(".txt"): 
		    continue

		with open(testExpectedTFPath + "/{0}/{1}".format(transactionName, filename)) as expTFfile:
			with open(actualOutputTFPath + "/{0}/{1}".format(transactionName, filename)) as actTFfile:
				
				exp = expTFfile.readlines()
				act = actTFfile.readlines()

				d = difflib.Differ()
				print(filename + "-"*15)
				pprint(list(d.compare(exp, act)))



	

def main():
	#runTransactionTests("createacct")
	#	runTransactionTests("deleteacct")

	compareAndGenerateReport("createacct")

if __name__ == "__main__":
	main()