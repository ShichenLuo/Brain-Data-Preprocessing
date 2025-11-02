import os
import subprocess
import sys
from pathlib import Path

def p(*parts):
    return os.path.join(*parts)

def process_subject_dir(output_directory,subject_dir,t1_directory,altas_directory):
    print(f"\nProcessing subject in directory: {subject_dir}")
    # === Step 1: Convert DWI and brain mask
    subprocess.run(f"mrconvert {subject_dir}data.nii.gz {output_directory}dwi.mif -fslgrad {subject_dir}bvecs {subject_dir}bvals")

    subprocess.run(f"mrconvert {subject_dir}nodif_brain_mask.nii.gz {output_directory}mask.mif")

    # === Step 2: Extract mean b=0 image
    subprocess.run(f"dwiextract {output_directory}dwi.mif - -bzero | mrmath - mean {output_directory}mean_b0.mif -axis 3",shell=True, check=True)

    # === Step 3: Convert T1 image
    subprocess.run(f"mrconvert {t1_directory}T1w_acpc_dc_restore_1.25.nii.gz {output_directory}T1.mif")

    # === Step 4: Create brain mask from T1 using nibabel
    subprocess.run(f"mrthreshold {output_directory}T1.mif -abs 0.000001 {output_directory}T1_mask.mif")

    # === Step 5: Nonlinear registration
    subprocess.run(f"mrregister {output_directory}T1.mif {output_directory}mean_b0.mif -mask1 {output_directory}T1_mask.mif -mask2 {output_directory}mask.mif \
                -nl_warp {output_directory}warp_forward.mif {output_directory}warp_inverse.mif")
    
    # === Step 6: Align parcellation
    subprocess.run(f"mrconvert {altas_directory}AAL.nii {output_directory}AAL_orig.mif")
    subprocess.run(f"labelconvert {output_directory}AAL_orig.mif {altas_directory}aal_LUT.txt {altas_directory}aal_index.txt {output_directory}AAL_indexed.mif")
    subprocess.run(f"mrtransform {output_directory}AAL_indexed.mif -template {output_directory}mean_b0.mif -interp nearest {output_directory}AAL_regrid.mif", shell=True, check=True)
    subprocess.run(f"mrtransform {output_directory}AAL_regrid.mif -template {output_directory}mean_b0.mif -interp nearest {output_directory}AAL_centered.mif", shell=True, check=True)
    subprocess.run(f"mrtransform {output_directory}AAL_centered.mif -template {output_directory}mean_b0.mif -interp nearest {output_directory}parcellation_dwi.mif", shell=True, check=True)
    
    # === Step 7: Estimate FOD
    cmd = (f"dwi2response dhollander {output_directory}dwi.mif {output_directory}wm.txt {output_directory}gm.txt {output_directory}csf.txt -mask {output_directory}mask.mif")
    subprocess.run(['bash', '-c', cmd], check=True)
    # cmd = (f"dwi2fod msmt_csd {output_directory}dwi.mif {output_directory}wm.txt {output_directory}wm_fod.mif {output_directory}gm.txt {output_directory}gm.mif\
    #                 {output_directory}csf.txt {output_directory}csf.mif -mask {output_directory}mask.mif")

    cmd = [
    "dwi2fod", "msmt_csd",
    p(output_directory, "dwi.mif"),
    p(output_directory, "wm.txt"),  p(output_directory, "wm_fod.mif"),
    p(output_directory, "gm.txt"),  p(output_directory, "gm.mif"),
    p(output_directory, "csf.txt"), p(output_directory, "csf.mif"),
    "-mask", p(output_directory, "mask.mif"),
    "-lmax", "8,0,0",
    "-nthreads", "1",
    "-force", "-debug"
    ]

    # print("CMD ARGS:", cmd)  # inspect the exact paths
    subprocess.run(cmd, check=True)
    # subprocess.run(['bash', '-c', cmd], check=True)

    # === Step 8: Tractogram and connectome
    subprocess.run(f"tckgen {output_directory}wm_fod.mif {output_directory}tracks.tck -seed_dynamic {output_directory}wm_fod.mif -select 5M -cutoff 0.06 -mask {output_directory}mask.mif", shell=True, check=True)
    subprocess.run(f"tcksift2 {output_directory}tracks.tck {output_directory}wm_fod.mif {output_directory}sift2_weights.txt")
    subprocess.run(f"tck2connectome {output_directory}tracks.tck {output_directory}parcellation_dwi.mif {output_directory}connectome.csv \
                -tck_weights_in {output_directory}sift2_weights.txt -zero_diagonal -symmetric -scale_invnodevol", shell=True, check=True)
    for filename in os.listdir(output_directory):
        file_path = os.path.join(output_directory, filename)
        if filename != "connectome.csv" and os.path.isfile(file_path):
            os.remove(file_path)
    print(f"Processing complete for {output_directory[:-1]}")

# === Call this with the correct path ===
source = "HCP_dMRI/"
for dir in os.listdir(source): 
    print(dir)
    ID = dir
    subject_directory = f"{source}/{ID}/T1w/Diffusion/"
    t1_directory = f"{source}/{ID}/T1w/"
    altas_directory = "./" #atlas, aal_index.txt, aal_LUT.txt
    output_directory = f'Processed_dMRI/{ID}/'
    os.makedirs(output_directory, exist_ok=True)
    process_subject_dir(output_directory,subject_directory,t1_directory,altas_directory)
