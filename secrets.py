#!/usr/bin/python3
import sys, math, argparse, string, codecs, binascii
import colorama
from colorama import Fore, Style

b_prefix = "["+Fore.RED+"*"+Style.RESET_ALL+"] "
g_prefix = "["+Fore.GREEN+"*"+Style.RESET_ALL+"] "

# TODO: Add arguments

def main(in_file):
    global g_prefix
    global b_prefix
    res_dict = []
    #res = _get_entropy_known_length(in_file)
    strings = list(_find_printable_strings(in_file))
    for item in strings:
        if _get_entropy_known_length(item) > 3.9:
            res_dict.append((item, _get_entropy_known_length(item)))

    for item in res_dict:
        print(g_prefix+item[0]+" "+str(item[1]))
    #if res is not 0:
    #    print(g_prefix+"Input String "+in_file)
    #    print(g_prefix+"Shannon Entropy: "+str(res))
    #else:
    #    print(b_prefix+"Something went wrong")
    sys.exit(0)

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
            if len(_result) >= min:
                yield _result
            _result = ""
        if len(_result) >= min:
            yield _result

def _find_nonprintable_strings(data, min=16, max=64):
    '''
    Function to parse given file for strings of non-printable
    characters (hex encoded) of length of at least 16
    
    @param  string filepath
    @param  integer min length of string (default=16)
    @param  integer max length of string (default=64)
    @return generator non-printable characters
    '''
    with open(data, errors="ignore") as f:
        _result = ""
        for i in f.read():
            if i not in string.printable:
                _result += i
                continue
            if len(_result) >= min:
                yield repr(_result)
            _result = ""
        if len(_result) >= min:
            yield repr(_result)

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

def _read_bin_data(data, data_size=256):
    '''
    Function to read binary file in 'size' sized increments

    The file will be read and returned in 'chunksize' increments.

    ###  TODO  ###
    Read and return 256 bytes at a time, then look through <somebyte> increments
    on the receiving end looking for interesting high entropy data.

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
    

if __name__ == "__main__":
    colorama.init()
    #main(sys.argv[1])
    #print(list(_find_printable_strings(sys.argv[1])))
    #print(list(_find_nonprintable_strings(sys.argv[1])))
    #print(repr(list(_find_nonprintable_strings(sys.argv[1]))))
    #print(_decode_nonprintable_strings(list(_find_nonprintable_strings(sys.argv[1]))))
    #_test(sys.argv[1])
    for i in _read_bin_data(sys.argv[1]):
        print(_bin_to_hex_str(i))
