#!/usr/bin/python3
import sys, math, argparse, enchant, string
import colorama
from colorama import Fore, Style

b_prefix = "["+Fore.RED+"*"+Style.RESET_ALL+"] "
g_prefix = "["+Fore.GREEN+"*"+Style.RESET_ALL+"] "

# TODO: Add arguments

def main(in_file):
    global g_prefix
    global b_prefix
    res_dict = []
    #res = _get_entropy_known_length(in_file)
    strings = list(_find_plaintext_strings(in_file))
    for item in strings:
        if _get_entropy_known_length(item) > 4.0:
            res_dict.append((item, _get_entropy_known_length(item)))

    for item in res_dict:
        print(g_prefix+item[0].replace('\n', '')+" "+str(item[1]))
    #if res is not 0:
    #    print(g_prefix+"Input String "+in_file)
    #    print(g_prefix+"Shannon Entropy: "+str(res))
    #else:
    #    print(b_prefix+"Something went wrong")
    sys.exit(0)

# Naming per pep-8: non-public methods and instance variables
def _get_entropy_known_length(secret):
    '''
    Function to parse given string and determine entropy 
    based on SHANNON function. Higher double values 
    means input value with high entropy (potential secret)

    Calculate Shannon Entropy with derived probabilities if > 0 using
    H = - [SUM(p_ilog_bp_i)] where p_i is the probability of character
    'i' apprearing in the input character string and 'b' is the log base
    
    @param  string secret
    @return double entropy
    '''
    if len(secret) < 2:
        return 0
    _entropy = 0
    # Find probabilities of ascii characters 0-255 in string 'secret'
    for i in range(256):
        p_i = float(secret.count(chr(i)))/len(secret)
        if p_i > 0:
            _entropy += - p_i*math.log(p_i, 2)
    return _entropy

def _find_plaintext_strings(data, min=4):
    '''
    Function to parse given file for strings of printable
    characters
    
    @param  string filepath
    @param  integer min length of string (default=4)
    @return generator strings
    '''    
    with open(data, errors="ignore") as f:
        result = ""
        for i in f.read():
            if i in string.printable:
                result += i
                continue
            if len(result) >= min:
                yield result
            result = ""
        if len(result) >= min:
            yield result

if __name__ == "__main__":
    colorama.init()
    main(sys.argv[1])
    #print(_find_plaintext_strings(sys.argv[1]))
