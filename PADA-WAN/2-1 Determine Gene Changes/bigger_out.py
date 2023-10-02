##################################################
#
# CHARACTERISE CHANGE IN PANELS
#
# i.e. compare  versions of the same panel to characterise how the panel has evolved
#
##################################################

#This script has been written to analyse different versions of the same panel and determine change 
#It achieves this by taking one version of a panel, and comparing it to the version of the panel from the month prior, this occurs for every available month 
#Unlike previous sciprts this one exclusively focuses on genes 

# Alan Robertson - Feburary 2022

# Version 1.0
# 2023-05-04 - PRODUCTIONISE

# Version 1.1
# 2023-09-07 - Updated to replace the deprecated append command with with the concat command 
################################################
# SCRIPT OUTLINE
################################################
# 1. Open ID file - for each panel in the id file
# 2. Open the panel's monthly breakdown - open the corresponding specific version of the panel
# 3. Ingest each version into a data frame (ID and gel status)
# 4. Append each version's df to the main data frame
# 5. print the results
################################################

import re
import datetime
import time
import numpy as np
import pandas as pd
import argparse
import os
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)	#silence the pandas append / concat warning 

############################################
#ARGY-BARGY: i.e. Import the key variables 
###########################################

#Define main function
def main(file_path: str):
	parameters_df = pd.read_csv(file_path,sep="\t")
	temp_name = parameters_df.iloc[0,1]
	temp_version = parameters_df.iloc[1,1]
	temp_outdir = parameters_df.iloc[2,1]
	temp_sdate = parameters_df.iloc[3,1]
	temp_edate = parameters_df.iloc[4,1]
	temp_id_loc = parameters_df.iloc[5,1]
	temp_id_file = parameters_df.iloc[6,1]
	temp_month_loc = parameters_df.iloc[7,1]	
	temp_panel_loc = parameters_df.iloc[8,1]
	return(temp_name, temp_version, temp_outdir, temp_sdate, temp_edate,temp_id_loc, temp_id_file, temp_month_loc, temp_panel_loc )

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
	source_x = '%s_' % (source)
	outdir = the_returned[2]

	temp_start = the_returned[3]
	temp_end = the_returned[4]
	#ensure dates are in correct format
	temp = re.split(r',', temp_start)
	start_date_y = int(temp[0])
	start_date_m = int(temp[1])
	start_date_d = int(temp[2])
	start_date = datetime.date(start_date_y,start_date_m, start_date_d)

	temp = re.split(r',', temp_end)
	end_date_y = int(temp[0])
	end_date_m = int(temp[1])
	end_date_d = int(temp[2])
	end_date = datetime.date(end_date_y,end_date_m, end_date_d)

	id_loc = the_returned[5]
	id_file = the_returned[6]
	monthly_summary_loc = the_returned[7]
	panel_loc = the_returned[8]

	#Check
	"""
	print("NAME:\t\t\t\t", name_exp)
	print("PANELAPP VERION:\t\t", source)
	print("OUTPUT-DIR:\t\t\t", outdir)
	print("Start Date:\t\t\t", start_date)
	print("End Date:\t\t\t", end_date)
	print("Location ID:\t\t\t", id_loc)
	print("ID File:\t\t\t", id_file)
	print("Location Monthly Summary:\t",monthly_summary_loc)	
	print("Panel loc:\t\t\t",panel_loc)	

	"""

###################################################
# From a list of panels, focus on a singular panel, extract source, name and ID
###################################################

temp = "%s/%s" % (id_loc, id_file)
file_ID = open(temp, "r")

for line in file_ID:
	line1 = re.split(r'\t', line)                  #for each line, seperate by tab
	panel_name = line1[0]
	if panel_name == 'Panel':
		continue

	panel_name=panel_name.strip()
	panel_name = panel_name.replace(' ', '_')
	panel_name_Y = panel_name.replace('/', '--')
	panel_name_temp = re.split(r'\(', panel_name_Y)
	panel_name_X = panel_name_temp[0]

	panel_id = line1[1]
	source = line1[8]
	source = source.strip()

#check
	print(panel_name_X, "-", panel_id)
	#time.sleep(5.0)
	
##################################################
# For each panel, create the output files
###################################################
	parent_location1 = outdir
	parent_location2 = "%s_%s_%s-Panel_GeneLevel_Matrix" % (source, panel_id, panel_name)

	reclassification_summary = "%s/%s(%s)-%s_GeneChange_Summary.txt" % (parent_location1, panel_name_Y, panel_id, source)
	reclassification_file = open(reclassification_summary, "w+")
	head_summary = "PANEL:\t%s(%s)-%s\tStart of Analysis Window:\t%s\tEnd of Analysis Window:\t%s\nPeriod\tVersion\tNo.Releases\tNo.Genes\tGenes.Added\tGenes.Removed\tNo.DiaGenes\tDiaGenes.Added\tDiaGenes.Upgraded\tDiaGenes.Removed\tDiaGenes.Downgraded\tDiaGene.Changes\tDiaGene.Gains\tDiaGene.Losses" % (panel_name, panel_id, source, start_date, end_date)
	#print(head_summary)
	print(head_summary, file=reclassification_file)

	changed_gene_summary = "%s/%s(%s)-%s_Changed-Genes.txt" % (parent_location1, panel_name_Y, panel_id, source)
	changed_gene_file = open(changed_gene_summary, "w+")
	print("Gene","ENSG-ID","Status","Prior Period","Current Period","Prior Diagnostic-Status","Current Diagnostic Status" ,"Change-Type", file=changed_gene_file, sep="\t")

##################################################
# Set up panel specific variables
#################################################
	master_df = pd.DataFrame(columns=['Genes'])

###################################################
# For each panel, open the monthly summary file
###################################################
	monthly_breakdown = "%s_%s(%s)-Monthly_Summary" %(source, panel_name_X, panel_id)
	#panel_name_X fixes CAKUT
	monthly_breakdown_loc = monthly_summary_loc
	monthly_path = ("%s/%s.txt") % (monthly_breakdown_loc, monthly_breakdown)

	file_monthlybreakdown = open(monthly_path, "r")
	for line_mbd in file_monthlybreakdown:
		line2 = re.split(r'\t', line_mbd)
		if line2[0] == 'Period':
			continue
		if "NOTE" in line2[0]:
			continue
		if "N/A" in line2[1]:
			new_panel_check = 1
			last_total_tge = 0
			last_total_dgge = 0
			continue
	
		new_panel_check = 0
		timepoint_date0 = line2[0]
		timepoint_line = re.split(r'-', timepoint_date0)
		timepoint_year = int(timepoint_line[0])
		timepoint_month = int(timepoint_line[1])
		timepoint_month1 = ("{:02d}".format(timepoint_month))
		timepoint_month2 = int(timepoint_month1)
		timepoint_day = int(timepoint_line[2])
		time_stamp = datetime.date(timepoint_year, timepoint_month, timepoint_day)
		time_stamp2 = "%s_%s_%s" % (timepoint_year, timepoint_month1, timepoint_day)
		time_stamp3 = "%s-%s" %(timepoint_year, timepoint_month1)
		this_month = time_stamp3
		last_month0 = timepoint_month2 - 1
		last_month0 = ("{:02d}".format(last_month0))

		if timepoint_month2 == 1:
			last_month0 = 12
			last_year = int(timepoint_year)-1
			last_month = "%s-%s" %(last_year, last_month0)
		else:
			last_month = "%s-%s" %(timepoint_year, last_month0)
		
		monthly_releases = line2[1]
		
		if time_stamp < start_date:
			continue

		version = line2[2]
		line22 = re.split(r'\(', version)
		version_processed = line22[0]

		if 'N/A' in version_processed:
			continue

		print("Opening", panel_name, "\t", time_stamp3, "\t", version_processed)

###################################################
# Read individual file  into data frame
###################################################

		individual_panel_location = "%s/%s_%s_%s" % ( panel_loc, source, panel_id, panel_name_Y)
		each_version_file = "%s_v%s(%s)_Annotated_PA-%s.tsv" % (panel_name_Y, version_processed, panel_id, source)
		version_specific_path = "%s/%s" % (individual_panel_location, each_version_file)
		file_specific_version = open(version_specific_path, "r")
		df_this_month = pd.DataFrame(columns=['Genes', time_stamp3])

		for gene_line in file_specific_version:	
			line3 = re.split(r'\t', gene_line)
			g_symbol = line3[0]
			g_status = line3[1]
			ensg_id_0 = line3[4]
			ensg_id = "%s-%s-%s" % (g_symbol, ensg_id_0, g_status)
			version_checker = line3[6]
			dge_status = line3[5]

			if 'GEL-Status' in line3[5]:
				continue
			if g_status != 'gene':
				continue

			if dge_status != "":
				if ensg_id in df_this_month.values:
					print("", end="")
				else:
					DGE = int(dge_status)
					df_temp = pd.DataFrame.from_dict({'Genes': [ensg_id], time_stamp3: [DGE]})
					#df_this_month = df_this_month.append(df_temp, ignore_index=True)
					df_this_month = pd.concat([df_this_month,df_temp], axis=0)	
		master_df = pd.merge(master_df, df_this_month, on='Genes', how='outer')

###################################################
# Compare this month to last month
###################################################

		add_count = 0
		dgge_add_count = 0
		same_count = 0
		up_count = 0
		dgge_up_count = 0
		down_count = 0
		dgge_down_count = 0
		remove_count = 0
		dgge_remove_count = 0

		gene_changes = 0
		gene_gains = 0
		gene_losses = 0

		for index, row in master_df.iterrows():
			y = row[this_month]
			if last_month not in master_df:
				add_count = add_count + 1
				om = row['Genes']
				alpha = om.split("-")
				alpha_gene = alpha[0]
				alpha_ensg = alpha[1]
				alpha_status = alpha[2]
				#print(this_month, alpha_gene, alpha_ensg, alpha_status, y ,"ADDED", sep="\t", file=changed_gene_file)	
				if y >= 3:
					dgge_add_count = dgge_add_count + 1
				same_count = 0
				up_count = 0
				down_count = 0
				remove_count = 0
				continue
		
			x = row[last_month]
			z = row['Genes']
			alpha = z.split("-")
			alpha_gene = alpha[0]
			alpha_ensg = alpha[1]
			alpha_status = alpha[2]

			if np.isnan(x) == True and np.isnan(y) == True:
				continue
			#ADD
			if np.isnan(x) == True and y >= 0:
				add_count = add_count + 1
				if y == 3:
					dgge_add_count = dgge_add_count + 1
					print(alpha_gene, alpha_ensg, alpha_status, last_month,this_month, x, y ,"NOVEL DIANGOSTIC GENE ADDED", sep="\t", file=changed_gene_file)
				else:
					print(alpha_gene, alpha_ensg, alpha_status, last_month,this_month, x, y ,"NOVEL GENE ADDED", sep="\t", file=changed_gene_file)
			#REMOVE
			if np.isnan(y) == True and x >= 0:
				remove_count = remove_count + 1
				#print(alpha_gene, alpha_ensg, alpha_status, last_month,this_month, x, y ,"GENE REMOVED", sep="\t", file=changed_gene_file)
				if x == 3:
					dgge_remove_count = dgge_remove_count + 1
					print(alpha_gene, alpha_ensg, alpha_status, last_month,this_month, x, y ,"DIAGNOSTIC GENE REMOVED", sep="\t", file=changed_gene_file)
				else:
					print(alpha_gene, alpha_ensg, alpha_status, last_month,this_month, x, y ,"GENE REMOVED", sep="\t", file=changed_gene_file)
			if x == y:
				same_count = same_count + 1
			#UPGRADE
			if y > x:
				up_count = up_count + 1
				if y == 3:
					dgge_up_count = dgge_up_count + 1
					print(alpha_gene, alpha_ensg, alpha_status, last_month,this_month, x, y ,"GENE UPGRADED TO DIAGNOSTIC", sep="\t", file=changed_gene_file)
			#DOWNGRADE
			if y < x:
				down_count = down_count + 1
				if x == 3:
					dgge_down_count = dgge_down_count + 1
					print(alpha_gene, alpha_ensg, alpha_status, last_month,this_month, x, y ,"GENE DOWNGRADED FROM DIAGNOSTIC", sep="\t", file=changed_gene_file)

		total_tge = last_total_tge + add_count - remove_count
		total_dgge = last_total_dgge + (dgge_add_count + dgge_up_count) - (dgge_remove_count + dgge_down_count)
		gene_gains = dgge_add_count + dgge_up_count
		gene_losses = dgge_remove_count + dgge_down_count 
		gene_changes = gene_gains + gene_losses
		print(this_month, version_processed, monthly_releases, total_tge, add_count, remove_count,
		total_dgge, dgge_add_count, dgge_up_count, dgge_remove_count, dgge_down_count, gene_changes, gene_gains, gene_losses, sep="\t", file=reclassification_file)
		last_total_tge = total_tge
		last_total_dgge = total_dgge

###################################################
# For each panel
###################################################
	this_month = "2019-11"
	last_month = "2019-10"
	time.sleep(1)
