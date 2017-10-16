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
			print("cannot create account number {0} as it already exists".format(accountNumber))
			return

		#validate account

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

def main():
	q = QBasic()
	q.run()

if __name__ == "__main__":
	main()