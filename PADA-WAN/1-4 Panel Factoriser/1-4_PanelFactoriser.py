##################################################
#
# PRODUCE MONTHLY SUMMARY MATIRX FOR EACH VARIABLE
#
##################################################

#This script has been written to combine ALL the different condensed panels into a single matrix for each variable 
#For example, it will produce a matrix containing all the diagnostic genes that are present in each panel at the end of month 

#Alan Robertson
#2022-01-31

#Version 1.0
#2023-05-04 - PRODUCTIONISE

################################################
#MODULE LOAD
import os
import re
import time
import pandas as pd
import numpy as np
import argparse

#SET UP BACKGROUND STUFF
period ="Period"
release = "Last-Release(Date)"

#ARGY-BARGY
#Define main function
def main(file_path: str):
	parameters_df = pd.read_csv(file_path,sep="\t")
	temp_name = parameters_df.iloc[0,1]
	temp_version = parameters_df.iloc[1,1]               # either AU or UK
	temp_input_dir = parameters_df.iloc[2,1]
	temp_outputdir = parameters_df.iloc[3,1]
	return(temp_name, temp_version, temp_input_dir, temp_outputdir)

#Excute the code to actually import the params file and extract the key values 
if __name__ == "__main__":
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument("--file-path", type=str, required=True, help="Path to parameter file")
	args, unknowns = parser.parse_known_args()
	file_path = args.file_path

	main(file_path=file_path,)     
	the_returned = main(file_path)
	name_exp = the_returned[0]
	version = the_returned[1]
	version_x = '%s_' % (version)
	indir = the_returned[2]
	outdir = the_returned[3]

	#print(the_returned)
	print(name_exp, "Parameters File Ingested. \nBeginning Script.")
	time.sleep(1)

#REPEAT SCRIPT FOR EACH VARIABLE (AND PRODUCE 1 MATRIX FOR EACH VARIABLE)
var_list = ["No.Ent","No.DiaEnt","No.Genes","No.DiaGenes","No.Repeats","No.DiaRepeats","No.CNVs","No.DiaCNVs", "Releases"]

for var in var_list:
	print("Producing Matrix for:", var)
	#time.sleep(3) 
	root_dir = indir
	input_dir = root_dir
	out_dir =outdir	
	out_name = '%s_%s_%s.txt' % (name_exp, var, version)
	out_name_T = '%s_%s_%s_TRANSPOSED.txt' % (name_exp, var, version) 
	outer = '%s/%s' % (out_dir, out_name)
	outer_T = '%s/%s' % (out_dir, out_name_T)

################
# For each file
# Open each file and extract the condition name, and ID
###############

	li = []
	for directory, subdirectories, files in os.walk(root_dir):
		for file in files:
			if file.endswith('.txt'):
				condition_raw = re.split(r'-Monthly_Summary', file)
				condition_raw1 = re.split(version_x, condition_raw[0])
				condition_raw2 = re.split(r'\(', condition_raw1[1])
				condition = condition_raw2[0]
				condition_raw3 = re.split(r'\)', condition_raw2[1])
				ID = condition_raw3[0]
				identifer = "%s(%s)" % (condition, ID)
				identifer = str(identifer)
				print(identifer)

				file0 = "%s/%s" % (input_dir, file)
				file1 = open(file0, "r")

				df = pd.read_csv(file0, index_col='Period', header=0, sep='\t', skipfooter=1, engine='python')
				c = '%s - %s' % (identifer, var)
				df.rename(columns={var: c}, inplace=True)
				li.append(df[c])
		
			df = pd.concat(li, axis=1, ignore_index=False)
			df.to_csv(outer, index=True, sep="\t", na_rep="n/a", float_format='%.0f')
			df1=df.transpose()
			df1.to_csv(outer_T, index=True, sep="\t", na_rep="n/a", float_format='%.0f')

	print ("Moving on to next variable:\n")
