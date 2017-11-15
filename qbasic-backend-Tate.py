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

			fields = str_split(line, 3)
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
			
			if not self.validate_fields(account1=account_num, amtStr=balance, name=name):
				raise QBasicBackEndException("Master Account File {0} error. Invalid field at line: {2}".format(filename, account_num, line_num))

			ret_dict_of_accounts[account_num] = (balanceAmt, name)

		return ret_dict_of_accounts


	def validate_fields(self, trans_code=None, account1=None, account2=None, name=None, amtStr=None):
		if trans_code != None:
			if not is_valid_trans_code(trans_code):
				return False
		if account1 != None:
			if not is_account_valid(account1):
				return False
		if account2 != None:
			if not is_account_valid(account2):
				return False:
		if name != None:
			if not is_name_valid(name):
				return False
		if amtStr != None:
			if not is_str_amount_valid(amtStr):
				return False
		return True




#NEW 1234567 234 0000000 






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
		'''Takes in balance as an int. Cannot be greater than 8 digits or less than 0
		Returns an empty string if valid'''
		if balance < 0:
			return "Balance {0} is under 0".format(balance)
		if balance >= 100000000: 
			return "Balance {0} has more than 8 digits".format(balance)
		return ""

	def is_valid_trans_code(self, trans_code):
		'''Returns empty string if valid. Returns error message if not in ["DEP", "WDR", "XFR", "NEW", "DEL"]'''
		if trans_code not in ["DEP", "WDR", "XFR", "NEW", "DEL"]:
			return "transaction code {0} not in [DEP, WDR, XFR, NEW, DEL]".format(trans_code)
		return ""

	def is_str_amount_valid(self, amtStr):
		'''Takes in an amount in string form and returns empty string if it is valid to be found in the master account or transaction summary file'''
		if len(amtStr) < 3:
			return "amount string {0} is not padded to at least 3 digits".format(amtStr)
		try:
			amt = int(amtStr)
		except ValueError:
			return "Amount {0} is not a string".format(amtStr)
		return is_balance_valid(amt)


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


def str_split(s, numFields):
	'''
	splits for the first < numfields on a space then slots the rest into the final field. This is to resolve the issue
	of spliting a string into fields, when the accountName field can have spaces in it. This also resolves the issue
	with having multiple spaces between fields which .split cannot catch. Errors if string starts with a space
	@returns empty list if there is an error
	'''
	if s.startswith(" "):
		return []
	ret_list = []
	i = 0
	space_count = 0
	temp = ""
	for j, char in enumerate(s):
		if char == " ":
			if space_count > 0:
				return []
			else:
				ret_list.append(temp)
				i += 1
				space_count = 1
				temp = ""
				if i == numFields - 1:
					break
		else:
			space_count = 0
			temp += char

	j +=1
	rest = s[j:]
	ret_list.append(rest)

	return ret_list

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
	#cmd_args = qbasic_backend_parse_args()
	#print(QBasicBackEnd().read_master_accounts_file(cmd_args["OldMasterAccountsFile"]))
	print(str_split("Hi My Name Is ",5))
	print(str_split(" This has spaces     ", 4))

if __name__ == "__main__":
	main()