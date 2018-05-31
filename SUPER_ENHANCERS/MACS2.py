#!/usr/bin/env python
__author__ = "Akhilesh Kaushal","Cristian Coarfa"
import os,sys,re,argparse
import pandas as pd
import numpy as np
import glob
from itertools import permutations
import datetime
import subprocess
import csv
import time
class MACS2_CALL:
    
    DEBUG = 1
    DEBUG_TrackCoverage = True
    #DEBUG_TrackCoverageLoad = None
    DEBUG_genomicHash = None
    
    
    def __init__(self, myArgs):
        print (myArgs)
        self.setParameters(myArgs)

    def setParameters(self, myArgs):
        print ("Setting parameters\n")
        self.myArgs = myArgs

    @staticmethod
    def parse_args():
        parser = argparse.ArgumentParser(description=
         """\
          Utility to identify peaks using MACS2 for multiple tracsks \n
          * Load a number of BED files (usually ChIP-Seq, ATAC-Seq, MeDIP-Seq, Chipmentation, etc)
          * TODO: ...
         """)
       
        parser.add_argument('-t','--trackFilePattern', help='pattern of tracks BED files',required=True)
        parser.add_argument('-i','--inputfile', help= '[OPTIONAL]input/control file', required=None)
        parser.add_argument('-g','--genome', help='[OPTIONAL]For human and mice specify hg or mm and leave blank for others',required=None)
        parser.add_argument('-o','--outfile', help='[OPTIONAL] output file name for overlap summary',required=None)
       
        try:
           args = parser.parse_args()

        except:
           args = None
        return args
    
    def setupAnalysis(self):
        """
           Setup analysis: Output directory
        """   
        sys.stderr.write("["+str(datetime.datetime.now())+"] setupAnalysis START \n")
        sys.stderr.write("["+str(datetime.datetime.now())+"] setupAnalysis STOP \n")
        
    
    def macs2_callpeak(self):
        """
            Use macs2 callpeak to get the peaks.
        """
        sys.stderr.write("["+str(datetime.datetime.now())+"] macs2 callpeak START \n")
        
        trackFileList = glob.glob(self.myArgs.trackFilePattern)
        inputfile = self.myArgs.inputfile
        if (len(trackFileList)<2):
            sys.stderr.write("This utility requires at least 2 distinct tracks \n")
            sys.exit(4)
        
        """
            Actual work area using MACS2
        """
        for trackFile in (trackFileList):
            OUT_NAME = trackFile.split(".")[0]+"_q_0.01"
            gene_name = self.myArgs.genome
            if (self.DEBUG_TrackCoverage):
                sys.stderr.write("["+str(datetime.datetime.now())+"] Getting peaks for file "+trackFile+"\n")
            
            #process1 = subprocess.Popen(["zcat", bedGZFile], stdout = subprocess.PIPE)
            #process2 = subprocess.Popen(["wc", "-l"], stdin=process1.stdout, stdout = subprocess.PIPE)
            if (self.myArgs.genome==None):
                if (self.myArgs.inputfile==None):
                     str1='macs2 callpeak -t '+ trackFile +' -n '+ OUT_NAME + ' -q 0.01 '
                else:
                      str1='macs2 callpeak -t '+ trackFile + ' -c ' + inputfile + ' -n '+ OUT_NAME + ' -q 0.01 '
                      
            else:
                if (self.myArgs.inputfile==None):
                     str1='macs2 callpeak -t '+ trackFile +' -n '+ OUT_NAME + ' -q 0.01 ' + ' -g ' + gene_name
                else:
                     str1='macs2 callpeak -t '+ trackFile + ' -c ' + inputfile + ' -n '+ OUT_NAME + ' -q 0.01 ' + ' -g ' + gene_name
                
            #process1 = subprocess.Popen([str1], stdout = subprocess.PIPE)
            if (self.DEBUG_TrackCoverage):
                sys.stderr.write("["+str(datetime.datetime.now())+"] Running command "+str1+"\n")
            os.system(str1)
            
    def work(self):
        self.setupAnalysis()
        self.macs2_callpeak()
        #self.loadHomerProfiles()
        #self.outputsummary()
        
        

########################################################################################
# MAIN
########################################################################################

# Process command line options
## Instantiate analyzer using the program arguments
## Analyze this !

if __name__ == '__main__':
        try:
                myArgs = MACS2_CALL.parse_args()
                print ("Program arguments: "+str(myArgs)+"\n")
                if (myArgs is None):
                        pass
                else:
                   sa = MACS2_CALL(myArgs)
                   sa.work()

        except:
                print ("An unknown error occurred.\n")
                raise
