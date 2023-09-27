#######################################
#
# DOWNLOAD EVERY VERSION OF EVERY PANEL
#
#######################################

#Introduction
#This script was written to take the list of ids downloaded from either PanelApp and download every version of every panel
#This script takes the JSON file from PanelApp, extracts the relevant information and produces a simple, STABLE, text file for each version of each panel. This will prevent the issue seen in the txt download, that panel get a bit wobbly when imported into excel
#This script also produces a summary file that contains a snapshot of each version of each panel, by examining the GEL status of each genes, this removes the issue seen in the prior version in which descripancies were produced when "Review Status: Green" was not spelt correctly

#If in the event that the download is incomplete, this will be recorded in a warning file
#The files produced here are used in later analysis 

#NOTE: the output for the timestamp is a little unusual, however, this format " "[date]" "[time], means that it will display properly in things like Excel, Google Sheets and Apple Numbers. We admit that this is an unorthodox approach for a time stamp, however, this script has been produced under the assumption that everyone, no matter the level of familiarity with things like JSON or dataframes should be able to access the information in PanelApp

#To run this script, please make sure you set up the params file, then run the script on the command line
#i.e. python3 PanelApp_ID.py params.txt
#If you unsure about the token value in the params file, and if the token value provided here does not work, please, if not please consult the ReadMe.md 

#Alan Robertson
#2021-12-06

#Version 1.0 
#2023-04-27: Productionise script 

#Version 1.1
#Address re-download quirk in PanelApp UK

#Import modules
import argparse
import pandas as pd
import numpy as np
import os
import re
import requests
import time
from datetime import datetime

#Setup variables
version = ''
now = datetime.now()
now = now.strftime("%Y-%m-%d_%H-%M")
count = 1
count_str = str(count)
rerun = "true"

#Open the params file 
#i.e. python3 this_script.py --file_path parameters.txt
 
#Define main function
def main(file_path: str):
	parameters_df = pd.read_csv(file_path,sep="\t")
	version = parameters_df.iloc[0,0]		# either AU or UK
	input_file = parameters_df.iloc[1,0] 
	if re.search(r"AU", version, re.IGNORECASE):
		outdir = parameters_df.iloc[3,0]
		path = parameters_df.iloc[4,0]
		token = parameters_df.iloc[5,0]
	elif re.search(r"UK", version, re.IGNORECASE):
		outdir = parameters_df.iloc[6,0]
		path = parameters_df.iloc[7,0]
		token = parameters_df.iloc[8,0]
	return(version, outdir, path, token, input_file )

#Excute the code to actually import the params file and extract the key values 
if __name__ == "__main__":
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument("--file-path", type=str, required=True, help="Path to parameter file")
	args, unknowns = parser.parse_known_args()
	file_path = args.file_path

	main(file_path=file_path,)	
	the_returned = main(file_path)
	version = the_returned[0]
	outdir = the_returned[1]
	partial_path = the_returned[2]
	token = the_returned[3]
	input_loc = the_returned[4]

print("PanelApp Version:\t", version)
print("Opening:\t\t", input_loc)

#Open ID file
file1 = open(input_loc, "r")

# Using for loop to read in each line
for line in file1:
	line1 = re.split(r'\t+', line)                  #for each line, seperate by tab

#Prepare variables - Condition
	condition=(line1[0])
	condition = condition.strip() 			#remove new lines and white space
	condition = condition.replace("/","--")		#replace slashes with something that won't break my code
	condition = condition.replace(" ", "_")		# replace slashes with something that won't break my code

#Skip ID file header
	if condition == 'Panel': 
		continue

#Prepare variables - Panel ID
	panel_id=(line1[1])                             #pull out panel id
	panel_id=panel_id.strip()
	check_id=int(panel_id)

#Skip panels that have serious error in their data
	if version == 'UK':
		if check_id == 111:		#skip the COVID Panel from PanelApp UK
			print ("Due to formatting errors introduced into the COVID panel, PADA-WAN (much like PanelApp) is unable to support the historic version of the COVID panel.")
			time.sleep(1)
			continue
		
#Prepare variables - Most recent panel
	version_max=(line1[2])	
	version_max=version_max.strip()
	print("Version Max\t:\t", version_max)
	
	#fix instances in which tools like excel replace versions numbers like '1.0' with '1'
	#this code will restore the minor version numbers
	for loop_variable in range (1,10):
		string_var = str(loop_variable)
		fix_var = str(string_var + ".0")
		print("Loop:\t", loop_variable, "\tVersion Max:\t", version_max)
		if version_max == string_var:
			version_max = fix_var
			print("Version Fix\t:\t", version_max)

	version_max=str(version_max)
	version_split = version_max.split(".")
	main_version_max = version_split[0]
	main_version_max = int(main_version_max)
	sub_version_max = version_split[1]
	sub_version_max = int(sub_version_max)

	print("Extracting data from ID file:", check_id,"\t",condition)
	#time.sleep(3)

#Prepare outputs
	parent = outdir
	filename_summary = "%s/%s_%s(%s)-Total_Summary.txt" % (parent,version ,condition, panel_id)
	path0 = ("%s/%s") %(parent,filename_summary)

	file_exists_0 = os.path.join(path0, filename_summary)
	if os.path.isfile(file_exists_0):
		time.sleep(0.05)
	else:
		output_summary = open(filename_summary, "a+")
		with open(filename_summary, 'a+') as output_summary:
			print('PanelName(PanelID)\tMaxVersion\tDateOfRelease\tExaminedVersion\tNo.Entities\tNo.DiaEnt\tNo.Genes\tNo.DiaGenes\tNo.STRs\tNo.DiaSTRs\tNo.CNVs\tNo.DiaCNVs', file=output_summary)
		output_summary.close()

#Make a directory for each of the downloaded panels to go (if they don't have one)
	directory = "%s_%s_%s" % (version, panel_id, condition)
	path = os.path.join(parent, directory)

	isExist = os.path.exists(path)
	if isExist == False:
		os.mkdir(path)
	
##################################################
# Iterarate through every version of every panel
#################################################

#Setup
	current_version_main = 0
	current_version_main_str = str(current_version_main)
	current_version_sub = 0
	current_version_sub_str = str(current_version_sub)
	query_version_id = ("%s.%s") % (current_version_main_str, current_version_sub_str)
	empty_count = 0
	entity_count = 0
	gene_count = 0
	region_count = 0
	str_count = 0
	green_count = 0

#Download the main file - query
	while current_version_main <= main_version_max:

		if empty_count >= 10:
			if current_version_main == main_version_max:
				if current_version_sub < sub_version_max:
					print("current version:", current_version_sub, " vs. ", sub_version_max)
					time.sleep(0.1)	
					filename_warning = "%s/_WARNING_%s(%s).txt" % (parent, condition, panel_id)
					output_warning = open(filename_warning, "w+")
					last_version_sub = current_version_sub - empty_count -1
					with open(filename_warning, 'a+') as output_warning:
						print("Warning! This panel may be incomplete. \nThe most recent downloaded version of this panel is:\t", current_version_main,".",last_version_sub, "\nThe most recent listed current version is:\t\t", main_version_max,".",sub_version_max, file=output_warning)
					output_warning.close()


			if current_version_main <= main_version_max:
				current_version_main = current_version_main + 1
				current_version_main_str = str(current_version_main)
				current_version_sub = 0
				current_version_sub_str = str(current_version_sub)
				query_version_id = ("%s.%s") % (current_version_main_str, current_version_sub_str)
				empty_count = 0

#skip if previously downloaded
		filename = "%s_v%s(%s)_Annotated_PA-%s.tsv" % (condition, query_version_id, panel_id,version)
		file_existing = os.path.join(path, filename)

		if os.path.isfile(file_existing):
			print(condition, "(", panel_id, ") V-", query_version_id,
				"\t has already been downloaded - skipping to next version")
			current_version_sub = current_version_sub + 1
			current_version_sub_str = current_version_sub
			query_version_id = ("%s.%s") % (current_version_main_str, current_version_sub_str)
			continue

		elif current_version_main <= main_version_max:
			if current_version_sub <= sub_version_max:
				output_file = open(file_existing, "a+")
				with open(file_existing, 'a+') as output_file:
					print(
						'Identifier\tEntity-Type\tEntity-Symbol\tENSG-37\tENSG-38\tGEL-Status\tVersion\tPanel-ID\tDate-Of-Release\tTime-Of-Release',
					file=output_file)
				output_file.close()

#build the request
		print(condition, "(", panel_id, ")\tCurrent Version:", query_version_id, " of ", version_max, "empties =", empty_count)

		headers2 = {
			'accept': 'application/json',
			'X-CSRFToken': token,
		}
		
		url2 = '%s%s/?version=%s' % (partial_path ,panel_id, query_version_id)
		#print("QUERY URL:\t", url2)
		#url2 = 'https://panelapp.agha.umccr.org/api/v1/panels/%s/?version=%s' % (panel_id, query_version_id)		
		#print("OLD URL:\t", url2)
		#url2 = 'https://panelapp.agha.umccr.org/api/v1/panels/3149/?version=%s' % (query_version_id)	
		#print("HARD URL:\t", url2)
		

#Connect to PanelApp
		response = requests.get(url2, headers=headers2)
		response_json = response.json()
		time.sleep(0.1)
		response_headers = response.headers
		#print(response_headers)
		#time.sleep(5)

# Skip empty panels
		check_validity = response
		if not check_validity:
			empty_count = empty_count + 1
			current_version_sub = current_version_sub + 1
			current_version_sub_str = current_version_sub
			query_version_id = ("%s.%s") % (current_version_main_str, current_version_sub_str)
			continue

#Handle Empty Panels
		gene_count = int(len(response_json["genes"]))
		region_count = int(len(response_json["regions"]))
		str_count = int(len(response_json["strs"]))

		entity_count = gene_count + region_count + str_count

		if entity_count == 0:  # skip empty panels
			current_version_sub = current_version_sub + 1
			current_version_sub_str = current_version_sub
			query_version_id = ("%s.%s") % (current_version_main_str, current_version_sub_str)
			empty_count = empty_count + 1
			continue

		check_validity = response_headers['Content-Type']
		if check_validity == 'application/json':
			empty_count = 0

		else:
			current_version_sub = current_version_sub + 1
			current_version_sub_str = current_version_sub
			query_version_id = ("%s.%s") % (current_version_main_str, current_version_sub_str)
			empty_count = empty_count + 1
			continue

# Process the JSON file
		#################
		#General
        	#################

		json_id = response_json["id"]
		#print(json_id)
		#time.sleep(5)
		json_panel_name = response_json["name"]
		json_version = response_json["version"]
		version_date = response_json["version_created"]
		version_date0 = response_json["version_created"]
		version_date1 = re.split(r'T', version_date0)
		version_date_part_1 = version_date1[0]
		version_time0 = re.split(r':', version_date1[1])
		version_time_hour = int(version_time0[0])
		version_time_min = int(version_time0[1])
		version_time_min = (f"{version_time_min:02d}")
		version_time_sec = version_time0[2][:-1]
		version_time_sec = float(version_time_sec)
		version_time_sec = round(version_time_sec, 2)
		version_date_part_2 = "%s:%s:%s" % (version_time_hour, version_time_min, version_time_sec)
		green_count = 0 #Reset Green Count
		diagene_count = 0
		diaregion_count = 0
		diastr_count = 0

		#################
		#Gene
		#################
		a = 0
		while a < gene_count:

			if response_json["genes"][a]["entity_type"] == 'gene':
				json_symbol = response_json["genes"][a]["entity_name"]
				json_type = response_json["genes"][a]["entity_type"]
				json_identifer = json_symbol
				try:
					json_ensg37 = response_json["genes"][a]["gene_data"]["ensembl_genes"]["GRch37"]["82"]["ensembl_id"]
				except KeyError:
					json_ensg37 = "N/A"
				try:
					json_ensg38 = response_json["genes"][a]["gene_data"]["ensembl_genes"]["GRch38"]["90"]["ensembl_id"]
				except KeyError:
					json_ensg38 = "N/A"

				json_conf = response_json["genes"][a]["confidence_level"]
				json_conf = int(json_conf)
				if json_conf > 2.9:
					green_count = green_count + 1
					diagene_count = diagene_count + 1

				with open(file_existing, 'a+') as output_file:
					print(json_identifer,json_type,json_symbol,json_ensg37,json_ensg38,json_conf, query_version_id, panel_id, version_date_part_1, version_date_part_2,
					sep='\t', file=output_file)
					output_file.close()

			a = a+1
		a = 0
                #################
                #STR
                #################	
		
		while a < str_count:
			if response_json["strs"][a]["entity_type"] == 'str':
				json_symbol = response_json["strs"][a]["entity_name"]
				json_type = response_json["strs"][a]["entity_type"]
				json_str_repeat_seq = response_json["strs"][a]["repeated_sequence"]
				json_identifer = "%s_%s" % (json_symbol, json_str_repeat_seq)
				try:
					json_ensg37 = response_json["strs"][a]["gene_data"]["ensembl_genes"]["GRch37"]["82"]["ensembl_id"]
				except KeyError:
					print("exit code 1 (37)-", json_symbol)
					json_ensg37 = "N/A"

				try:
					json_ensg38 = response_json["strs"][a]["gene_data"]["ensembl_genes"]["GRch37"]["82"]["ensembl_id"]
				except KeyError:
					print("exit code 1 (38)-", json_symbol)
					json_ensg38 = "N/A"

				json_conf = response_json["strs"][a]["confidence_level"]
				json_conf = int(json_conf)

				if json_conf > 2.9:
					green_count = green_count + 1
					diastr_count = diastr_count + 1

				with open(file_existing, 'a+') as output_file:
					print(json_identifer,json_type,json_symbol,json_ensg37,json_ensg38,json_conf, query_version_id, panel_id, version_date_part_1, version_date_part_2, sep='\t', file=output_file)
					output_file.close()
				a = a+1

		a = 0
		#################
		#cnv
		###############
		while a < region_count:
			if response_json["regions"][a]["entity_type"] == 'region':
				json_symbol = response_json["regions"][a]["entity_name"]
				json_type = response_json["regions"][a]["entity_type"]
				json_identifer = json_symbol
				json_ensg37 = 'N/A'
				json_cnv_chr = response_json["regions"][a]["chromosome"]
				json_cnv_start = response_json["regions"][a]["grch38_coordinates"][0]
				json_cnv_stop = int(response_json["regions"][a]["grch38_coordinates"][1])
				json_ensg38 = "chr%s:%s-%s" % (json_cnv_chr, json_cnv_start, json_cnv_stop)

				json_conf = response_json["regions"][a]["confidence_level"]
				json_conf = int(json_conf)

				if json_conf > 2.9:
					green_count = green_count + 1
					diaregion_count = diaregion_count + 1

				with open(file_existing, 'a+') as output_file:
					print(json_identifer,json_type,json_symbol,json_ensg37,json_ensg38,json_conf, query_version_id, panel_id, version_date_part_1, version_date_part_2, sep='\t', file=output_file)
				output_file.close()
			a = a +1

#Produce summary file
		with open(filename_summary, 'a+') as output_summary:
			print(json_panel_name, "(", panel_id,")\t",version_max, "\t", " ",version_date_part_1," ",version_date_part_2, "\t", query_version_id, "\t", entity_count, "\t", green_count, "\t", gene_count,"\t", diagene_count, "\t", str_count, "\t", diastr_count,"\t", region_count, "\t", diaregion_count, "\t", sep="" ,file=output_summary)
			output_summary.close()

		current_version_sub = current_version_sub + 1
		current_version_sub_str = current_version_sub
		query_version_id = ("%s.%s") % (current_version_main_str, current_version_sub_str)


