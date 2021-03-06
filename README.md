# secrets

**Version**

&nbsp;&nbsp;1.2

Script that finds ascii and base64 encoded hex strings in a compiled binary, calculates the Shannon entropy of any strings found, and saves results to text and csv files.  Minimum entropy and binary data chunk size are defined in the ```src/secrets.conf``` file.  Entropy must be a floating point number between 1.0 and 8.0 inclusive.  Chunk size is set to 512 bytes by default, but can be any size.<br />

The following two directories will be created in the ```secrets.py``` root directory (if ```-o``` option is not used):<br />
&nbsp;&nbsp;-```logs/```&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Stores session logs as ```sec.log```<br />
&nbsp;&nbsp;-```results/```&nbsp;&nbsp;&nbsp;Stores resulting files as ```<input_file_name>.txt``` and ```<input_file_name>.csv```<br />


**Package requirements:**

&nbsp;&nbsp;install requirements
```
pip install -r requirements.txt
```

**System Requirements:**

&nbsp;&nbsp;python 3

**Usage:**
```
usage: secrets.py [-h] [-a] [-s] [-e] [-m] [-o OUT] -i IN_FILE

optional arguments:
  -h, --help     show this help message and exit
  -v, --version	 Print version and exit
  -a, --all      Use all methods [DEFAULT OPTION]
  -s, --strings  Find ascii strings
  -e, --encoded  Find base64 encoded strings in memory
  -m, --hashed   Find hashes
  -o OUT         Output file [path only, I'll name it]

required arguments:
  -i IN_FILE     Input binary
```
