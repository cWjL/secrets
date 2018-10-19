# -*- coding: utf-8 -*-

import binascii, base64
import math,sys
from progressbar import ProgressBar

class Secret():
    def __init__(self, bin, log_obj, opt=None):
        self.bin = bin
        self.opt = opt
        self.log = log_obj
        if self._get_conf("ENT") is not None:
            self.entropy = float(self._get_conf("ENT"))
        if self._get_conf("CHUNK") is not None:
            self.chunk = int(self._get_conf("CHUNK"))
    
    def get_secrets(self):
        '''
        Determine option to run and import the appropriate module.  Returns tuple list
        of the form (strings found, calculated entropy), or None if something went wrong

        @param none
        @return tuple (string, float)
        '''
        if self.opt is None:
            self.log.info('running all methods')
            from src.s_str import StringSec
            from src.s_enc import EncodedSec
        
            string_sec = StringSec(self.bin, 4)
            str_list = string_sec.get_strs()
            # need to return both string and encoded........
            
        elif self.opt == 0:
            self.log.info('running strings only')
            from src.s_str import StringSec
            string_sec = StringSec(self.bin, 4)
            str_list = string_sec.get_strs()

        elif self.opt > 0:
            tmp = "run encoded only"
            self.log.info('running encoded only')
            from src.s_enc import EncodedSec
            enc_sec = EncodedSec(self.bin, self.chunk)
            str_list = enc_sec.get_strs()
            ####  NOT RETURNING ANYTHING.  SOMETHING BROKEN IN EncodedSec ###
            
        return self._get_sec_lst(str_list)

    def _get_entropy(self, secret):
        '''
        Parse given string and determine entropy 
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
        for i in range(256):
            p_i = float(secret.count(chr(i)))/len(secret)
            if p_i > 0:
                _entropy += - p_i*math.log(p_i, 2)
        
        return _entropy

    def _get_sec_lst(self, in_list):
        '''
        Return tuple in the form (string, entropy)

        @param string list
        @return tuple (string:float)
        '''
        bar = ProgressBar(maxval=len(in_list)).start()
        _sec_lst = []
        for i, item in enumerate(in_list):
            if self._get_entropy(item) >= self.entropy:
                _sec_lst.append((item, self._get_entropy(item)))
            bar.update(i)
        bar.finish()
        return _sec_lst

    def _get_conf(self, opt):
        '''
        Import configuration file and return 'opt' element
        
        @param option (string)
        @return string
        '''
        conf_lines = []
        with open('src/secrets.conf', 'r') as conf:
            all_conf_lines = conf.readlines()
            for line in all_conf_lines:
                if '#' not in line:
                    conf = line.split(' ')
                    conf_lines.append((conf[0].replace('\n',''), conf[1].replace('\n', '')))
        for item in conf_lines:
            if opt in item[0]:
                return item[1]
        return None
           
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
