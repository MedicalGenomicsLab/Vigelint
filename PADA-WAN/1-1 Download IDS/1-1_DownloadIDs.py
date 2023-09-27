#######################################
#
# DOWNLOAD IDs FROM PANELAPP
#
#######################################

#Introduction
#This script was written to download a list of panel IDS from PanelApp
#This script will work with both Genomics England instance of PanelApp as well as PanelApp Australia
#This script is the first part of the pipeline to download historic version of panels 

#To run this script, please make sure you set up the params file, then run the script on the command line
#i.e. python3 PanelApp_ID.py params.txt
#If you unsure about the token value in the params file, and if the token value provided here does not work, please, if not please consult the ReadMe.md 

#Alan Robertson
#2021-12-02

#Version 1.0 
#2023-04-26: Productionise script 

#Import modules
import argparse
import pandas as pd
import re
import requests
import time
from datetime import datetime
import pandas

#Setup global variables
version = ''
now = datetime.now()
now = now.strftime("%Y-%m-%d_%H-%M")

#Set up variables to allow downloads from multiple pages
count = 1
count_str = str(count)
rerun = "true"

#Open the params file 
#i.e. python3 this_script.py --file_path parameters.txt
 
#Define main function
def main(file_path: str):
	parameters_df = pd.read_csv(file_path,sep="\t")
	version = parameters_df.iloc[0,0]
	if re.search(r"AU", version, re.IGNORECASE):
		outdir = parameters_df.iloc[2,0]
		path = parameters_df.iloc[3,0]
		token = parameters_df.iloc[4,0]
	elif re.search(r"UK", version, re.IGNORECASE):
		outdir = parameters_df.iloc[5,0]
		path = parameters_df.iloc[6,0]
		token = parameters_df.iloc[7,0]
	return(version, outdir, path, token )

#Excute the code to actually import the params file and extract the key values 
if __name__ == "__main__":
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument("--file-path", type=str, required=True, help="Path to parameter file")
	args, unknowns = parser.parse_known_args()
	file_path = args.file_path

	#main(file_path=file_path,)
	the_returned = main(file_path)
	version = the_returned[0]
	outdir = the_returned[1]
	partial_path = the_returned[2]
	token = the_returned[3]

print("PanelApp Version:\t", version)
time.sleep(1)
	
#Prepare to connect to the PanelApp API
path = partial_path + count_str
headers = {
	'accept': 'application/json',
	'X-CSRFToken': token,
}
aDict={}
filename = "%s/%s_PA-%s_Panel_IDs.tsv" %(outdir,now,version)

#Setup output file
f = open(filename, "w")
f.write("Panel\tID\tVersion\tRelease-Date\tNo.Genes\tNo.STRs\tNo.Regions\tSuperPanel-Status\tSource\tDisease-Group\tPanelType\n")
print("Output file created")

#The solution to getting IDs from different pages of PA (i.e. if you want more than the first 100 panels)

while rerun == 'true':
	response = requests.get(path, headers=headers)
	check = response
	check_str = str(check)
	print('Panel App Page Number:', count,)
	data = response.json()
	for line in data['results']:
		b = "Panel"
		a = line['types']
		c = "Misc."
		for a1 in a:                            #for each list inside types
			a11 = a1['description']
			if re.search(r'uper', a11):
				b = "Super Panel"

			if re.search(r'uper',line['name']):
				b = "Super Panel"

			a22 = a1['slug']
			if re.search(r'rare', a22):
				c = "Rare Disease"

		print(line['name'], line["id"], line["version"], line["version_created"], line['stats']["number_of_genes"], line['stats']["number_of_strs"], line['stats']["number_of_regions"], b, version, line["disease_group"], c,sep="\t", file=f)

	count = count + 1
	count_str = str(count)
	path = partial_path + count_str
	response2 = requests.get(path, headers=headers)
	check_data = str(response2)
	print("Check:", check_data)
	if check_data != "<Response [200]>":
		rerun = "false"
		print('More Pages =',rerun)
	else:
        	print('More Pages =',rerun)
