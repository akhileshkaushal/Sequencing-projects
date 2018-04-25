#!/usr/bin/env python
__author__ = "Akhilesh Kaushal","Cristian Coarfa"

import pandas as pd
from collections import OrderedDict
from itertools import izip, repeat, chain
import os,sys,re,argparse
import pandas as pd
import numpy as np
import glob
from pandas import Series

class Genes_TSS:
    
    DEBUG = 1
    
    def __init__(self, myArgs):
        print str(myArgs)
        self.setParameters(myArgs)

    def setParameters(self, myArgs):
        print "Setting parameters\n"
        self.myArgs = myArgs

    @staticmethod
    def parse_args():
        parser = argparse.ArgumentParser(description='Creates Overlap result from bed files')
        parser.add_argument('-f1', '--infile1', help='BED FILE1', required=True)
        parser.add_argument('-f2', '--infile2', help='BED FILE2', required=True)
        parser.add_argument('-o1', '--outfile1', help='[OPTIONAL] output BED FILE1 name', required=None)
        parser.add_argument('-o2', '--outfile2', help='[OPTIONAL] output BED FILE1 name', required=None)
        try:
           args = parser.parse_args()

        except:
           args = None
        return args
    
    def setupAnalysis(self):
        if (self.DEBUG):
           print "Setting up analysis !"
        
        if (self.myArgs.outfile1==None ) :
          self.myArgs.outfile1 = self.myArgs.infile1 +"_Overlap.bed"
          self.myArgs.outfile1 = self.myArgs.outfile1
          
        if (self.myArgs.outfile2==None ) :
          self.myArgs.outfile2 = self.myArgs.infile2 +"_Overlap.bed"
          self.myArgs.outfile2 = self.myArgs.outfile2
   
    def overlap(self):  

       global genes1
       global genes2
       global file1
       global file2
       
       file1 = pd.read_table(self.myArgs.infile1,header=0,sep="\t")
       s1 = file1['change'].str.split(';').apply(Series, 1).stack()
       s1.index = s1.index.droplevel(-1)
       s1.name = 'change'
       del file1['change']
       file1 = file1.join(s1)
       
       file2 = pd.read_table(self.myArgs.infile2,header=0,sep="\t")
       s2 = file2['change'].str.split(';').apply(Series, 1).stack()
       s2.index = s2.index.droplevel(-1)
       s2.name = 'change'
       del file2['change']
       file2 = file2.join(s2)
       
       #genes1 = file1.change.str.split(';').tolist()
       genes1 = file1['change']
       genes2 = file2['change']
       #genes2 = file2.change.str.split(';').tolist()

       ##Flattening Gene List
       #flat_list_genes1 = [item for sublist in genes1 for item in sublist]
       #flat_list_genes1 = set(flat_list_genes1)
       #flat_list_genes2 = [item for sublist in genes2 for item in sublist]
       #flat_list_genes2 = set(flat_list_genes2)

    def intersect(self, a, b):
        return set(a).intersection(set(b))

    def output(self):
        
        genes = self.intersect(genes1,genes2)
        genes = set(genes)
        
        file11 = file1[file1[file1.columns[6]].isin(genes)]
        #file11 = file1[file1.change.isin(genes)]
        file11.to_csv(self.myArgs.outfile1,"\t",header=True, index=False)
        file21 = file2.loc[file2['change'].isin(genes)]
        #file21 = file2[file2.change.isin(genes)]
        file21.to_csv(self.myArgs.outfile2,"\t",header=True, index=False)
    
    def work(self):
        self.setupAnalysis()
        self.overlap()
        self.output()
        
########################################################################################
# MAIN
########################################################################################

# Process command line options
## Instantiate analyzer using the program arguments
## Analyze this !

if __name__ == '__main__':
        try:
                myArgs = Genes_TSS.parse_args()
                print "Program arguments: "+str(myArgs)+"\n"
                if (myArgs is None):
                        pass
                else:
                   sa = Genes_TSS(myArgs)
                   sa.work()

        except:
                print "An unknown error occurred.\n"
                raise
