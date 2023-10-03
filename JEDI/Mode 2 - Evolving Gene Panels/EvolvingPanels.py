# #############################################################
# Module Load
# ############################################################

import pandas as pd
import os
import datetime
import time
import re
import numpy as np
import argparse

# #############################################################
#  Argy-Bargy 
# ############################################################

# Define the arg parse function
def main(file_path: str):
	parameters_df = pd.read_csv(file_path,sep="\t")
	temp_1 = parameters_df.iloc[0,1]
	temp_2 = parameters_df.iloc[1,1]
	temp_3 = parameters_df.iloc[2,1]
	temp_4 = parameters_df.iloc[3,1]
	temp_5 = parameters_df.iloc[4,1]
	temp_6 = parameters_df.iloc[5,1]
	temp_7 = parameters_df.iloc[6,1]
	temp_8 = parameters_df.iloc[7,1]
	temp_9 = parameters_df.iloc[8,1]
	temp_10 = parameters_df.iloc[9,1]
	temp_11 = parameters_df.iloc[10,1]
	temp_12 = parameters_df.iloc[11,1]
	temp_13 = parameters_df.iloc[12,1]
	temp_14 = parameters_df.iloc[13,1]
	temp_15 = parameters_df.iloc[14,1]
	temp_16 = parameters_df.iloc[15,1]

	return(temp_1, temp_2, temp_3, temp_4, temp_5, temp_6, temp_7, temp_8, temp_9, temp_10, temp_11, temp_12, temp_13, temp_14, temp_15, temp_16)

#Excute the code to actually run the function
if __name__ == "__main__":
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument("--file-path", type=str, required=True, help="Path to parameter file")
	args, unknowns = parser.parse_known_args()
	file_path = args.file_path

	main(file_path=file_path,)
	the_returned = main(file_path)

	start_date_y = int(the_returned[0])
	start_date_m = int(the_returned[1])
	start_date_d = int(the_returned[2])
	end_date_y = int(the_returned[3])
	end_date_m = int(the_returned[4])
	end_date_d = int(the_returned[5])
	start_date = datetime.date(start_date_y, start_date_m, start_date_d)	
	end_date = datetime.date(end_date_y, end_date_m, end_date_d)

	temp_id_loc = the_returned[6] 
	temp_file_id = the_returned[7] 
	monthly_breakdown_loc_au = the_returned[8]
	monthly_breakdown_loc_uk = the_returned[9]
	output_loc_au = the_returned[10]
	output_loc_uk = the_returned[11]
	au_individual_panel_loc = the_returned[12]
	uk_individual_panel_loc = the_returned[13]
	temp_matrix_loc = the_returned[14]
	temp_matrix_file = the_returned[15]

#Dates - note start should be a month eariler than the acutal start date
#start_date = datetime.date(2018, 3, 1)
#end_date = datetime.date(2023, 5, 1)

#Location of file with all the comparisons 
temp_id_file = "%s/%s" % (temp_id_loc, temp_file_id)

#location of the monthly breakdownd
parent_loc1_au = output_loc_au 
parent_loc1_uk = output_loc_uk

#location of the clinvar matrix
matrix_file = '%s/%s' % (temp_matrix_loc, temp_matrix_file)

# #############################################################
# Ingest ClinVar Matrix
# ############################################################

full_df = pd.read_csv(matrix_file, sep='\t', header=0, skip_blank_lines=False)
mat_df = full_df.set_index(['ENSG-ID'])

#replace NA with 0
mat_df = mat_df.fillna(0)

#Determine ensg-ids that match to multiple NCBI ids
repeated_ids_df = mat_df.index.value_counts()

# #############################################################
# Open file containing the list of panels to analyse
# ############################################################

id_file = open(temp_id_file, "r")

for line in id_file:
	line1 = re.split(r'\t', line)
	panel_name_full = line1[0] 
	panel_name_full=panel_name_full.strip()
	panel_name_full = panel_name_full.replace(' ', '_')
	panel_name_full = panel_name_full.replace('/', '--')

	panel_name_temp = re.split(r'\(', line1[0])
	if len(panel_name_temp) > 1:
		panel_name = (panel_name_temp[0])
		panel_name = panel_name.replace(' ', '_')
	else:
		panel_name = panel_name_temp[0]
	
	if panel_name == 'Panel':
		continue
	
	panel_name=panel_name.strip()	
	panel_name = panel_name.replace(' ', '_')
	panel_name_Y = panel_name.replace('/', '--')		#Dystonia(291) is the worst

	#print(("this is a test ----%s----") % (panel_name))

	panel_id = line1[1]
	source = line1[8]
	source = source.strip()
	monthly_breakdown = "%s_%s(%s)-Monthly_Summary" %(source, panel_name_Y, panel_id)
	print(monthly_breakdown)

	if source == 'UK':
		monthly_breakdown_loc = monthly_breakdown_loc_uk
		parent_location1 = parent_loc1_uk

	if source == 'AU':
		monthly_breakdown_loc = monthly_breakdown_loc_au
		parent_location1 = parent_loc1_au

# #############################################################
# Create output files
# ############################################################

	#panel_name_Y = panel_name.replace('/', '--')	
	parent_location2 = "%s_%s_%s-VariantsInPanels" % (source, panel_id, panel_name_Y)
	path_01 = os.path.join(parent_location1, parent_location2)
	
	isExist = os.path.exists(path_01)
	if isExist == False:
		os.mkdir(path_01)

	output_summary = "%s/%s(%s)-%s_VariantsInPanels_MonthlySummary.txt" % (parent_location1, panel_name_Y, panel_id, source)
	bastard = open(output_summary, "a+")

	head_summary = ("Date\tVersion\tNo.Iterations\tTotalGenes\tMatchedGenes\tNo.MissingGenes\tMissingGenes\tAllVariantsInGenes\tVUSInGenes\tPLPInGenes\tDiagnosticGenes\tMatchedDiagnosticGenes\tNo.MissingDiagnosticGenes\tMiaaingDiagnsoticGenes\tAllVariantsInDiagnosticGenes\tVUSInDiagnosticGenes\tPLPInDiagnosticGenes")

	print(head_summary, file=bastard)


# #############################################################3
# For each panel, open the monthly_breakdown, and extract the version of the panel that was present at each month of the analysis window
# #############################################################

	version = 0	# re-set version counter
	path0 = ("%s/%s.txt") % (monthly_breakdown_loc, monthly_breakdown)
	
	file_monthlybreakdown = open(path0, "r")

	for line_mbd in file_monthlybreakdown:
		line2 = re.split(r'\t', line_mbd)
	
		if line2[0] == 'Period':
			continue
		if "NOTE" in line2[0]:
			continue	

		timepoint_date0 = line2[0]
		timepoint_line = re.split(r'-', timepoint_date0)
		timepoint_year = int(timepoint_line[0])
		timepoint_month = int(timepoint_line[1])
		timepoint_month1 = ("{:02d}".format(timepoint_month))
		timepoint_day = int(timepoint_line[2])

		#Create variables so that we can search the correct columns in the clinvar matrix
		timepoint_header_base = "%s_%s" % (timepoint_year, timepoint_month1)
		timepoint_header_all =  "%s-all" % (timepoint_header_base)
		timepoint_header_vus =  "%s-vus" % (timepoint_header_base)
		timepoint_header_plp =  "%s-plp" % (timepoint_header_base)

		timepoint_date = datetime.date(timepoint_year, timepoint_month, timepoint_day)
		
		if timepoint_date <start_date:
			continue 

		if timepoint_date > start_date and timepoint_date < end_date:
			version = line2[2]

			line22= re.split(r'\(', version)
			version_processed = line22[0]
			if 'N/A' in version_processed:
				continue
	
			version_processed = version_processed.replace(" ", "")
			total_genes = line2[5]
			total_dgg = line2[4]
			no_iterations = line2[1]		
	
# #############################################################
# From information in the monthly summary file, open the specific version of that panel 
# #############################################################

			if source == "UK":
				individual_panel_location = "%s/%s_%s_%s" % (uk_individual_panel_loc, source, panel_id, panel_name_full)
			if source == "AU":
				individual_panel_location = "%s/%s_%s_%s" % (au_individual_panel_loc, source, panel_id, panel_name_full)

			each_version_file = "%s_v%s(%s)_Annotated_PA-%s.tsv" %(panel_name_full,version_processed,panel_id,source)
			
			path1 = "%s/%s" % (individual_panel_location, each_version_file)

			#Create output files
			output_gene = "%s/%s-%s(%s)-%s-v%s_Gene_Specific_Summary.txt" % (path_01, timepoint_date,panel_name_Y, panel_id, source,version_processed)
			XXX = open(output_gene, "a+")
			head_summary_1 = "Date\tVersion\tENSG-ID\tSymbol\tEntity-Status\tDGE-Status\tNo.Variants\tNo.VUS\tNo.PLP"
			print(head_summary_1, file=XXX)		
			#print (head_summary_1)

			file_specific_version = open(path1, "r")
			print("Opening:", panel_name, "(", panel_id, ")\t Version:", version_processed, "\t Time Point:\t", timepoint_date)
			#time.sleep(.1)

			timepoint_all_sum = 0
			timepoint_plp_sum = 0
			timepoint_vus_sum = 0
			timepoint_all_dge_sum = 0
			timepoint_plp_dge_sum = 0
			timepoint_vus_dge_sum = 0
			gene_count = 0
			DGE_count = 0
			DGGE_TOTAL = 0

			missing_count = 0
			DGE_missing_count = 0

			missing_str = ''
			missing_dge_str = ''

# ########################################################################
# for each gene in present in the specific version of the panel ₍ᐢ•ﻌ•ᐢ₎*･ﾟ｡
# ########################################################################

			for gene_line in file_specific_version:
				line3 = re.split(r'\t', gene_line)
				ensg_id = line3[4]
				g_symbol = line3[0]
				dge_status = line3[5]
				entitiy_status = line3[1]
				
				if 'GEL-Status' in line3[5]:
					continue

				if 'gene' in entitiy_status:
					print("", end="")
				else:
					continue

				if 'ENSG-ID' in ensg_id:
					continue 
				
				if 'NA' in ensg_id:
					continue

				DGE = int(dge_status)	

				all_variants = 0
				vus_variants = 0
				plp_variants = 0
				matched_count = 0
				
				######################3
				# if ensg-id in clinvar
				######################	
			
				if ensg_id in mat_df.index:

					multi_match_check = repeated_ids_df.loc[ensg_id]	
					if multi_match_check == 2:
						#print(ensg_id, multi_match_check ,sep=' ')
						x = mat_df.at[ensg_id, timepoint_header_all]		#pandas series 
						v1 = (x[0])
						v2 = (x[1])
						if v1 > v2:
							all_variants = v1
							
							x2 = mat_df.at[ensg_id, timepoint_header_vus]
							x21 = (x2[0])
							vus_variants = x21

							x3 = mat_df.at[ensg_id, timepoint_header_plp]
							x31 = (x3[0])
							plp_variants = x31
							
						if v1 < v2:
							all_variants = v2
							x2 = mat_df.at[ensg_id, timepoint_header_vus]
							x21 = (x2[1])
							vus_variants = x21

							x3 = mat_df.at[ensg_id, timepoint_header_plp]
							x31 = (x3[1])
							plp_variants = x31

						time.sleep(1)
				
			
					if multi_match_check == 1: 
						all_variants = mat_df.at[ensg_id, timepoint_header_all]
						vus_variants = mat_df.at[ensg_id, timepoint_header_vus]
						plp_variants = mat_df.at[ensg_id, timepoint_header_plp]

					if DGE > 2.5:
						DGE_count = DGE_count + 1

					gene_count = gene_count + 1
					matched_count = matched_count + 1	


				 # add the values to the summary variables
					timepoint_all_sum = timepoint_all_sum + all_variants
					timepoint_vus_sum = timepoint_vus_sum + vus_variants
					timepoint_plp_sum = timepoint_plp_sum + plp_variants

					if DGE > 2.5:
						timepoint_all_dge_sum = timepoint_all_dge_sum + all_variants
						timepoint_vus_dge_sum = timepoint_vus_dge_sum + vus_variants
						timepoint_plp_dge_sum = timepoint_plp_dge_sum + plp_variants	

				#######################
				# if ensg from panelapp no longer exists
				######################
				
				else:
					missing_count = missing_count + 1
				
					missing_str = '%s(%s),%s' % (ensg_id, g_symbol, missing_str)		
					if DGE > 2.5:
						DGE_missing_count = DGE_missing_count + 1
						missing_dge_str = '%s(%s),%s' % (ensg_id, g_symbol, missing_dge_str)
					
				#print(timepoint_date, version_processed, ensg_id,g_symbol, entitiy_status, dge_status, all_variants, vus_variants, plp_variants, sep='\t')	
				print(timepoint_date, version_processed, ensg_id,g_symbol,entitiy_status,dge_status,all_variants,vus_variants, plp_variants, sep='\t', file=XXX)		
				#time.sleep(.1)

			
# ########################################################################3
# Produce summary file
# ########################################################################3	

		DGGE_TOTAL = DGE_count + DGE_missing_count
		if not missing_str:
			missing_str = 'N/A'
		
		if not missing_dge_str:
			missing_dge_str = 'N/A'
		
		#CHECK
		#print("Date:\t", timepoint_date)
		#print("Version\t:", version_processed)
		#print("No.Iterations:\t", no_iterations)
		#print("TotalGenes:\t", total_genes) 
		#print("MatchedGenes:\t", gene_count) 
		#print("MissingGenes:\t", missing_count) 
		#print("AllVariantsInGenes:\t", timepoint_all_sum) 
		#print("VUSInGenes:\t", timepoint_vus_sum) 
		#print("PLPInGenes:\t", timepoint_plp_sum)
		#print("DiagnosticGenes:\t", DGGE_TOTAL) 
		#print("MatchedDiagnosticGenes:\t", DGE_count) 
		#print("MissingDiagnosticGenes:\t", DGE_missing_count) 
		#print("AllVariantsInDiagnosticGenes:\t", timepoint_all_dge_sum)
		#print("VUSInDiagnosticGenes:\t", timepoint_vus_dge_sum)
		#print("PLPInDiagnosticGenes:\t", timepoint_plp_dge_sum)  
		#time.sleep(1)

		#print(timepoint_date,version_processed,no_iterations,total_genes,gene_count,missing_count,timepoint_all_sum, timepoint_vus_sum, timepoint_plp_sum, DGGE_TOTAL ,DGE_count, DGE_missing_count,timepoint_all_dge_sum, timepoint_vus_dge_sum, timepoint_vus_dge_sum, sep='\t')
		#print("finished processing:", panel_name,timepoint_date,version_processed, sep='\t')
		print(timepoint_date,version_processed,no_iterations,total_genes,gene_count,missing_count,missing_str,timepoint_all_sum, timepoint_vus_sum, timepoint_plp_sum, DGGE_TOTAL ,DGE_count, DGE_missing_count,missing_dge_str,timepoint_all_dge_sum, timepoint_vus_dge_sum, timepoint_plp_dge_sum, sep='\t', file=bastard)			
			

