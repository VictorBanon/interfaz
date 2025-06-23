from pathlib import Path

def taxon_rst(file_path:Path,link_list,taxon)->None:

    content = f"""{taxon}  
==============

.. toctree::
    :maxdepth: 2
    :caption: Contents:

"""
    content += "\n".join(link_list)
    file_path.write_text(content, encoding='utf-8')