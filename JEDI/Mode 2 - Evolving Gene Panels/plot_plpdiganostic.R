#Plot the evolving gene panels 

##########################################################################
# set up libraries
#########################################################################

library(ggplot2)
library(zoo)
library(dplyr)
library(tidyr)
library(stringr)

#########################################################################
#ARG revised
#########################################################################

args = commandArgs(trailingOnly=TRUE)
if (length(args)==0) {stop("At least one argument must be supplied (input file).n", call.=FALSE)}

id_location = args[1]
id_file = args[2]
panel_file = paste(id_location, id_file, sep='/')
input_loc = args[3]
panel_source = args[4]
out_loc= args[5]
message(panel_source)

message("ARGS1 = ID LOCATION:\t", id_location)
message("ARGS2 = ID FILE:\t", id_file)
message("ARGS3 = INPUT LOC:\t", input_loc)
message("ARGS4 = PANEL SOURCE:\t", panel_source)
message("ARGS5 = OUT LOC:\t", out_loc)

Sys.sleep(1)

ids <- read.csv(panel_file, sep="\t", header=TRUE, stringsAsFactors=FALSE)

pans <- as.list(ids$Panel)
identifer <- as.list(ids$ID)
additional_text <- paste('-',panel_source,'_VariantsInPanels_MonthlySummary.txt',sep='')

#########################################################################
# For each panel in the ID file
#########################################################################

for(i in 1:nrow(ids)) {      
  panel_name <- ids$Panel[i]
  message('Starting Analysis of ', panel_name, sep=" ")
  Sys.sleep(1)
  panel_file_temp_1 <- gsub(" ", "_", panel_name)
  panel_file_temp_2 = str_split(panel_file_temp_1,'[(]')
  panel_file <- panel_file_temp_2[[1]][1]
  panel_file <- gsub("/", "--", panel_file)
  panel_ident <- ids$ID[i]
  individual_file <- paste(panel_file,'(',panel_ident,')',additional_text,sep='')
  each_file <- paste(input_loc,"/" ,individual_file,sep = '') 
  ingest <- read.csv(each_file, sep="\t", header=TRUE, stringsAsFactors=FALSE)

  #Sys.sleep(1)
	
  title_1 = paste("The monthly changes in the number of P/LP variants in the diagnostic genes from the ", panel_name, " panel", sep='')
  title_2 = paste("The number of diagnostic genes in the ", panel_name, " panel each month", sep='')
  
#########################################################################
#Ingest file for plotting
#########################################################################
  
  #ingest <- read.csv(plot_file, sep="\t", header=TRUE)
  df <- data.frame(ingest)
  df$Date <- as.Date(df$Date, format = "%Y-%m-%d")
  df$MatchedDiagnosticGenes <- as.numeric(df$MatchedDiagnosticGenes)
  df$PLPInDiagnosticGenes <- as.numeric(df$PLPInDiagnosticGenes)
  message(df$Date[1])
  Sys.sleep(1)

#########################################################################
# Plot P/LP variants in diagnostic genes 
#########################################################################
  
  ggplot(df, aes(x=Date, y=PLPInDiagnosticGenes, group=1, colour='')) +
    ylab("No. P/LP Variants in Diagnostic Genes") +
    xlab("Date (Years)") +
    theme_linedraw() + theme(text = element_text(size = 5)) +
    theme(legend.position = "bottom") +
    theme(panel.grid.minor = element_blank()) +
    geom_line(aes(y=PLPInDiagnosticGenes), color=c("#00843D"), linetype="solid") +
    ggtitle(title_1)  + 
    theme(plot.title = element_text(hjust = 0.5)) + 
    theme(plot.title = element_text(face = "bold"))
 
  message(panel_file)
  out_put_name = paste(panel_file,'_MonthlyDiagnosticPLPChanges.pdf', sep=' ')
  
#Save
  ggsave(out_put_name, plot= last_plot(), path=out_loc, width = 120, height = 80, units = "mm", dpi = 1000)
  
  
#########################################################################
# Plot  diagnostic genes 
#########################################################################
 
#  ggplot(df, aes(x=Date, y=PLPInDiagnosticGenes, group=1, colour='')) +
#    ylab("No. Diagnostic Genes") +
#    xlab("Date (Years)") +
#    theme_linedraw() + theme(text = element_text(size = 5)) +
#    theme(legend.position = "bottom") +
#    theme(panel.grid.minor = element_blank()) +
#    geom_line(aes(y=MatchedDiagnosticGenes), color=c("#00843D"), linetype="dashed") +
#    ggtitle(title_2) + 
#    theme(plot.title = element_text(hjust = 0.5)) + 
#    theme(plot.title = element_text(face = "bold"))
  
#  out_put_name = paste(panel_file,'_MonthlyDiagnosticGeneChanges.pdf', sep='')
  
#Save
#  ggsave(out_put_name, plot= last_plot(), path=out_loc, width = 120, height = 80, units = "mm", dpi = 1000)  

}
