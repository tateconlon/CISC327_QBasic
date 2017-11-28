#script for running a weeks worth of daily transactions
#python qbasic-daily.py VALIDACCOUNTS.TXT input1.txt input2.txt input3.txt
import os
import argparse

daily_cmd = "python qbasic-daily.py {old_va} {old_ma} {new_va} {new_ma} -input {inputs}"

va_dir = "ValidAccounts"
ma_dir = "MasterAccounts"

va_fn_format = "{dir}/{week}_{day}_va.txt"
ma_fn_format = "{dir}/{week}_{day}_ma.txt"


def run(week, old_va_fn, old_ma_fn):
    
    os.makedirs(va_dir, exist_ok=True)
    os.makedirs(ma_dir, exist_ok=True)

    prev_va = old_va_fn
    prev_ma = old_ma_fn

    for day in range(1,6):

        new_va_fn = va_fn_format.format(dir=va_dir, week=week, day=day)
        new_ma_fn = ma_fn_format.format(dir=ma_dir, week=week, day=day)

        inputList = generate_input_files_list(week*5 + day, 3)

        print("***** RUN DAILY SESSION {0} *****".format(day))
        os.system(daily_cmd.format(old_va=prev_va, old_ma=prev_ma, new_va=new_va_fn, new_ma=new_ma_fn, inputs=inputList))

        prev_va = new_va_fn
        prev_ma = new_ma_fn

def generate_input_files_list(startNum, numFiles):
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
