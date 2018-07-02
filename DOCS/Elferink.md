

# Chip-Seq
## 1. Read Trimming
    for k in $(ls *_1.fq.gz|cut -f1,1 -d"_"|sort -u) 
    do 
        echo $k 
        ls -latrh ${k}
        submitTrimGalore.cc.py -f ${k}_1.fq.gz -F ${k}_2.fq.gz -q dque -c PBS -o ${k} -O trim.${k}.fastq.gz
 done 

Submitted this job using shell script "submitTrimGalore1.sh"

Steps:<br />
  -- Get to directory containing only the fastq.gz <br />
  -- Execute the shell script "submitTrimGalore1.sh" <br />

## 2. Mapping with HISAT2

    for f in $(ls *gz|cut -f1,2 -d"."|sort -u)
    do 
        echo $f
        ls -latrh ${f}.R1.fastq.gz ${f}.R2.fastq.gz
        submitHISAT2.cc.py -f ${f}.R1.fastq.gz -F  ${f}.R2.fastq.gz  \ 
        -G /store1_d/modac/data/hisat2/mm10_snp_tran_ercc/Mus_musculus.GRCm38.90.gtf \ 
        -b /store1_d/modac/data/hisat2/mm10_snp_tran_ercc/genome_snp_tran  \ 
        -t 2 -q dque -c PBS -o rnamap.${f}
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

