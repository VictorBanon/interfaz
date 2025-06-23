#!/usr/bin/env -S uv run --script --quiet
# /// script
# requires-python = ?
# dependencies = ?
# ///

"""A simple python script template.

"""

import pandas as pd 
from pathlib import Path

from rst_maker_individual import individual_rst
from rst_maker_taxon import taxon_rst 


def tree_folder(df,taxon_list,path,taxon,path_data): 

    if len(taxon_list)>0:  
        link_list = []
        for unique_value in df[taxon_list[0]].unique():
            print(unique_value)
            df_taxon = df[df[taxon_list[0]]==unique_value]
            # create folder
            # Define folder and file paths
            folder = path/(unique_value.replace(" ","_"))
            file_path = path / 'index.rst'

            # Create folder (if it doesn't exist)
            folder.mkdir(parents=True, exist_ok=True) 

            # create subfolder
            tree_folder(df_taxon,taxon_list[1:],folder,unique_value,path_data) 
                    
            link_list.append(f"    {(unique_value.replace(" ","_"))}/index") 

        # Write text to the file
        taxon_rst(file_path,link_list,taxon)

    else:   
        path_data_files = path_data/path.name/"analysis"/f"chromosome_{path.name}_hc_all.html"
        individual_rst(path,path_data_files) 

def main():

    path_file = Path("/home/banongav/Documents/GitHub/2024-victor-IRs-Victor/results/12-rep")

    taxonomy = pd.read_csv(path_file/"taxonomy.csv") 
    taxon_list = ["superkingdom","phylum","class","order","family","genus","species","ID"]

    tree_folder(taxonomy,taxon_list,Path("./source/data"),"Data",path_file)

if __name__ == '__main__':
    main() 

