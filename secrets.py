#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys,argparse,os,logging,csv,time,traceback,re
from datetime import datetime
import colorama
from colorama import Fore, Style
from src.secret import Secret

def main():
    '''
    Entry main

    @param path to log
    '''
    b_prefix = "["+Fore.RED+"*"+Style.RESET_ALL+"] "
    g_prefix = "["+Fore.GREEN+"*"+Style.RESET_ALL+"] "
    l_prefix = "[ ] "
    in_file = None

    parser = argparse.ArgumentParser()
    parser.add_argument("-a","--all",action='store_true',dest='all',help='Use all methods [DEFAULT OPTION]')
    parser.add_argument("-s","--strings",action='store_true',dest='strs',help='Find ascii strings')
    parser.add_argument("-e","--encoded",action='store_true',dest='enc',help='Find base64 encoded strings in memory')
    parser.add_argument("-m","--hashed",action='store_true',dest='hsh',help='Find hashes')
    # Future state
    #parser.add_argument("-d",action='store_true',dest='dyn',help='Run dynamic analysis, store strings as ascii')
    parser.add_argument("-o",action='store',dest='out',help='Output file [path only, I\'ll name it]')
    reqd_args = parser.add_argument_group('required arguments')
    reqd_args.add_argument('-i',action='store',dest='in_file',help='Input binary',required=True)
    
    args = parser.parse_args()

    log = logging.getLogger(__name__)
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)-8s %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S', filename='logs/sec.log', filemode='w')
 
    if os.path.isfile(os.path.abspath(args.in_file)):
        in_file = os.path.abspath(args.in_file)
        log.info("input file "+in_file+" found")
    else:
        print(b_prefix+"Check your input file. Is it correct?")
        log.error("bad input file: "+args.in_file)
        sys.exit(1)
        
    out_file = "results/"+_get_bin_name(in_file)
    
    if args.out:
        if os.path.isdir(args.out):
            out_file = ck_path(args.out)+_get_bin_name(in_file)
            log.info("output file location for "+out_file+" found")
        else:
            print(b_prefix+"Check your output file path. Is it correct?")
            log.error("bad output filepath: "+args.out)
            sys.exit(1)
            
    print(g_prefix+"Processing binary file...")
    time.sleep(2)
    try:
        get_sec = Secret(in_file, log)
        if not (args.strs and args.enc and args.hsh):
            sec_list = get_sec.get_secrets(True, True, True)
        else:
            sec_list = get_sec.get_secrets(args.strs, args.enc, args.hsh)
        print(g_prefix+"Done")
        time.sleep(2)
        if sec_list is not None and (len(sec_list) > 0):
            print(g_prefix+"Printing strings and associated entropy")
            time.sleep(2)
            log.info("writing out data")
            _write_to_terminal(sec_list, l_prefix)
            _write_out(out_file, sec_list)
            print(g_prefix+"Results written to "+out_file+".txt"+", and "+out_file+".csv")
            time.sleep(2)
            print(g_prefix+"Exiting...")
            log.info("wrote "+out_file+".txt"+" and "+out_file+".csv")
        else:
            print(g_prefix+"No strings were found")
            time.sleep(2)
            print(g_prefix+"Exiting...")
            time.sleep(2)
            log.info("found no strings in "+in_file)
    except Exception as e:
        print(b_prefix+"Error has occured. Check log for details")
        log.error("error: "+str(e))
        log.error(traceback.format_exc())
        sys.exit(1)
        
    sys.exit(0)
    
def _get_bin_name(in_file):
    if '\\' in in_file:
        return in_file[in_file.rfind('\\')+1:]
    else:
        return in_file[in_file.rfind('/')+1:]

def _write_to_terminal(in_list, prefix):
    '''
    Write data to terminal with formatted prefix 'prefix'
    
    [] must be filtered out in order to print to terminal. The 
    unfiltered string will be written to the text and csv output files

    @param data tuple
    @param formatted prefix
    @return none
    '''
    for item in in_list:
        if "::" in item[0]:
            _tmp = item[0].split("::")
            print(prefix+"\t"+re.sub('[]', '', _tmp[0])+"  "+str(item[1])+"  "+_tmp[1])
        else:
            print(prefix+"\t"+re.sub('[]', '', item[0])+"  "+str(item[1]))

def _write_out(out_file, out_list):
    '''
    Write data to text and csv files.  Data is written results/
    directory, unless otherwise specified with '-o' option
    
    To read UTF-8 formatted output, open text file in a properly formatted reader
    (notepad++, emacs, nano, etc.)

    @param filename
    @param data tuple
    @return none
    '''
    with open(out_file+".txt", 'w+') as wo:
        wo.write("["+str(datetime.now())+"] Strings found in file "+out_file+"\n\n")
        for line in out_list:
            if "::" in line[0]:
                _tmp = line[0].split("::")
                wo.write(_tmp[0]+" "+str(line[1])+" "+_tmp[1]+"\n")
            else:
                wo.write(line[0]+" "+str(line[1])+"\n")
    with open(out_file+".csv", 'w+', newline='', encoding='utf-8') as wo:
        writer = csv.writer(wo)
        writer.writerow(["["+str(datetime.now())+"] Strings found in file "+out_file])
        for line in out_list:
            if "::" in line[0]:
                _tmp = line[0].split("::")
                writer.writerow([_tmp[0],line[1],_tmp[1]])
            else:
                writer.writerow([line[0],line[1]])
    
def ck_path(fp):
    '''
    Check for properly formatted file path

    @param filepath
    @return formatted filepath
    '''
    if fp[len(fp)-1] == "\\" or fp[len(fp)-1] == "/":
        return fp
    else:
        if "\\" in fp:
            fp = fp + "\\"
        else:
            fp = fp + "/"
    return fp

if __name__ == "__main__":
    colorama.init()
    if not os.path.exists("logs"):
        os.makedirs("logs")
    if not os.path.exists("results"):
        os.makedirs("results")
    main()
