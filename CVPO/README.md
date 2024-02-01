<h1> CVPO - ClinVar Peroid Organiser </h1>

**CVPO** has been designed to take information the monthly gene specific summary files from ClinVar and combine them into a single, queriable matrix. 

An overview of CVPO can be seen in Figure 1.

![Screenshot 2024-02-01 at 2 32 46 pm](https://github.com/MedicalGenomicsLab/Vigelint/assets/15273099/bea6aed6-4184-4972-8674-8e8f0550d4fd)

# System requirements
CVPO requires Python/3.9.13

CVPO has been tested on a local, desktop computer (MacOS 13.3.1) and a cluster computer running qsun.

## Python dependencies
- pandas 1.1.5
- argparse
- re
- time


# CVPO Overview 

CVPO is broken into two parts, a manual part, and a automatic part.

**Note** Unlike the other tools inthe Vigelint, CVPO requires a number of manual steps to acquire the data, asign the correct date to these files, and to move them into the correct location. 

# Manual Steps

_Manual Step 1:_ **Download the Gene Specific Summary Files**
Navigate to:
  [ClinVar FTP Archive](https://ftp.ncbi.nlm.nih.gov/pub/clinvar/tab_delimited/archive/)

Download the _Gene Specific Summary_ file for each period, that you wish to merge into a single matrix.

_Manual Step 2:_ **Rename the Gene Specific Summary Files**
Once downloaded and extracted, the resulting file will be named _gene_specific_summary.txt_. Unfortunately, this process strips the time period from the name of the file.
As ClinVar uses an alternative method to define a month (A Thursday close to the start of the month) to the one used by used by PADA-WAN (11:59pm on the last day of the month), this provides us with an oppurtunity to assign a consistent time peroid to each

For example; this means the _Gene Specific Summary file_ originally labelled as gene_specific_summary_2023-06.txt.gz will be renamed to be ______
 
_Manual Step 3:_ **Move The Gene Specific Summary Files**

To ensure that CVPO can analysed each renamed file, all the 

# Automated Steps 



EDIT:
Upon review, the 
