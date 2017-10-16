import sys
class QBasic():

	def __init__(self):
		self.transactionFile = [] #list of strings
		self.validAccounts = []	#list of strings

	def run(self, validAccountsFileName, transactionFileName):

		pass

	def login(self, validAccountsFileName):
		'''returns permissionType as string. returns empty string if invalid login attempt.'''
		#read valid Accounts file
		permissionType = input('Please enter desired permission type (agent/machine): ')
		if(permissionType not in ['agent', 'machine']):
			print("login permission {0} invalid. Please choose agent or machine.".format(permissionType))
			return ""
		
		loadValidAccounts(validAccountsFileName)
		return permissionType

	def create_acct(self, permissionType):
		if(permissionType != 'agent'):
			print("createacct not available with permission type {0}".format(permissionType))
		
		accountNumber = input('Please enter the account number (8 digits): ')
		if accountNumber in validAccounts:
			print("Cannot create account number {0} as it already exists".format(accountNumber))
			return

		if not isAccountValid(acountNumber):
			print("Account number {0} not valid (req. 8 digits long, no leading 0)".format(accountNumber))

		transLine = "NEW {0} 000 00000000 {1}"

	def delete_acct(self, permissionType):
		pass

	def deposit(self, permissionType):
		pass

	def transfer(self, permissionType):
		pass

	def logout(self):
		#write and clear transaction file
		pass

	def loadValidAccounts(self, validAccountsFileName):
		#end at 0000000
		pass

	def isAccountValid(self, accountStr):
		'''Checks if an account number (represented as a string) is valid (8 numbers long, no leading 0)'''
		return len(accountStr) == 8 and accounStr.isdigit() and accountStr[0] == "0"


def main():
	q = QBasic()
	q.run()

if __name__ == "__main__":
	main()