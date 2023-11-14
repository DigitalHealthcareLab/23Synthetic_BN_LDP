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

file_name = "LUNG_PT_BSNF"

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

    data = data.dropna(subset=data.columns[1:-1],how='any')
    data = data.drop('BSPT_FRST_DIAG_YMD',axis=1)
    data = data.rename(columns={'TIME':"BSPT_FRST_DIAG_YMD"})

    data = data.drop_duplicates(subset='PT_SBST_NO')

    original_path = PROJ_PATH.joinpath(f'/home/dogu86/lung_synthesis/data/raw/{file_name}.xlsx')
    original_data = pd.read_excel(original_path)
    head = pd.read_excel(original_path, nrows = 0)

    data['BSPT_BRYM'] = data['BSPT_FRST_DIAG_YMD'] - pd.to_timedelta(data['BSPT_AGE']*365, 'days')
    data = data.rename(columns={'BSPT_AGE':"BSPT_IDGN_AGE"})
    dead = pd.read_excel(f'/mnt/synthetic_data/lung/data/processed/3_postprocess/LUNG_DEAD_NFRM_{args.epsilon}.xlsx')
    dead['PT_SBST_NO'] = dead['PT_SBST_NO'].astype('str')
    dead = dead.rename(columns={'DEAD_YMD':"BSPT_DEAD_YMD"})

    data = pd.merge(data,dead[['PT_SBST_NO','BSPT_DEAD_YMD']],how='left',on='PT_SBST_NO')

    oprt = pd.read_excel(f'/mnt/synthetic_data/lung/data/processed/3_postprocess/LUNG_OPRT_NFRM_{args.epsilon}.xlsx')
    oprt['PT_SBST_NO'] = oprt['PT_SBST_NO'].astype('str')
    oprt = oprt.drop_duplicates(subset='PT_SBST_NO')
    oprt = oprt.rename(columns={"OPRT_YMD":"BSPT_FRST_OPRT_YMD"})

    data = pd.merge(data,oprt[['PT_SBST_NO','BSPT_FRST_OPRT_YMD']],how='left',on='PT_SBST_NO')

    rdt = pd.read_excel(f'/mnt/synthetic_data/lung/data/processed/3_postprocess/LUNG_TRTM_RD_{args.epsilon}.xlsx')
    rdt['PT_SBST_NO'] = rdt['PT_SBST_NO'].astype('str')
    rdt = rdt.rename(columns={"RDT_STRT_YMD":"BSPT_FRST_RDT_STRT_YMD"})

    data = pd.merge(data,rdt[['PT_SBST_NO','BSPT_FRST_RDT_STRT_YMD']],how='left',on='PT_SBST_NO')

    reference1 = original_data[['BSPT_FRST_DIAG_CD','BSPT_FRST_DIAG_NM']].drop_duplicates().reset_index(drop=True)
    head = pd.read_excel(original_path, nrows = 0)
    head = head.drop(columns=["BSPT_FRST_DIAG_CD","BSPT_FRST_DIAG_NM"])
    data = pd.concat([head,data])

    data = data.merge(reference1, how='left', on='BSPT_FRST_DIAG_CD')

    regn = pd.read_excel(f'/mnt/synthetic_data/lung/data/processed/3_postprocess/LUNG_TRTM_CASB_{args.epsilon}.xlsx')
    regn['PT_SBST_NO'] = regn['PT_SBST_NO'].astype('str')

    regn_info = []
    for i in regn['PT_SBST_NO'].unique():
        grouped = regn[regn['CSTR_CYCL_VL'] == 1].groupby(by='PT_SBST_NO').get_group(i)
        start = grouped['CSTR_STRT_YMD'].iloc[0]
        end = grouped['CSTR_END_YMD'].iloc[-1]
        regn_info.append([i,start,end])

    regn_info_pd = pd.DataFrame(regn_info,columns=['PT_SBST_NO','CSTR_STRT_YMD','CSTR_END_YMD'])

    a = data.copy()
    #dead_ymd = pd.merge(a['PT_SBST_NO'],dead[['PT_SBST_NO','BSPT_DEAD_YMD']], on='PT_SBST_NO', how='left')['BSPT_DEAD_YMD']
    #oprt_ymd = pd.merge(a['PT_SBST_NO'],oprt[['PT_SBST_NO','OPRT_YMD']], on='PT_SBST_NO', how='left')['OPRT_YMD']
    #rdt_ymd = pd.merge(a['PT_SBST_NO'],rdt[['PT_SBST_NO','RDT_STRT_YMD']], on='PT_SBST_NO', how='left')['RDT_STRT_YMD']
    regn_strt_ymd = pd.merge(a['PT_SBST_NO'],regn_info_pd[['PT_SBST_NO','CSTR_STRT_YMD']], on='PT_SBST_NO', how='left')['CSTR_STRT_YMD']

    data['BSPT_FRST_ANCN_TRTM_STRT_YMD'] = regn_strt_ymd

    dtypes = head.dtypes.to_dict()
    data = data.astype(dtypes)
    data['BSPT_BRYM']= data['BSPT_BRYM'].astype('datetime64[ns]')
    data['BSPT_FRST_DIAG_YMD']= data['BSPT_FRST_DIAG_YMD'].astype('datetime64[ns]')
    data['BSPT_FRST_OPRT_YMD']= data['BSPT_FRST_OPRT_YMD'].astype('datetime64[ns]')
    data['BSPT_FRST_RDT_STRT_YMD']= data['BSPT_FRST_RDT_STRT_YMD'].astype('datetime64[ns]')
    data['BSPT_FRST_ANCN_TRTM_STRT_YMD']= data['BSPT_FRST_ANCN_TRTM_STRT_YMD'].astype('datetime64[ns]')
    data['BSPT_DEAD_YMD']= data['BSPT_DEAD_YMD'].astype('datetime64[ns]')

    data['CENTER_CD'] = 00000
    data['IRB_APRV_NO'] = '2-2222-02-22'
    data['CRTN_DT'] = '2023-10-20'

    data = data[original_data.columns]


    data.to_excel(OUTPUT_PATH.joinpath(f'{file_name}_{args.epsilon}.xlsx'))
    pass

if __name__ == "__main__":
    main()