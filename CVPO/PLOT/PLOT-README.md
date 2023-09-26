# CVPO PLOTS

This document describes how to generate a plot from the output of CVPO. This plot will show the number of PLP variants and the number of VUS in each month of the analysis window, while also showing the total number of alleles in ClinVar (less the no. PLP + VUS). This plot is similar to the plot shown in Robertson et al (2023). An example of this plot is shown below.

![image](https://github.com/MedicalGenomicsLab/Vigelint/assets/15273099/bd87a95f-c19a-4ed0-9cce-89204d2977b7)


## Making the plots

**Requirements**

* R
	* ggplot2
	* zoo
	* dplyr
	* tidyr

**Running CVPO**

CVPO is run using the following command.

    Rscript PlotChangesInClinVar.R [location of the matrixes produced by CVPO] [name of the "full" CVPO matrix] [Experiment Name]
