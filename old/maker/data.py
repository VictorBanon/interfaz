from pathlib import Path
import pandas as pd 
# Read CSV into DataFrame
df = pd.read_csv("maker/list_with_taxonomy.csv").fillna('Unclqssified')

# order family

taxon_list = [
  'superkingdom',
  'phylum',
  'class',
  'order',
  'family',
  'genus',
  'species',
  'strain',
  "#Organism Name"
]


def create_folder(folder_name,df, taxon_list,value=None):
    """TODO."""
    
    if taxon_list != []:  
        taxon = taxon_list[0] 
        pages=[]
        for unique_value in df[taxon].unique():
            # Create folder for each unique value in the specified taxon
            folder_path = Path(folder_name) / unique_value
            folder_path.mkdir(exist_ok=True)
            print(f"Created folder: {folder_path}")
            pages.append(folder_path.name+"/"+"index")

            create_folder(folder_path,df[df[taxon]==unique_value],taxon_list[1:],unique_value)

        page_list = '\n    '.join(pages)  # 4 spaces for each page

        import textwrap
        content = textwrap.dedent(f"""
Taxon: {value}
=========================================

.. toctree::
    :maxdepth: 2
    :caption: Contents:

    {page_list}
""")



        # Define the output path (for example, inside 'source' directory)
        output_path = Path(folder_name) / "index.rst" 
        # Write content to index.rst
        output_path.write_text(content.strip(), encoding='utf-8')
    
folder_path = Path("source/data")
create_folder(folder_path,df,taxon_list)

