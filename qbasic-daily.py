import os
import datetime
import argparse
import re

#run this file from the command line with 5 arguments
#old_validAccounts.txt old_masterAccounts.txt new_validAccounts.txt new_masterAccounts.txt -input [list of input textfiles representing qbasic front end commands]


class QBasicDaily:
    '''QBasic Daily class runs a minimum of 3 front end sessions that represent a day afterwhich their transaction summary files
    get merged and sent to a back end session which outputs a new master accounts file and a new valid accounts file.''' 

    front_end_cmd = "python qbasic.py {va} {out_ts} < {inp}"        #the command used to run the qbasic front end with an input text file
    front_end_cmd_interactive = "python qbasic.py {va} {out_ts}"    #the command used to run the qbasic front end interactively
    back_end_cmd = "python qbasic-backend.py {ma} {ts} {out_ma} {out_va}"   #the command used to run the qbasic back end

    ts_fn_format = "{dir}/{0}_ts.txt"               #transaction summary filepath format
    merged_ts_fn_format = "{dir}/merged_ts.txt"     #merged transaction summary filepath format

    def __init__(self):
        timeStamp = '{:%Y-%m-%d_%H-%M-%S-%f}'.format(datetime.datetime.now()) #this way the daily session directories will be unique
        self.dir = "d_session_{0}".format(timeStamp)    #the directory all daily session files are stored (transaction summary and merged transaction summary files)

    def run(self, old_va_fn, old_ma_fn, new_va_fn, new_ma_fn, inputList):
        '''Runs the front session for a minimum of 3 times. If less than 3 input lists are present, the remaining sessions are interactive front end.
        Then it merges the transaction files for all the front end sessions for this run and passes it to the back-end.
        All daily session inputs and outputs must be passed in. All internal files (transaction summary files and merged transaction summary files)
        are handled.
        @params: 
        old_va_fn: valid accounts filename for the front end runs
        old_ma_fn: master accounts filename for the back end run
        new_va_fn: filename of the new valid accounts file produced by back-end run
        new_ma_fn: filename of the new master accounts file produced by the back end run
        '''
        os.makedirs(self.dir, exist_ok=True)
        
        for i, input_fn in enumerate(inputList):
            self.runFrontEnd(old_va_fn, i, input_fn)
            pass

        #runs interactive sessions until minimum 3 sessions are run
        while i < 2:
            self.runFrontEnd(old_va_fn, i)
            i += 1

        merged_ts_fn = self.mergeTransactionFiles()

        self.runBackEnd(old_ma_fn, merged_ts_fn, new_ma_fn, new_va_fn)


    def runBackEnd(self, old_ma_fn, merged_TS_fn, new_ma_fn, new_va_fn):
        '''Runs a QBasic back end session'''
        os.system(self.back_end_cmd.format(ma=old_ma_fn, ts=merged_TS_fn, out_ma=new_ma_fn, out_va=new_va_fn))

    def mergeTransactionFiles(self):
        '''Merges all transaction files that are in self.dir and writes the merged transaction file
        Returns the filename of the merged transaction summary file.
        '''

        merged_trans_list = []  #a list of transaction summary lines (excluding EOS)
        regex = re.compile(r"[0-9]+_ts.txt")    #the regular expression for a transaction summary file

        for root, dirs, files in os.walk(self.dir): #loop through all files in daily session directory
            for file in files:
                if regex.match(file):   #is a transaction summary file
                    full_fn = os.path.join(root, file)
                    temp_lines = self.read_transaction_summary(full_fn)
                    merged_trans_list += temp_lines

        merged_trans_list.append("EOS")
        merged_ts_contents = "\n".join(merged_trans_list)

        merged_ts_fn = self.merged_ts_fn_format.format(dir=self.dir)

        self.write_file(merged_ts_fn, merged_ts_contents)   #write the merged transaction summary file

        return merged_ts_fn_format 

    def read_transaction_summary(self, filename):
        '''Reads a transaction summary file. Returns a list of it's transaction codes excluding the last "EOS" line.
        '''
        lines = self.read_file(filename)
        if lines[-1] == "EOS":
            lines = lines[:-1]
        else:
            print("***** TRANSACTION SUMMARY FILE DID NOT END WITH EOS **********")
        return lines

    def runFrontEnd(self, va_fn, session_num, input_fn=None):
        '''Runs a QBasic front end session'''
        out_ts_fn = self.ts_fn_format.format(session_num, dir=self.dir)

        if input_fn == None:
            print("\n**** QBASIC INTERACTIVE SESSION BEGUN ****")
            os.system(self.front_end_cmd_interactive.format(va=va_fp, out_ts=out_ts_fn))
        else:
            os.system(self.front_end_cmd.format(va=va_fn, out_ts=out_ts_fn, inp=input_fn))

    def read_file(self, filename, keep_newlines=False):
        '''Reads a file into a list of lines and returns them '''
        with open(filename, "r") as f:
            if keep_newlines:
                return f.readlines()
            else:
                return [x.rstrip("\n") for x in f.readlines()]

    def write_file(self, filename, lines): 
        '''Writes a list of lines to a file.'''   
        with open(filename, "w") as f:
            f.writelines(lines)



def parse_cmd_args():
    '''Validates and parses the command line arguments and returns a dictionary containing them'''
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("old_va_fn",
                            help="valid accounts filename to read from",
                            type=str)
    arg_parser.add_argument("old_ma_fn",
                            help="old master accounts filename to read from",
                            type=str)
    arg_parser.add_argument("new_va_fn",
                            help="new valid accounts filename to generate",
                            type=str)
    arg_parser.add_argument("new_ma_fn",
                            help="new master accounts filename to generate",
                            type=str)
    arg_parser.add_argument('-inputs','--inputList', 
                            nargs='+', 
                            help='input files')

    args = vars(arg_parser.parse_args()) #returns dict {"name": val}

    return args


def main():
    args = parse_cmd_args()
    daily = QBasicDaily()
    daily.run(args["old_va_fn"], args["old_ma_fn"], args["new_va_fn"], args["new_ma_fn"], args["inputList"])
    pass

if __name__ == "__main__":
    main()