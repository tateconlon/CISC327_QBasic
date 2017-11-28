#script for running a weeks worth of daily transactions
#python qbasic-daily.py VALIDACCOUNTS.TXT input1.txt input2.txt input3.txt
import os

def day1():
    #
    os.system("python qbasic-daily.py VALIDACCOUNTS.TXT MASTERACCOUNTS.TXT input1.txt input2.txt input3.txt")

def day2():
    #
    os.system("python qbasic-daily.py VALIDACCOUNTS.TXT MASTERACCOUNTS.TXT input4.txt input5.txt input6.txt")
    
def day3():
    #
    os.system("python qbasic-daily.py VALIDACCOUNTS.TXT MASTERACCOUNTS.TXT input7.txt input8.txt input9.txt")

def day4():
    #
    os.system("python qbasic-daily.py VALIDACCOUNTS.TXT MASTERACCOUNTS.TXT input10.txt input11.txt input12.txt")

def day5():
    #
    os.system("python qbasic-daily.py VALIDACCOUNTS.TXT MASTERACCOUNTS.TXT input13.txt input14.txt input15.txt")

def main():
    input("Press Enter to advance to Day 1.")
    day1()
    input("Press Enter to advance to Day 2.")
    day2()
    input("Press Enter to advance to Day 3.")
    day3()
    input("Press Enter to advance to Day 4.")
    day4()
    input("Press Enter to advance to Day 5.")
    day5()

main()
