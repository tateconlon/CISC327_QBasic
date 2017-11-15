import argparse

class QBasicBackEnd():

    dict_of_accounts = {} #key = str(accountName): val = (int(balance), str(name))
    MAX_MASTER_ACCOUNTS_LINE_LENGTH = 47

    def read_master_accounts_file(self, filename):
        ''' Read Master Accounts File and parse it into accounts with a balance and name.
        @returns a dictionary in the form of {str(account): [int(balance, str(name)])}
        '''
        lines = read_file(filename)

        ret_dict_of_accounts = {} #empty dict_of_accounts
        past_account_num = ""

        for line_num, line in enumerate(lines):
            line_num = line_num + 1 #line_num starts at 0

            #line length checking
            if len(line) > self.MAX_MASTER_ACCOUNTS_LINE_LENGTH:
                return -1

            fields = str_split(line, 3)
            if len(fields) != 3:    #incorect number of fields
                return -1

            account_num, balance, name = fields

            #check ascending order
            if account_num < past_account_num:
                return -1

            past_account_num = account_num

            #Account number: no duplicates, no invalid account numbers
            if account_num in ret_dict_of_accounts:
                return -1 

            error_fields, balanceAmt = self.validate_fields(account1=account_num, amtStr=balance) #exclude name as *** would return as valid when it's not
            if error_fields != []:
                return -1 

            if not self.is_name_valid(name): #must check for a valid account name
                return -1 

            ret_dict_of_accounts[account_num] = [balanceAmt, name]

        return ret_dict_of_accounts



    def validate_fields(self, trans_code=None, account1=None, account2=None, name=None, amtStr=None):
        '''
        Validates fields as they would appear in the transaction summaryy file and (mostly) in the Master Accounts file.
        Cannot validate name for master accounts here as in the master accounts file *** is not a valid name
        '''
        ret_error_fields = []
        intAmt = -1
        if trans_code != None:
            if not self.is_valid_trans_code(trans_code):
                ret_error_fields.append("trans_code")
        if account1 != None:
            if not self.is_account_valid(account1):
                ret_error_fields.append("account1")
        if account2 != None:
            if not self.is_account_valid(account2) and account2 != "0000000": #% is_account_valid is false for 0000000 but it is a valid filed
                ret_error_fields.append("account2")
        if name != None:
            if not self.is_name_field_valid(name):
                ret_error_fields.append("name")
        if amtStr != None:
            intAmt = self.is_amt_field_valid(amtStr)
            if intAmt == -1:
                ret_error_fields.append("amtStr")
        return (ret_error_fields, intAmt)


    def read_merged_transaction_summary_file(self, filename):
        MTSFLines = read_file(filename)
        parsedMTSF = []
        seenEOS = False
        for line in MTSFLines:
            if seenEOS:     #Last line should have been EOS, if still in loop and has seen EOS, file error
                return -1 #% error handling

            if line == "EOS" and not seenEOS: #first time seeing EOS should be the end
                seenEOS = True
                continue   #continue should break out of loop

            fields = str_split(line, 5)
            if len(fields) != 5:
                return -1 #% error handling raise InvalidFieldFatalError("Merged Transaction Summary File has an invalid line")
            
            trans_code, account1, amtStr, account2, name = fields
            error_fields, amt = self.validate_fields(trans_code=trans_code, account1=account1, amtStr=amtStr, account2=account2, name=name)
            if error_fields != []:
                print(error_fields)
                return -1 #% error handling

            #% parsing for valid fields for specific transactions in transaction summary file (eg. deposit must have 0000000 and *** as account2 and name)
            parsedMTSF.append({"trans_code": trans_code, "account1":account1, "amt":amt, "account2":account2, "name":name})

        if not seenEOS:
            return -1 #% error handling. Didn't see EOS in transaction summary file

        return parsedMTSF


    def run(self, oldMAF, MTSF, newMAF,newVAF):
        ''' Runs the qBasicBackEnd by parsing oldMaster Acconunts File, merged transaction summary file


        Parameters: 
        oldMAF -old Master Accounts Filename 
        MTSF - Merged Transation Summary Filename
        newMAF - new Master Accounts Filename
        newVAF - new Valid Accounts Filename
        '''
        retVal = self.read_master_accounts_file(oldMAF)
        if retVal == -1:
            print("Invalid Master Accounts File. Abort.")
            return

        retVal = self.dict_of_accounts
        
        transaction_list = self.read_merged_transaction_summary_file(MTSF)
        if transaction_list == -1:
            print("Invalid Transaction Summary File. Abort.")
            return

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
        '''Writes a valid accounts file to param filename using accounts in self.dict_of_accounts'''
        accts = sorted(list(self.dict_of_accounts.keys()))
        accts = ["{0}\n".format(x) for x in accts] #add a newline after each

        accts.append("0000000")
        write_file(filename, accts)

    def write_master_accounts(self, filename):
        '''Write to the new master accounts file to filename using self.dict_of_accounts'''

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
        '''If account doesn't exist, creates an account and adds it to self.dict_of_accounts. 
        Assumes entered name is a valid name'''
        #account can't already exist
        if account in self.dict_of_accounts:
            print("Cannot create new account {0} as it already exists".format(account))
            return

        self.dict_of_accounts[account] = [0, name]

    def delete_acct(self, account, name):
        '''Deletes an account with matching account number and name if it has a non-zero balance'''
        
        #account has to exist
        if account not in self.dict_of_accounts:
            print("Cannot delete account {0}, it does not exist".format(account))
            return
        
        #can't delete account with non-zero balance
        acct_bal = self.dict_of_accounts[account][0]
        if acct_bal != 0:
            print("Cannot delete account {0} with non-zero balance {1}".format(account, acct_bal))
            return

        #names have to match
        acct_name = self.dict_of_accounts[account][1]
        if acct_name != name:
            print("Cannot delete account {a} {n} as supplied name {n2} does not match".format(a=account, n=acct_name, n2=name))

        self.dict_of_accounts.pop(account)

    def is_name_valid(self, nameStr):
        '''Checks if name is between 3-30 characters, [A-Z][a-z][0-9] without leading/trailing spaces'''
        if(len(nameStr) < 3 or len(nameStr) > 30 or nameStr[0].isspace() or nameStr[-1].isspace()):
            return False

        return nameStr.replace(' ','').isalnum() #all non spaces are alpha-numeric

    def is_name_field_valid(self, nameStr):
        '''Checks if account name field is valid. This occurs when the account name is valid or it is ***'''
        return self.is_name_valid(nameStr) or nameStr == "***"

    def is_account_valid(self, accountStr):
        '''
        Checks if an account number (represented as a string) is valid (7 numbers long, no leading 0)
        This does not check if an account exists.
        '''
        return len(accountStr) == 7 and accountStr.isdigit() and accountStr[0] != "0"

    def is_balance_valid(self, balance):
        '''Takes in balance as an int and checks if it is within 0 and 99999999 inclusive'''
        if balance < 0 or balance >= 100000000: #cannot be greater than 8 digits or less than 0
            return False
        return True

    def is_valid_trans_code(self, trans_code):
        '''Returns True if tran_code is a valid transaction code (["DEP", "WDR", "XFR", "NEW", "DEL"])
        return trans_code in ["DEP", "WDR", "XFR", "NEW", "DEL"]

    def is_amt_field_valid(self, amtStr):
        '''Takes in an amount field in string form and returns amount in interger 
        if it valid to be found in the master account or transaction summary file.
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


def str_split(s, numFields):
    '''
    splits for the first < numfields on a space then slots the rest into the final field. 

    This is to resolve the issue of spliting a string into fields, when the accountName field can have spaces in it. This also resolves the issue
    with having multiple spaces between fields which .split cannot catch. Errors if string starts with a space
    Returns empty list if there is an error (double spacing or string starts with a space).
    '''
    if s.startswith(" "):
        return []

    #
    ret_list = []
    i = 0
    space_count = 0
    temp = ""   #field we're currently parsing
    for j, char in enumerate(s):
        if char == " ": 
            if space_count > 0: #If double space, return error
                return []
            else:
                ret_list.append(temp)
                i += 1
                space_count = 1
                temp = ""
                if i == numFields - 1:  #if we're about to parse the last field, break out of loop
                    break
        else:   #not a space
            space_count = 0
            temp += char

    j +=1 #go increment past the space character
    rest = s[j:] #get everything to the end of the line
    ret_list.append(rest)

    return ret_list

def qbasic_backend_parse_args():
    '''Validates and parses the command line arguments and returns a dictionary containing them'''
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

def read_file(filename, keep_newlines=False):
    '''Reads a file into a list of lines and returns them '''
    with open(filename, "r") as f:
        if keep_newlines:
            return f.readlines()
        else:
            return [x.rstrip("\n") for x in f.readlines()]

def write_file(filename, lines): 
    '''Writes a list of lines to a file
    '''   
    with open(filename, "w") as f:
        f.writelines(lines)

def main():
    cmd_args = qbasic_backend_parse_args()
    back_end = QBasicBackEnd()
    back_end.run(cmd_args["old_MA_file"], cmd_args["merged_TS_file"], cmd_args["new_MA_file"], cmd_args["new_VA_file"])
    

if __name__ == "__main__":
    main()