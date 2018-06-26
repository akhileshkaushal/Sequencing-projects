
# To Do list:

## (1) PI: Pavlos

Recieved tables summarizing the differential expression (for protein-coding RNA and non-protein-coding RNA) of RMC tissues from 11 patients with RMC tumors (n=11 samples) vs adjacent normal controls (n=6 samples). These 11 patients include the 4 patients (RMC2, RMC4, RMC30, RMC31) we analyzed with H3K27me3 ChIP-seq. If needed, I can give you the FPKM values for the individual samples.

“padj” in the columns corresponds to p-values adjusted by the Benjamini & Hochberg method. 

Pending analyses for the project per today’s discussion: (Task list)
   - [ ] 1) Integrate the attached RNAseq signatures with the H3K27me3 results
   - [ ] 2) Determine which genes have H3K27me3 peaks or not (yes vs. no) in each of the samples. If yes, is it on the promoter    region,   gene body or elsewhere? (as we discussed, this can be done as part of the integration with the RNAseq data) 
   - [ ] 3) Make a figure with epigenomic partition distribution of H3K27me3 in RMC tumor and normal tissues using fetal kidney from the epigenomics roadmap as the template
   - [ ] 4) Perform H3K27me3 motif analysis for tumor vs normal using HOMER
   - [ ] 5) Compare our H3K27me3 tumor vs normal peaks in RMC with the MRT tumor vs normal peaks from the TARGET database (this will be done after we have access to that database)


## (2) PI: Charles Foulds
   - [x] Rerun the samtosignal pipeline with proper names for the file (e.g. include the GSM number as one of the identifiers in filenames. 

**Note:** Inspect the sam.gz file before executing this pipeline. If the file contains string like chr1,chr2,etc. then do not use the **-a** flag of the pipeline.
    
 ## (3) [PI: Tiffany Katz (Prof. Walker and Prof. Coarfa)](https://github.com/CoarfaBCM/Akhilesh_Projects/blob/master/DOCS/3_Tiffany_Katz_Chip-Seq_MD_Anderson.md)
 Received the RNA-seq and Chip-Seq data from Md Anderson. Need to discuss with Prof. Coarfa regarding the future analysis.
 
 ## (4) [PI: Pavlos](https://github.com/CoarfaBCM/Akhilesh_Projects/blob/master/DOCS/4_RNA-Seq_Pavlos.md)
 
 Map the RNA-Seq from Pavlos, generate BED files, then score the eRNa using the RNA-seq pipeline.
 Chip-Seq files were mapped to hg19.
 
 ## (5) Enhancers
 
 Similarly, score eRNAs using the mm10 data for Fantom enhancers.
 
 
 
 ## eRNA and Super-Enhancer:
 Need to discuss with Prof. Coarfa regarding the future analysis incorporating Target and Encode data along with mice chip-seq data from Prof. Walker
 
 ## (6) [PI: Elferink]
