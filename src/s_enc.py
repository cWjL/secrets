import binascii, base64, sys

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
        for cnk in self._read_bin_data(self.bin_path, self.chunk):
            try:
                _printable_strs.append(base64.b64decode(cnk))
            except Exception as e:
                self._less(cnk[:(len(cnk)-4)], _printable_strs)

        tmp = self._get_printable_char_list(_printable_strs)
        print("Length " + str(len(tmp)))
        for i in tmp:
            print(i)
        sys.exit(0)

        #return _printable_strs

    def _less(self, data_cnk, lst):
        '''
        Check for base64 encoded strings by recursively shrinking the size of the binary 
        data chunk by 4 bytes

        @param binary data
        @param string list
        @return string list
        '''
        ### THIS IS BROKEN ###
        ### RecursionError: maximum recursion depth exceeded in __instancecheck__
        if len(data_cnk) == 0:
            return
        ####################################################################################
        #tmp = data_cnk+b"\x3d\x3d\x3d"
        #print(tmp)
        #if b"\x3d\x3d\x3d" in tmp:
        #    print("yep")
        #sys.exit(0)
        ####################################################################################
        try:
            lst.append(base64.b64decode(data_cnk))
            self._less(data_cnk[:(len(data_cnk)-2)], lst)
        except binascii.Error:
            if b"\x3d\x3d\x3d" in data_cnk:
                self._less(data_cnk[:(len(data_cnk)-6)], lst)
            else:
                self._less(data_cnk+b"\x3d", lst)
            

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
        for i in hex_list:
            try:
                _result.append(binascii.unhexlify(i))
            except:
                continue
        return _result

    def _bin_to_hex_str(self, encoded_data):
        '''
        Decode binary data

        Takes integer binary data, converts to bytestring, then converts and returns
        string formatted hex value

        @param binary data
        @return string
        '''
        hex_encoded = binascii.b2a_hex(encoded_data.to_bytes((encoded_data.bit_length() + 7) // 8, 'big'))
        return binascii.a2b_hex(hex_encoded)

    def _read_bin_data(self, data, data_size):
        '''
        Read binary file in 'data_size' sized increments (bytes)

        The file will be read and returned in 'chunksize' increments.

        https://stackoverflow.com/a/1035456/4678883

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
