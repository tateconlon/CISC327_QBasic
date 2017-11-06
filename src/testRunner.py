import os

qbasicProgramPath = "src/qbasic.py"
testInputPath = "test/inputs"
testExpectedOutputPath = "test/expectedOutput"
testExpectedTransFileSummaryPath = "test/expectedTF"
testValidAccountsPath = "test/validAccounts"




def runTransactionTests(transactionName):
	os.system("cls")