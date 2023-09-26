# CVPO PLOTS

This document describes how to generate a plot from the output of CVPO. This plot will show the number of PLP variants and the number of VUS in each month of the analysis window, while also showing the total number of alleles in ClinVar (less the no. PLP + VUS). This plot is similar to the plot shown in Robertson et al (2023). An example of this plot is shown below.

[Figure 1]


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
