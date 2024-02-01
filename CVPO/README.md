<h1> CVPO - ClinVar Peroid Organiser </h1>

**CVPO** has been designed to take information the monthly gene specific summary files from ClinVar and combine them into a single, queriable matrix. 

An overview of CVPO can be seen in Figure 1.

![Screenshot 2024-02-01 at 2 32 46 pm](https://github.com/MedicalGenomicsLab/Vigelint/assets/15273099/bea6aed6-4184-4972-8674-8e8f0550d4fd)

# System requirements
PADA-WAN requires Python/3.9.13, and R/4.2.0 .

PADA-WAN has been tested on a local, desktop computer (MacOS 13.3.1) and a cluster computer running qsun.

## Python dependencies
- pandas 1.1.5
- numpy 1.19.5
- argparse
- re
- requests
- time
- datetime 

## R dependencies
- ggplot2
- readxl
- tidyr
- stringr

# PADA-WAN Overview 

**Note** CVPO requires a number of manual steps to acquire the data, and asign the correct date to them. 

# Manual Steps

_Manual Step 1:_ **Download the Gene Specific Summary Files**
Navigate to:
  [ClinVar FTP Archive](https://ftp.ncbi.nlm.nih.gov/pub/clinvar/tab_delimited/archive/)

Download the _Gene Specific Summary_ file for each peroid.

_Manual Step 2:_ **Rename the Gene Specific Summary Files**
Rename 
Note - ClinVar uses an alternative method to define a month (A Thursday close to the start of the month)
In contrast to definition of a month used by PADA-WAN (11:59pm on the last day of the month)

_Manual Step 3:_ **Move The Gene Specific Summary Files**

# Automated Steps 



EDIT:
Upon review, the 
