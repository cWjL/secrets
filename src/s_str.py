# -*- coding: utf-8 -*-

import binascii, base64

class StringSec():
    def __init__(self, bin_path, minlen=4):
        self.min_len = minlen
        self.bin_path = bin_path

    def get_strs(self):
        '''
        Function to return list of printable strings
        
        @param  none
        @return string list
        ''' 
        return list(_find_printable_strings(self.bin_path))
        
            

    def _find_printable_strings(data, min=4):
        '''
        Function to parse given file for strings of printable
        characters.  Newlines and tabs filtered.
        
        @param  string filepath
        @param  integer min length of string (default=4)
        @return generator strings
        '''    
        with open(data, errors="ignore") as f:
            _result = ""
            for i in f.read():
                if i in string.printable and "\n" not in i  and "\t" not in i:
                    _result += i
                    continue # next loop iteration, skipping the next if statement
                if len(_result) >= self.min_len:
                    yield _result
                _result = ""
            if len(_result) >= self.min_len:
                yield _result
