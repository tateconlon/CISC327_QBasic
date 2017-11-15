import argparse

class QBasicBackEndException(Exception):
        """Base class for all other exceptions specific to the QBasic Back End"""
        def __init__(self,*args,**kwargs):
                Exception.__init__(self,*args,**kwargs)

class NonZeroBalanceError(QBasicBackEndException):
        """no account should ever have a negative balance"""
        def __init__(self,*args,**kwargs):
                QBasicBackEndException.__init__(self,*args,**kwargs)

class NegativeBalanceError(QBasicBackEndException):
        """a deleted account must have a zero balance"""
        def __init__(self,*args,**kwargs):
                QBasicBackEndException.__init__(self,*args,**kwargs)

class AccountNumberInUseError(QBasicBackEndException):
        """a created account must have a new, unused account number"""
        def __init__(self,*args,**kwargs):
                QBasicBackEndException.__init__(self,*args,**kwargs)

class NameMismatchError(QBasicBackEndException):
        """the name given in a delete transaction must match the name associated with the deleted account"""
        def __init__(self,*args,**kwargs):
                QBasicBackEndException.__init__(self,*args,**kwargs)

class InvalidFieldFatalError(QBasicBackEndException):
        """Back End encounters an invalid field, it should immediately stop and log a fatal error on the terminal"""
        def __init__(self,*args,**kwargs):
                QBasicBackEndException.__init__(self,*args,**kwargs)




class QBasicBackEnd():

    dict_of_accounts = {} #key = str(accountName): val = (int(balance), str(name))
    MAX_MSTER_ACCOUNTS_LINE_LENGTH = 47

    def read_master_accounts_file(self, filename):
        lines = read_file(filename)

        ret_dict_of_accounts = {} #empty dict_of_accounts

        past_account_num = ""

        for line_num, line in enumerate(lines):

            if(line[0] == "#"): #TODO: only for testing, delete this
                continue

            line_num = line_num + 1 #line_num starts at 0

            #line length checking
            if len(line) > self.MAX_MSTER_ACCOUNTS_LINE_LENGTH:
                raise QBasicBackEndException("Master Account File {0} error. Line longer than {1} chars | line: {2}".format(filename, self.MAX_MSTER_ACCOUNTS_LINE_LENGTH, line_num))

            fields = str_split(line, 3)
            if len(fields) != 3:
                raise QBasicBackEndException("Master Accounts File has invalid line {0} | line #{1}".format(line, line_num))

            account_num, balance, name = fields

            #check ascending order
            if account_num < past_account_num:
                raise QBasicBackEndException("Master Account File {0} error. Account numbers {1} & {2} are not in ascending order | line: {3}".format(filename, account_num, past_account_num, line_num))
            past_account_num = account_num

            #Account number: no duplicates, no invalid account numbers
            if account_num in ret_dict_of_accounts:
                raise QBasicBackEndException("Master Account File {0} error. Defines two accounts with same account number {1} | line: {2}".format(filename, account_num, line_num))

            error_fields, balanceAmt = self.validate_fields(account1=account_num, amtStr=balance, name=name)
            if error_fields != []:
                raise QBasicBackEndException("Master Account File {0} error. Invalid field(s) {fields} in line: {1} | line #{2}".format(filename, line, line_num, fields=", ".join(error_fields)))

            ret_dict_of_accounts[account_num] = (balanceAmt, name)

        return ret_dict_of_accounts


    def validate_fields(self, trans_code=None, account1=None, account2=None, name=None, amtStr=None):
        ret_error_fields = []
        intAmt = -1
        if trans_code != None:
            if not self.is_valid_trans_code(trans_code):
                ret_error_fields.append("trans_code")
        if account1 != None:
            if not self.is_account_valid(account1):
                ret_error_fields.append("account1")
        if account2 != None:
            if not self.is_account_valid(account2):
                ret_error_fields.append("account2")
        if name != None:
            if not self.is_name_valid(name):
                ret_error_fields.append("name")
        if amtStr != None:
            intAmt = self.is_str_amount_valid(amtStr)
            if intAmt == -1:
                ret_error_fields.append("amtStr")
        return (ret_error_fields, intAmt)


    def read_merged_transaction_summary_file(self, filename):
        MTSFLines = read_file(filename)
        parsedMTSF = []
        seenEOS = False
        for line in MTSFLines:

            if seenEOS:     #Last line should have been EOS, if still in loop and has seen EOS, file error
                pass #TODO: error handling

            if line == "EOS" and not seenEOS: #first time seeing EOS should be the end
                seenEOS = True
                continue   #continue should break out of loop

            fields = str_split(line, 5)
            if len(fields) != 5:
                raise InvalidFieldFatalError("Merged Transaction Summary File has an invalid line")
            
            trans_code, account1, amtStr, account2, name = fields
            error_fields, amt = self.validate_fields(trans_code=trans_code, account1=account1, amtStr=amtStr, account2=account2, name=name)
            if error_fields != []:
                pass #TODO: error handling

            #TODO: parsing for valid fields for specific transactions in transaction summary file (eg. deposit must have 0000000 and *** as account2 and name)
            parsedMTSF.append({"trans_code": trans_code, "account1":account1, "amt":amt, "account2":account2, "name":name})

        if not seenEOS:
            pass #TODO: Error handling. EOS not seen in transaction summary file
        return parsedMTSF


    #param - MTSF Merged Transation Summary File, oldMAF old Master Accounts File, newMAF new Master Accounts File, newVAF new Valid Accounts File"""
    def run(self, oldMAF, MTSF, newMAF,newVAF):
        self.dict_of_accounts = self.read_master_accounts_file(oldMAF)

        
        transaction_list = self.read_merged_transaction_summary_file(MTSF)

        for trans in transaction_list:
            code = trans["trans_code"]
            if code == "DEP":
                self.deposit(trans["account1"], trans["amt"])
            elif code == "WDR":
                self.withdraw(trans["account1"], trans["amt"])
            elif code == "XFR":
                self.transfer(trans["account1"], trans["account2"], trans["amt"])
            elif code == "NEW":
                self.create_acct(trans["account1"], trans["name"])
            elif code == "DEL":
                self.delete_acct(trans["account1"], trans["name"])

        self.write_valid_accounts(newVAF)
        self.write_master_accounts(newMAF)

    def write_valid_accounts(self, filename):

        accts = sorted(list(self.dict_of_accounts.keys()))
        accts = ["{0}\n".format(x) for x in accts] #add a newline after each

        accts.append("0000000")
        write_file(filename, accts)


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
            
            #Error if the line is longer than 47 charachters - 30 for name - 7 for acct num - 8 for bal
            if len(line) > 47:
                #REDUNDANT?
                raise InvalidFieldFatalError("Line length greater than 47") 
            
            new_master_acct_txt += line + "\n"

        write_file(filename, new_master_acct_txt)


    def transfer(self, accountTo, accountFrom, amount):
        pass

    def withdraw(self, account, amt):
        #can't over withdraw
        pass

    def deposit(self, account, amt):
        pass

    def create_acct(self, account, name):
        #account can't exist
        if account in self.dict_of_accounts:
            print("Cannot create new account {0} as it already exists".format(account))
            return

        self.dict_of_accounts[account] = (0, name)

    def delete_acct(self, account, name):
        #can't delete account with non-zero balance
        #names have to match
        #account has to exist
        if account not in self.dict_of_accounts:
            print("Cannot delete account {0}, it does not exist".format(account))
            return

        acct_bal = self.dict_of_accounts[account][0]
        if acct_bal != 0:
            print("Cannot delete account {0} with non-zero balance {1}".format(account, acct_bal))
            return

        acct_name = self.dict_of_accounts[account][1]
        if acct_name != name:
            print("Cannot delete account {a} {n} as supplied name {n2} does not match".format(a=account, n=acct_name, n2=name))

        self.dict_of_accounts.pop(account)

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
        '''Takes in balance as an int'''
        if balance < 0 or balance >= 100000000: #cannot be greater than 8 digits or less than 0
            return False
        return True

    def is_valid_trans_code(self, trans_code):
        return trans_code not in ["DEP", "WDR", "XFR", "NEW", "DEL"]

    def is_str_amount_valid(self, amtStr):
        '''Takes in an amount in string form and returns amount in intergerif it is valid to be found in the master account or transaction summary file.
        Returns -1 if not valid'''
        if len(amtStr) < 3:
            return False
        try:
            amt = int(amtStr)
        except ValueError:
            return False
        if self.is_balance_valid(amt):
            return amt
        return -1


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
    if rest.endswith("\n"):
        rest = rest[:-1]
    ret_list.append(rest)

    return ret_list

def qbasic_backend_parse_args():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("old_MA_file",
                            help="old master accounts filename",
                            type=str)
    arg_parser.add_argument("merged_TS_file",
                            help="merged transaction summary filename",
                            type=str)
    arg_parser.add_argument("new_MA_file",
                            help="new master accounts filename",
                            type=str)
    arg_parser.add_argument("new_VA_file",
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
    back_end = QBasicBackEnd()
    back_end.run(cmd_args["old_MA_file"], cmd_args["merged_TS_file"], cmd_args["new_MA_file"], cmd_args["new_VA_file"])
    

if __name__ == "__main__":
    main()