##################################################
#
# CREATE CLINVAR MATRIX
#
# i.e. make a huge matrix that shows the number of variants that align within each gene for each month during the analysis window
#
##################################################

# This script has been written to create a resource that shows the number of variants in each gene an analysis window. This resource can be quiried for an answer about the number of variants in gene

# This script is really made of four big parts:
#	1. set everything up
#	2. read ensg and entrez id 
#	3. for each month in the analysis window import the correct monthly clinvar gene specific summary file add to the end of a dataframe
#	4. print the dataframe
#	5. summarise dataframe 

# Alan Robertson - Feb 8th 2022

# Version 1.0
# 2023-05-16 - PRODUCTIONISE

#Version 1.0.1
# 2023-08-07 - Fix pandas append/concat inline update

#Version 1.0.2
# 2023-09-11 - Monthly summary support 

 
################################################

#import modules
import argparse
import re
import time
import pandas as pd

###############################################

#arg parser

#set up main function
def main(file_path: str):
	parameters_df = pd.read_csv(file_path,sep="\t")
	temp_rosetta_loc = parameters_df.iloc[3,1]
	temp_rosetta_file = parameters_df.iloc[4,1]
	temp_rosetta = '%s/%s' %(temp_rosetta_loc, temp_rosetta_file)
	temp_gss_loc = parameters_df.iloc[5,1]
	temp_end_year = parameters_df.iloc[1,1]
	temp_end_month = parameters_df.iloc[2,1]
	temp_out_loc = parameters_df.iloc[6,1]
	temp_exp_name = parameters_df.iloc[0,1]
	return(temp_exp_name, temp_end_year, temp_end_month, temp_rosetta, temp_gss_loc, temp_out_loc)


#Excute the code to actually run the function

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument("--file-path", type=str, required=True, help="Path to parameter file")
	args, unknowns = parser.parse_known_args()
	file_path = args.file_path

	main(file_path=file_path,)
	the_returned = main(file_path)
	exp_name = the_returned[0]
	end_year = str(the_returned[1])
	end_month = str(the_returned[2])
	final_month = int(the_returned[2]) + 1
	rosetta = the_returned[3]
	gene_specific_summary_loc = the_returned[4]
	out_loc = the_returned[5]

	#end_month = final_month +1
	if re.search('1',end_month):
		end_month = str('01')
		final_month = str('02')
	if re.search('2',end_month):
		end_month = str('02')
		final_month = str('03')
	if re.search('3',end_month):
		end_month = str('03')
		final_month = str('04')
	if re.search('4',end_month):	
		end_month = str('04')
		final_month = str('05')	
	if re.search('5',end_month):
		end_month = str('05')
		final_month = str('06')
	if re.search('6',end_month):
		end_month = str('06')
		final_month = str('07')	
	if re.search('7',end_month):
		end_month = str('07')
		final_month = str('08')
	if re.search('8',end_month):
		end_month = str('08')
		final_month = str('09')
	if re.search('9',end_month):
		end_month = str('09')
		final_month = str('10')
	if re.search('10',end_month):
		end_month = str('10')
		final_month = str('11')
	if re.search('11',end_month):
		end_month = str('11')
		final_month = str('12')
	if re.search('12',end_month):
		end_month = str('12')
		final_month = str('01')
		end_year = int(the_returned[1]) +1
		end_year = str(end_year)
	end_switch = '%s_%s' % (end_year, end_month)
	final_switch = '%s_%s' % (end_year, final_month)
	
out_name = '%s_CLINVAR-full-matirx.txt' %(exp_name)
all_name = '%s_CLINVAR-alleles-matirx.txt' %(exp_name)
vus_name = '%s_CLINVAR-vus-matirx.txt' %(exp_name)
plp_name = '%s_CLINVAR-plp-matirx.txt' %(exp_name)
sum_name = '%s_CLINVAR-monthly_summary.txt' %(exp_name)
##############################################
#PART ONE
# set up key dictionaries 
master_id_dict = {}         #
ensembl_id_dict = {}        # entrez_id (key )/ ensembl
dict_of_dicts = {}

#Import rosetta file (Entrez, Ensembl, Gene Symbols)
file_ensembl = open(rosetta, "r")
for line in file_ensembl:
	line1 = re.split(r'\t+', line)
	temp = (line1[0])

	id_entrez = line1[0]
	if id_entrez == "":
		continue
	id_ensembl = line1[1]
	id_symbol_entrez = line1[2]
	#id_symbol_ensg = line1[3]
	#id_symbol_ensg = id_symbol_ensg.rstrip()
	#ensembl_id_dict[id_entrez] = [id_symbol_entrez, id_ensembl, id_symbol_ensg]
	ensembl_id_dict[id_entrez] = [id_symbol_entrez, id_ensembl]

#############################################
#PART TWO - LOOP DE LOOP
# loop to make dictionaries and to store each the number plp / vus / total variants for each month 
loop_years = ["2016", "2017", "2018", "2019", "2020", "2021", "2022", "2023", "2024", "2025", "2026", "2027", "2028", "2029", "2030", "2031", "2032", "2033"]
loop_month = ["01","02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
loop_type = ["all", "vus", "plp"]
period_count = 0

for ly in loop_years:					#for each year in window
	if (ly > end_year):
		#print("Beginning:\t", ly)
		break
	for lm in loop_month:				#for each month in window
		
		if re.search('2016',ly) and re.search('01|02|03|04',lm):	
			continue	

		period = '%s_%s' % (ly,lm)
		print ("OPENING", period)	
		if ly == end_year:
			if lm == final_month:
				print("SKIPPING PERIOD: ", period)
				break
							
		period_count = period_count + 1
		name_dict = 'dict_%s_%s' % (ly, lm)
		name_head = '%s_%s' % (ly, lm) 	
		globals()[f'dict_{ly}_{lm}'] = {}
		dict_of_dicts[name_dict] = name_dict

		#open up monthly ClinVar file 
		monthly_name = '%s-gene_specific_summary.txt' % (period)
		file_loc = '%s/%s' % (gene_specific_summary_loc , monthly_name)
		monthly_file = open(file_loc, "r")

		for line in monthly_file:
			line1 = re.split(r'\t+', line)
			temp = (line1[0])
			if re.match('#', temp ):
				continue
			ent_id = line1[1]	
			master_id_dict[ent_id] = ent_id
			alleles = line1[3]
			plp = line1[5]
			if plp == '-':
				plp = 0
			vus = line1[7]
			if vus == '-':
				vus = 0
			globals()[f'dict_{ly}_{lm}'][ent_id] = [alleles, vus, plp]

		monthly_file.close()

print("Ingestion Complete\n")
######################################			
# Fill in blank data for genes not in earlier versions
#######################################

gene_count = 0
missing_ensg = 0
empty_months = 0

#Make master gene list df
master_df = pd.DataFrame.from_dict(master_id_dict, orient='index', columns=['ENTREZ'])
	
print("Beginning Data Cleaning and Formatting")

#in each month  
for ly in loop_years:
	if (ly > end_year):
		break
	for lm in loop_month:
		break_switch = '%s_%s' % (ly,lm)
		period = '%s_%s' % (ly,lm)
		if re.search('2016',ly) and re.search('01|02|03|04',lm):		
			continue
		if (period == final_switch):
			break
		
		for entrez_id in master_id_dict:
			gene_count = gene_count + 1

			check = globals()[f'dict_{ly}_{lm}'].get(entrez_id)
			check == str(globals()[f'dict_{ly}_{lm}'].get(entrez_id))
					
			if check == None:	
				globals()[f'dict_{ly}_{lm}'][entrez_id] = ["NA","NA","NA"]
				empty_months = empty_months + 1
		
			check2 = ensembl_id_dict.get(entrez_id)
			check2 = str(ensembl_id_dict.get(entrez_id))

			if check2 == 'None':
				missing_ensg = missing_ensg + 1
				ensembl_id_dict[entrez_id] =  ["NA","NA","NA"]

		#store 
		globals()[f'df_{ly}_{lm}'] = pd.DataFrame.from_dict(globals()[f'dict_{ly}_{lm}'], orient='index')	
		#rename
		temp_all = "%s_%s-all" %(ly, lm)
		temp_vus = "%s_%s-vus" %(ly, lm)		
		temp_plp = "%s_%s-plp" %(ly, lm)
		globals()[f'df_{ly}_{lm}'].columns = [temp_all, temp_vus, temp_plp]
		#sort
		globals()[f'df_{ly}_{lm}'].sort_index()
		#check

		#print(ly, lm)
		#print(globals()[f'df_{ly}_{lm}'].head())
		#print( len(master_id_dict), ly,lm, ":", len(globals()[f'dict_{ly}_{lm}']))
		#combine
		frames = [master_df, globals()[f'df_{ly}_{lm}']]
		master_df = pd.concat(frames, axis=1)
		#print(master_df.head())
	


#print(master_df.head())

##########################################
# NEW VERSION
#########################################

rosetta_df = pd.DataFrame.from_dict(ensembl_id_dict, orient='index')
rosetta_df.sort_index()
rosetta_df = rosetta_df.set_axis(axis=1, labels=['NCBI-SYM', 'ENSG-ID', 'ENSG-SYM'])
rosetta_df = rosetta_df.tail(-1)
column_headers = list(rosetta_df.columns.values)
frames = [rosetta_df, master_df]
df = pd.concat([rosetta_df, master_df], axis=1)

############################################

#drop empty rows
df1 =  df.dropna(axis=0, thresh=9)
df1 = df1.drop('ENTREZ', axis=1)
df1 = df1.drop('ENSG-SYM', axis=1)
df1.index.name = 'NCBI-ID'
df1 = df1.sort_values(['ENSG-ID', 'NCBI-ID'], ascending = [True, True])

df_all = df1.iloc[:, : 2]
df_temp = df1.filter(regex='all')
frames = [df_all, df_temp]
df_all = pd.concat(frames, axis=1)

df_vus = df1.iloc[:, : 2]
df_temp = df1.filter(regex='vus')
frames = [df_vus, df_temp]
df_vus = pd.concat(frames, axis=1)

df_plp = df1.iloc[:, : 2]
df_temp = df1.filter(regex='plp')
frames = [df_plp, df_temp]
df_plp = pd.concat(frames, axis=1)

out_file = '%s/%s' %(out_loc,out_name )
out_all = '%s/%s' %(out_loc, all_name)
out_vus = '%s/%s' %(out_loc, vus_name)
out_plp = '%s/%s' %(out_loc, plp_name)

df1.to_csv(out_file, sep='\t')
df_all.to_csv(out_all, sep='\t')
df_vus.to_csv(out_vus, sep='\t')
df_plp.to_csv(out_plp, sep='\t')
print("Complete")
