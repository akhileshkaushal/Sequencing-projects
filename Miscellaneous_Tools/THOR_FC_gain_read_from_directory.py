#!/usr/bin/python
import os,sys,re,argparse
import gzip
import glob
import numpy as np
from math import log

"""
example usage:
python THOR_FC.py -g THOR_H3K4me1_5mo_M-diffpeaks.bed-gain.bed -f 2 -out THOR_H3K4me1_5mo_M-diffpeaks.bed-gain_2x.bed
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
        parser = argparse.ArgumentParser(description='Returns bed file with 1.5 and 2 fold chnage')
        parser.add_argument('-d', '--directory', help='DIRECTORY OF THOR DIFFPEAKS BED GAIN FILE', required=True)
        parser.add_argument('-f', '--fold_change', help='FOLD_CHANGE either 1.5, 2 or 3', type=float, required=True)
        parser.add_argument('-od', '--outdirectory', help='Directory name for the output files', required=True)   
        try:
           args = parser.parse_args()
				
        except:
           args = None
        return args
		
    def unique_reads(self):
	    
        path = os.makedirs(self.myArgs.outdirectory)
        filename = glob.glob(self.myArgs.directory+"/*.bed")
        inval = float(self.myArgs.fold_change)
		
        for i in range(len(filename)):
            infile = filename[i]
            out_name = filename[i].split(".")[0]+"_"+str(inval)+"X.bed"
            #completeName = os.path.join(path,out_name)
            out_writer = open(out_name,'w')
            with open(infile,'r') as f:
                 for line in f:
                     line1 = line.split("\t")
                     TBT = np.array(line1[10].split(";")[0].split(":")).astype(np.float)
                     TBT_AVE = np.mean(TBT)
                     VEH = np.array(line1[10].split(";")[1].split(":")).astype(np.float)
                     VEH_AVE = np.mean(VEH)
                     if (TBT_AVE > 0 and VEH_AVE > 0):
                         RATIO = TBT_AVE/VEH_AVE
                         if (RATIO >= inval):
                             out_writer.write(line)
                 out_writer.close()
        
		

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
