#!/usr/bin/env python
__author__ = "Akhilesh Kaushal","Cristian Coarfa"
import os,sys,re,argparse
import pandas as pd
import numpy as np
import glob
import itertools
import datetime
import subprocess
import csv
import time
from itertools import permutations

class RPM_SCORE:
    
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
          Computes the RPM score based upon the information from dedup.bed.gz file generated from\n
          "bedToWig.cc.v002.py" program\n
          * Load a number of BED files (usually ChIP-Seq, ATAC-Seq, MeDIP-Seq, Chipmentation, etc)
          * TODO: ...
         """)
       
        parser.add_argument('-t1','--trackFilePattern1', help='pattern of tracks BED files',required=True)
        parser.add_argument('-t2','--trackFilePattern2', help='pattern of tracks dedup files',required=True)
        parser.add_argument('-d','--outDir', help='output directory',required=True)
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
        
        os.system("mkdir -p "+self.myArgs.outDir)
         # Check if the scratch directory exist
        if not os.path.isdir(self.myArgs.outDir):
            sys.exit('Error: Output directory '+self.myArgs.outDir+' does not exist!\n')
        
        sys.stderr.write("["+str(datetime.datetime.now())+"] setupAnalysis STOP \n")
        
        if (self.myArgs.outfile==None ) :
          self.myArgs.outfile = str("summary_non-overlap.xls")
        else:
          self.myArgs.outfile= self.myArgs.outfile
    
    
    def calculate_rpm(self):
        """
            calculate the RPM score of the resulting merged peaks from BEDTOOLS.
        """
        ##Two lines Added by Akhilesh
        #out_coverage = self.myArgs.outfile
        #out_coverage_writer = open(out_coverage,'wb')
        sys.stderr.write("["+str(datetime.datetime.now())+"] STARTING the Calculation of  RPM SCORE \n")
        trackFileList1 = glob.glob(self.myArgs.trackFilePattern1)
        trackFileList2 = glob.glob(self.myArgs.trackFilePattern2)
        
        
        """
            Actual work area using BEDTOOLS
        """
        for trackFile1, trackFile2 in itertools.izip(trackFileList1, trackFileList2):
            bedfile = trackFile1.split(".")[0]
            dedupfile = trackFile2.split(".")[0]
            out_name = trackFile1.split(".")[0] + "_rpm.bed"
            
            if (bedfile==dedupfile):
                score = len(open(trackFile2).readlines(  ))
                if (self.DEBUG_TrackCoverage):
                    sys.stderr.write("["+str(datetime.datetime.now())+"] calculating RPM score for file "+trackFile1+"\n")
                
                data = pd.read_table(trackFile1,header=None,sep="\t")
                per_million = 1000000.0/float(score)
                rpm = data.iloc[:,3]/per_million
                data["RPM"] = rpm

                data.to_csv(out_name,sep="\t",index=False,header=0,index_label=None)
            
            else:
                sys.stderr.write("["+str(datetime.datetime.now())+"] One of the files is missing"+trackFile1+"or"+trackFile2+"\n")
            
            
    def work(self):
        self.setupAnalysis()
        self.calculate_rpm()
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
                myArgs = RPM_SCORE.parse_args()
                print ("Program arguments: "+str(myArgs)+"\n")
                if (myArgs is None):
                        pass
                else:
                   sa = RPM_SCORE(myArgs)
                   sa.work()

        except:
                print ("An unknown error occurred.\n")
                raise
