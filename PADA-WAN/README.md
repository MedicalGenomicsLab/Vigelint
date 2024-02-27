<h1> PADA-WAN 2.0: A pipeline designed to download and analyse the information from PanelApp Web Applications. </h1>

**PanelApp Downloader, Analyser - Web Application Navigator (PADA-WAN)** is a series of custom python scripts designed to download the information from either PanelApp or PanelApp Australia and characterise how each panel has evolved over a period of time. This pipeline was originally developed for Evolution of virtual gene panels over time and implications for genomic data re-analysis (Robertson et al., 2023), but has since been updated to support both PanelApp Australia and the Genomics England Instance of PanelApp and fix some errors when dealing with outlyer panels. Resultingly, this version replaces the version listed in the PanelApp-Pipeline.

**If you want jump right into running each of the scripts, please check out these links **

- [Running PADA-WAN](#running-pada-wan)
  - [Download IDs](#1-1-Download-IDs)
  - [Download Panels](#1-2-Download-Panels)
  - [Summarise Panels](#13-Summarise-Panels)
  - [Determine How Genes Change](#21-Download-Panels)
  - [Determine The Cumulative Gene Changes](#23-Download-Panels)


# PADA-WAN Overview 
 
 PADA-WAN is made of two parts. 
 
 ***Part 1*** is responsible for downloading and summarising the information from PanelApp
 
 ***Part 2*** focuses on characterising change and an option set of R scripts makes it possible to visualise these changes

An overview of PADA-WAN can be seen in Figure 1 and Figure 2.

![image](https://github.com/MedicalGenomicsLab/Vigelint/assets/15273099/29cf14e9-5a12-4b3b-8755-1e55c1f593ff)

![image](https://github.com/MedicalGenomicsLab/Vigelint/assets/15273099/cec928ed-48c7-44c9-969d-cc8890732f82)


---
# Setting up PADA-WAN 

This section describes 

- [System requirements](#system-requirements)
  - [Python dependencies](#python-dependencies)
  - [R dependencies](#r-dependencies)
  - [PanelApp Tokens](#panelapp-tokens)


# System requirements

PADA-WAN requires Python/3.9.13, and R/4.2.0 .

PADA-WAN has been tested on a local, desktop computer (MacOS 13.3.1) and a cluster computer running qsun.

## Python dependencies
- pandas 1.1.5
- numpy 1.19.5
- argparse
- requests
- datetime
- re (will not require pip to install)
- time (will not require pip to install)

## R dependencies
- ggplot2
- readxl
- tidyr
- stringr

## PanelApp Tokens

In order to connect to PanelApp and PanelApp Australia API, you will need to get a token. These tokens are needed for Scripts 1-1, and 1-2.
While the example scripts, contain a working PanelApp and PanelApp Australia token, it is best practice to get your own tokens.

***PanelApp Australia Token*** 
1. Navigate to: https://panelapp.agha.umccr.org/api/docs/

2. Under panels, select 'Get'
![Screenshot 2024-02-27 at 9 14 07 am](https://github.com/MedicalGenomicsLab/Vigelint/assets/15273099/523f25d5-1127-405d-a120-6895382945ef)

3. Click the 'Try it out' button
![Screenshot 2024-02-27 at 9 14 24 am](https://github.com/MedicalGenomicsLab/Vigelint/assets/15273099/945081a8-0b8e-4b31-b5e7-de3f993edd45)

4. Click the large button labelled execute
![Screenshot 2024-02-27 at 9 14 41 am](https://github.com/MedicalGenomicsLab/Vigelint/assets/15273099/33bb9991-6fa2-4761-ab24-b8b777b7d676)

5. In the black text box, copy the long string of text named X-CSRFToken
![Screenshot 2024-02-27 at 9 14 57 am](https://github.com/MedicalGenomicsLab/Vigelint/assets/15273099/3b6cb859-9403-4eef-98d3-77c895751f34)

6. Paste the text into the params file, if the last character is a quotation mark, you can remove it

***Obtainign the token for the Genomics England instance of PanelApp*** 

This process is largely the same as the process of PanelApp Australia described above, however, there are some subtle differences.

1. Navigate to: https://panelapp.genomicsengland.co.uk/api/docs/

2. When copying the token from the black text box, the output will look slightly different, but it contains the same information.
![Screenshot 2024-02-27 at 9 19 51 am](https://github.com/MedicalGenomicsLab/Vigelint/assets/15273099/2bd433d1-b841-4d40-95a2-778b043dddba)


# Running PADA-WAN

This section decribes the steps involved in running each of the scripts that make up the PADA-WAN pipeline, as well as the information that's described in each of the parameters files.
 
## 1-1 Download IDs

The first script in the PADA-WAN pipeline queries the PanelApp API to retrieve a list containing all available panels. In addition to this informaiton, this script also collects information about each panel’s numeric panel-ID, and super panel / rare-disease status. Information about the most current version, the date of release of this version and the number of genetic entities are also downloaded. 

This script has been updated to support both the PanelApp Australia, and the Genomics England Instance of Panel App 

This script requires a parameters file, which contains information about the version of PanelApp to query, as well as the the input / output directories. The parameter file also contains the token files for both PanelApp Australia and Genomics England instance of PanelApp. You can replace the example token files in this file by following the steps above.

***The Parameters File***

An example of the parameter file can be found in /PADA-WAN/1-1 Download IDS/ as _1-1_params.txt_
This parameters file contains the following information:
1. **INDIVIDUAL_RUN**:   [either 'AU' or 'UK'] - this value tells the script which version of PanelApp to download the IDs from
2. **OUT-DIRAU:**        [location] - this value defines where the output from this script is stored
3. **PATH_AU:**          _https://panelapp.agha.umccr.org/api/v1/panels/?page=_  - this is the address of PanelApp Australia - you should _not_ need to change this
4. **TOKEN_AU:**         LytbzDyWsuzun1ScDq2tvYd1RA4e4zQdrbvnSmmpfjsmOqAaPk5hD8KFJtO1vqUr - this is token for PanelApp Australia - you _should_ change this - see the method above for advice
5. **OUT-DIRUK:**        [location] - this value defines where the output from this script is stored
6. **PATH_UK:**          https://panelapp.genomicsengland.co.uk/api/v1/panels/?page= - this is the address of PanelApp UK  - you should _not_ need to change this
7. **TOKEN_UK:**         VpObfRKKvsvhH0Fzq5cgb37JWyMKIn11f7U8lhO2U4IpjnXJpa2qmCtog9c8Nej7 - this is token for PanelApp UK - you _should_ change this - see the method above for advice

***Running the script***

  To run this script use the following commands:

    python3 1-1_DownladIDs.py --file-path parameters_file.txt

If run correctly it will produce a .tsv file containing information for each panel in the PanelApp of your choice.

_Notes on the 1-1 params file_
Note: When preparing the parameters file, please ensure that there is no trailing white space, as this can cause issues


## 1-2 Download Panels

This script takes each of the panels in the listed in the output file from the Download IDs script (1.1,) and uses this information to download begin to download individual panels from the PanelApp / PanelApp Australia API. 

***The Parameters File***
1. **PANELAPP_VERSN:**    [either 'AU' or 'UK'] - this value tells the script which version of PanelApp to download the IDs from
2. **ID_LOCATION:**       [location/name_of_id_file_from_1-1.tsv] - this value tells where the ID file you downloaded using 1-1_Download IDS is
3. **OUT-DIRAU:**        [location] - this value defines where the output from **PanelApp** is stored, it _should_ be different from the ID folder
3. **PATH_AU:**          _https://panelapp.agha.umccr.org/api/v1/panels/?page=_  - this is the address of PanelApp Australia - you should _not_ need to change this
4. **TOKEN_AU:**         LytbzDyWsuzun1ScDq2tvYd1RA4e4zQdrbvnSmmpfjsmOqAaPk5hD8KFJtO1vqUr - this is token for PanelApp Australia - you _should_ change this - see the method above for advice
5. **OUT-DIRUK:**        [location] - this value defines where the output from **PanelApp** is stored, it _should_ be different from the ID folder
6. **PATH_UK:**          https://panelapp.genomicsengland.co.uk/api/v1/panels/?page= - this is the address of PanelApp UK  - you should _not_ need to change this
7. **TOKEN_UK:**         VpObfRKKvsvhH0Fzq5cgb37JWyMKIn11f7U8lhO2U4IpjnXJpa2qmCtog9c8Nej7 - this is token for PanelApp UK - you _should_ change this - see the method above for advice
  
Two examples of the parameter files can be found in /PADA-WAN/1-2 Download Panels/Example_ID-Files/. This folder contains ID files used to download epilepsy panels (EPIL.tsv) from both PanelApp Aus and UK, as well as ID files designed to test if this script is working properly (TEST.tsv)

_***Notes on the ID file***_

1. The ID file we produced in step 1-1 is critical to this script. However are a few things to note - editting the ID file means that you can remove panels you do not wish to download, this is how we created the smaller, example test ID  files in the Examples folders
2. **NOTE - ID location should match the Version of PanelApp - trying to download Australian Panels, using the English version of PanelApp will only result in heartache (and errors)**

***Running the script***

  To run this script use the following commands:

    python3 1-2_PanelDownloader.py --file-path parameters_file.txt

***Notes on this script***

There are some things to note about this approach:

1. As PanelApp uses both minor and major releases, and there is a large in the number of minor releases before a major release we developed a system to accoutn for this variability. To ensure that that every possible version of a panel was downloaded, this script systematically attempt to download every version from 0.0 until the current release.If a specific minor version of this panel was not available, the script skips it and attempts to download the next minor release of the panel. If the script was unable to download ten consecutive minor versions of panel, the script assumes that there are no more minor releases associated with this major version, and moves to next major release of the panel. If the script failed to download the version of the panel listed in the ID file, a warning file is produced.
2. In addition to processing every available version of a panel, this script also produces a summary file, that contains the number of genes as well as the total number of genes in a specific version of panel.
3. As the information from PanelApp is stored in the JSON format, it can be challenging for people to access this information.To make this information more accessible, it is stored here as a tab delimited text file.
4. When preparing the parameters file, please ensure that there is no trailing white space.
5. As downloading every version of every panel from PanelApp can take a significant amount of time, to facilitate testing we have provided an ID file that only contains a small number of panels to download. These files have been generated for PanelApp and PanelApp Australia and can be found in 1-2 Download Panels/Example_ID-Files.
6. This script was developed in Australia, and during testing, we found that requesting data from the Genomics England version of PanelApp would occassionally time out. Despite a generous retry time limit, this issue persisted. Restarting the script addresses this issue. While this issue is likely due to the ~16,000km between the PanelApp server and the requesting computing, we highlight this issue incase people in Europe run into issues when trying to download data from PanelApp Australia.


## 13 - Summarise-Panels

The third script opens the summary file produced by the second script, and, identifies the specific version of a panel present one last day of each month. It produces a monthly summary file for each panel downloaded by script 1.2, that only shows 1 version of the panel for each month. This output from this script is very important to the following analyses. This script has been updated to automatically produce plots showing the number of genes and diagnostic genes each month of the analysis window.

***The Parameters File***

This script also requires a parameters file. This file contains the location the files produced by 1.2, as well as the information needed to plot the information in the monthly summaries.
The information in the parameters file are as follows:

1. **VERSION:**         [either 'AU' or 'UK']
2. **INPUT_DIR:**       [directory location] - Location of the raw panel data
3. **OUTPUTDIR:**       [directory location] - Location of the processed panel data
4. **ID_DATE:**         [YYYY,MM,DD] - When was the ID file generated
5. **STARTDLDATE:**     [YYYY,MM,DD] - When were raw panels begin downloading
6. **ENDDLDATE:**       [YYYY,MM,DD] - When did the downloading of the panels finish
7. **ANALYSIS_DATE:**   [YYYY,MM,DD] - When does this analysis take place?
8. **PLOT_DIR:**        [directory location] - where should the plots go?

**An example of the parameter file can be found in /PADA-WAN/1-3 Summarise Panels/**

  _Notes on 1-3_
1. When preparing the parameters file, please ensure that there is no trailing white space.
2. It is not required to plot the monthly changes, but I find it to be helpful

***Running the scripts***

  To run these scripts use the following commands:

    python3 1-3_SummarisePanels.py --file-path parameters_file.txt
    Rscript PlotMonthlyChanges.R [DIRECTORY CONTAIN MONTHLY SUMMARIES] [DIRECTORY FOR PLOTS]

## 1.4 - Panel Factoriser 

The matrices script, opens the monthly summary file for each panel and combines this information into a matrix for a specific variable (no. of releases, no. of genes, no. of diagnostic genes, etc). For example, this script produces an output file that shows number of releases there was been for each panel, over the space of each month.

This script also requires a parameters file. An example of the parameter file can be found in /PADA-WAN/1-4 Panel Factoriser/

***The Parameters File***

1. **EXP_NAME:**      [Name of your experiment]
2. **VERSION:**	      [either 'AU' or 'UK']
3. **INPUT_DIR:**	    [directory location]
4. **OUTPUTDIR**:	    [directory location]
5. **ID_DATE:**	      [YYYY,MM,DD] - When was the ID file generated
6. **STARTDLDATE:**	  [YYYY,MM,DD] - When were raw panels begin downloading
7. **ENDDLDATE:**	    [YYYY,MM,DD] - When did the downloading of the panels finish
8. **ANALYSIS_DATE:** [YYYY,MM,DD] - When does this analysis take place?

***Running the scripts***

  To run this script use the following commands:

    python3 1-4_FactorisePanels.py --file-path parameters_file.txt
    
_Notes on 1-4_
This script is not required for the Vigilent Pipeline, however it has been included here, because the prior 'PanelApp Pipeline' has been superseeded by this version of the tools.
    

## 21 - Characterise Gene Changes

This script determines the genes that have been added to, and removed from a panel, as well as the genes that have been upgraded to and downgraded from diagnostic status. This script has been upgraded to list the individual genes that have been changed, instead of just determining the number of gene changes. Thanks to those who highlighted this oversight.

***The Parameters File***

1. **EXP_NAME**:	        [Name of your experiment]
2. **VERSION**:	          [either 'AU' or 'UK']
3. **OUTPUTDIR**:	        [directory location]
4. **START_DATE**:	      [YYYY,MM,DD]
5. **END_DATE**:	        [YYYY,MM,DD]
6. **ID_LOCATION**:	      [directory location]
7. **ID_FILE**:	          [name of ID file]
8. **MONTHLY_LOC**:	      [directory location]
9. **PANEL_LOC**:	        [directory location]
10. **ANALYSIS_DATE**:    [YYYY,MM,DD]

***Running the scripts***

  To run this script use the following commands:

    python3 2-1_DetermineChange.py --file-path parameters_file.txt

  This script also requires a parameters file. An example of the parameter file can be found in /PADA-WAN/2-1 Determine Gene Changes/

## 223 - Cumulative Gene Changes

This script determines the cumulative number of gene changes that occur each month of the analysis window. This script has been re-written from version 1.0 by combining 2.2 and 2.3 so that the Gene Changes are automatically ploted.

***The Parameters File***

1. **EXP_NAME:**	        [Name of your experiment]
2. **VERSION:**	          [either 'AU' or 'UK']
3. **INPUTDIR:**	        [directory location - Gene Changes]
4. **OUTPUTDIR:**	        [directory location - Cumulative Changes]
5. **PLOTDIR:**	          [directory location - plot]

***Running the scripts***

  To run this script use the following commands:

    python3 2-2_CumulativeChanges.py --file-path parameters_file.txt
    Rscript PlotChanges.R [DIRECTORY CONTAIN MONTHLY SUMMARIES] [DIRECTORY FOR PLOTS]

  An example of the parameter file can be found in /PADA-WAN/2-2 Cumulative Changes/ - however, there should not be any trailing white space characters after the values of importance.
    
_____



