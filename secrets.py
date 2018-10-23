#!/usr/bin/python3
import sys,argparse,os,logging,csv,time
import colorama
from colorama import Fore, Style
from src.secret import Secret

#TODO add import of src/secret. 

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
    parser.add_argument("-a",action='store_true',dest='all',help='Use all methods [DEFAULT OPTION]')
    parser.add_argument("-s",action='store_true',dest='str',help='Find ascii strings')
    parser.add_argument("-e",action='store_true',dest='enc',help='Find encoded strings, decode them, store them as ascii')
    # Future state
    #parser.add_argument("-d",action='store_true',dest='dyn',help='Run dynamic analysis, store strings as ascii')
    parser.add_argument("-o",action='store',dest='out',help='Output file [path only, I\'ll name it!]')
    reqd_args = parser.add_argument_group('required arguments')
    reqd_args.add_argument('-i',action='store',dest='in_file',help='Input binary',required=True)
    
    args = parser.parse_args()

    log = logging.getLogger(__name__)
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)-8s %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S', filename='logs/sec.log', filemode='w')
    
    out_file = "secrets.txt"
 
    if os.path.isfile(os.path.abspath(args.in_file)):
        in_file = os.path.abspath(args.in_file)
        log.info("input file "+in_file+" found")
    else:
        print(b_prefix+"Check your input file. Is it correct?")
        log.error("bad input file: "+args.in_file)
        sys.exit(1)
    
    if args.out:
        if os.path.isdir(args.out):
            out_file = ck_path(args.out)+out_file
            log.info("output file location "+out_file+" found")
        else:
            print(b_prefix+"Check your output file path. Is it correct?")
            log.error("bad output filepath: "+args.out)
            sys.exit(1)
    if (args.str and args.enc and args.all) or (args.str and args.enc) or (not args.all and not args.str and not args.enc) or args.all:
        opt = None
    elif not args.enc and args.str:
        opt = 0
    elif args.enc:
        opt = 1
        
    print(g_prefix+"Processing binary file...")
    time.sleep(2)
    get_sec = Secret(in_file, log, opt)
    sec_list = get_sec.get_secrets()
    if sec_list is not None:
        print(g_prefix+"Printing strings and associated entropy")
        time.sleep(2)
        _write_to_terminal(sec_list, l_prefix)
        _write_out("strings", sec_list)
        print(g_prefix+"Results written to results/strings.txt, and results/strings.csv")
        time.sleep(2)
        print(g_prefix+"Exiting...")
        log.info("wrote strings.txt and strings.csv to results/ dir")
    else:
        print(g_prefix+"No strings were found")
        time.sleep(2)
        print(g_prefix+"Exiting..")
        time.sleep(2)
        log.info("found no strings in "+in_file)

    sys.exit(0)

def _write_to_terminal(in_list, prefix):
    '''
    Write data to terminal with formatted prefix 'prefix'

    @param data tuple
    @param formatted prefix
    @return none
    '''
    for item in in_list:
        print(prefix+"\t"+item[0]+"\t"+str(item[1]))

def _write_out(out_file, out_list):
    '''
    Write data to text and csv files.  Data is written results/
    directory

    @param filename
    @param data tuple
    @return none
    '''
    
    with open("results/"+out_file+".txt", 'w+') as wo:
        wo.write("Strings found in file\n\n")
        for line in out_list:
            wo.write(line[0]+" "+str(line[1])+"\n")
    with open("results/"+out_file+".csv", 'w+') as wo:
        writer = csv.writer(wo)
        writer.writerow(["Strings found in file"])
        for line in out_list:
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
