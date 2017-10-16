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
		return ""

	def create_acct(self, permissionType):
		pass

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