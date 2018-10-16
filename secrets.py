#!/usr/bin/python3
import sys,math,argparse,os,logging
import colorama
from colorama import Fore, Style
from src.secret import Secret

#TODO add import of src/secret. 

def main(logpath):
    b_prefix = "["+Fore.RED+"*"+Style.RESET_ALL+"] "
    g_prefix = "["+Fore.GREEN+"*"+Style.RESET_ALL+"] "

    log = logging.getLogger(__name__)
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)-8s %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S', filename=logpath+'sec.log', filemode='w')
#    log.warning('this is a warning')
#    log.error('this is an error')
#    sys.exit(0)
    parser = argparse.ArgumentParser()
    parser.add_argument("-a",action='store_true',dest='all',help='Use all methods [DEFAULT OPTION]')
    parser.add_argument("-s",action='store_true',dest='str',help='Find ascii strings')
    parser.add_argument("-e",action='store_true',dest='enc',help='Find encoded strings, decode them, store them as ascii')
    #parser.add_argument("-d",action='store_true',dest='dyn',help='Run dynamic analysis, store strings as ascii') # Future functionality
    parser.add_argument("-o",action='store',dest='out',help='Output file [path only, I\'ll name it!]')
    reqd_args = parser.add_argument_group('required arguments')
    reqd_args.add_argument('-i',action='store',dest='in_file',help='Input binary',required=True)
    
    args = parser.parse_args()
    out_file = "secrets.txt"
    in_file = None
    
    if args.out:
        if os.path.isdir(args.out):
            out_file = ck_path(args.out)+out_file
        else:
            print(b_prefix+"Check your output file path. Is it correct?")
            log.error('Bad output filepath')
            sys.exit(1)
    if (args.str and args.enc and args.all) or (args.str and args.enc) or (not args.all and not args.str and not args.enc) or args.all:
        opt = None
    elif not args.enc and args.str:
        opt = 0
    elif args.enc:
        opt = 1
        
    get_sec = Secret(args.in_file, log, opt)
    tmpstr = get_sec.get_secrets()
    print(tmpstr)
    sys.exit(0)

def write_out(out, out_list):
    with open(out, 'w+') as wo:
        for line in out_list:
            wo.write(line)
    
def ck_path(fp):
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
    main(os.path.abspath("logs"))
