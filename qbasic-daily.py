import os
import datetime
import argparse
import re

#python qbasic-daily.py VALIDACCOUNTS.TXT  input1.txt input2.txt input3.txt


front_end_cmd = "python qbasic.py {va} {out_ts} < {inp}" 
front_end_cmd_interactive = "python qbasic.py {va} {out_ts}" 
back_end_cmd = "python qbasic-backend.py {ma} {ts} {out_ma} {out_va}"


#run qbasic from command line
#new folder for daily session
#after 3 sessions, merge transaction files
#point output files to backend input

#takes a list of file names (1 for each session inputs)
    #if there's a list of file names, no interactive session
#else ALL INTERACTIVE SESSIONS
class QBasicDaily:

    timeStamp = ""
    ts_fn_format = "{dir}/{0}_ts.txt"
    merged_ts_fn_format = "{dir}/merged_ts.txt"
    output_ma_fn_format = "{dir}/new_ma.txt"
    output_va_fn_format = "{dir}/new_va.txt"

    def __init__(self):
        self.timeStamp = '{:%Y-%m-%d_%H-%M-%S-%f}'.format(datetime.datetime.now())
        self.dir = "d_session_{0}".format(self.timeStamp)

    def run(self, validAccountsFilename, inputList, oldMasterAccountsFilename):

        os.makedirs("{0}".format(self.dir), exist_ok=True)
        
        for i, f_name in enumerate(inputList):
            self.runFrontEnd(validAccountsFilename, i, f_name)
            pass

        #runs interactive sessions until minimum 3 sessions are run
        while i < 2:
            self.runFrontEnd(validAccountsFilename, i)
            i += 1

        self.mergeTransactionFiles()

        self.runBackEnd(oldMasterAccountsFilename, "merged_ts.txt", "new_ma.txt", "new_va.txt") #TODO: Cleanup


    def runBackEnd(self, old_ma_fn, merged_TS_fn, new_ma_fn, new_va_fn):
        old_ma = old_ma_fn #TODO: fix directories
        ts = self.getFullPath(merged_TS_fn)
        new_ma = self.getFullPath(new_ma_fn)
        new_va = self.getFullPath(new_va_fn)
        os.system(back_end_cmd.format(ma=old_ma, ts=ts, out_ma=new_ma, out_va=new_va))

    def mergeTransactionFiles(self):
        merged_trans_list = []
        regex = re.compile(r"[0-9]+_ts.txt")
        for root, dirs, files in os.walk(self.dir):
            for file in files:
                if regex.match(file):
                    full_fn = os.path.join(root, file)
                    temp_lines = self.read_transaction_summary(full_fn)
                    merged_trans_list += temp_lines

        merged_trans_list.append("EOS")
        merged_ts_contents = "\n".join(merged_trans_list)

        self.write_file(self.merged_ts_fn_format.format(dir=self.dir), merged_ts_contents)

    def read_transaction_summary(self, filename):
        lines = self.read_file(filename)
        if lines[-1] == "EOS":
            lines = lines[:-1]
        else:
            print("***** TRANSACTION SUMMARY FILE DID NOT END WITH EOS **********")
        return lines

    def runFrontEnd(self, validAccountsFilename, session_num, input_fn=None):
        out_ts_fn = self.ts_fn_format.format(session_num, dir=self.dir)

        if input_fn == None:
            print("\n**** QBASIC INTERACTIVE SESSION BEGUN ****")
            os.system(front_end_cmd_interactive.format(va=validAccountsFilename, out_ts=out_ts_fn))
        else:
            os.system(front_end_cmd.format(va=validAccountsFilename, out_ts=out_ts_fn, inp=input_fn))

    def getFullPath(self, filename):
        return "{dir}/{fn}".format(dir=self.dir, fn=filename)

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



def qbasic_backend_parse_args():
    '''Validates and parses the command line arguments and returns a dictionary containing them'''
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("va_fn",
                            help="valid accounts filename",
                            type=str)
    arg_parser.add_argument("ma_fn",
                            help="master accounts filename",
                            type=str)
    arg_parser.add_argument('-inputs','--inputList', 
                            nargs='+', 
                            help='input files')

    args = vars(arg_parser.parse_args()) #returns dict {"name": val}

    return args


def main():
    dic = qbasic_backend_parse_args()
    print(dic)
    daily = QBasicDaily()
    daily.run(dic["va_fn"], dic["inputList"], dic["ma_fn"])
    pass

if __name__ == "__main__":
    main()