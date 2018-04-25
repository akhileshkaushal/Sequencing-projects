#!/usr/bin/env python
import os,sys,re,argparse
import gzip
import glob
import numpy as np

"""
example usage:
python unique1.py -in Bowtie_control_500_rows_output.sam.gz -m 10 -o results.sam.gz
"""
class Unique:

    def __init__(self, myArgs):
        print str(myArgs)
        self.setParameters(myArgs)

    def setParameters(self, myArgs):
        print "Setting parameters\n"
        self.myArgs = myArgs
            
    @staticmethod
    def parse_args():
        parser = argparse.ArgumentParser(description='Extract Unique mapped reads from .sam.gz')
        parser.add_argument('-i', '--infile', help='sam.gz file', required=True)
        parser.add_argument('-m', '--mapq', help='mapq score between 3-42', metavar='N',type=int, required=False)
        parser.add_argument('-o', '--outfile', help='file name for Unique mapped reads', required=True)   
        try:
           args = parser.parse_args()
                
        except:
           args = None
        return args
        
    def unique_reads(self):
        inval = int(self.myArgs.mapq)
        out_unique_writer = gzip.open(self.myArgs.outfile,'wb')
        with gzip.open(self.myArgs.infile,'rb') as f:
             for line in f:
                 li = line.strip()
                 if li.startswith("@"):
                    out_unique_writer.write(line)
                 if not li.startswith("@"):
                    if re.search("(.*)XS(.*)",line) is None:
                       if inval is not None:
                          if (int(line.split()[4]) >= inval): ## and line.split()[6] != '*'):
                           #print line.split()[4]
                              out_unique_writer.write(line)
                       #else:
                           #if (line.split()[6] != "*"):
                            #out_unique_writer.write(line)
                
        out_unique_writer.close()
        
    def work(self):
            self.unique_reads()
        

########################################################################################
# MAIN
########################################################################################

# Process command line options
## Instantiate analyzer using the program arguments
## Analyze this !

if __name__ == '__main__':
        try:
                myArgs = Unique.parse_args()
                print "Program arguments: "+str(myArgs)+"\n"
                if (myArgs is None):
                        pass
                else:
                   sa = Unique(myArgs)
                   sa.unique_reads()
                        
        except:
                print "An unknown error occurred.\n"
                raise
