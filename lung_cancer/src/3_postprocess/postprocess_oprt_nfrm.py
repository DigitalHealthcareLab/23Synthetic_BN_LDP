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

file_name = "LUNG_OPRT_NFRM"

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

    data = data.dropna(subset=['OPRT_LUCN_OPRT_KIND_CD'])
    data = data.drop_duplicates(subset=['PT_SBST_NO','OPRT_LUCN_OPRT_KIND_CD'])
    data = data.rename(columns={"TIME":"OPRT_YMD"})

    original_path = PROJ_PATH.joinpath(f'data/raw/{file_name}.xlsx')

    original_data = pd.read_excel(original_path)

    reference1 = original_data[['OPRT_LUCN_OPRT_KIND_CD','OPRT_LUCN_OPRT_KIND_NM']].drop_duplicates().reset_index(drop=True)
    head = pd.read_excel(original_path, nrows = 0)
    head = head.drop(columns=["OPRT_EDI_CD","OPRT_NM"])
    data = pd.concat([head,data])

    data = data.drop(columns='OPRT_LUCN_OPRT_KIND_NM')
    data = data.merge(reference1, how='left', on='OPRT_LUCN_OPRT_KIND_CD')
    data = data.drop(data[data['OPRT_LUCN_OPRT_KIND_CD']==99].index)
    data = data.drop(data[data['OPRT_LUCN_OPRT_KIND_CD']==15].index)
    data['CENTER_CD'] = 00000
    data['IRB_APRV_NO'] = '2-2222-02-22'
    data['CRTN_DT'] = '2023-10-20'
    data['OPRT_SEQ'] = 1
    dtypes = head.dtypes.to_dict()

    data = data.astype(dtypes)
    data['OPRT_YMD']= data['OPRT_YMD'].astype('datetime64[ns]')
    data = data[head.columns]

    data=data.dropna(subset='OPRT_LUCN_OPRT_KIND_NM')

    data.to_excel(OUTPUT_PATH.joinpath(f'{file_name}_{args.epsilon}.xlsx'))
    pass

if __name__ == "__main__":
    main()