#This script has been written to download all the Tab Delimited Gene Specific Summary files from ClinVar 

#The command follows the following structure:
rsync -avm --include="gene_specific_summary_*" --exclude='*' rsync://ftp.ncbi.nlm.nih.gov/pub/clinvar/tab_delimited/archive/[YEAR] [/OUTPUT LOCATION]

#2014
rsync -rvP --include="gene_specific_summary_*" --exclude='*' rsync://ftp.ncbi.nlm.nih.gov/pub/clinvar/tab_delimited/archive/2014/ .

#2015
rsync -rvP --include="gene_specific_summary_*" --exclude='*' rsync://ftp.ncbi.nlm.nih.gov/pub/clinvar/tab_delimited/archive/2015/ .

#2016
rsync -rvP --include="gene_specific_summary_*" --exclude='*' rsync://ftp.ncbi.nlm.nih.gov/pub/clinvar/tab_delimited/archive/2016/ .

#2017
rsync -rvP --include="gene_specific_summary_*" --exclude='*' rsync://ftp.ncbi.nlm.nih.gov/pub/clinvar/tab_delimited/archive/2017/ .

#2018
rsync -rvP --include="gene_specific_summary_*" --exclude='*' rsync://ftp.ncbi.nlm.nih.gov/pub/clinvar/tab_delimited/archive/2018/ .

#2019
rsync -rvP --include="gene_specific_summary_*" --exclude='*' rsync://ftp.ncbi.nlm.nih.gov/pub/clinvar/tab_delimited/archive/2019/ .

#From 2020 Onwards
rsync -rvP --include="gene_specific_summary_*" --exclude='*' rsync://ftp.ncbi.nlm.nih.gov/pub/clinvar/tab_delimited/archive/ .
