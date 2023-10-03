##################################################
#
# VARIANTS FROM STATIC GENE LIST 
#
# i.e. open the huge matrix and extract the variants for each gene in a gene list

##################################################

# This script queires the huge matrix made by the 3-1 PanelVan
# It produces 4 outputs, the total number of alleles, the number of vuses, the number of plp variants, and a combined matrix which shows all three

# Alan Robertson
# 2023-05-19

################

import pandas as pd
import time
import argparse

#############################3
# Variables for ARG
#############################

def main(file_path: str):
	parameters_df = pd.read_csv(file_path,sep="\t")
	temp_experimental_name = parameters_df.iloc[0,1]
	temp_matrix_loc = parameters_df.iloc[1,1] 
	temp_matrix_name = parameters_df.iloc[2,1]
	temp_matrix_all = parameters_df.iloc[3,1]
	temp_matrix_vus = parameters_df.iloc[4,1]
	temp_matrix_plp = parameters_df.iloc[5,1]
	temp_gene_list = parameters_df.iloc[6,1]
	temp_gene_loc = parameters_df.iloc[7,1]
	temp_out_loc = parameters_df.iloc[8,1]
	return(temp_experimental_name, temp_matrix_loc, temp_matrix_name, temp_matrix_all, temp_matrix_vus, temp_matrix_plp, temp_gene_list, temp_gene_loc, temp_out_loc) 

#Excute the code to actually run the function

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument("--file-path", type=str, required=True, help="Path to parameter file")
	args, unknowns = parser.parse_known_args()
	file_path = args.file_path

	main(file_path=file_path,)
	the_returned = main(file_path)
	exp_name = the_returned[0]
	mat_loc = the_returned[1]
	mat_name = the_returned[2]
	mat_all = the_returned[3] 
	mat_vus = the_returned[4]
	mat_plp = the_returned[5] 
	gl_name = the_returned[7]
	gl_loc = the_returned[6]
	out_loc = the_returned[8] 

	#Check
	print('experiment name:\t', exp_name)
	print('gene loc:\t', gl_loc)
	print('gene names:\t', gl_name)
	print('out location:\t', out_loc)

	outfile = '%s-full.txt' % (exp_name)
	out_all = '%s-alleles.txt' % (exp_name)
	out_vus = '%s-vus.txt' % (exp_name)
	out_plp = '%s-plp.txt' % (exp_name)

	matrix_file = '%s/%s' %(mat_loc, mat_name)
	all_file = '%s/%s' %(mat_loc, mat_all)
	vus_file= '%s/%s' %(mat_loc, mat_vus)
	plp_file = '%s/%s' %(mat_loc, mat_plp)

	genelist_file = '%s/%s' %(gl_loc, gl_name)
	
##########################
# Read in Raw Data
##########################

mat_df = pd.read_csv(matrix_file, sep='\t', header=0)

all_df = pd.read_csv(all_file, sep='\t', header=0)
vus_df = pd.read_csv(vus_file, sep='\t', header=0)
plp_df = pd.read_csv(plp_file, sep='\t', header=0)

##############################
# Read in Gene List
#############################3

gl_df = pd.read_csv(genelist_file, sep='\t', header=0)

mat_df = mat_df.set_index('NCBI-ID')
all_df = all_df.set_index('NCBI-ID')
vus_df = vus_df.set_index('NCBI-ID')
plp_df = plp_df.set_index('NCBI-ID')

gl_df = gl_df.set_index('NCBI-ID')
gl_df.index.names = ['NCBI-ID']
gl_df.sort_index()

#print(mat_df.head())
#print(gl_df.head())

df = mat_df.merge(gl_df, how='right', on='NCBI-ID') 
#df = df.drop(columns=['ENSG-SYMBOL','NCBI-ID'])

df_all = all_df.merge(gl_df, how='right', on='NCBI-ID')
#df_all = df_all.drop(columns=['ENSG-SYMBOL','NCBI-ID'])
df_vus = vus_df.merge(gl_df, how='right', on='NCBI-ID')
#df_vus = df_vus.drop(columns=['ENSG-SYMBOL','NCBI-ID'])
df_plp = plp_df.merge(gl_df, how='right', on='NCBI-ID')
#df_plp = df_plp.drop(columns=['ENSG-SYMBOL','NCBI-ID'])

out_file = '%s/%s' % (out_loc, outfile)
df.to_csv(out_file, sep='\t')

out_file = '%s/%s' % (out_loc, out_all)
df_all.to_csv(out_file, sep='\t')

out_file = '%s/%s' % (out_loc, out_vus)
df_vus.to_csv(out_file, sep='\t')

out_file = '%s/%s' % (out_loc, out_plp)
df_plp.to_csv(out_file, sep='\t')

