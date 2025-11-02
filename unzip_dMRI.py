
import zipfile
import gzip
import os,io,sys
import re, nilearn
from nilearn import image, input_data
from scipy.io import savemat
import numpy as np



output_dir = 'HCP_dMRI'


for Dir,_,file_names in os.walk('raw_data\\'): 
    for file_name in file_names:
        if file_name[7:16] == 'Diffusion' and file_name[-1] == 'p':
            id = file_name[0:6]
            with zipfile.ZipFile('raw_data\\'+file_name, 'r') as zip_ref:
                zip_ref.extractall(output_dir)

            print(f"Extracted contents of '{file_name}' to '{output_dir}'")