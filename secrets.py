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

def _get_entropy_unknown_length(secret_str):
    if len(secret_str) < 2:
        return 0
    _entropy = 0

def _find_plaintext_passwd(data):
    '''
    Function to parse given data for readable strings

    @type data: string
    @param data: the data to be parsed
    @type alpha_list: string
    @rtype: string, None
    @return: string if found, None otherwise
    '''

    ###  THIS IS BROKEN  ###
    ###  Check the if len(poss_word) == len(data) ###
    
    alpha = ['bcdefghjklmnopqrstuvwxyz']
    index = 0
    poss_word = ''
    str_dict = enchant.Dict("en_US")
    data = data.lower()
    data_length = len(data)
    string_length = 0
    for i in range(len(data)+1):
        try:
            if all(c in string.printable for c in data):
                if i > 1 and (data[index:i] not in alpha) and (str_dict.check(data[index:i] or data[index:i] == ' ')):
                    poss_word = poss_word + data[index:i]
                    index = i
                    string_length += 1
                    if len(poss_word) == len(data) or (len(poss_word) == (len(data)-1)) or (len(poss_word) == (len(data)+1)):
                        return poss_word
        except Exception as e:
            print("Exception in check_words()"+str(e))
            continue
    return None

if __name__ == "__main__":
    colorama.init()
    #main(sys.argv[1])
    print(_find_plaintext_passwd(sys.argv[1]))
