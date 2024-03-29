
# Chip-Seq (DEHP,Pb, HighBPA, LowBPA)
## 1. Read Trimming
    for k in $(ls *gz|cut -f1,1 -d"."|sort -u)
       do 
          echo $k
          ls -latrh ${k}
          submitTrimGalore.cc.py -f ${k}.fastq.gz -q dque -c PBS -o ${k} -O trim.${k}.fastq.gz
    done

Submitted this job using shell script "submitTrimGalore.sh"

Steps:<br />
  -- Get to directory containing only the fastq.gz <br />
  -- Execute the shell script "submitTrimGalore.sh" <br />

## 2. Mapping with BOWTIE2

    for f in *fastq.gz; 
        do echo $g; 
           e=$(basename $f|sed -e 's/.fastq.gz//'); echo $e;  
           submitBowtie2Job.py  -G /store1_d/modac/data/bowtie2/mm10/mm10 -f $f -t 2 -q dque -c \
           PBS -x $TMPDIR -o b2map-$e &> log.submit.$e.txt ; 
        done

## 3. Converting SAM.GZ to BED.GZ format
      
     for f in *sam.gz; 
         do echo $g; 
            e=$(basename $f|sed -e 's/bowtie2map.trim.//' sed -e 's/.fastq.gz.fastq.gz.sam.gz//'); echo $e;  
            convertSamToBed.cc.py -s $f -m BOWTIE2 -o $e.bed.gz &> log.samToBed;
         done
   ## OR
   
    python PBS_convertSamtoBed.cc.py -d "$PWD"
    
 ## 4. Signal generation

     bedToWig.cc.py -b Treatment.chr10.bed.gz -x ${TMPDIR} -e 200 -u -o \
     Treatment.signal -t Treatment -d "Treatment, 200bp extension, de-dup" \
     -c 255,0,0 -C mm10.chr10.chromosomes -r &> log.mm10.bedToWig
Above python script is encapsulated in "Python_PBS_for_bedToWig.cc.py" and then used "wig_to_tdf.py"
         
        Python_PBS_for_bedToWig.cc.py -d $PWD -t "$PWD/temp" -c "/store1_d/modac/akaushal/mm10/mm10.txt"
        
        wig_to_tdf.py  -d "$PWD" -g mm10

________________________________________________________________________________________________________________________________
________________________________________________________________________________________________________________________________

# RNA-Seq (10 months Adenoma)

## 1. Read Trimming using TrimGalore

      for k in $(ls *_R1_001.fastq.gz|cut -f1,2,3 -d"_"|sort -u) 
          do 
              echo $k 
              ls -latrh ${k}
              submitTrimGalore.cc.py -f ${k}_R1_001.fastq.gz -F ${k}_R2_001.fastq.gz -q dque -c PBS -o ${k} -O trim.${k}
      done
    

## 2. Mapping with HISAT2 and Stringtie/FeatureCounts

      for k in $(ls *gz|cut -f1,2 -d"."|sort -u);do echo $k;ls -latrh ${k}.R1.fastq.gz ${k}.R2.fastq.gz;submitHISAT2.cc.py -f ${k}.R1.fastq.gz -F ${k}.R2.fastq.gz -G /store1_d/modac/data/hisat2/mm10_snp_tran_ercc/Mus_musculus.GRCm38.90.gtf -b /store1_d/modac/data/hisat2/mm10_snp_tran_ercc/genome_snp_tran -t 2 -q dque -c PBS -o rnamap.${k};done

## [Quality Control](https://github.com/CoarfaBCM/Akhilesh_Projects/blob/master/DOCS/QC_Mouse_RNA-seq.txt)

## 3. Combining gene abundance data
      # prepare a configuration file
      for f in rnamap.trim.*Abun*; do echo $f; done > conf-on-mm10
      # combine gene profile abundance from StringTie (FPKM) and featureCounts (read counts)
      combineCocktailGeneAbundance.cc.py -q conf-on-mm10  -g /store1_d/modac/data/hisat2/mm10_snp_tran_ercc/Mus_musculus.GRCm38.90.gtf  -o combined-rnaseq-10months &> log.txt

## 4. Generating signal maps (WIG, TDF)

     Will do this later for 10 months (adenoma data)
     I do not have FASTQ files for 3wk and 5mo
     
## 5. Pathway Enrichment (ORA - over representation analysis)

# ATAC-seq

## 1. Read Trimming
## 2. Paired End Mapping with BOWTIE2

     
  
