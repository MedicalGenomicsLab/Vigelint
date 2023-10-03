#Static Gene List Revised

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

location = args[1]
#location = "Downloads/"

input_file  = args[2]
#input_file = "JEDI-PRODUCTION-TEST-full.txt"

input = paste(location, input_file, sep='')

top_genes = args[3]
top_genes <- as.numeric(top_genes)
#top_genes <- 5

time_snapshot = args[5]
exp_name = args[4]

#########################################################################
#Ingest file for plotting
#########################################################################

ingest <- read.csv(input, sep="\t", header=TRUE)
df_temp <- data.frame(ingest)

#########################################################################
#Data transformation 
#########################################################################

df <- subset(df_temp, select = -c(ENSG.SYMBOL, ENSG.ID_y, STATUS))  # remove additional columns
df<- df[!(is.na(df[,4])), ] # remove if line is empty

#to focus on the plp make a new df only contaning this information 
df_plp_genelist <- df[ , grepl( "plp" , names( df ) ) ] 
df_plp_names <- df$NCBI.SYM
df_plp_var <- merge(df_plp_names, df_plp_genelist, by = 'row.names', all = TRUE)
df_plp_var <- df_plp_var[,-1] 
colnames(df_plp_var)[1] <- "Symbol"

#sort the data by panels that have the most number of variants in the last month of the analysis window 
df_plp_var <- df_plp_var %>% arrange(desc(.[ncol(.)]))

#extract and transform the top x no. of genes 
df_plp_head <- head(df_plp_var, n=top_genes)
plot_df <- t(df_plp_head)
plot_df <- as.data.frame(plot_df, header=TRUE, stringsAsFactors = FALSE)
names(plot_df) <- lapply(plot_df[1, ], as.character)
symbols <- plot_df[1, ]
plot_df <- plot_df[-1,] 

#transmute data into meaningful form
plot_df$row_names <- row.names(plot_df)
plot_df <- plot_df %>% separate(row_names, c('Year', 'Month', 'Class'))
plot_df$period <- paste(plot_df$Year,plot_df$Month)
plot_df$period <- gsub("X", "", as.character(plot_df$period))  
plot_df$period <- gsub(" ", "-", as.character(plot_df$period))
plot_df$period <- as.yearmon(plot_df$period, "%Y-%m")
plot_df <- plot_df %>%select(period, everything())
plot_df <- plot_df[1:(length(plot_df)-3)]

#define columns that contain gene data
positions <- c(2:(top_genes+1))
# ensure all gene columns have numeric data
test_df <- plot_df %>% mutate_at(c(positions), as.numeric)
rownames(test_df)<-NULL

test_df1 <- test_df 
colnames(test_df1)[1] ="0"

#transform data
df_test3 <- test_df1 %>% pivot_longer(cols=matches("[A-Z]"),
                                      names_to='Genes',
                                      values_to='PLP Variants')

#rename data
colnames(df_test3)[1] ="Month"
colnames(df_test3)[2] ="Genes"
colnames(df_test3)[3] ="Variants"

#########################################################################
#plot data
#########################################################################

ggplot(data=df_test3, aes(x=Month, y=Variants, group=Genes)) + 
  geom_line(aes(linetype=Genes, color=Genes)) +
  theme_light() + theme(text = element_text(size = 5), panel.grid.minor.x= element_blank(), panel.grid.major.x= element_blank(), legend.position = "right") + 
  ylab("No. P/LP Variants") +
  xlab("Date (Years)")

out_file = paste(time_snapshot,"-",exp_name,".pdf", sep="")

#Save
ggsave(out_file, plot= last_plot(), path=location, width = 120, height = 80, units = "mm", dpi = 1000)

