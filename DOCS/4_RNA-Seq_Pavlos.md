
RNA-seq data is paired end. By Visualising top three lines of paired file (Suggested by Prof. Coarfa) we conlcuded that RNA-seq data is paired end read.

**(1) Read Trimming using TrimGalore**

    for k in $(ls *_1.fq.gz|cut -f1,1 -d"_"|sort -u) 
        do 
            echo $k 
            ls -latrh ${k}
            submitTrimGalore.cc.py -f ${k}_1.fq.gz -F ${k}_2.fq.gz -q dque -c PBS -o ${k} -O trim.${k}.fastq.gz
     done 

Submitted this job using shell script "submitTrimGalore_RNA_Seq_paired.sh" <br />

Steps:<br />
  -- Get to directory containing only the fastq.gz <br />
  -- Execute the shell script "submitTrimGalore_RNA_Seq_paired.sh" <br />

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
        
**[Quality Control Report](https://github.com/CoarfaBCM/Akhilesh_Projects/blob/master/DOCS/QC.txt)
     

**(3) Combining gene abundance data**

       # prepare a configuration file
       for f in rnamap.*Abun*; do echo $f; done > conf-on-hg19
       # combine gene profile abundance from StringTie (FPKM) and featureCounts (read counts)
       combineCocktailGeneAbundance.cc.py -q conf-on-hg19  -g /store1_d/modac/data/hisat2/hg19/Gencode.V24.on.hg19.hisat2.chr.gtf -o combined-rnaseq-Sample1_Sample2 &> log.txt
