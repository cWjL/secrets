#!/usr/bin/python3
import sys, math, argparse
import colorama
from colorama import Fore, Style

b_prefix = "["+Fore.RED+"*"+Style.RESET_ALL+"] "
g_prefix = "["+Fore.GREEN+"*"+Style.RESET_ALL+"] "

# TODO: Add arguments

def main(in_file):
    global g_prefix
    global b_prefix
    res = _get_entropy_known_length(in_file)
    if res is not 0:
        print(g_prefix+"Input String "+in_file)
        print(g_prefix+"Shannon Entropy: "+str(res))
    else:
        print(b_prefix+"Something went wrong")
    sys.exit(0)

# Naming per pep-8: non-public methods and instance variables
def _get_entropy_known_length(secret):
    if len(secret) < 2:
        return 0
    _entropy = 0
    # Find probabilities of ascii characters 0-255 in string 'secret'
    for i in range(256):
        p_i = float(secret.count(chr(i)))/len(secret)
        # Calculate Shannon Entropy with derived probabilities if > 0 using
        # H = - [SUM(p_ilog_bp_i)] where p_i is the probability of character
        # 'i' apprearing in the input character string and 'b' is the log base
        if p_i > 0:
            _entropy += - p_i*math.log(p_i, 2)
    return _entropy

if __name__ == "__main__":
    colorama.init()
    main(sys.argv[1])
