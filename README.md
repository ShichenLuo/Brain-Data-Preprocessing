

## 1. Data Download
  ### (1) Go to website: https://balsa.wustl.edu/ and login.
 ### (2) Select ConnectomeDB and HCP-Young Adault 2025
<img width="415" height="133" alt="image" src="https://github.com/user-attachments/assets/f8b181bc-6661-4195-b9bc-0b9ffd8bcbcd" /># Brain-Data-Preprocessing
### (3) Find Subject ID and click.
### (4) Download the circled three files to “raw_data” directory .
<img width="415" height="47" alt="image" src="https://github.com/user-attachments/assets/5da591b3-507d-46f5-9e3f-d4b1ac876cc3" />


## 2. Process fMRI and dMRI data
### (1) Process fMRI data.
    #### (a) Run “Process_fMRI.bat”, or run“prep_fMRI.py” and “merge.py” sequentially.
        This script will process all fMRI-related files in the “raw_data” directory and generate two output files: “output_temp.mat” and “output_final.mat” in the “Processed_fMRI” directory.
        “output_temp.mat” contains the processed samples currently stored in “raw_data”.
        “output_final.mat” contains all processed data, including both the samples currently in “raw_data” and those processed previously.

### (2) Process dMRI data.
#### (a) Download and install MRtrix3.
#### (b) Run “unzip_dMRI.py” to extract the dMRI data.
#### (c) Launch MSYS2 MINGW64 (MRtrix3 terminal).
#### (d) In the opened terminal, run the command “python dMRI_to_graph.py”. (The output will be a directory, named according to the processed subject’s ID, genereated within the “Processed_dMRI” directory.)
#### (e) If the program crashes, delete the directory in “Processed_dMRI” that is named after the unsuccessfully processed subject’s ID.

### (3) Delete processed data.
#### Delete successfully processed data from “raw_data” directory.
#### Delete all files contained in the “HCP_dMRI” directory.
