<h1> JEDI: A pipeline designed to combined gene and variant information for a specific disease. </h1>

Join External genetic Disease Information (JEDI) is a series of scripts design to combine gene and variant information. **JEDI supports two different approaches (or modes).**

<h2> Summary of the different modes:</h2>

# Mode 1
![Screenshot 2024-02-08 at 10 56 40 am](https://github.com/MedicalGenomicsLab/Vigelint/assets/15273099/e891d7f9-a51a-4fab-92c7-f047b3ba616b)


# Mode 2
![Screenshot 2024-02-08 at 11 00 55 am](https://github.com/MedicalGenomicsLab/Vigelint/assets/15273099/1ba663b8-aa98-47ed-a4c4-955a59cc17a3)


# System requirements
JEDI requires Python/3.9.13, and R/3.5.0 .

JEDIhas been tested on a local, desktop computer (MacOS 13.3.1) and a cluster computer running qsun.

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
