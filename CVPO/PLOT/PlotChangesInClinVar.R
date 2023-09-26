#CVPO Revised

##########################################################################
# set up libraries
#########################################################################

library(ggplot2)
library(zoo)
library(dplyr)
library(tidyr)

#########################################################################
#ARG revised
#########################################################################

args = commandArgs(trailingOnly=TRUE)
if (length(args)==0) {stop("At least one argument must be supplied (input file).n", call.=FALSE)}

#location = "/working/lab_nicw/alanR/"
location = args[1]

#input_file = "APRIL-2023_CLINVAR-full-matirx.txt"
input_file  = args[2]

#time_snapshot = "2023-04"
time_snapshot = args[3]

input = paste(location, input_file, sep='')

#########################################################################
#Ingest file for plotting
#########################################################################

ingest <- read.csv(input, sep="\t", header=TRUE)
df <- data.frame(ingest)

#########################################################################
#Data transformation 
#########################################################################

#df <- subset(df_temp, select = -c(ENSG.SYMBOL, ENSG.ID_y, STATUS))  # remove additional columns
df[is.na(df)] <- 0

#seperate data types
df_all_temp <- df[ , grepl( "all" , names( df ) ) ] # seperate into types
df_vus_temp <- df[ , grepl( "vus" , names( df ) ) ] 
df_plp_temp <- df[ , grepl( "plp" , names( df ) ) ] 

#determine total no. of variants for each month 
temp_all <- colSums(df_all_temp[,-1])
temp_vus<- colSums(df_vus_temp[,-1])
temp_plp <- colSums(df_plp_temp[,-1])

#########################################################################
#For each type of variant
#########################################################################

df_all <- data.frame(temp_all)
df_all$row_names <- row.names(df_all)
df_all <- df_all %>% separate(row_names, c('Year', 'Month', 'Class'))
df_all$period <- paste(df_all$Year,df_all$Month)
df_all$period <- gsub("X", "", as.character(df_all$period))  
df_all$period <- gsub(" ", "-", as.character(df_all$period))  
df_all$period <- as.yearmon(df_all$period, "%Y-%m")

df_all_plot <- data.frame(df_all$period, df_all$temp_all, df_all$Class)
colnames(df_all_plot)[1] ="Date"
colnames(df_all_plot)[2] ="Variants"
colnames(df_all_plot)[3] ="Class" 

#----

df_vus <- data.frame(temp_vus)
df_vus$row_names <- row.names(df_vus)
df_vus <- df_vus %>% separate(row_names, c('Year', 'Month', 'Class'))
df_vus$period <- paste(df_vus$Year,df_vus$Month)
df_vus$period <- gsub("X", "", as.character(df_vus$period))  
df_vus$period <- gsub(" ", "-", as.character(df_vus$period))  
df_vus$period <- as.yearmon(df_vus$period, "%Y-%m")

df_vus_plot <- data.frame(df_vus$period, df_vus$temp_vus, df_vus$Class)
colnames(df_vus_plot)[1] ="Date"
colnames(df_vus_plot)[2] ="Variants"
colnames(df_vus_plot)[3] ="Class" 

#----

df_plp <- data.frame(temp_plp)
df_plp$row_names <- row.names(df_plp)
df_plp <- df_plp %>% separate(row_names, c('Year', 'Month', 'Class'))
df_plp$period <- paste(df_plp$Year,df_plp$Month)
df_plp$period <- gsub("X", "", as.character(df_plp$period))  
df_plp$period <- gsub(" ", "-", as.character(df_plp$period))  
df_plp$period <- as.yearmon(df_plp$period, "%Y-%m")

df_plp_plot <- data.frame(df_plp$period, df_plp$temp_plp, df_plp$Class)
colnames(df_plp_plot)[1] ="Date"
colnames(df_plp_plot)[2] ="Variants"
colnames(df_plp_plot)[3] ="Class" 

#########################################################################
#Adjust the total number of variants, so that plp / vus aren't counted twice in plot
#########################################################################

#Minus the no. of vus and plp variants from the total number of variants
df_all_minus <- within(merge(df_all_plot,df_vus_plot,by="Date"), {Variants <- Variants.x - Variants.y})[,c("Date","Variants")]
df_all_minus <- within(merge(df_all_minus,df_plp_plot,by="Date"), {Variants <- Variants.x - Variants.y})[,c("Date","Variants")]
df_all_plot_modified <- df_all_plot
df_all_plot_modified$Variants <- df_all_minus$Variants

#reombine for plotting
df_combined_plot <- rbind(df_all_plot_modified, df_vus_plot, df_plp_plot)
df_combined_plot$Class <- gsub("all", "Total No. Variants", as.character(df_combined_plot$Class))
df_combined_plot$Class <- gsub("vus", "VUS", as.character(df_combined_plot$Class)) 
df_combined_plot$Class <- gsub("plp", "P/LP", as.character(df_combined_plot$Class)) 

#path
out_name = "ClinVarSummary"
out_file = paste(time_snapshot,"-",out_name,".pdf", sep="")

#labels
part_1 = "No. Variants in ClinVar ( "
part_2 = ")"
label = paste(part_1, time_snapshot, part_2, sep=" ")

#########################################################################
#Plot
#########################################################################

ggplot(df_combined_plot, aes(x=Date, y=Variants, fill = factor(Class, levels=c("Total No. Variants", "VUS", "P/LP")))) + 
  geom_bar(stat="identity") +
  scale_fill_manual(values=c("#6C698D", "#380036", "#8D0801")) +
  theme_linedraw() + theme(text = element_text(size = 5)) +
  theme(legend.position = "bottom") +
  theme(panel.grid.minor = element_blank()) +
  ylab(label) +
  xlab("Date (Months)") +
  theme(legend.title=element_blank()) +
  scale_y_continuous(labels = scales::comma)

#Save
ggsave(out_file, plot= last_plot(), path=location, width = 100, height = 80, units = "mm", dpi = 1000)




