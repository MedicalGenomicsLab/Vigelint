# CVPO

This document describes how to run the ClinVar Peroid Organiser (CVPO). CVPO takes renamed genes specific summary files from ClinVar and combines them into queryable matrixes. These matrixes provide efficient means to lookup how the variants associated with a gene change over time.

A simplified version of the approach used by CVPO is shown in Figure 1.

![image](https://github.com/MedicalGenomicsLab/Vigelint/assets/15273099/5350d9b0-2fb1-41f9-ba2d-3e7e845e3ba2)


**CVPO is performed in two stages.** One stage is run manually, and the other stage is run computationally. The the activities in each of these stages is shown in Figure 2.

![image](https://github.com/MedicalGenomicsLab/Vigelint/assets/15273099/bb4278d0-eaa2-407d-a7c8-dbe9bef316ca)


## Stage 1 - Collecting Variant Information 

**Requirements**
* An internet connection 
* A method to unzip gzip files 

---
**Collecting and Processing the Data**

1. **Navigate to https://ftp.ncbi.nlm.nih.gov/pub/clinvar/tab_delimited/archive/**

*Note*  it is possible to manually navigate to these files. This can be achieved by going to https://ftp.ncbi.nlm.nih.gov/pub/clinvar/, then selecting the **tab_delimited** option, then selecting the **archive** option

2. **Download (an unzip) the gene specific summary files for each month you want to test**

Each gene specific summary file will be available as a gzipped tab delimited text file. It is important to note that while the gzip file contains the date in the file name, the unzipped file does not. 

For example if you wish to download the gene specific summary file for March 2020, you will need to download the file labelled 'gene_specific_summary_2020-03.txt.gz'


3. **Rename each unzipped gene specific summary file**

As the unzipped files do not contain information about the time period they represent in their filenames, we have designed this renaming process an oppuruntity to complete a number of important tasks. These important tasks include

 - Before a file is re-named we recommend opening the file and confirming the date matches the assumed date
 - The correct name ensures that stage 2 of CVPO will properly ingest the variant files 
	 - for the correct format for each gene specific summary file is:
		 -  [YEAR]_[MONTH]-gene_specific_summary.txt
		 - *i.e. 2023_09-gene_specific_summary.txt*


 - Standardise time formats 
	 - PADA-WAN defines the version of a panel present at 11:59pm on the last day of the month to be the monthly representative for that panel
	 - ClinVar is not as strict with times, and *usually* defines a monthly summary as a date within a few days of the start of the month. For example, the Gene Specific Summary File for March 2020 was released on the 2nd of March 2020, while the Gene Specific Summary file for Jan 2020, was released on the 31st of December 2019
	- **As ClinVar and PADA-WAN détermine months differently (Start of month and end of month respectively), we recommend adopting a single approach to times**
	- To convert a ClinVar date to a PADA-WAN date, you simply move the month back by one. For example the January 2020 gene specific summary file, should be renamed to be the December 2019 Gene Specific Summary file 
	- Even if you aren't planning on comparing the information in these files to the information in PanelApp, it is recommended that people adopt a similar date system to the PADA-WAN, as this tool was written to expect PADA-WAN dates


## Stage 2 - Running CVPO

**Requirements**
* Python 
	* argparse
	* re
	* time
	* pandas
* R
	* xx

* A file containing both Ensembl-IDs to NCBI-IDs for each gene that has both

**Running CVPO**

CVPO is run using the following command.

    python3 cvpo.py --file-path cvpo_params.txt

In order to run CVPO you will require a parameters file. An example parameters file is provided, as is, an example PBS script. The parameters file contains the following information:
1. Experiment Name
2. End Year
3. End Month
4. Location of the NCBI/ENSG-ID file 
5. name of the NCBI/ENSG-ID file 
6. Location of the gene specific summary files 
7. Location of the out-put files
