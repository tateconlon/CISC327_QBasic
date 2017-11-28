#script for running a weeks worth of daily transactions
#python qbasic-daily.py VALIDACCOUNTS.TXT input1.txt input2.txt input3.txt
import os

def day1():
    #
    os.system("python qbasic-daily.py VALIDACCOUNTS.TXT input1.txt input2.txt input3.txt")

def day2():
    #
    os.system("python qbasic-daily.py VALIDACCOUNTS.TXT input4.txt input5.txt input6.txt")
    
def day3():
    #
    os.system("python qbasic-daily.py VALIDACCOUNTS.TXT input7.txt input8.txt input9.txt")

def day4():
    #
    os.system("python qbasic-daily.py VALIDACCOUNTS.TXT input10.txt input11.txt input12.txt")

def day5():
    #
    os.system("python qbasic-daily.py VALIDACCOUNTS.TXT input13.txt input14.txt input15.txt")

def main():
    day1()
    day2()
    day3()
    day4()
    day5()

main()
