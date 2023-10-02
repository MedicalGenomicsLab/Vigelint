##################################################
#
# DETERMINE CUMULATIVE CHANGES 
#
# i.e. how much change has occured between two time points
# or, how would we actually graph everything? 
#
##################################################

#This script has been designed to characterise the cumulative changes each month for a panel 

# Alan Robertson - Feburary 2022

# Version 0.1
# 2023-05-05 - PRODUCTIONISE

# Version 0.2
# 2023-09-07 - Refine to code to better support automatic figure generation  

###############################################

import os
import re
import time
import argparse
import pandas as pd

###############################################

#Define main function
def main(file_path: str):
	parameters_df = pd.read_csv(file_path,sep="\t")
	temp_name = parameters_df.iloc[0,1]
	temp_version = parameters_df.iloc[1,1]
	temp_indir = parameters_df.iloc[2,1]
	temp_outdir = parameters_df.iloc[3,1]
	return(temp_name, temp_version, temp_indir, temp_outdir)

#Excute the code to actually import the params file and extract the key values
if __name__ == "__main__":
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument("--file-path", type=str, required=True, help="Path to parameter file")

	args, unknowns = parser.parse_known_args()
	file_path = args.file_path

	main(file_path=file_path,)
	the_returned = main(file_path)
	name_exp = the_returned[0]
	source = the_returned[1]
	source_x = "-%s" % (source)
	input_dir = the_returned[2]
	out_dir = the_returned[3]

##################################################
# Open date-matrix
#################################################

date_loc = '/working/lab_nicw/alanR/DATE_MATRIX'
date_file = 'Month_Matrix.txt'
date_ingest = '%s/%s' % (date_loc, date_file)

datetrix_df = pd.read_csv(date_ingest, sep="\t")
#print(datetrix_df)
#df = datetrix_df

#month = "2018-04"

#a = (df[df['Period'].str.contains(month)])
#b=a.iloc[0]['Date']
#print(b)

###################################################
# From a list of panels, focus on a singular panel, extract source, name and ID
###################################################

for directory, subdirectories, files in os.walk(input_dir):
	for file in files:
		if file.endswith('.txt'):
			net_genes = 0
			last_month_net_genes = 0
			total_tges = 0
			last_month_total_tges = 0
			monthly_tges_added = 0
			monthly_tges_removed = 0
			cum_tges_added = 0
			cum_tges_removed = 0
			cum_total_tge = 0
			cum_dgges_added = 0
			cum_dgges_removed = 0
			cum_dgges_up = 0
			cum_dgges_down = 0
			cum_total_dgge = 0
			cum_releases = 0

			counter = 0

			condition_raw = re.split(r'_GeneChange_Summary', file)
			version_01 = re.split(r'\)-', condition_raw[0])
			source = version_01[1]
			source_x = "-%s" % (source)
			condition_raw1 = re.split(source_x, condition_raw[0])
			condition_raw2 = re.split(r'\(', condition_raw1[0])
			condition = condition_raw2[0]   #Condition Name

			condition_raw3 = re.split(r'\)', condition_raw2[1])
			ID = condition_raw3[0]          #Condition Raw
			identifer = "%s(%s)" % (condition, ID)
			identifer = str(identifer)
			print(identifer)

			out_name = '%s_%s_Cumulative_Changes_AUGUST.txt' % (identifer, source)
			outer = '%s/%s' % (out_dir, out_name)
			outer_file = open(outer, "w")

			print("PANEL:",identifer,"\nMonth","Releases", "Cumulative_Releases(AfterIntitalReleaseWindow)","No.Genes","Genes_Added(Month)","Genes_Removed(Month)","Genes_Added(Cumulative)","Genes_Removed(Cumulative)","Cumulative_Changed_Genes","No.DiaGenes", "DiaGenes_Added(Month)", "DiaGenes_Upgraded(Month)" ,"DiaGenes_Removed(Month)", "DiaGenes_Downgraded(Month)", "DiaGene.Gains(Cumulative)", "DiaGene.Losses(Cumulative)", "DiaGene.Changes(Cumulative)", sep="\t", file=outer_file)

			file0 = "%s/%s" % (input_dir, file)
			file1 = open(file0, "r")

			for line in file1:
				line2 = re.split(r'\t', line)
				if line2[0] == 'PANEL:':
					continue	
				if line2[0] == 'Period':
					continue
				month_temp = line2[0]

################
# FIX DATES
################		
				month_temp1 = (datetrix_df[datetrix_df['Period'].str.contains(month_temp)])
				month=month_temp1.iloc[0]['Date']
				print(month_temp, month, sep="\t")	

###########################
# RESUME PROCESSING FILE
##########################
				version = line2[1]
				releases = int(line2[2])
				no_tges = int(line2[3])
				tges_added = int(line2[4])
				tges_removed = int(line2[5])
				no_dgges = int(line2[6])
				dgges_added = int(line2[7])
				dgges_removed = int(line2[9])
				dgges_upgraded = int(line2[8])
				dgges_downgraded = int(line2[10])

				if counter == 0:
					print("", end="")
				else:
					cum_tges_added = cum_tges_added + tges_added
					cum_tges_removed = cum_tges_removed + tges_removed
					cum_total_tge = cum_tges_added + cum_tges_removed
					cum_dgges_added = dgges_added + dgges_upgraded + cum_dgges_added
					cum_dgges_removed = dgges_removed + dgges_downgraded + cum_dgges_removed
					cum_total_dgge = cum_dgges_removed + cum_dgges_added
					cum_releases = releases + cum_releases

				print(month, releases, cum_releases, no_tges, tges_added, tges_removed, cum_tges_added, cum_tges_removed, cum_total_tge, no_dgges, dgges_added, dgges_upgraded, dgges_removed, dgges_downgraded, cum_dgges_added, cum_dgges_removed, cum_total_dgge, sep="\t", file=outer_file)
				counter = counter + 1
				time.sleep(0.25)



