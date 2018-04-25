#!/usr/bin/env python
__author__ = "Akhilesh Kaushal","Cristian Coarfa"
import os,sys,re,argparse
import pandas as pd
import numpy as np
import glob
from itertools import permutations
import datetime
import csv

class Subtract_Permutation:
    
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
          Utility that computes non-overlap between all combinations of input bed files\n
          and outputs the non-overlap bed files and csv file contining the log2FC for each non-overlap\n
          * Load a number of BED files (usually ChIP-Seq, ATAC-Seq, MeDIP-Seq, Chipmentation, etc)
          * TODO: ...
         """)
       
        parser.add_argument('-t','--trackFilePattern', help='pattern of tracks BED files',required=True)
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
          
       
    def generateoverlapbetweenTracks(self):
        """
            Use BEDTOOLS INTERSECT to generate overlap signal between tracks.
        """
        sys.stderr.write("["+str(datetime.datetime.now())+"] generateoverlapbetweenTracks START \n")
        
        trackFileList = glob.glob(self.myArgs.trackFilePattern)
        if (len(trackFileList)<2):
            sys.stderr.write("This utility requires at least 2 distinct tracks \n")
            sys.exit(4)
        
        """
           Store the combination of trackLabels to use as Header for ouput Summary
        """
        
        self.trackLabels = []
        for trackFile1, trackFile2 in permutations(trackFileList,2):
            baseTrack = os.path.basename(trackFile1) + "_" + os.path.basename(trackFile2)
            self.trackLabels.append(baseTrack)
            
        numberOfTracks = len(self.trackLabels)
        print ("Number of Tracks: "+str(numberOfTracks)+"\n")
        print ("followed by \n")
        print ("Track Labels: "+str(self.trackLabels)+"\n")
        
        """
            create an Empty Dataframe to store the output summary and
            list to append the columns in loop
        """
        
        self.coverageMatrix = pd.DataFrame()
        list_ = []
        
        """
            Actual work area using BEDTOOLS SUBTRACT
        """
        for trackFile1, trackFile2 in permutations(trackFileList,2):
            if (self.DEBUG_TrackCoverage):
                sys.stderr.write("["+str(datetime.datetime.now())+"] Getting Overlap for file "+trackFile1+" and  "+trackFile2+"\n")
             
             
            outCoverageFile = os.path.join(self.myArgs.outDir,os.path.basename(trackFile1)+"."+os.path.basename(trackFile2)+"_non-overlap.bed")
            str2='bedtools subtract -a '+ trackFile1 + ' -b '+ trackFile2 + ' > ' + outCoverageFile
            if (self.DEBUG_TrackCoverage):
                sys.stderr.write("["+str(datetime.datetime.now())+"] Running command "+str2+"\n")
            os.system(str2)
            
            df = pd.read_table(outCoverageFile, header = None, index_col=None, usecols = [11])
            list_.append(df)
            
        self.coverageMatrix = pd.concat(list_, axis = 1)
        
    def outputsummary(self):
        """
            Output the summary
        """
        outputFileName = self.myArgs.outfile
        self.coverageMatrix.to_csv(outputFileName, header = self.trackLabels, sep="\t")
        pass
        
    def work(self):
        self.setupAnalysis()
        self.generateoverlapbetweenTracks()
        #self.loadHomerProfiles()
        self.outputsummary()
        
        

########################################################################################
# MAIN
########################################################################################

# Process command line options
## Instantiate analyzer using the program arguments
## Analyze this !

if __name__ == '__main__':
        try:
                myArgs = Subtract_Permutation.parse_args()
                print ("Program arguments: "+str(myArgs)+"\n")
                if (myArgs is None):
                        pass
                else:
                   sa = Subtract_Permutation(myArgs)
                   sa.work()

        except:
                print ("An unknown error occurred.\n")
                raise
