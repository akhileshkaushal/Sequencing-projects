#!/usr/bin/python
#!/usr/bin/env python
__author__ = "Akhilesh Kaushal","Cristian Coarfa"

import os,sys,re,argparse
import glob
from subprocess import Popen, PIPE
from popen2 import popen2
import time


# If you want to be emailed by the system, include these in job_string:
#PBS -M akhilesh.kaushal@bcm.edu
#PBS -m abe  # (a = abort, b = begin, e = end)

class PBS_Batch_Submission:

    def __init__(self, myArgs):
        print str(myArgs)
        self.setParameters(myArgs)

    def setParameters(self, myArgs):
        print "Setting parameters\n"
        self.myArgs = myArgs
			
    @staticmethod
    def parse_args():
        parser = argparse.ArgumentParser(description='Python Utility for submitting multiple PBS jobs')
        parser.add_argument('-d','--directory', help='Directory of tracks BED files',required=True)
        
        try:
           args = parser.parse_args()
				
        except:
           args = None
        return args
    
    def pbs_qsub(self):
        
        filename = glob.glob(self.myArgs.directory+"/*.bed.gz")
        # Loop over your jobs
        for i in range(len(filename)):
            # Open a pipe to the qsub command.
            f = open("PBS_FILE"+str(i)+".sh",'w')
            output, input = popen2('qsub')
            # Customize your options here
            email = "akhilesh.kaushal@bcm.edu"
            job_name = "my_job_%d"%i
            walltime = "24:00:00"
            processors = "nodes=1:ppn=1"
            VMEM = "vmem=2GB"
            PMEM = "pmem=2GB"
            command = "./my_program -n %d"%i
            FILE_NAME = filename[i]
            OUT_NAME = filename[i].split(".")[0]
    
            job_string = """#!/bin/bash
            #PBS -M %s
            #PBS -N %s
            #PBS -l walltime=%s
            #PBS -l %s
            #PBS -l %s
            #PBS -l %s
            #PBS -o %s.out
            #PBS -e %s.err
            cd $PBS_O_WORKDIR
            module load python/2.7.9
            module load python-packages/2.7
            module load anaconda2/4.3.1
            module load bedtools/2.17.0
            python bedToWig.cc.v002.py -b %s -x /mount/modac/akaushal/temp -e 200 -o %s -t %s -d %s -c 250,0,0 -u -C rn5.chromosomes -r
            %s""" %(email, job_name, walltime, processors, VMEM, PMEM, job_name, job_name, FILE_NAME, OUT_NAME, OUT_NAME, OUT_NAME,command)
     
            # Send job_string to qsub
            input.write(job_string)
            input.close()
     
            f.write(job_string)
            f.close()
	        # Print your job and the system response to the screen as it's submitted
            print(job_string)
            print output.read()
	
    
        time.sleep(0.1)
        ##os.system('qsub '+input)
	
	
########################################################################################
# MAIN
########################################################################################

# Process command line options
## Instantiate analyzer using the program arguments
## Analyze this !

if __name__ == '__main__':
        try:
                myArgs = PBS_Batch_Submission.parse_args()
                print "Program arguments: "+str(myArgs)+"\n"
                if (myArgs is None):
                        pass
                else:
                   sa = PBS_Batch_Submission(myArgs)
                   sa.pbs_qsub()
                        
        except:
                print "An unknown error occurred.\n"
                raise
							
   