from scipy.io import loadmat, savemat
import pandas as pd
import numpy as np
import sys,os

# mat1 = loadmat('output.mat')
mat_cur = loadmat('Processed_fMRI/output_temp.mat')


keys = ['ID', 'REST2', 'EMOTION', 'GAMBLING', 'LANGUAGE', 'MOTOR', \
'RELATIONAL', 'SOCIAL', 'WM']

# print(mat_cur)
if os.path.exists('Processed_fMRI/output_final.mat'):
    mat_tar = loadmat('Processed_fMRI/output_final.mat')
    mat_out = loadmat('Processed_fMRI/output_final.mat')
    for key in keys:
        if key=='ID':
            mat_out[key] = np.concatenate((mat_cur[key],mat_tar[key]),-1)
        else:
            mat_out[key] = np.concatenate((mat_cur[key],mat_tar[key]),0)

    assert mat_out['ID'].shape[0] == mat_tar['ID'].shape[0]+ mat_cur['ID'].shape[0]
    assert len(mat_out['ID']) == len(np.unique(mat_out['ID']))

    for key in keys:
        assert mat_out[key].shape[0] == mat_out['ID'].shape[0], f"Shape mismatch for {key}: {mat_out[key].shape[0]} != {mat_tar['ID'].shape[0]}"
    print(np.sort(mat_out['ID']).shape)

    savemat('Processed_fMRI/output_final.mat',mat_out)
else:
    savemat('Processed_fMRI/output_final.mat',mat_cur)
