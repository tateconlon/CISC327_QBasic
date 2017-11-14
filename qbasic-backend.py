import argparse

class QBasicBackEndException(Exception):
	pass


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

			if dict_of_accounts[fields]


	def run(self, filenames):

		try:
			pass
		except e as QBasicBackEndException:
			pass
		except e as:
			pass



	def read_transaction_summary_file(self, filename):
		pass

	def write_master_accounts(self, filename):
		#need to sort
		#fuckin' write dawg
		#make sure that a line is not oer 47 characters


	def transfer(self, accountTo, accountFrom, amount):
		pass

	def withdraw(self, account, amt):
		#can't over withdraw
		pass

	def deposit(self, account, amt):
		pass

	def create_acct(self, account, name):
		#account can't exist
		pass

	def delete_acct(self, account, name):
		#can't delete account with non-zero balance
		#names have to match
		#account has to exist
		pass


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