#!/usr/bin/env python
__author__ = "Akhilesh Kaushal","Cristian Coarfa"

import os,sys,re,argparse
import pandas as pd
import numpy as np
import glob
from itertools import combinations
import datetime
import csv

class Overlap_Combination:
    
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
          Utility that computes overlap between all combinations of input bed files\n
          and outputs the intersected bed files and csv file contining the log2FC for each overlap\n
          * Load a number of BED files (usually ChIP-Seq, ATAC-Seq, MeDIP-Seq, Chipmentation, etc)
          * TODO: ...
         """)
       
        parser.add_argument('-t','--trackFilePattern', help='pattern of tracks BED files',required=True)
        parser.add_argument('-d','--outDir', help='output directory',required=True)
        parser.add_argument('-o1','--outfile1', help='[OPTIONAL] output file name for overlap summary',required=None)
        parser.add_argument('-o2','--outfile2', help='[OPTIONAL] output file name for overlap summary',required=None)
        
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
        
        if (self.myArgs.outfile1==None ) :
          self.myArgs.outfile1 = str("summary_overlap1.xls")
        else:
          self.myArgs.outfile1= self.myArgs.outfile1
          
        if (self.myArgs.outfile2==None ) :
          self.myArgs.outfile2 = str("summary_overlap2.xls")
        else:
          self.myArgs.outfile2= self.myArgs.outfile2
          
    """
    def loadGenomicFeatures(self, genomicFeaturesBEDFile):
        
            Load a canonical name chrom:start-stop for each genomic feature
        
        
        sys.stderr.write("["+str(datetime.datetime.now())+"] loadGenomicFeatures START \n")
        genomicFeatureArray = []
        genomicFeatureReader = open(genomicFeaturesBEDFile, "r")
        global genomicFeatureIndexHash
        genomicFeatureIndexHash = {}
        genomicFeatureIndex = 0
        for line in genomicFeatureReader.readlines():
            col = line.strip().split("\t")
            featureName = col[0]+"_"+col[1]+"_"+col[2]
            ##Akhilesh_check
            ##print "feature name: "+featureName+"\n"
            genomicFeatureArray.append(featureName)
            genomicFeatureIndexHash[featureName]=genomicFeatureIndex
            ##Akhilesh_Check
            ##print genomicFeatureIndexHash.keys()
            if (self.DEBUG_genomicHash):
                sys.stderr.write("Genomic Hash "+featureName+" ~~> "+str(genomicFeatureIndexHash[featureName])+"\n")
            
            genomicFeatureIndex += 1
        
        genomicFeatureReader.close()
        sys.stderr.write("["+str(datetime.datetime.now())+"] generateIndividualTrackCoverages STOP \n")
        
        return genomicFeatureArray, genomicFeatureIndexHash
        
     """   
        
    def generateoverlapbetweenTracks(self):
        """
            Use BEDTOOLS INTERSECT to generate overlap signal between tracks.
        """
        ##Two lines Added by Akhilesh
        #out_coverage = self.myArgs.outfile
        #out_coverage_writer = open(out_coverage,'wb')
        
        sys.stderr.write("["+str(datetime.datetime.now())+"] generateoverlapbetweenTracks START \n")
        
        trackFileList = glob.glob(self.myArgs.trackFilePattern)
        if (len(trackFileList)<2):
            sys.stderr.write("This utility requires at least 2 distinct tracks \n")
            sys.exit(4)
        
        """
           Store the combination of trackLabels to use as Header for ouput Summary
        """
        
        self.trackLabels1 = []
        self.trackLabels2 = []
        for trackFile1, trackFile2 in combinations(trackFileList,2):
            baseTrack1 = os.path.basename(trackFile1) + "_" + os.path.basename(trackFile2)
            baseTrack2 = os.path.basename(trackFile2) + "_" + os.path.basename(trackFile1)
            self.trackLabels1.append(baseTrack1)
            self.trackLabels2.append(baseTrack2)
        numberOfTracks = len(self.trackLabels1)
        print ("Number of Tracks: "+str(numberOfTracks)+"\n")
        print ("followed by \n")
        print ("Track Labels: "+str(self.trackLabels1)+"\n")
        
        """
            create an Empty Dataframe to store the output summary and
            list to append the columns in loop
        """
        
        self.coverageMatrix1 = pd.DataFrame()
        self.coverageMatrix2 = pd.DataFrame()
        list1_ = []
        list2_ = []
        
        
        """
            Actual work area using BEDTOOLS INTERSECT
        """
        for trackFile1, trackFile2 in combinations(trackFileList,2):
            if (self.DEBUG_TrackCoverage):
                sys.stderr.write("["+str(datetime.datetime.now())+"] Getting Overlap for file "+trackFile1+" and  "+trackFile2+"\n")
             
            ##Understand this area_Akhilesh   
            outCoverageFile = os.path.join(self.myArgs.outDir,os.path.basename(trackFile1)+"."+os.path.basename(trackFile2)+".intersect.bed")
            str2='bedtools intersect -a '+ trackFile1 + ' -b '+ trackFile2 + ' -wa ' + ' -wb ' ' > ' + outCoverageFile
            if (self.DEBUG_TrackCoverage):
                sys.stderr.write("["+str(datetime.datetime.now())+"] Running command "+str2+"\n")
            os.system(str2)
            
            df1 = pd.read_table(outCoverageFile, header = None, index_col=None, usecols = [11])
            df2 = pd.read_table(outCoverageFile, header = None, index_col=None, usecols = [39])
            list1_.append(df1)
            list2_.append(df2)
        
        self.coverageMatrix1 = pd.concat(list1_, axis = 1)
        self.coverageMatrix2 = pd.concat(list2_, axis = 1)
		
    def outputsummary(self):
        """
            Output the summary
        """
        outputFileName1 = self.myArgs.outfile1
        outputFileName2 = self.myArgs.outfile2
        self.coverageMatrix1.to_csv(outputFileName1, header = self.trackLabels1, sep="\t")
        self.coverageMatrix2.to_csv(outputFileName2, header = self.trackLabels2, sep="\t")
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
                myArgs = Overlap_Combination.parse_args()
                print ("Program arguments: "+str(myArgs)+"\n")
                if (myArgs is None):
                        pass
                else:
                   sa = Overlap_Combination(myArgs)
                   sa.work()

        except:
                print ("An unknown error occurred.\n")
                raise
