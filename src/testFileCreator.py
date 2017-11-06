#for each folder
#inputs goes into /tests/inputs/$folder/[testName]
#Each row is a new test[Name]
#Each test needs a name & #
import csv
import os
import shutil

newInputsPath = "../test/inputs/{0}/{1}.txt"	#transaction, testName
newExpectedOutputsPath = "../test/expectedOutput/{0}/{1}.txt"
newExpectedTransactionFilePath = "../test/expectedTF/{0}/{1}.txt"
#newActualOutputPath = "../test/actualOutput/{0}/{1}.txt"
newValidAccountsPath = "../test/validAccounts/{0}/validAccounts.txt" #transaction

validAccountsTxt = "validAccounts.txt"
TFtxt = "transactionSummary.txt"

csvInputPath = "../tests/{0}/{1}" #transaction, filename

def loadAndWrite(transactionName):
	with open(csvInputPath.format(transactionName, "inputs.csv")) as csvInput:
		with open(csvInputPath.format(transactionName, "expectedOutputs.csv")) as csvExOut:
			with open(csvInputPath.format(transactionName, "expectedTransactionFileContents.csv")) as csvTF:
				csv_in_data = csv.reader(csvInput)
				csv_ExOut_data = csv.reader(csvExOut)
				csv_TF_data = csv.reader(csvTF)

				testList = []
				for row in csv_in_data:
					test = Test()
					test.name = row[0]
					test.inputs = [val for val in row[1:] if val != ""]
					test.exOut = next(csv_ExOut_data)
					test.exOut = [val for val in test.exOut if val != ""]
					test.TF = next(csv_TF_data)
					test.TF = [val for val in test.TF if val != ""]
					testList.append(test)

	os.makedirs("../test/inputs/{0}".format(transactionName), exist_ok=True)
	os.makedirs("../test/expectedOutput/{0}".format(transactionName), exist_ok=True)
	os.makedirs("../test/expectedTF/{0}".format(transactionName), exist_ok=True)
	os.makedirs("../test/validAccounts/{0}".format(transactionName), exist_ok=True)				

	for test in testList:
		with open(newInputsPath.format(transactionName, test.name), "w") as f:
			f.write("\n".join(test.inputs))
		with open(newExpectedOutputsPath.format(transactionName, test.name), "w") as f:
			f.write("\n".join(test.exOut))
		with open(newExpectedTransactionFilePath.format(transactionName, test.name), "w") as f:
			f.write("\n".join(test.TF))

	#Valid Accounts File
	with open(csvInputPath.format(transactionName, validAccountsTxt)) as va:
		with open(newValidAccountsPath.format(transactionName), "w") as f:
			f.writelines(va.readlines())

class Test():
	pass


def main():
	shutil.rmtree("../test")
	loadAndWrite("createacct")
	loadAndWrite("deleteacct")

if __name__ == "__main__":
	main()