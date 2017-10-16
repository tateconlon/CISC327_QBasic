import sys
class QBasic():

	def __init__(self):
		self.transactionFile = [] #list of strings
		self.validAccounts = []	#list of strings

	def run(self, validAccountsFileName, transactionFileName):

		pass



        def loggedInState(self, permissionType):
                loggedOut = False
                while (!loggedOut):
                        transactionInput = input("Input the transaction code: ")
                        if transactionInput == "deposit":
                                deposit(permissionType)
                        elif transactionInput == "withdraw":
                                withdraw(permissionType)
                        elif transactionInput == "transfer":
                                transfer(permissionType)
                        elif transactionInput == "logout":
                                loggedOut = True
                                logout()
                        elif transactionInput == "create_acct" and permissionType = "agent":
                                create_acct()
                        elif transactionInput == "delete_acct" and permissionType = "agent":
                                delete_acct()
                        else:
                                print("transaction code {0} invalid.".format(transactionCodes))
                return 0

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

        def withdraw(self, permissionType):
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
