
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
            convertSamToBed.cc.py -s $f \
            -m BOWTIE2 -o $e.bed.gz &> log.samToBed &
         done
