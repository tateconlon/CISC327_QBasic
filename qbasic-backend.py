import argparse

class QBasicBackEndException(Exception):
        """Base class for all other exceptions specific to the QBasic Back End"""
        def __init__(self,*args,**kwargs):
                Exception.__init__(self,*args,**kwargs)
	pass

class NonZeroBalanceError(QBasicBackEndException):
        """no account should ever have a negative balance"""
        def __init__(self,*args,**kwargs):
                QBasicBackEndException.__init__(self,*args,**kwargs)
        pass

class NegativeBalanceError(QBasicBackEndException):
        """a deleted account must have a zero balance"""
        def __init__(self,*args,**kwargs):
                QBasicBackEndException.__init__(self,*args,**kwargs)
        pass

class AccountNumberInUseError(QBasicBackEndException):
        """a created account must have a new, unused account number"""
        def __init__(self,*args,**kwargs):
                QBasicBackEndException.__init__(self,*args,**kwargs)
        pass

class NameMismatchError(QBasicBackEndException):
        """the name given in a delete transaction must match the name associated with the deleted account"""
        def __init__(self,*args,**kwargs):
                QBasicBackEndException.__init__(self,*args,**kwargs)
        pass

class InvalidFieldFatalError(QBasicBackEndException):
        """Back End encounters an invalid field, it should immediately stop and log a fatal error on the terminal"""
        def __init__(self,*args,**kwargs):
                QBasicBackEndException.__init__(self,*args,**kwargs)


class QBasicBackEnd():

	dict_of_accounts = {} #key = str(accountName): val = (int(balance), str(name))

	def read_master_accounts_file(self, filename):
		lines = read_file(filename)

		dict_of_accounts = {} #empty dict_of_accounts

		for i, line in enumerate(lines):
			fields = line.split()
			if len(fields != 3):
				raise QBasicBackEndException("Master Accounts File has invalid line @ line #")

			account_num, balance, name = fields[0], fields[1], fields[2]

			#if dict_of_accounts[fields]


	def run(self, filenames):
		try:
                        #conditional
                        #raise specific QBasicBackEndException
			pass
		except e as QBasicBackEndException:
			pass
		except e as Exception:
			pass



	def read_merged_transaction_summary_file(self, filename):
                try:
                        pass
                except e as InvalidFieldFatalError:
                        print("Invalid Field")
                        exit(1)
                
		pass

	def write_master_accounts(self, filename):
	"""write to the new master accounts file"""

		#sorts all account numbers
		accts = sorted([acct for acct in self.dict_of_accounts])

		new_master_acct_txt = ""		
		#Write account number, account balance in cents, and the account name 
		for acct in accts:
			bal = str(self.dict_of_accounts[acct][0])
			name = self.dict_of_accounts[acct][1]
			line = acct + " " + bal + " " + name

			# Error if the line is longer than 47 charachters - 30 for name - 7 for acct num - 8 for bal
			if len(line) > 47:
				#THROW ERROR OR LOG?
				pass
			new_master_acct_txt += line + "\n\n"

		self.write_file(filename, new_master_acct_txt)
		return


	def transfer(self, accountTo, accountFrom, amount):
		self.change_balance(accountTo,amt)
		self.change_balance(accountFrom,-amt)
		return

	def withdraw(self, account, amt):
		self.change_balance(account,amt)
		return

	def deposit(self, account, amt):
		self.change_balance(account,amt)
		return

	def create_acct(self, account, name):
		"""Create an account with initial balance of 0"""
		if account in self.dict_of_accounts:
			# LOG ACCOUNT ALREADY EXISTS
			pass
		else:
			self.dict_of_accounts[account] = (0, name)
		pass

	def delete_acct(self, account, name):
		"""Deletes the account if it exists, has a zero balance, and account name matches param"""
		if account not in self.dict_of_accounts:
			# LOG ACCOUNT DOES NOT EXIST
			pass
		else:
			if self.dict_of_accounts[account][0] != 0:
				#LOG Can't delete because not a zero balance
				pass
			elif self.dict_of_accounts[account][1] != name:
				#LOG can't delete because account name doesn't match
			else:
				del self.dict_of_accounts[account]

		return



	def change_balance(self, account, val):
	    """change the balance of the account in the parameter by the val param"""
	    new_balance = self.dict_of_accounts[account][0] + val

	    # CHECK THE BALANCE IS LEGAL 

	    # IF SO THEN MAKE THE CHANGE 
		self.dict_of_accounts[account][0] += val
		return
		


	#reads in OldMasterAccountsFile - accounts with #, balance and names
	#If Master Accounts File is malformed, abort
	#applies transactions from merged transaction summary file:
	#if a *constraint* is violated, then you skip the line (causes a negative balance, account already exists, attempting to delete account with money in it)
	#Need to validate the transaction summary lines: if a transaction is malformed it should abort and quit entirely

# dictionary_of_accounts = {accountNumber : (balance, name)}
# dictionary['1234567'] = (1234, "fuck")


#SORTING PSEUDO
#list_of_account_nums = dict.keys()
#list_of_account_nums.sort()
#for each num in sortedListNums: write dict[num]


	pass



def qbasic_backend_parse_args():
	arg_parser = argparse.ArgumentParser()
	arg_parser.add_argument("OldMasterAccountsFile",
							help="old master accounts file",
							type=str)
	arg_parser.add_argument("MergedTransactionSummaryFileName",
							help="merged transaction summary filename",
							type=str)
	arg_parser.add_argument("NewMasterAccountsFile",
							help="new master accounts file",
							type=str)
	arg_parser.add_argument("NewValidAccountsFileName",
							help="new valid accounts filename",
							type=str)

	args = vars(arg_parser.parse_args()) #returns dict {"name": val}

	return args

def read_file(filename):
	with open(filename, "r") as f:
		return f.readlines()

def write_file(filename, lines):	
		with open(filename, "w") as f:
			f.writelines(lines)



def main():
	cmd_args = qbasic_backend_parse_args()
	print(cmd_args)
	fields = [1,2,3]
	account_num, balance, name = fields[0], fields[1], fields[2]
	print(account_num, balance, name)

if __name__ == "__main__":
	main()
