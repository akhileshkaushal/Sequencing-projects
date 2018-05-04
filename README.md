# Enhancer_Project_Akhilesh
Enhancer sequences are regulatory DNA sequences that, when bound by specific proteins called transcription factors, enhance the transcription of an associated gene. Regulation of transcription is the most common form of gene control, and the activity of transcription factors allows genes to be specifically regulated during development and in different types of cells.(Source: https://www.nature.com/scitable/definition/enhancer-163). This project is related to the identification of Super Enhancers. The term 'super-enhancer' has been used to describe groups of putative enhancers in close genomic proximity with unusually high levels of Mediator binding, as measured by chromatin immunoprecipitation and sequencing (ChIP-seq). (Source: Pott S, Lieb JD: What are super-enhancers? Nature Genetics 2014, 47:8.)

Super Enhancer identification in this project is based upon the method described in _**McKeown MR, Corces MR, Eaton ML, Fiore C, Lee E, Lopez JT, Chen MW, Smith D, Chan SM, Koenig JL et al: Superenhancer Analysis Defines Novel Epigenomic Subtypes of Non-APL AML, Including an RARalpha Dependency Targetable by SY-1425, a Potent and Selective RARalpha Agonist. Cancer Discov 2017, 7(10):1136-1153**_.

Steps involved in identification of Super Enahncers:

(1) Using `MACS2.py` to call peaks genome-wide in the aligned H3K27Ac read data using the aligned IP bed file as the ChIP-seq foreground and the aligned IN bed file (if available) as the control background data. FDR cutoff of 0.01 was used to call the peaks.

(2) Identified peaks were then merged together if they had less than or equal to 12,500 base pairs between them using `Merging_Narrowpeak_within_12.sh` script. The script also produces a file containing the union of the coordinates of each peak from a given sample with all the peaks that overlapped it from the other samples.

Modifications:
    
    Remove all the sites/regions within 3kb of TSS
    Bedtool command to generate the Union of co-ordinate without TSS +/- 3kb
   
    --bedtools window -a UNION_ALL_merged.bed -b rn5-Gencode79.protein_coding.TSS.bed -w 3000 > UNION_ALL_merged_TSS_3kb.bed_
     
    --bedtools subtract -a UNION_ALL_merged.bed -b UNION_ALL_merged_TSS_3kb.bed  -A > UNION_ALL_merged_wo_TSS.bed_


(3) Quantification of each enriched region was done using programs `Coverage.sh` and `Enhancer_RPM.py`.

(4) Finally negative binomial distribution was fitted to RPM scores from each sample using `NB.R` program. Enriched regions with scores above 97.5 percentile were categorized as "Super Enhancers" and remaining as "Typical Enhancers".
