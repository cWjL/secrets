# -*- coding: utf-8 -*-

import string

class StringSec():
    def __init__(self, bin_path, minlen=4):
        self.min_len = minlen
        self.bin_path = bin_path

    def get_strs(self):
        '''
        Return list of printable strings
        
        @param  none
        @return string list
        '''
        _tmp_lst = list(self._find_printable_strings(self.bin_path))
        
        if _tmp_lst is not None and len(_tmp_lst) > 0:
            return _tmp_lst
        else:
            return _tmp_lst.append("No strings found")   
            
    def _find_printable_strings(self, data):
        '''
        Parse given file for strings of printable
        characters.  Newlines and tabs filtered.
        
        @param  string filepath
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

