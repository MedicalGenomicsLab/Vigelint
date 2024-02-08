<h1> JEDI: A pipeline designed to combined gene and variant information for a specific disease. </h1>

Join External genetic Disease Information (JEDI) is a series of scripts design to combine gene and variant information. **JEDI supports two different approaches (or modes).**

# Mode 1: Static Gene List 
![Screenshot 2024-02-08 at 10 56 40 am](https://github.com/MedicalGenomicsLab/Vigelint/assets/15273099/e891d7f9-a51a-4fab-92c7-f047b3ba616b)

### Mode 1: Overview
Mode 1 has been designed to extract the number of variants that align to a specific gene, from the variant matrix produced by CVPO.
This is a very simple script. It simply just takes a list of genes and for each gene, looks up the information in the ClinVar Matrix file, and outputs the results. By using R we can plot how the number of variants in these genes change.

### Mode 1: System requirements
JEDI requires Python/3.9.13, and R/3.5.0 .

JEDI has been tested on a local, desktop computer (MacOS 13.3.1) and a cluster computer running qsun.

### Mode 1: Python dependencies
- pandas 1.1.5
- argparse
- time

### Mode 1: R dependencies
- library(ggplot2)
- library(zoo)
- library(dplyr)
- library(tidyr)

### Mode 1: Data dependencies 
1. A list of the genes you want to examine
2. CVPO Variant Matrix

## Running Mode 1

This section describes the individal scripts that make up JEDI-MODE1.
 
### Running the Python Script 

The Mode 1 python script takes the information from the CVPO variant matrix and extracts that records that are present in a pre-defined gene list.
An example of a gene list can be seen in:
 EXAMPLE_GENE_LIST.txt

This script requires a parameters file, an example of which can be seen in JEDI-param.txt

To run this script use following command:
  python3 JEDI-StaticGeneLisy.py --file-path JEDI-param.txt

### Running the R Script 

The R script plots the results from the Python using ggplot.

To run this script use following command:
  R 2023-09-24_ChangesInStaticGeneList.R --file-path Argument-1 Argument-2 Argument-3 Argument-4 Argument-5

- Argument 1 = Location of results from JEDI-StaticGeneLisy.py
- Argument 2 = Name of results from JEDI-StaticGeneLisy.py
- Argument 3 = Number of 'top genes'
- Argument 4 = Name of experiment
- Arugment 5 = Time Peroid

# Mode 2: Static Gene List 
![Screenshot 2024-02-08 at 11 00 55 am](https://github.com/MedicalGenomicsLab/Vigelint/assets/15273099/1ba663b8-aa98-47ed-a4c4-955a59cc17a3)


### Mode 2: Overview
Mode 2 has been designed to take a panel, determine which version of a panel was present at a specific time point, and determine the variants known to be within those genes at the same point in time. 
This mode is more complex than Mode 1. It's not only uses the variant matrix produced by CVPO, but also the monthly summary files produced by PADA-WAN, as well as the raw panel data downloaded from PanelApp. 

# Mode 2: System requirements
Mode 2 requires Python/3.9.13, and R/3.5.0 .

Mode 2 has been tested on a local, desktop computer (MacOS 13.3.1) and a cluster computer running qsun.

## Mode 2: Python dependencies
- pandas 1.1.5
- os
- datetime
- argparse
- re
- numpy
- time

## Mode 2: R dependencies
- library(ggplot2)
- library(zoo)
- library(dplyr)
- library(tidyr)
- library(stringr)

## Mode 1: Data dependencies 
1. A list of the panels you want examine
2. The Panel ID file from PADA-WAN
3. The monthly summary file produced by PADA-WAN
4. The individiaul raw panels downloaded by PADA-WAN
5. CVPO Variant Matrix

# Running Mode 2

This section describes the individal scripts that make up JEDI:
 
## Running the Python Script 

The Mode 2 python script takes the information from a list of panels you wish examine, An example of a panel list can be seen in:
 EXAMPLE_PANEL_LIST.txt

This script requires a parameters file, an example of which can be seen in JEDI-param.txt

To run this script use following command:
  python3 EvolvingPanels.py --file-path params.txt

## Running the R Script 

The R script plots the results from the Python using ggplot.

To run this script use following command:
  R plot_plpdiagnostic.R --file-path Argument-1 Argument-2 Argument-3 Argument-4 Argument-5

- Argument 1 = id file location 
- Argument 2 = Name of panel id file
- Argument 3 = Monthly breakdown file location 
- Argument 4 = Source
- Arugment 5 = Directory of R PLots 


