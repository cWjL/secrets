import base64, binascii

class EncodedSec():
    def __init__(self, bin_path, minlen=4):
        self.min_len = minlen
        self.bin_path = bin_path

    def get_strs(self):
        #TODO get encoded string stuff
        tmp = ""
        for chunk in _read_bin_data(self.bin_path, 512):
            do_stuff = None

    def _decode_nonprintable_strings(nonprintable_list):
        '''
        Function to decode binary hex input

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

    def _bin_to_hex_str(encoded_data):
        '''
        Decode binary data

        Takes integer binary data, converts to bytestring, then converts and returns
        string formatted hex value

        @param binary data
        @return string
        '''
        hex_encoded = binascii.b2a_hex(encoded_data.to_bytes((encoded_data.bit_length() + 7) // 8, 'big'))
        return binascii.a2b_hex(hex_encoded)

    def _read_bin_data(data, data_size):
        '''
        Function to read binary file in 'data_size' sized increments (bytes)

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
