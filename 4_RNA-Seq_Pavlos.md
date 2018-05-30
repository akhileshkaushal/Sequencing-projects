
RNA-seq data is paired end. By Visualising top three lines of paired file we conlcuded that RNA-seq data is paired end read.

**(1) Read Trimming using TrimGalore**

    for k in $(ls *gz|cut -f1,1 -d"."|sort -u) <br />
        &nbsp;&nbsp; do <br />
              &nbsp;&nbsp;&nbsp; echo $k <br />
              &nbsp;&nbsp;&nbsp; ls -latrh ${k} <br />
              &nbsp;&nbsp;&nbsp; submitTrimGalore.cc.py -f ${k}.fastq.gz -q dque -c PBS -o ${k} -O trim.${k}.fastq.gz <br />
    done <br />

Submitted this job using shell script "submitTrimGalore.sh" <br />

Steps:
  -- Get to directory containing only the fastq.gz
  -- Execute the shell script "submitTrimGalore.sh"

**(2) Paired end mapping using HISAT2 and StringTie/FeatureCounts**

for f in $(ls *gz|cut -f1,2 -d"."|sort -u)
do 
echo $f
ls -latrh ${f}.R1.fastq.gz ${f}.R2.fastq.gz
submitHISAT2.cc.py -f ${f}.R1.fastq.gz -F  ${f}.R2.fastq.gz  \ 
  -G /store1_d/modac/data/hisat2/hg19/Gencode.V24.on.hg19.hisat2.chr.gtf \ 
    -b /store1_d/modac/data/hisat2/hg19/genome  \ 
    -t 2 -q dque -c PBS -o rnamap.${f}
done

