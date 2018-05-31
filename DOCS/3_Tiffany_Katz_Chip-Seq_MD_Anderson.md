
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
