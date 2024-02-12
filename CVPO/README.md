<h1> CVPO - ClinVar Peroid Organiser </h1>

**CVPO** has been designed to take information the monthly gene specific summary files from ClinVar and combine them into a single, queriable matrix. 

An overview of CVPO can be seen in Figure 1.

![Screenshot 2024-02-01 at 2 32 46 pm](https://github.com/MedicalGenomicsLab/Vigelint/assets/15273099/bea6aed6-4184-4972-8674-8e8f0550d4fd)

# System requirements
CVPO requires Python/3.9.13

CVPO has been tested on a local, desktop computer (MacOS 13.3.1) and a cluster computer running qsun.

## R dependencies 
- R version 4.3.2
- BiocManager
- biomaRt 

## Python dependencies
- pandas 1.1.5
- argparse
- re
- time

# CVPO Overview 

CVPO is broken into two parts, a manual part, and an automatic part. **The manual part is centred around downloading the correct data from ClinVar and ensuring that data is labelled correctly.**

<h2> Preparing the data for CVPO </h2>

# Downloading the Getting the Gene Data From ClinVar

_Step 1:_ open Gene_Specific_Summary_rsync.sh. Copy the command for the time interval you want to examine. With the command line natigate to the folder you wish to store the data in. In the command line enter the command you copied. Repeat for each time peroid you're interested in.

_Manual Alternative:_ **Download the Gene Specific Summary Files**

- CVPO requires the information in the offical ClinVar tab delimited Gene Specific Summary files.

- To access the Tab-delimited Gene Specific Summary files from ClinVar, navigate to:
  [ClinVar FTP Archive](https://ftp.ncbi.nlm.nih.gov/pub/clinvar/tab_delimited/archive/)

- Download the _Gene Specific Summary_ file for each period, that you wish to merge into a single matrix.

_Step 2:_ **Manually Rename the Gene Specific Summary Files**
- Once downloaded and extracted, the resulting file will be named _gene_specific_summary.txt_. Unfortunately, this process strips the time period from the name of the file.
As ClinVar uses an alternative method to define a month (A Thursday close to the start of the month) to the one used by used by PADA-WAN (11:59pm on the last day of the month), this provides us with an oppurtunity to assign a consistent time peroid to each.

- CVPO has been designed to expect files in the following format 'year'_'month'-gene_specific_summary.txt. In this model, year should be written 2024, and months should be written as two digit numbers (i.e. May is 05).

- For example; this means the _Gene Specific Summary file_ originally labelled as gene_specific_summary_2023-06.txt.gz (released on the 1st of June 2023) will be renamed to be 2023_05-gene_specific_summary.txt as it is the most comparible to the PADA-WAN data from May 2023 (representing PanelApp on 2023-05-31).
 
_Step 3:_ **Manually Move The Gene Specific Summary Files**

To ensure that CVPO analyses the appropriate file, each renamed file should be stored in a folder that only contains renamed gene specific summary files.

# Automated Steps - Creating the Rosetta Stone (NCBIxENSG)

Update the 'fileloc' variable in the Rosetta_Script.R.
Run the script using the following command:

    R Rosetta_Script.R 

Note the variable describing the location of file produced from this work needs to be updated for your system.

<h2> Running CVPO </h2>

The next part of CVPO is automated. To run CVPO, modify the attached parameters file (cvpo_params.txt), and use the following commands:

    python3 CVPO.py --file-path cvpo_params.txt

In the params file you will need to list:
1. The location of the renamed _Gene Specific Summary Files_ (GSS)
2. The location of the output matrix
3. The location and name of the Rosetta_File


EDIT:
Upon review it is clear that the Gene Specific Summary file uses the term 'allele' to refer to all alleles (SNVs, CNVs, etc) when describing all alleles, but when descibing pathogenic alleles, this term exclusively refers to SNVs.
