import os
import argparse

#run this file from the command line with 3 arguments
# week_number validAccountsFilename masterAccountsFilename


daily_cmd = "python qbasic-daily.py {old_va} {old_ma} {new_va} {new_ma} -input {inputs}" #command to run daily session

va_dir = "ValidAccounts"
ma_dir = "MasterAccounts"

va_fn_format = "{dir}/{week}_{day}_va.txt" #valid accounts naming convention
ma_fn_format = "{dir}/{week}_{day}_ma.txt" #master accounts naming convention


def run(week, old_va_fn, old_ma_fn):
    '''
    Runs a week long QBasic session by running 5 daily scripts, 
    each passing the output of one daily script as the input to another.
    Takes a week number, a valid accounts file and a master accounts (to pass to the first daily session)
    All daily session outputted valid accounts go into the ValidAccoutns directory.
    All daily session outputted master accounts go into the MasterAccounts directory.
    '''
    
    os.makedirs(va_dir, exist_ok=True)
    os.makedirs(ma_dir, exist_ok=True)

    prev_va = old_va_fn
    prev_ma = old_ma_fn

    #5 days
    for day in range(0,5):

        #generate daily out valid account and master account filenames
        new_va_fn = va_fn_format.format(dir=va_dir, week=week, day=day)
        new_ma_fn = ma_fn_format.format(dir=ma_dir, week=week, day=day)

        inputList = generate_input_files_list((day*3)+1, 3)

        #run daily session
        os.system(daily_cmd.format(old_va=prev_va, old_ma=prev_ma, new_va=new_va_fn, new_ma=new_ma_fn, inputs=inputList))

        #set past outputs as new inputs
        prev_va = new_va_fn
        prev_ma = new_ma_fn

def generate_input_files_list(startNum, numFiles):
    '''Retuns a space delimited string of input files to input to the daily session
    @params:
    startNum: input file # to start at
    numFiles: number of input files to include
    '''
    file_list = []
    for i in range(startNum, startNum + numFiles):
        file_list.append("daily_inputs/input{0}.txt".format(i))

    return " ".join(file_list)


def parse_cmd_args():
    '''Validates and parses the command line arguments and returns a dictionary containing them'''
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("week_num",
                            help="week number (starts at 0)",
                            type=int)
    arg_parser.add_argument("va_fn",
                            help="valid accounts filename to read from",
                            type=str)
    arg_parser.add_argument("ma_fn",
                            help="old master accounts filename to read from",
                            type=str)

    args = vars(arg_parser.parse_args()) #returns dict {"name": val}

    return args

def main():
    args = parse_cmd_args()
    run(args["week_num"], args["va_fn"], args["ma_fn"])

if __name__ == "__main__":
    main()
