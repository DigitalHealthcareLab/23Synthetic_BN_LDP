#%%
import pandas as pd
import numpy as np
import pickle
import os, sys
from pathlib import Path
import argparse


PROJ_PATH = Path('/home/dogu86/lung_synthesis')
sys.path.append(PROJ_PATH.joinpath('src').as_posix())

from MyModule.utils import *
config = load_config()
INPUT_PATH = Path('/mnt/synthetic_data/lung/data/processed/2_restore/restore_to_db_form')
OUTPUT_PATH = Path('/mnt/synthetic_data/lung/data/processed/3_postprocess')

if not OUTPUT_PATH.exists() :
    OUTPUT_PATH.mkdir(parents=True)

file_name = "LUNG_EX_PLMN"

# %%
def load_file_epsilon(epsilon):
    return read_file(INPUT_PATH, f'{file_name}_{epsilon}.pkl')


#%%
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--epsilon', '--e', help="epsilon values")
    args = parser.parse_args()
#%%
    data = load_file_epsilon(args.epsilon)

    original_path = PROJ_PATH.joinpath(f'data/raw/{file_name}.xlsx')
    head = pd.read_excel(original_path, nrows = 0)

    data_melted = pd.melt(data, id_vars=['PT_SBST_NO','TIME'])

    data_melted = data_melted.dropna(subset='value')
    data_melted = data_melted.drop_duplicates(subset=['PT_SBST_NO','TIME','value'])
    data_melted = data_melted.drop_duplicates(subset=['PT_SBST_NO','variable','value'])
    data_melted = data_melted.rename(columns ={'TIME':'PLEX_YMD','variable':'PLEX_NM','value':'PLEX_RSLT_VL'})
    
    original_data = pd.read_excel(original_path)
    head = pd.read_excel(original_path, nrows = 0)

    data_melted = pd.concat([head,data_melted])

    data_melted['CENTER_CD'] = 00000
    data_melted['IRB_APRV_NO'] = '2-2222-02-22'
    data_melted['CRTN_DT'] = '2023-10-20'
    data_melted['PLEX_SEQ'] = 0
    data_melted['PLEX_KIND_CD'] = 1
    data_melted['PLEX_KIND_NM'] = '호흡기능검사'

    dtypes = head.dtypes.to_dict()

    data_melted = data_melted.astype(dtypes)
    data_melted['PLEX_YMD']= data_melted['PLEX_YMD'].astype('datetime64[ns]')

    data_melted.to_excel(OUTPUT_PATH.joinpath(f'{file_name}_{args.epsilon}.xlsx'))
    pass

if __name__ == "__main__":
    main()