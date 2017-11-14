import argparse

class QBasicBackEndException(Exception):
	pass


class QBasicBackEnd():

	dict_of_accounts = {} #key = str(accountName): val = (int(balance), str(name))
	MAX_MSTER_ACCOUNTS_LINE_LENGTH = 47

	def read_master_accounts_file(self, filename):
		lines = read_file(filename)

		ret_dict_of_accounts = {} #empty dict_of_accounts

		past_account_num = ""

		for line_num, line in enumerate(lines):

			if(line[0] == "#"):
				continue

			line_num = line_num + 1 #line_num starts at 0

			#line length checking
			if len(line) > MAX_MSTER_ACCOUNTS_LINE_LENGTH:
				raise QBasicBackEndException("Master Account File {0} error. Line longer than {1} chars | line: {2}".format(filename, self.MAX_MSTER_ACCOUNTS_LINE_LENGTH, line_num))

			fields = line.split()
			if len(fields) != 3:
				raise QBasicBackEndException("Master Accounts File has invalid line | line: {0}".format(line_num))

			account_num, balance, name = fields[0], fields[1], fields[2]

			#check ascending order
			if account_num < past_account_num:
				raise QBasicBackEndException("Master Account File {0} error. Account numbers {1} & {2} are not in ascending order | line: {3}".format(filename, account_num, past_account_num, line_num))
			past_account_num = account_num

			#Account number: no duplicates, no invalid account numbers
			if account_num in ret_dict_of_accounts:
				raise QBasicBackEndException("Master Account File {0} error. Defines two accounts with same account number {1} | line: {2}".format(filename, account_num, line_num))
			
			if not self.isAccountValid(account_num):
				raise QBasicBackEndException("Master Account File {0} error. Contains invalid account number {1} | line: {2}".format(filename, account_num, line_num))

			#Balance: padded to 3 spots, valid integer, valid Account balance
			if len(balance) < 3:
				raise QBasicBackEndException('Master Account File {0} error. {1} for balance is not padded to 3 spots | line: {2}'.format(filename, balance, line_num))

			try:
				balanceAmt = int(balance)
			except ValueError:
				raise QBasicBackEndException('Master Account File {0} error. {1} for balance is not a valid integer | line: {2}'.format(filename, balanceAmt, line_num))

			if not is_balance_valid(balanceAmt):
				raise QBasicBackEndException("Master Account File {0} error. Account {1} contains invalid balance {2} | line: {3}".format(filename, account_num, balanceAmt, line_num))

			#Name: Valid name
			if not self.isNameValid(name):
				raise QBasicBackEndException("Master Account File {0} error. Account number {1} has invalid name {2} | line: {3}".format(filename, account_num, name, line_num))

			ret_dict_of_accounts[account_num] = (balanceAmt, name)

		return ret_dict_of_accounts


#NEW 1234567 234 0000000 

	def str_split(self, s, numFields):
		'''
		'''
		ret_list = []
		i = 0
		space_count = 0
		for char in s:
			if char == " ":
				space_count++
			if space_count != 
			ret_list[i] += char

	def run(self, filenames):

			read_master()
			read_TF()








	def read_transaction_summary_file(self, filename):
		pass

	def write_master_accounts(self, filename):
		#need to sort
		#fuckin' write dawg
		#make sure that a line is not oer 47 characters
		pass


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

	def is_name_valid(self, nameStr):
		'''Checks if name is between 3-30 characters, [A-Z][a-z][0-9] without leading/trailing spaces'''
		if(len(nameStr) < 3 or len(nameStr) > 30 or nameStr[0].isspace() or nameStr[-1].isspace()):
			return False

		return nameStr.replace(' ','').isalnum() #all non spaces are alpha-numeric

	def is_account_valid(self, accountStr):
		'''
		Checks if an account number (represented as a string) is valid (7 numbers long, no leading 0)
		This does not check if an account exists.
		'''
		return len(accountStr) == 7 and accountStr.isdigit() and accountStr[0] != "0"

	def is_balance_valid(self, balance):
		if balance < 0 or balance >= 100000000: #cannot be greater than 8 digits or less than 0
			return False
		return True


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
	print(QBasicBackEnd().read_master_accounts_file(cmd_args["OldMasterAccountsFile"]))

if __name__ == "__main__":
	main()