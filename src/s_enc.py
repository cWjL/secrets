import binascii, base64

class EncodedSec():
    def __init__(self, bin_path, chnk_sz):
        self.chunk = chnk_sz
        self.bin_path = bin_path

    def get_strs(self):
        '''
        
        '''
        _printable_strs = []
        for cnk in self._read_bin_data(self.bin_path, self.chunk):
            _byte_str = self._bin_to_hex_str(cnk)
            if self._is_printable_char_str(_byte_str) is not None:
                _printable_strs.append(self._is_printable_char_str(_byte_str))

    def _decode_nonprintable_strings(self, nonprintable_list):
        '''
        Decode binary hex input

        @param list of binary data
        @return list of decoded strings
        '''
        _hex_str = ""
        for i in nonprintable_list:
            try:
                _hex_str = i.replace('\\x', '')
                _decoded.append(binascii.a2b_hex(_hex_str.replace(' ', '')))
            except Exception as ex:
                continue
        return _decoded

    def _is_printable_char_str(self, hex_arr):
        '''
        Determine if hex array contains printable string, return it if so

        @param hex array
        @return string or none
        '''
        _result = ""
        _decode = base64.b64decode(hex_arr)
        for i in _decode:
            if i in string.printable and "\n" not in i  and "\t" not in i:
                _result += i
                continue # next loop iteration, skipping the next if statement
            if len(_result) >= self.min_len:
                yield _result
            _result = ""

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
                    #for b in chunk:
                    #    yield b
                    yield from chunk
                else:
                    break
