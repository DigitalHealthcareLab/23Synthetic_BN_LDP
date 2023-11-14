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

file_name = "LUNG_PTH_SRGC"

# %%
def load_file_epsilon(epsilon):
    return read_file(INPUT_PATH, f'{file_name}_{epsilon}.pkl')




#%%
# 여기서 데이터를 조금 정제해야 함

#%%
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--epsilon', '--e', help="epsilon values")
    args = parser.parse_args()
#%%
    data = load_file_epsilon(args.epsilon)

    data = data.rename(columns = {'TIME':'SGPT_ACPT_YMD'})
    data["SGPT_READ_YMD"] = data["SGPT_ACPT_YMD"] + pd.to_timedelta(3, 'days')
    
    data.drop(data[data['SGPT_LUNGM_SIZE_VL']==0].index)
    
    original_path = PROJ_PATH.joinpath(f'data/raw/{file_name}.xlsx')
    head = pd.read_excel(original_path, nrows=0)

    data = data.dropna(subset=data.columns[2:-1],how='all')
    
    #head = head.drop(columns=['SGPT_LN_DSCT_CONT','SGPT_MTST_LMP_SITE_CONT','SGPT_PATL_ETC_STAG_VL'])

    data = pd.concat([head, data])

    ### T = 1
    data.loc[(data['SGPT_PATL_T_STAG_VL']==1) & (data['SGPT_PATL_N_STAG_VL']==0), 'SGPT_PATL_STAG_VL'] = 1
    data.loc[(data['SGPT_PATL_T_STAG_VL']==1) & (data['SGPT_PATL_N_STAG_VL']==1), 'SGPT_PATL_STAG_VL'] = 2
    data.loc[(data['SGPT_PATL_T_STAG_VL']==1) & (data['SGPT_PATL_N_STAG_VL']==2), 'SGPT_PATL_STAG_VL'] = 3
    data.loc[(data['SGPT_PATL_T_STAG_VL']==1) & (data['SGPT_PATL_N_STAG_VL']==3), 'SGPT_PATL_STAG_VL'] = 3

    # T = 2
    data.loc[(data['SGPT_PATL_T_STAG_VL']==2) & (data['SGPT_PATL_N_STAG_VL']==0), 'SGPT_PATL_STAG_VL'] = 1
    data.loc[(data['SGPT_PATL_T_STAG_VL']==2) & (data['SGPT_PATL_N_STAG_VL']==1), 'SGPT_PATL_STAG_VL'] = 2
    data.loc[(data['SGPT_PATL_T_STAG_VL']==2) & (data['SGPT_PATL_N_STAG_VL']==2), 'SGPT_PATL_STAG_VL'] = 3
    data.loc[(data['SGPT_PATL_T_STAG_VL']==2) & (data['SGPT_PATL_N_STAG_VL']==3), 'SGPT_PATL_STAG_VL'] = 3

    # T = 3
    data.loc[(data['SGPT_PATL_T_STAG_VL']==3) & (data['SGPT_PATL_N_STAG_VL']==0), 'SGPT_PATL_STAG_VL'] = 2
    data.loc[(data['SGPT_PATL_T_STAG_VL']==3) & (data['SGPT_PATL_N_STAG_VL']==1), 'SGPT_PATL_STAG_VL'] = 3
    data.loc[(data['SGPT_PATL_T_STAG_VL']==3) & (data['SGPT_PATL_N_STAG_VL']==2), 'SGPT_PATL_STAG_VL'] = 3
    data.loc[(data['SGPT_PATL_T_STAG_VL']==3) & (data['SGPT_PATL_N_STAG_VL']==3), 'SGPT_PATL_STAG_VL'] = 3

    # T = 4
    data.loc[(data['SGPT_PATL_T_STAG_VL']==4) & (data['SGPT_PATL_N_STAG_VL']==0), 'SGPT_PATL_STAG_VL'] = 3
    data.loc[(data['SGPT_PATL_T_STAG_VL']==4) & (data['SGPT_PATL_N_STAG_VL']==1), 'SGPT_PATL_STAG_VL'] = 3
    data.loc[(data['SGPT_PATL_T_STAG_VL']==4) & (data['SGPT_PATL_N_STAG_VL']==2), 'SGPT_PATL_STAG_VL'] = 3
    data.loc[(data['SGPT_PATL_T_STAG_VL']==4) & (data['SGPT_PATL_N_STAG_VL']==3), 'SGPT_PATL_STAG_VL'] = 3

    # M = 1
    data.loc[data['SGPT_PATL_M_STAG_VL']==1, 'SGPT_PATL_STAG_VL'] = 4


    data['CENTER_CD'] = 00000
    data['IRB_APRV_NO'] = '2-2222-02-22'
    data['CRTN_DT'] = '2023-10-20'
    data['SGPT_SEQ'] = 1


    dtypes = head.dtypes.to_dict()
    data = data.astype(dtypes)

    data['SGPT_ACPT_YMD']= data['SGPT_ACPT_YMD'].astype('datetime64[ns]')
    data['SGPT_READ_YMD']= data['SGPT_READ_YMD'].astype('datetime64[ns]')

    data = data[head.columns]


    data.to_excel(OUTPUT_PATH.joinpath(f'{file_name}_{args.epsilon}.xlsx'))
    pass

if __name__ == "__main__":
    main()