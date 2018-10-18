# -*- coding: utf-8 -*-

import binascii, base64

class Secret():
    def __init__(self, bin, log_obj, opt=None):
        self.bin = bin
        self.opt = opt
        self.log = log_obj
    
    def get_secrets(self):
    
        if self.opt is None:
            tmp = "Run all methods"
            self.log.warning('Run all methods')
            #from src.s_str import StringSec
            #from src.s_enc import EncodedSec
            #from src.s_dyn import DynamicSec # TODO implement this [floss?] https://github.com/fireeye/flare-floss
        elif self.opt == 0:
            tmp = "Run strings only"
            self.log.warning('Run strings only')
            from src.s_str import StringSec
            string_sec = StringSec(self.bin, 4)
            str_list = string_sec.get_strs()
            # pass StringSec the binary file path
            # StringSec reads binary,extracts strings and returns a list of them
            # Secret() calculates the entropy of each string in the list, adds the string
            # and calculated entropy to a dictionary and returns item
            # DICT: https://www.w3schools.com/python/python_dictionaries.asp
            '''
                thisdict =	{
                "brand": "Ford",
                "model": "Mustang",
                "year": 1964
                }
                x = thisdict["model"] or x = thisdict.get("model")
            '''
        else:
            tmp = "Run encoded only"
            self.log.warning('Run encoded only')
            #from src.s_enc import EncodedSec
        return tmp

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
           
    def _test(data):
        '''
        Test function.  Reads text file containing hex encoded strings,  
        converts to ascii characters, then prints to stdout

        @param filepath to data
        @return none
        '''
        global g_prefix
        global b_prefix
        with open(data, 'r') as f:
            hex_list = [line.replace('\\x', '').strip('\n') for line in f]

        print(g_prefix+"Encoded hex values: ")
        for item in hex_list:
            print(g_prefix+item)
            
        print(g_prefix+"Decoded hex values: ")
        for item in hex_list:
            ###  Binascii is the way to go...this worked perfectly when codecs didn't  ###
            print(g_prefix+str(binascii.a2b_hex(item.replace(' ', ''))))

        sys.exit(0)