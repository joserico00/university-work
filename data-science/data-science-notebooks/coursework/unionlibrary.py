import nbformat as nbf
import os
import glob

# Define a function to combine notebooks
def combine_notebooks(filenames):
    merged_notebook = nbf.v4.new_notebook()
    for filename in filenames:
        with open(filename) as f:
            notebook = nbf.read(f, as_version=4)
            merged_notebook.cells.extend(notebook.cells)
    return merged_notebook

# Gather list of all ipynb files
ipynb_files = glob.glob('*.ipynb')

# Combine notebooks
merged = combine_notebooks(ipynb_files)

# Write the combined notebook to a new file
with open('merged_notebook.ipynb', 'w') as f:
    nbf.write(merged, f)
