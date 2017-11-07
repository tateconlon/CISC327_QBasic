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
					test.inputs = sanatize_input(row[1:])
					test.exOut = sanatize_input(next(csv_ExOut_data))
					test.TF = sanatize_input(next(csv_TF_data))
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

def sanatize_input(lines):
	new_lines = []
	for line in lines:
		temp_line = line.strip()
		if temp_line != "":
			new_lines.append(temp_line)

	return new_lines

class Test():
	pass

def main():
	shutil.rmtree("../test", ignore_errors=True )
	loadAndWrite("createacct")
	loadAndWrite("deleteacct")
	#loadAndWrite("logout")
	loadAndWrite("login")


if __name__ == "__main__":
	main()