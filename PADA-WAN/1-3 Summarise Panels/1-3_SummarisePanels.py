##############################
#
# CONDENSE EVERY VERSION OF A PANEL INTO A MONTHLY BREAKDOWN
#
##############################

# Introduction
# There are a lot of different versions of panel in PanelApp, like tens of thousands of them
# So in order to find meaning in this sea of data, this script was written to find the last panel released each month , and compare this to the month proceeding

# Alan Robertson
# 2022-01-25

# VERSION 1.0
# 2022-05-02 - PRODUCTIONISE SCRIPT

# Version 1.1
# 2023-09-27 - optimise for Vigelent pipleline 
# To do: tidy up params file 

###############################
#Load the modules
import argparse
import os
import re
import datetime
import time
from datetime import date
from dateutil.relativedelta import relativedelta
import pandas as pd
import numpy as np

#IMPORT INFORMATION FROM THE PARAMS FILE
#Define main function
def main(file_path: str):
	parameters_df = pd.read_csv(file_path,sep="\t")
	temp_00 = parameters_df.iloc[0,1]
	temp_01 = parameters_df.iloc[1,1]
	temp_02 = parameters_df.iloc[2,1]
	temp_03 = parameters_df.iloc[3,1]
	temp_04 = parameters_df.iloc[4,1]
	temp_05 = parameters_df.iloc[5,1]
	return(temp_01, temp_02, temp_03, temp_04, temp_05, temp_00 )	

#Excute the code to actually import the params file and extract the key values 
if __name__ == "__main__":
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument("--file-path", type=str, required=True, help="Path to parameter file")
	args, unknowns = parser.parse_known_args()
	file_path = args.file_path

	#extract variables from params file and put into correct format      
	the_returned = main(file_path)
	in_dir = the_returned[0]
	outdir = the_returned[1]
	id_date = the_returned[2]
	start_dl = the_returned[3]
	end_dl = the_returned[4]
	#version = the_returned[5]
	
	#ensure dates are in correct format
	temp = re.split(r',', id_date)
	id_date_y = int(temp[0])
	id_date_m = int(temp[1])
	id_date_d = int(temp[2])
	temp = re.split(r',', start_dl)
	start_dl_y = int(temp[0])
	start_dl_m = int(temp[1])
	start_dl_d = int(temp[2])	
	temp = re.split(r',', end_dl)
	end_dl_y = int(temp[0])
	end_dl_m = int(temp[1])
	end_dl_d = int(temp[2])
	
#Setup Variables
id_date = datetime.date(id_date_y,id_date_m, id_date_d)			#When was ID file downloaded?
download_start = datetime.date(start_dl_y,start_dl_m, start_dl_d)		#When did the panel begin downloading?
download_end = datetime.date(end_dl_y,end_dl_m, end_dl_d)			#When did the panel finsh downloading?
#version_x = "%s_" % (version)

################
# For each panel
# Open file and extract the condition name, and ID
###############

for directory, subdirectories, files in os.walk(in_dir):
	for file in files:
		if file.endswith('.txt'):	
			condition_raw = re.split(r'Total_Summary', file)
			condition_raw1 = re.split(r'_', condition_raw[0])	
			version = condition_raw1[0]
			version_x = "%s_" % (version)
			condition_raw1 = re.split(version_x, condition_raw[0])	
			condition_raw2 = re.split(r'\(', condition_raw1[1])
			condition = condition_raw2[0]	
			condition_raw3 = re.split(r'\)', condition_raw2[1])
			if condition_raw3[0].isdigit():
				ID = condition_raw3[0]
			else:
				condition_raw4 = re.split(r'\)', condition_raw2[2])
				ID = condition_raw4[0]
			print(condition,ID)


################
# Condense for the end of each month
# While still in each file
###############

			#Determine the start date for each 
			if re.search(r"AU", version, re.IGNORECASE):			
				start_date = datetime.date(2019, 10, 1)
			elif re.search(r"UK", version, re.IGNORECASE):
				start_date = datetime.date(2017, 1, 1)
			current_date = start_date

			end_date0 = date.today()
			end_date = end_date0 + relativedelta(months=0)
			last_date = datetime.date(2019, 10, 31)  # start date minus one month
			y_delta = datetime.timedelta(days=1)

			carry_over = "N/A"
			hold_over = "N/A\tN/A(N/A)\tN/A\tN/A\tN/A\tN/A\tN/A\tN/A\tN/A\tN/A"
			counter = 1
			output_dict = {}

###############
#Actually open the file
###############
			while current_date <= end_date:
				this_month = current_date - y_delta
				file0 = "%s/%s" % (in_dir,file)
				file1 = open(file0, "r")

				for line in file1:
					line1 = re.split(r'\t+', line)
					version_id_str0 = str(line1[0])
					if version_id_str0 == "PanelName(PanelID)":
						continue
					version_id_str = str(line1[3])
					raw_timestamp = line1[2]
					test_inter = re.split(' ', raw_timestamp)
					version_dateraw = test_inter[1]
					version_year = int(re.split("-", version_dateraw)[0])
					version_month = int(re.split("-", version_dateraw)[1])
					version_day = int(re.split("-", version_dateraw)[2])
					version_date = datetime.date(version_year, version_month, version_day)
					version_time = test_inter[1]
					
					gene_count = line1[6]
					diagene_count = line1[7]
					str_count = line1[8]
					diastr_count = line1[9]
					region_count = line1[10]
					diaregion_count = line1[11]
					diaregion_count = diaregion_count.replace('\n', '')

					if last_date < version_date <= this_month:
						output_dict[this_month] = ("%s\t%s(%s)\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s") % (
						counter, version_id_str, version_date, line1[4], line1[5], gene_count, diagene_count, str_count, diastr_count, region_count, diaregion_count)
						hold_over = ("0\t%s(%s)\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s") % (
						version_id_str, version_date, line1[4], line1[5], gene_count, diagene_count, str_count, diastr_count, region_count, diaregion_count)
						counter = counter + 1

					if counter == 1:
						output_dict[this_month] = hold_over

			# prepare for next cycle
				current_date = current_date + relativedelta(months=+1)
				last_date = this_month
				counter = 1
				file1.close()

##########
# Part Two
##########

# print the output
		output_file = "%s/%s_%s(%s)-Monthly_Summary.txt" %(outdir, version, condition, ID)
		file_001 = open(output_file, "w+")
		head = "Period\tReleases\tLast-Release(Date)\tNo.Ent\tNo.DiaEnt\tNo.Genes\tNo.DiaGenes\tNo.Repeats\tNo.DiaRepeats\tNo.CNVs\tNo.DiaCNVs"
		print(head, file=file_001)
		for k,v in output_dict.items():
			print(k, "\t", v, file=file_001)
			#print(k, "\t", v)
		print("NOTE: The summary of information that's described as", last_date, "was determined on", end_date0, "using IDs downloaded on", id_date, " Data was downloaded between", download_start,"and",download_end, file=file_001)


