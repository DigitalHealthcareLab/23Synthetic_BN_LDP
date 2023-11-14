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

file_name = "LUNG_TRTM_CASB"

# %%
def load_file_epsilon(epsilon):
    return read_file(INPUT_PATH, f'{file_name}_{epsilon}.pkl')


# Define a custom function to calculate and fill null values
def fill_null_with_calculated_value(column):
    result = []
    calculated_value = None

    for i, value in enumerate(column):
        if pd.notna(value):
            result.append(value)
        else:
            calculated_value = column.iloc[i+1] - pd.to_timedelta(28, 'days')
            result.append(calculated_value)
            
    return result


#%%
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--epsilon', '--e', help="epsilon values")
    args = parser.parse_args()
#%%
    data = load_file_epsilon(args.epsilon)

    data = data.rename(columns = {'TIME':'CSTR_STRT_YMD'})
    data = data.dropna(subset=['CSTR_CLSF_NM', 'CSTR_PRPS_CD'], how='any')
    data['CSTR_END_YMD'] = data['CSTR_STRT_YMD'] + pd.to_timedelta(28, 'days') # need to check quantity of additonal
    data['CSTR_CYCL_VL'] = data.groupby(['PT_SBST_NO','CSTR_PRPS_CD']).cumcount()+1

    grouped = data.groupby(['PT_SBST_NO', 'CSTR_PRPS_CD'])
    data['CSTR_STRT_YMD'] = grouped['CSTR_END_YMD'].shift(1)
    data['CSTR_STRT_YMD'] = grouped['CSTR_STRT_YMD'].apply(lambda x: x.fillna('2222-02-22'))

    original_path = PROJ_PATH.joinpath(f'data/raw/{file_name}.xlsx')
    original_data = pd.read_excel(original_path)
    head = pd.read_excel(original_path, nrows=0)
    data = data.drop(data[data['CSTR_PRPS_CD']==0].index)
    data = data.drop(data[data['CSTR_PRPS_CD']==121].index)
    data = pd.concat([head, data])
    
    reference1 = original_data[['CSTR_PRPS_CD','CSTR_PRPS_NM']].drop_duplicates().reset_index(drop=True)
    data = data.drop(columns='CSTR_PRPS_NM')
    data = data.merge(reference1, how='left', on='CSTR_PRPS_CD')



    data['CENTER_CD'] = 00000
    data['IRB_APRV_NO'] = '2-2222-02-22'
    data['CRTN_DT'] = '2023-10-20'
    data['CSTR_SEQ'] = 1

    dtypes = head.dtypes.to_dict()
    data = data.astype(dtypes)
    
    data['CSTR_STRT_YMD']= data['CSTR_STRT_YMD'].astype('datetime64[ns]')
    data['CSTR_END_YMD']= data['CSTR_END_YMD'].astype('datetime64[ns]')
    data['CSTR_STRT_YMD'] = fill_null_with_calculated_value(data['CSTR_STRT_YMD'])
    data = data[head.columns]

    data.to_excel(OUTPUT_PATH.joinpath(f'{file_name}_{args.epsilon}.xlsx'))
    pass

if __name__ == "__main__":
    main()