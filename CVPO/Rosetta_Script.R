############################################
# Making an Ensembl x NCBI Rosetta Stone
############################################

#Set up Bioconductor and BioMart
if (!require("BiocManager", quietly = TRUE))
  install.packages("BiocManager")

BiocManager::install("biomaRt")

###########################################
# Note this script requires the most recent version of Bioconductor (3.18), you will need to be running the most recent version of R(4.3.2) to run this version of bioc
# Please update the following location to store the results of this work:
fileloc <- "~/Downloads/"     #your location here
##########################################

#Run the actual tool
library(biomaRt)

#select the appopriate species from the avaialble dataset
ensembl<-useMart("ENSEMBL_MART_ENSEMBL", dataset="hsapiens_gene_ensembl")


#Collect appropriate data from biomart 
rosetta <- getBM(attributes = c("entrezgene_id","ensembl_gene_id","entrezgene_accession","external_gene_name"), 
              mart= ensembl)

#Name file
time <- c(Sys.Date())
version <- c(listMarts()[1,2])
version <- as.character(version)
version <- gsub(" ", "-", version)
filename <- paste("NCBIxENSG",time,version, sep="_")
filename <- paste(filename,".txt", sep="")

file <- paste(fileloc,filename, sep="")

#Save data 
write.table(rosetta, file, quote = FALSE, sep="\t", row.names = FALSE)

