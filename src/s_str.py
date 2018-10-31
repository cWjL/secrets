# -*- coding: utf-8 -*-

import string,re,enchant
from progressbar import ProgressBar

class StringSec():
    def __init__(self, bin_path, minlen=4):
        self.min_len = minlen
        self.bin_path = bin_path
        self.dic = enchant.Dict("en_US")

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
            return _tmp_lst.append("~~~~~~ No strings found ~~~~~~")   
            
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
                    continue
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
        _HASHES = [("MD5", 32),("SHA_1", 40),
                   ("SHA_2_224", 56),
                   ("SHA_2_256", 64),
                   ("SHA_2_384", 96),
                   ("SHA_2_512", 128),
                   ("SHA_2_512/224", 56),
                   ("SHA_2_512/256", 64),
                   ("SHA_3_224", 56),
                   ("SHA_3_256", 64),
                   ("SHA_3_384", 96),
                   ("SHA_3_512", 128),
                   ("RSA_512", 128),
                   ("RSA_1024", 256),
                   ("RSA_2048", 512),
                   ("RSA_4096", 1024),
                   ("AES_128", 32),
                   ("AES_256", 64),
                   ("EC_128", 32),
                   ("EC_256", 64)
                   ]
        _hashes = []
        _hex_filter = re.compile('^[a-zA-Z0-9]+$')
        _base64_filter = re.compile('^[a-zA-Z0-9\+\/\=]+$')
        _printable = list(self._find_printable_strings(data))
        _bar = ProgressBar(maxval=len(_printable)).start()
        for tic, i in enumerate(_printable):
            if not self._is_printable(i) and len(i) > 6:
                _match = False
                _hash_labels = "::"
                if _hex_filter.match(i):
                    for hsh in _HASHES:
                        if len(i) == hsh[1]:
                            _match = True
                            _hash_labels = _hash_labels + hsh[0] + ":"
                    if not _match:
                        _match = True
                        _hash_labels = _hash_labels + "BASE_64?" + ":"
                elif _base64_filter.match(i):
                    _match = True
                    _hash_labels = _hash_labels + "BASE_64?" + ":"

                if _match:
                    _hashes.append(i+_hash_labels[:len(_hash_labels)-1])
            _bar.update(tic)
        _bar.finish()
        return _hashes

    def _is_printable(self, chk_str):
        '''
        Parse given string looking for dictionary words greater than four
        characters long. Return True if one is found.

        @param string
        @return boolean
        '''
        _chk_this = ""
        for i in range(len(chk_str)):
            _j = i + 4
            while _j < len(chk_str)+1:
                _tmp_str = chk_str[i:_j]
                if self.dic.check(_tmp_str):
                    try:
                        int(_tmp_str)
                    except ValueError:
                        return True
                _j += 1
        return False

