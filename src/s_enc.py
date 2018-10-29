# -*- coding: utf-8 -*-

import binascii, base64
from progressbar import ProgressBar

class EncodedSec():
    def __init__(self, bin_path, chnk_sz):
        self.chunk = chnk_sz
        self.bin_path = bin_path

    def get_strs(self):
        '''
        Return list of printable strings

        @param none
        @return string list
        '''
        _printable_strs = []
        _tmp_lst = []
        for cnk in self._read_bin_data(self.bin_path, self.chunk):
            try:
                _printable_strs.append(base64.b64decode(cnk))
            except Exception as e:
                self._less(cnk[:(len(cnk)-4)], _printable_strs)
        
        _tmp_lst = self._get_printable_char_list(_printable_strs)
        
        if _tmp_lst is not None and len(_tmp_lst) > 0:
            return _tmp_lst
        else:
            return _tmp_lst.append("No encoded strings found")

    def _less(self, data_cnk, lst):
        '''
        Check for base64 encoded strings by recursively shrinking the size of the binary 
        data chunk by 4 bytes

        @param binary data
        @param string list
        @return string list
        '''
        while True:
            if len(data_cnk) <= 0:
                break
            try:
                lst.append(base64.b64decode(data_cnk))
                break
            except binascii.Error:
                #print("cnk Length: "+str(len(data_cnk)), end='\r') #DEBUG
                # try to add missing padding
                if b"\x3d\x3d\x3d" in data_cnk:
                    data_cnk = data_cnk[:(len(data_cnk)-5)]
                else:
                    data_cnk = data_cnk+b"\x3d"            

    def _decode(self, byte_in):
        '''
        Return hex string representation of binary string passed to it

        @param binary bytes
        @return decoded string
        '''
        _hex_str = ""
        try:
            _hex_str = i.replace('\\x', '')
            _decoded.append(binascii.a2b_hex(_hex_str.replace(' ', '')))
        except Exception as ex:
            return None
        return _decoded

    def _get_printable_char_list(self, hex_list):
        '''
        Determine if hex array contains printable strings, return a list 
        of them if it so

        @param hex array
        @return string or none
        '''
        _result = []
        _bar = ProgressBar(maxval=len(hex_list)).start()
        for tic, i in enumerate(hex_list):
            try:
                _bar.update(tic)
                _result.append(i.decode('utf-8'))
                _result.append(i.decode('ascii'))
            except:
                _bar.update(tic)
                continue
        if len(_result) == 0:
            _result.append("No encoded strings found")
            _bar.finish()
            return _result
        _bar.finish()
        return _result

    def _bin_to_hex_str(self, encoded_data):
        '''
        Decode binary data

        Takes integer binary data, converts to bytestring, then converts and returns
        string formatted hex value

        @param binary data
        @return string
        '''
        _hex_encoded = binascii.b2a_hex(encoded_data.to_bytes((encoded_data.bit_length() + 7) // 8, 'big'))
        return binascii.a2b_hex(_hex_encoded)

    def _read_bin_data(self, data, data_size):
        '''
        Read binary file in 'data_size' sized increments (bytes)

        The file will be read and returned in 'chunksize' increments.

        @param binary data file path
        @return data_size chunk of binary data
        '''
        with open(data, "rb") as f:
            while True:
                chunk = f.read(data_size)
                if chunk:
                    yield chunk
                else:
                    break
