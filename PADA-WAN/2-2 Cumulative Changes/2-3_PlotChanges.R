#PADA-WAN Revised

##########################################################################
# set up libraries
#########################################################################

library(ggplot2)
library(readxl)
library(tidyr)

#########################################################################
#ARG revised
#########################################################################

args = commandArgs(trailingOnly=TRUE)
if (length(args)==0) {stop("At least one argument must be supplied (input file).n", call.=FALSE)}

location = args[1]
out_dir = args[2]

#########################################################################
#For each file in this folder
#########################################################################

files <- list.files(path=location, pattern="*.txt", full.names=TRUE, recursive=FALSE)

lapply(files, function(x) {
  #read each file in a specific way so that I can attract the panel ID without messing out the header
  temp <- read.table(x, sep="\t", fill=TRUE, header = FALSE)
  Panel_ID <- temp[1,2]
  Panel_title <- gsub("_", " ", Panel_ID)
  print(Panel_title)
 
  #re-read file to preserve header
  t <- read.table(x, sep="\t", skip = 1, header = TRUE)
  
  #prepare for plotting 
  df_production <- data.frame(t)
  df_plot <- df_production[,c("Month","No.DiaGenes", "DiaGene.Gains.Cumulative.","DiaGene.Losses.Cumulative.")]
  
  #make gene losses more apparent 
  df_plot[4] <- df_plot[4]/-1

  #ensure that the columns are in the correct format 
  df_plot$Month <- as.Date(df_production$Month, format = "%Y-%m-%d")
  colnames(df_plot)[2] ="No. of Diagnostic Genes"
  colnames(df_plot)[3] ="No. of Diagnostic Genes Gained"
  colnames(df_plot)[4] ="No. of Diagnostic Genes Lost"
  
  #transform data
  df_plot <- df_plot %>% pivot_longer(cols=c('No. of Diagnostic Genes', 'No. of Diagnostic Genes Gained', 'No. of Diagnostic Genes Lost'),
                                      names_to='Class',
                                      values_to='GeneChanges')
  
  #plot the data
  ggplot(data=df_plot, aes(x=Month, y=GeneChanges, group=Class)) + 
    geom_line(aes(linetype=Class, color=Class)) + 
    scale_linetype_manual(values=c("solid", "dashed", "dashed")) + 
    scale_color_manual(values=c("#00843D","#04395E","#C73E1D")) +
    theme_light() + theme(text = element_text(size = 5), panel.grid.minor.x= element_blank(), panel.grid.major.x= element_blank(), legend.position = "bottom") + 
    ylab("No. Genes") +
    xlab("Date (Years)") +
    ggtitle(Panel_title) + 
    theme(plot.title = element_text(hjust = 0.5)) +
    theme(plot.title = element_text(face = "bold"))
 
  #prepare output 
  out_name <- paste("Gene_Evolution-",Panel_ID,".pdf",sep="",collapse=NULL)
  out_name
  
  #save output 
  ggsave(out_name, plot= last_plot(), path=out_dir, width = 160, height = 90, units = "mm", dpi = 1000)
  }
)
