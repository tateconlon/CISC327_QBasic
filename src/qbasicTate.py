import sys
class QBasic():

	def __init__(self):
		self.transactionFile = [] #list of strings
		self.validAccounts = []	#list of strings

	def run(self, validAccountsFileName, transactionFileName):

		pass

	def loggedInState(self, permissionType):
		loggedOut = False
		while (not loggedOut):
			transactionInput = input("Input the transaction code: ")
			if transactionInput == "deposit":
				self.deposit(permissionType)
			elif transactionInput == "withdraw":
				self.withdraw(permissionType)
			elif transactionInput == "transfer":
				self.transfer(permissionType)
			elif transactionInput == "logout":
				loggedOut = True
				self.logout()
			elif transactionInput == "createacct":
				self.create_acct(permissionType)
			elif transactionInput == "deleteacct":
				self.delete_acct(permissionType)
			else:
				print("transaction code {0} invalid.".format(transactionInput))	

	def login(self, validAccountsFileName):
		'''returns permissionType as string. returns empty string if invalid login attempt.'''
		#read valid Accounts file
		permissionType = input('Please enter desired permission type (agent/machine): ')
		if(permissionType not in ['agent', 'machine']):
			print("login permission {0} invalid. Please choose agent or machine.".format(permissionType))
			return ""
		
		loadValidAccounts(validAccountsFileName)

		print("login as {0} successful.".format(permissionType))
		return permissionType

	def create_acct(self, permissionType):
		if(permissionType != 'agent'):
			print("createacct not available with permission type {0}".format(permissionType))
		
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
		pass

	def deposit(self, permissionType):
		'''Deposit money into an account that has been created by the backend.
		1) Asks for valid account number.
		2) Asks for amount to deposit in cents.
		3) Dep Amt less than $1000.00 for machine, less than $999,999.99 for agent
		4) Writes to transaction file
		'''
		accountNumber = input('Please enter the account number to deposit into: ')
		if(accountNumber not in self.validAccounts):
			print('Account {0} does not exist'.format(accountNumber))
			return

		depAmtStr = input('Please enter the amount to deposit (in cents): ')
		try:
			depAmt = int(depAmtStr)
		except ValueError:
			print('{0} is not a valid number'.format(depAmtStr))
			return

		if(permissionType == 'agent' and deptAmt > 99999999):
			print('Cannot deposit more than $999,999.99 in a single transaction in agent mode')
			return

		if(permissionType == 'machine' and deptAmt > 100000):
			print('Cannot deposit more than $1000.00 in a single transaction in machine mode')
			return

		newTransLine = "DEP {0} {1} 00000000 ***".format(accountNumber, depAmtStr)
		self.transactionFile.append(newTransLine)

		print('deposit {0} {1} successful.'.format(accountNumber, depAmtStr))
		return
		

	def transfer(self, permissionType):
		pass

	def logout(self):
		#write and clear transaction file
		pass

	def loadValidAccounts(self, validAccountsFileName):
		#end at 0000000
		pass

	def isNameValid(self, nameStr):
		'''Checks if name is between 3-30 characters, [A-Z][a-z][0-9] without leading/trailing spaces'''
		if(len(nameStr) < 3 or len(nameStr) > 30 or nameStr[0].isspace() or nameStr[-1].isspace()):
			return False

		return nameStr.replace(' ','').isalnum() #all non spaces are alpha-numeric


	def isAccountValid(self, accountStr):
		'''Checks if an account number (represented as a string) is valid (7 numbers long, no leading 0)'''
		return len(accountStr) == 7 and accountStr.isdigit() and accountStr[0] != "0"


def main():
	q = QBasic()
	q.loggedInState('agent')

if __name__ == "__main__":
	main()