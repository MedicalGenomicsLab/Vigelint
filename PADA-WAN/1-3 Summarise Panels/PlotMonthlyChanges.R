##########################################################################
# set up libraries
#########################################################################

library(ggplot2)
library(readxl)
library(tidyr)
library(stringr)

#########################################################################
#ARG revised
#########################################################################
args = commandArgs(trailingOnly=TRUE)
if (length(args)==0) {stop("At least one argument must be supplied (input file).n", call.=FALSE)}

location = args[1]
out_loc = args[2]

#########################################################################
#For each file in this folder
#########################################################################

files <- list.files(path=location, pattern="*.txt", full.names=TRUE, recursive=FALSE)

lapply(files, function(x) {
  #y <- str_split(x,'//')
  #z <- y[[1]][[2]]
  y <- strsplit(x,split = '/')
  z <- y[[1]][[9]]
  panel_title_temp <- str_split(z,'-M')
  panel_name <- panel_title_temp[[1]][[1]]
  panel_title <- gsub("_", " ", panel_name)
  panel_title <- gsub("AU ", "PanelApp Aus - ", panel_title)
  panel_title <- gsub("UK ", "PanelApp GEL - ", panel_title)

  #message("test\t", panel_title)
  
  t <- read.table(x, sep="\t", header = TRUE)
  
  df_production <- data.frame(t)
  df_plot <- df_production[,c("Period","No.Genes","No.DiaGenes")]
  
  df_plot[df_plot == "N/A"] <- "NA"
  
  #ensure that the columns are in the correct format 
  df_plot$Period <- as.Date(df_production$Period, format = "%Y-%m-%d")
  df_plot$No.Genes <- as.numeric(df_plot$No.Genes)
  df_plot$No.DiaGenes <- as.numeric(df_plot$No.DiaGenes)
  colnames(df_plot)[2] ="No. of Genes"
  colnames(df_plot)[3] ="No. of Diagnostic Genes"
  
  df_plot <- df_plot %>% pivot_longer(cols=c('No. of Genes', 'No. of Diagnostic Genes'),
                                      names_to='Class',
                                      values_to='PanelChanges')
  
  ggplot(data=df_plot, aes(x=Period, y=PanelChanges, group=Class)) + 
    geom_line(aes(linetype=Class, color=Class)) +
    scale_linetype_manual(values=c("solid", "solid")) + 
    scale_color_manual(values=c("#00843D", "#291200")) + 
    theme_light() + theme(text = element_text(size = 5), panel.grid.minor.x= element_blank(), panel.grid.major.x= element_blank(), legend.position = "bottom") + 
    ylab("No. Genes") +
    xlab("Date (Years)") +
    ggtitle(panel_title) + 
    theme(plot.title = element_text(hjust = 0.5)) + 
    theme(plot.title = element_text(face = "bold"))
  
  out_name <- paste("Monthly_Summary-", panel_name,".pdf",sep="",collapse=NULL)
  
  ggsave(out_name, plot= last_plot(), path=out_loc, width = 160, height = 90, units = "mm", dpi = 1000)
  
  }
)
