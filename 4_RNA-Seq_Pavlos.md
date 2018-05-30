
**(1) Read Trimming using TrimGalore

for k in $(ls *gz|cut -f1,1 -d"."|sort -u)
  do 
     echo $k
     ls -latrh ${k}
    submitTrimGalore.cc.py -f ${k}.fastq.gz -q dque -c PBS -o ${k} -O trim.${k}.fastq.gz
Done

Submitted this job using shell script "submitTrimGalore.sh"

Steps:
  -- Get to directory containing only the fastq.gz
  -- Execute the shell script "submitTrimGalore.sh"

**(2) Paired end mapping using HISAT2 and StringTie/FeatureCounts

for f in $(ls *gz|cut -f1,2 -d"."|sort -u)
do 
echo $f
ls -latrh ${f}.R1.fastq.gz ${f}.R2.fastq.gz
submitHISAT2.cc.py -f ${f}.R1.fastq.gz -F  ${f}.R2.fastq.gz  \ 
  -G /store1_d/modac/data/hisat2/hg19/Gencode.V24.on.hg19.hisat2.chr.gtf \ 
    -b /store1_d/modac/data/hisat2/hg19/genome  \ 
    -t 2 -q dque -c PBS -o rnamap.${f}
done
