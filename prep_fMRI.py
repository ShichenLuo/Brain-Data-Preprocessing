import zipfile
import gzip
import os,io,sys
import re, nilearn
from nilearn import image, input_data
from scipy.io import savemat
import numpy as np
atlas = 'AAL.nii'

def extract_and_rename(zip_path, file_name, target_directory, new_name):
    print(f'reading {zip_path}')
    # Ensure target directory exists
    if not os.path.exists(target_directory):
        os.makedirs(target_directory)
    # Open the zip file
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        # Extract the specific file
            with zip_ref.open(target_gz) as zipped_gz:
                with gzip.GzipFile(fileobj=io.BytesIO(zipped_gz.read())) as unzipped_nii:
                    nii_data = unzipped_nii.read()

            # Write the uncompressed .nii file with new name
            output_path = os.path.join(target_directory, new_name)
            print(f'saving {output_path}')
            with open(output_path, 'wb') as f_out:
                f_out.write(nii_data)
    # sys.exit()
def read_nii(path):
    atlasimg = image.load_img(atlas)
    fmri_img = image.load_img(path)
    masker = input_data.NiftiLabelsMasker(labels_img=atlasimg,
                                        standardize=True,
                                        detrend=True,
                                        verbose=1)

    time_series = masker.fit_transform(fmri_img)
    time_series = time_series.transpose(1,0)
    return time_series

target_directory = 'data\HCP_fMRI'
new_name = 'newfilename.txt'
keys = ['ID', 'REST2', 'EMOTION', 'GAMBLING', 'LANGUAGE', 'MOTOR', 'RELATIONAL', 'SOCIAL', 'WM']
output = {i:[] for i in keys}
count=0
for Dir,_,file_names in os.walk('raw_data/'): 
    for file_name in file_names:
        if re.search('Rest',file_name) and file_name[-1]== 'p':
            target_gz = f'{file_name[0:6]}/MNINonLinear/Results/rfMRI_REST2_LR/rfMRI_REST2_LR_hp2000_clean_rclean_tclean.nii.gz'
            new_name = file_name[0:6]+'_rest.nii'
            if os.path.exists(target_directory+'/'+new_name):
                ts = read_nii(target_directory+'/'+new_name)
                output['ID'].append(file_name[0:6])
                output['REST2'].append(ts)
            else:
                extract_and_rename(Dir+file_name,target_gz,target_directory,new_name)
                ts = read_nii(target_directory+'/'+new_name)
                output['ID'].append(file_name[0:6])
                output['REST2'].append(ts)
        elif re.search('Task',file_name) and file_name[-1]== 'p':
            for task in keys[2:]:
                target_gz = f'{file_name[0:6]}/MNINonLinear/Results/tfMRI_{task}_LR/tfMRI_{task}_LR_hp0_clean_rclean_tclean.nii.gz'
                new_name = file_name[0:6]+f'_{task}.nii'
                if os.path.exists(target_directory+'/'+new_name):
                    ts = read_nii(target_directory+'/'+new_name)
                    output[task].append(ts)
                else:
                    extract_and_rename(Dir+file_name,target_gz,target_directory,new_name)
                    ts = read_nii(target_directory+'/'+new_name)
                    output[task].append(ts)
        count+=1
for key in keys[1:]:
    output[key] = np.array(output[key])


savemat('Processed_fMRI\output_temp.mat',output)

for filename in os.listdir(target_directory):
    if filename.endswith(".nii") or filename.endswith(".nii.gz"):
        file_path = os.path.join(target_directory, filename)
        os.remove(file_path)