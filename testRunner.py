import os
import difflib
from pprint import pprint

import testFileCreator

qbasicProgramPath = "src/qbasic.py"
testInputPath = "test/inputs"
testExpectedOutputPath = "test/expectedOutput"
testExpectedTFPath = "test/expectedTF"
testValidAccountsPath = "test/validAccounts"
actualOutputTFPath = "test/actualOutputTF"
actualOutputPath = "test/actualOutput"
reportFN = "report.txt"

commandString = "python src/qbasic.py {va} {tf} < {input} > {output}" #ValidAccount, outputTransactionFile, inputs, outputs

failureDict = {}

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

		os.system(commandString.format(va=validAccountsFile, tf=outputTFFile, input=inputFile, output=outputFile))

def compareAndGenerateReport(transactionName):

	failureDict[transactionName] = []
	directory = os.fsencode(testInputPath + "/{0}".format(transactionName))

	for file in os.listdir(directory):
		filename = os.fsdecode(file)

		if not filename.endswith(".txt"): 
		    continue

		if os.path.exists(testExpectedTFPath + "/{0}/{1}".format(transactionName, filename)) and os.path.exists(actualOutputTFPath + "/{0}/{1}".format(transactionName, filename)):
			with open(testExpectedTFPath + "/{0}/{1}".format(transactionName, filename)) as expTFfile:
				with open(actualOutputTFPath + "/{0}/{1}".format(transactionName, filename)) as actTFfile:
					
					exp = expTFfile.readlines()
					act = actTFfile.readlines()

					d = difflib.Differ()
					#print("Transaction Files " + filename + "-"*15)
					result = list(d.compare(exp, act))
					
					#if any line differs, print diff
					failed = False
					for line in result:
						if not line.startswith("  "):
							failed = True
							break

					if failed:
						print("*********FAILURE**********")
						print("FAILURE tf {0}/{1}".format(transactionName, filename))
						pprint(result)
						failureDict[transactionName].append("TF: " + filename)
					else:
						#print("- pass tf {0}/{1}".format(transactionName, filename))
						pass

		if os.path.exists(testExpectedOutputPath + "/{0}/{1}".format(transactionName, filename)) and os.path.exists(actualOutputPath + "/{0}/{1}".format(transactionName, filename)):
			with open(testExpectedOutputPath + "/{0}/{1}".format(transactionName, filename)) as expOutFile:
				with open(actualOutputPath + "/{0}/{1}".format(transactionName, filename)) as actOutFile:
					
					exp = expOutFile.readlines()
					act = actOutFile.readlines()

					d = difflib.Differ()
					#print("Transaction Files " + filename + "-"*15)
					result = list(d.compare(exp, act))
					
					#if any line differs, print diff
					failed = False
					for line in result:
						if not line.startswith("  "):
							failed = True
							break

					if failed:
						print("*********FAILURE**********")
						print("FAILURE output {0}/{1}".format(transactionName, filename))
						pprint(result)
						failureDict[transactionName].append("TF: " + filename)
					else:
						pass
						#print("- pass output {0}/{1}".format(transactionName, filename))


testTrans = ["createacct", "deleteacct", "login"]
	

def main():
	os.system("cls")
	testFileCreator.init()

	for trans in testTrans:
		testFileCreator.loadAndWrite(trans)
		runTransactionTests(trans)
		compareAndGenerateReport(trans)

if __name__ == "__main__":
	main()