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

file_name = "LUNG_DEAD_NFRM"

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

    #%%
    data = data.query('DEAD == 1').reset_index(drop=True)

    #%%
    data = data.drop(columns = "DEAD")
    data = data.rename(columns={'TIME':"DEAD_YMD"})

    original_path = PROJ_PATH.joinpath(f'data/raw/{file_name}.xlsx')
    head = pd.read_excel(original_path, nrows=0)
    data = pd.concat([head, data])
    #%%

    data['CENTER_CD'] = 00000
    data['IRB_APRV_NO'] = '2-2222-02-22'
    data['CRTN_DT'] = '2023-10-20'
    dtypes = head.dtypes.to_dict()
    #%%
    data['DEAD_YMD']= data['DEAD_YMD'].astype('datetime64[ns]')
    data = data.astype(dtypes)

    data.to_excel(OUTPUT_PATH.joinpath(f'{file_name}_{args.epsilon}.xlsx'),index=False)
    pass

if __name__ == "__main__":
    main()