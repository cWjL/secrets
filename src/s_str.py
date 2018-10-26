# -*- coding: utf-8 -*-

import string,re

class StringSec():
    def __init__(self, bin_path, minlen=4):
        self.min_len = minlen
        self.bin_path = bin_path

    def get_strs(self, hash_opt=False):
        '''
        Return list of printable strings
        
        @param  none
        @return string list
        '''
        _tmp_lst = []

        if hash_opt:
            _tmp_lst.append("~~~~~~ Hash strings found ~~~~~~")
            _tmp_lst.extend(self._find_hash_strings(self.bin_path))
        else:
            _tmp_lst.append("~~~~~~ Strings found ~~~~~~")
            _tmp_lst.extend(list(self._find_printable_strings(self.bin_path)))

        if _tmp_lst is not None and len(_tmp_lst) > 1:
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

    def _find_hash_strings(self, data):
        '''
        Parse given file for strings of printable
        characters matching common hash formats.
        
        @param  string filepath
        @return generator strings
        '''
        _HASHES = [("MD5", 32),("SHA_1", 40),("SHA_2_224", 56),
                   ("SHA_2_256", 64),("SHA_2_384", 96),("SHA_2_512", 128),
                   ("SHA_2_512/224", 56),("SHA_2_512/256", 64),("SHA_3_224", 56),
                   ("SHA_3_256", 64),("SHA_3_384", 96),("SHA_3_512", 128)]
        _hashes = []
        _hex_filter = re.compile('^[a-zA-Z0-9]+$')
        _printable = list(self._find_printable_strings(data))
        for i in _printable:
            if _hex_filter.match(i):
                _hash_labels = "::"
                _match = False
                for hsh in _HASHES:
                    if len(i) == hsh[1]:
                        _match = True
                        _hash_labels = _hash_labels + hsh[0] + ":"
                if _match:
                    _hashes.append(i+_hash_labels[:len(_hash_labels)-1])
        return _hashes

