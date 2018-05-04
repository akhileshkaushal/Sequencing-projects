##############################################################################################
##AUTHOR: Akhilesh Kaushal, Cristian Coarfa
##DATE: April 20 2018
##DESCRIPTION: Fits negative binomial distribution to the RPM score and categorizes
## RPM score as 0, 1 with scores above 97.5 percentiles as 1 and remaining as 0
###############################################################################################
rm(list=ls())
library(MASS)
library(plyr)
library(tools)
#set.seed(123)
#x4 <- rnbinom(n=500, size = 10, p= 0.1)
#data<-fitdistr(x4, "negative binomial")
#pnbinom(0.975,size=9.78,mu=88.91,lower.tail=T)
#qnbinom(0.975,size=9.78,mu=88.91,lower.tail=T)
#plot(x4)
#options(op)
setwd("D:\\Dr_Trevino_Jan12_2018\\Enhancers\\April_20_2018_ALL\\RPM_BED1\\")
trim <- function (x) gsub("^\\s+|\\s+$", "", x)

file_list1 <- list.files(,pattern="*.bed")
#mat_data<-vector("list",length(unlist(file_list)))
for (i in 1:length(unlist(file_list1))){
  
  data1<-read.table(file_list1[i],header=F,sep="\t",check.names=F,strip.white=T)
  #head(data1)
  x1<-ceiling(data1[,5])
  x1_nb<-fitdistr(x1,"Negative Binomial")
  #x1_nb
  #pnbinom(0.975, size=x1_nb[1]$estimate["size"], mu=x1_nb[1]$estimate["mu"], lower.tail=T)
  data1$percentiles <- round(pnbinom(x1, size=x1_nb[1]$estimate["size"], mu=x1_nb[1]$estimate["mu"], lower.tail=T),digits=5)
  score_97.5<-qnbinom(0.975, size=x1_nb[1]$estimate["size"], mu=x1_nb[1]$estimate["mu"], lower.tail=T)
  data1$Super_Enhancer <- ifelse(data1[,5]>score_97.5,1,0)
  #data1$Super_Enhancer <- trim(data1$Super_Enhancer)
  data1 <- colwise(trim)(data1)
  #data1=data1[order(-data1[,5]),]
  #data2=data1[,-4]
  data1=data1[,c(1,2,3,6,7,5,4)]
  data1$Score<-paste(data1[,4],data1[,5],data1[,6],sep="_")
  data1=data1[,c(1,2,3,8,4,5,6,7)]
  write.table(data1,file=paste(file_path_sans_ext(file_list1[i]),"_NB_score.bed"),sep="\t",row.names=F,col.names=F,quote=F)
  
}

file_list2 <- list.files(,pattern="*_NB_score.bed")

for (i in 1:length(unlist(file_list2))){
  
  data2<-read.table(file_list2[i],header=F,sep="\t",check.names=F,strip.white=T)
  
  data = data2[which(data2[,6]==1),]
  
  write.table(data,file=paste(file_path_sans_ext(file_list2[i]),"_NB_wo_zeros.bed"),sep="\t",row.names=F,col.names=F,quote=F)
  
}
  

files <- list.files(pattern = "*_NB_wo_zeros.bed")

DF <-  read.table(files[1],header=F,sep="\t")
for (f in files[-1]) DF <- rbind(DF, read.table(f)) 
DF1 <- unique(DF)
write.table(DF1, "All_appended.bed", sep="\t",row.names=FALSE, quote=FALSE)
  

