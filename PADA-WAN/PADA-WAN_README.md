<h1> PADA-WAN: A pipeline designed to download and analyse the information from PanelApp Web Applications. </h1>

*** PanelApp Downloader, Analyser - Web Application Navigator (PADA-WAN) *** is a series of custom python scripts designed to download the information from either PanelApp or PanelApp Australia and characterise how each panel has evolved over a period of time. This pipeline was developed for Evolution of virtual gene panels over time and implications for genomic data re-analysis (Robertson et al., 2023)

- [System requirements](#system-requirements)
  - [Python dependencies](#python-dependencies)
  - [R dependencies](#r-dependencies)
  
- [PADA-WAN Overview ](#padawan-overview)
- [PADA-WAN Components](#padawan-components)


# System requirements
PADA-WAN requires Python/3.9.13, and R/3.5.0 .

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

# PADA-WAN Overview 
 
 PADA-WAN is made of two parts. 
 
 ***Part 1*** is responsible for downloading and summarising the information from PanelApp
 
 ***Part 2*** focuses on characterising change and an option set of R scripts makes it possible to visualise these changes

# PADA-WAN Components

This section describes the individal scripts that make up PADA-WAN.
 
## 1.1 - Download IDs

The first script in the PADA-WAN pipeline queries the PanelApp / PanelApp Australia API to retrieve a list containing all available panels. In addition to this informaiton, this script also collects information about each panel’s numeric panel-ID, and super panel / rare-disease status. Information about the most current version, the date of release of this version and the number of genetic entities are also downloaded. 

This script requires a parameters file, which contains information about the version of PanelApp to query, as well as the the input / output directories. The parameter file also contains the token files for both PanelApp Australia and Genomics England instance of PanelApp. 

An example of the parameter file can be found in /PADA-WAN/1-1/

To run this script use following command:
  python3 1-1_Downlad-IDs.py --file-path parameters_file.txt

If run correctly it will produce a .tsv file containing information for each panel in the PanelApp of your choice.

## 1.2 - Panel Downloader

This script takes each of the panels in the listed in the output file from the Download IDs script (1.1,) and uses this information to download begin to download individual panels from the PanelApp / PanelApp Australia API. 

There are some things to note about this approach:

1. As PanelApp uses both minor and major releases, and there is a large in the number of minor releases before a major release we developed a system to accoutn for this variability. To ensure that that every possible version of a panel was downloaded, this script systematically attempt to download every version from 0.0 until the current release.If a specific minor version of this panel was not available, the script skips it and attempts to download the next minor release of the panel. If the script was unable to download ten consecutive minor versions of panel, the script assumes that there are no more minor releases associated with this major version, and moves to next major release of the panel. If the script failed to download the version of the panel listed in the ID file, a warning file is produced.
2. In addition to processing every available version of a panel, this script also produces a summary file, that contains the number of genes as well as the total number of genes in a specific version of panel.
3. As the information from PanelApp is stored in the JSON format, it can be challenging for people to access this information.To make this information more accessible, it is stored here as a tab delimited text file. 

This script also requires a parameters file. This file contains the location of the ID file produced by 1.1 as well as the tokens for both PanelApp Australia and the Genomics England instance of the resource.

Two example of the parameter files can be found in /PADA-WAN/1-2/

This script is run using the following command:
  python3 1-2_PanelDownloader.py --file-path parameters_file.txt

## 1.3 - Panel Summariser

The third script opens the summary file produced by the second script, and, identifies the specific version of a panel present one last day of each month. It produces a summary file for each panel downloaded by script 1.2, that only shows 1 version of the panel for each month.

This script also requires a parameters file. This file contains the location the files produced by 1.2.

An example of the parameter file can be found in /PADA-WAN/1-3/

This script is run using the following command:
  python3 1-3_PanelSummariser.py --file-path parameters_file.txt

## 1.4 - Panel Factoriser 

The matrices script, opens the monthly summary file for each panel and combines this information into a matrix for a specific variable (no. of releases, no. of genes, no. of diagnostic genes, etc). For example, this script produces an output file that shows number of releases there was been for each panel, over the space of each month.

This script also requires a parameters file. 

An example of the parameter file can be found in /PADA-WAN/1-4/

This script is run using the following command:
  python3 1-4_PanelFactoriser.py --file-path parameters_file.txt

## 2.1 - Characterise Gene Changes

The other series of scripts, describes the process of determining the genes that have been added to, and removed from a panel, as well as the genes that have been upgraded to and downgraded from diagnostic status. 

This script also requires a parameters file. 

An example of the parameter file can be found in /PADA-WAN/2-1/

This script is run using the following command:
  python3 2-1_CharacteriseGeneChanges.py --file-path parameters_file.txt

## 2.2 - Determine Cumulative Gene Changes

This script also requires a parameters file. 

An example of the parameter file can be found in /PADA-WAN/2-2/

This script is run using the following command:
  python3 2-2_CumulativeGeneChanges.py --file-path parameters_file.txt
_____

## 2.3 - Visualisations

