import sys
import argparse

class QBasic():
	'''
	This class represents the QBasic front end. QBasic is a simple banking interface
	that reads in a valid accounts file full of valid account numbers and after the session
	outputs a transaction summary file that represents the transactions that occured during that session.
	Valid account and Transaction Summary files (path relative to script) must be given in order to create a QBasic object.

	To begin a QBasic session, use the .run method
	'''
	def __init__(self, validAccountsFilename, transactionSummaryFileName):
		'''
		validAccountsFileName and transactionSummaryFileName are both path relative to this script.
		'''
		self.transactionFile = [] #list of strings. Added onto throughout execution, gets written to transaction summary file
		self.validAccounts = []	#list of strings representing accounts read from valid accounts file
		self.validAccountsFileName = validAccountsFilename
		self.transactionSummaryFileName = transactionSummaryFileName
		self.loggedIn = False

	def __del__(self):
		'''
		Deconstructor logs out. This means that upon unexpected abort, transaction summary file still gets written
		'''
		if self.loggedIn:
			self.logout()

	def run(self):
		'''Starts a QBasic session'''
		self.loggedIn = False
		print('Welcome to QBasic!')
		
		#log in
		while not self.loggedIn:
			while(input('Please type login to log in: ') != "login"):
				pass
			permissionType = self.login()
			
			if not self.loggedIn:	#log in unsuccessful
				continue #go back to top of while True

		#log in successful
		self.startLoggedInState(permissionType)

		#return from logged in state means logout has occurred, and the session is over


	def startLoggedInState(self, permissionType):
		'''A loop that represents the logged in state. A return from this means they've logged out.
		Sets logged in to true.
		'''
		if not self.loggedIn:
			print("You are not logged in, you cannot enter the logged in state!")
			return

		while (self.loggedIn):
			transactionInput = input("Input the transaction code: ")
			if transactionInput == "logout":
				self.logout()
			elif transactionInput == "deposit":
				self.deposit(permissionType)
			elif transactionInput == "withdraw":
				self.withdraw(permissionType)
			elif transactionInput == "transfer":
				self.transfer(permissionType)
			elif transactionInput == "createacct":
				self.create_acct(permissionType)
			elif transactionInput == "deleteacct":
				self.delete_acct(permissionType)
			else:
				print("transaction code {0} invalid.".format(transactionInput))


	def login(self):
		'''returns permissionType as string. returns empty string if invalid login attempt.'''
		#read valid Accounts file
		permissionType = input('Please enter desired permission type (agent/machine): ')
		if(permissionType not in ['agent', 'machine']):
			print("login permission {0} invalid. Please choose agent or machine.".format(permissionType))
			return ""
		
		try:
			self.loadValidAccounts()
		except Exception as e:
			print("login unsuccessful due to {0}".format(e))
			return ""

		self.loggedIn = True
		print("login as {0} successful.".format(permissionType))
		return permissionType

	def create_acct(self, permissionType):
		'''
		Creates an account. Only valid if permissionType is 'agent'.
		1) Asks for new account number (cannot already exist)
		2) Asks for new account's name
		'''
		if(permissionType != 'agent'):
			print("createacct not available with permission type {0}".format(permissionType))
			return
		
		accountNumber = input('Please enter the account number (7 digits): ')
		if accountNumber in self.validAccounts:
			print("Cannot create account number {0} as it already exists".format(accountNumber))
			return

		if not self.isAccountValid(accountNumber):
			print("Account number {0} not valid (req. 7 digits long, no leading 0)".format(accountNumber))
			return

		name = input('Please enter the account name (3-30 chars): ')

		if not self.isNameValid(name):
			print('{0} is not a valid account name. Valid account names are 3-30 alpha characters long, no leading/trailing spaces, but spaces are allowed inside'.format(name))
			return

		newTransLine = "NEW {0} 000 00000000 {1}".format(accountNumber, name)
		self.transactionFile.append(newTransLine)

		print("createacct {0} {1} successful.".format(accountNumber, name))
		return

	def delete_acct(self, permissionType):
		'''
		Deletes an account. Only valid if permissionType is 'agent'.
		1) Asks for delete account number (must already exist)
		2) Asks for deleted account's name
		'''
		if(permissionType != 'agent'):
			print("deleteacct not available with permission type {0}".format(permissionType))
			return
		
		# Take account number and check it's valid
		accountNumber = input('Please enter the account number (7 digits): ')
		if accountNumber not in self.validAccounts:
			print("Cannot delete account number {0} as it does not exist".format(accountNumber))
			return

		# Take account number and check it's valid
		accountName = input('Please input the account name: ')
		if not self.isNameValid(accountName):
			print('Cannot delete account with name {0}. Valid account names are 3-30 alpha characters long, no leading/trailing spaces, but spaces are allowed inside'.format(name))
			return

		newTransLine = "DEL {0} 000 0000000 {1}".format(accountNumber, accountName)
		self.transactionFile.append(newTransLine)

		print("Deletion of account {0} {1} successful".format(accountNumber, accountName))
		return

	def withdraw(self, permissionType):
		'''Withdraw money that has been created by the backend.
		1) Asks for valid account number.
		2) Asks for amount to withdraw in cents.
		3) Wdr Amt must be less than $1000.00 for machine, less than $999,999.99 for agent
		4) Writes to transaction file
		'''
		if permissionType not in ['agent', 'machine']:
			print('Cannot access deposit with permission type {0}'.format(permissionType))
			return 


		# Enter account number and check that it's valid
		accountNumber = input('Please enter the account number to withdraw from: ')
		if(accountNumber not in self.validAccounts):
			print('Account {0} does not exist'.format(accountNumber))
			return

		wdrAmtStr = input('Please enter the amount to withdraw (in cents): ')
		try:
			wdrAmt = int(wdrAmtStr)
		except ValueError:
			print('{0} is not a valid number'.format(wdrAmtStr))
			return

		# Check withdrawal amount is valid for agent session
		if(permissionType == 'agent' and wdrAmt > 99999999):
			print('Cannot withdraw more than $999,999.99 in a single transaction in agent mode')
			return

		# Check withdrawal amount is valid for machine session
		if(permissionType == 'machine' and wdrAmt > 100000):
			print('Cannot withdraw more than $1000.00 in a single transaction in machine mode')
			return

		newTransLine = "WDR {0} {1} 00000000 ***".format(accountNumber, wdrAmtStr)
		self.transactionFile.append(newTransLine)

		print('withdraw {0} {1} successful.'.format(accountNumber, wdrAmtStr))
		return	

	def deposit(self, permissionType):
		'''Deposit money into an account that has been created by the backend.
		1) Asks for valid account number.
		2) Asks for amount to deposit in cents.
		3) Dep Amt less than $1000.00 for machine, less than $999,999.99 for agent
		4) Writes to transaction file
		'''
		if permissionType not in ['agent', 'machine']:
			print('Cannot access deposit with permission type {0}'.format(permissionType))
			return 

 		# Enter account number and check that it's valid
		accountNumber = input('Please enter the account number to deposit into: ')
		if(accountNumber not in self.validAccounts):
			print('Account {0} does not exist'.format(accountNumber))
			return

		# Enter deposit amount
		depAmtStr = input('Please enter the amount to deposit (in cents): ')
		try:
			depAmt = int(depAmtStr)
		except ValueError:
			print('{0} is not a valid number'.format(depAmtStr))
			return

		# Check deposit amount is valid for agent session
		if(permissionType == 'agent' and depAmt > 99999999):
			print('Cannot deposit more than $999,999.99 in a single transaction in agent mode')
			return

		# Check deposit amount is valid for machine session
		if(permissionType == 'machine' and depAmt > 100000):
			print('Cannot deposit more than $1000.00 in a single transaction in machine mode')
			return

		newTransLine = "DEP {0} {1} 00000000 ***".format(accountNumber, depAmtStr)
		self.transactionFile.append(newTransLine)

		print('deposit {0} {1} successful.'.format(accountNumber, depAmtStr))
		return	


	def transfer(self, permissionType):
		'''Transfer money from an account to another. Both accounts must be created by the backend.
		1) Asks for valid account number FROM.
		2) Asks for valid account number TO.
		3) Asks for amount to transfer in cents.
		3) Transfer Amt less than $1000.00 for machine, less than $999,999.99 for agent
		4) Writes to transaction file
		'''
		if permissionType not in ['agent', 'machine']:
			print('Cannot access transfer with permission type {0}'.format(permissionType))
			return 

		accountNumber1 = input('Please enter the account number to tranfer from: ')
		if(accountNumber1 not in self.validAccounts):
			print('Account {0} does not exist'.format(accountNumber1))
			return

		accountNumber2 = input('Please enter the account number to tranfer from: ')
		if(accountNumber2 not in self.validAccounts):
			print('Account {0} does not exist'.format(accountNumber2))
			return
		if(accountNumber2 == accountNumber1):
			print('{0} -> {1}. Cannot transfer into the same account'.format(accountNumber1, accountNumber2))
			return

		transAmtStr = input('Please enter the amount to deposit (in cents): ')
		try:
			transAmt = int(transAmtStr)
		except ValueError:
			print('{0} is not a valid number'.format(transAmtStr))
			return

		if(permissionType == 'agent' and transAmt > 99999999):
			print('Cannot deposit more than $999,999.99 in a single transaction in agent mode')
			return

		if(permissionType == 'machine' and transAmt > 100000):
			print('Cannot deposit more than $1000.00 in a single transaction in machine mode')
			return

		newTransLine = "XFR {0} {1} {2} ***".format(accountNumber1, transAmtStr, accountNumber2)
		self.transactionFile.append(newTransLine)

		print('transfer of {1} cents from {0} to {2} successful.'.format(accountNumber, transAmtStr, accountNumber2))
		pass

	def logout(self):
		'''returns True if logout successful'''
		if(self.loggedIn == False):
			print('Cannot logout if already logged out.')
			return

		try:
			self.writeTransactionSummary()
		except Exception as e:
			print("logout unsuccessful due to: {0}".format(e))
			return

		print("Transaction summary written and system logged out successfully.")
		self.loggedIn = False

	def loadValidAccounts(self):
		'''loads self.validAccounts from valid accounts file. Assumes Valid Accounts file is formatted perfectly'''
		with open(self.validAccountsFileName, "r") as f:
			lines = [x.strip() for x in f.readlines()]
		self.validAccounts = lines[:-1] #0000000 is the last line

	def isNameValid(self, nameStr):
		'''Checks if name is between 3-30 characters, [A-Z][a-z][0-9] without leading/trailing spaces'''
		if(len(nameStr) < 3 or len(nameStr) > 30 or nameStr[0].isspace() or nameStr[-1].isspace()):
			return False

		return nameStr.replace(' ','').isalnum() #all non spaces are alpha-numeric

	def isAccountValid(self, accountStr):
		'''
		Checks if an account number (represented as a string) is valid (7 numbers long, no leading 0)
		This does not check if an account exists.
		'''
		return len(accountStr) == 7 and accountStr.isdigit() and accountStr[0] != "0"

	def writeTransactionSummary(self):
		'''Writes the transaction summary file and clears self.transactionFile list'''
		self.transactionFile.append("EOS")
		with open(self.transactionSummaryFileName, "w") as f:
			f.write('\n'.join(self.transactionFile))
		
		self.transactionFile = [] #clear transactionFile

	


def main():
	'''runs when script run from command-line'''

	#parse command-line arguments
	arg_parser = argparse.ArgumentParser()
	arg_parser.add_argument("validAccountFileName",
							help="valid account filename",
							type=str)
	arg_parser.add_argument("transactionSummaryFileName",
							help="transaction summary filename",
							type=str)

	args = vars(arg_parser.parse_args()) #returns dict {"name": val}

	#create and run qbasic session
	q = QBasic(args['validAccountFileName'], args['transactionSummaryFileName'])
	q.run()

#if run as script, run main()
if __name__ == "__main__":
	main()
