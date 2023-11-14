#%%
import pandas as pd
import numpy as np
import pickle
import os, sys
from pathlib import Path
import argparse

from requests import head

PROJ_PATH = Path('/home/dogu86/colon_synthesis_2')
sys.path.append(PROJ_PATH.joinpath('src').as_posix())

from MyModule.utils import *
config = load_config()

PROJ_PATH = Path(config['path_config']['project_path'])

INPUT_PATH = PROJ_PATH.joinpath('/mnt/synthetic_data/data/processed/2_restore/restore_to_db_form/D0')
OUTPUT_PATH = PROJ_PATH.joinpath('/mnt/synthetic_data/data/processed/3_postprocess/')

if not OUTPUT_PATH.exists() :
    OUTPUT_PATH.mkdir(parents=True)

file_name = "CLRC_PT_BSNF"

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

    #data = data.dropna(subset=['OPRT_CLCN_OPRT_KIND_CD','OPRT_CURA_RSCT_CD'])

    #%%
    first_diag = data.groupby(['PT_SBST_NO','BSPT_FRST_DIAG_YMD'],as_index=False).TIME.min()

    #%%
    first_diag = first_diag.drop(columns =['BSPT_FRST_DIAG_YMD'])
    #%%
    first_diag = first_diag.rename(columns={'TIME':"BSPT_FRST_DIAG_YMD"})
    #%%
    data = data.drop(columns = ['TIME','BSPT_FRST_DIAG_YMD'])
    #%%
    data = data.drop_duplicates()
    data = data.merge(first_diag, on='PT_SBST_NO')

    data = data.dropna(subset=['BSPT_FRST_DIAG_CD','BSPT_IDGN_AGE'])

    #%%
    original_path = PROJ_PATH.joinpath(f'/mnt/synthetic_data/data/raw/{file_name}.xlsx')
    original_data = pd.read_excel(original_path)
    head = pd.read_excel(original_path, nrows = 0)
    #%%
    head

    #%%
    data['BSPT_BRYM'] = data['BSPT_FRST_DIAG_YMD'] - pd.to_timedelta(data['BSPT_IDGN_AGE']*365, 'days')

    dead = pd.read_excel(f'/mnt/synthetic_data/data/processed/3_postprocess/CLRC_DEAD_NFRM_{args.epsilon}.xlsx')
    dead['PT_SBST_NO'] = dead['PT_SBST_NO'].astype('str')
    dead = dead.rename(columns={'DEAD_YMD':"BSPT_DEAD_YMD"})

    data = pd.merge(data,dead[['PT_SBST_NO','BSPT_DEAD_YMD']],how='left',on='PT_SBST_NO')

    oprt = pd.read_excel(f'/mnt/synthetic_data/data/processed/3_postprocess/CLRC_OPRT_NFRM_{args.epsilon}.xlsx')
    oprt['PT_SBST_NO'] = oprt['PT_SBST_NO'].astype('str')
    oprt = oprt.drop_duplicates(subset='PT_SBST_NO')
    oprt = oprt.rename(columns={"OPRT_YMD":"BSPT_FRST_OPRT_YMD"})

    data = pd.merge(data,oprt[['PT_SBST_NO','BSPT_FRST_OPRT_YMD']],how='left',on='PT_SBST_NO')

    rdt = pd.read_excel(f'/mnt/synthetic_data/data/processed/3_postprocess/CLRC_TRTM_RD_{args.epsilon}.xlsx')
    rdt['PT_SBST_NO'] = rdt['PT_SBST_NO'].astype('str')
    rdt = rdt.rename(columns={"RDT_STRT_YMD":"BSPT_FRST_RDT_STRT_YMD"})

    data = pd.merge(data,rdt[['PT_SBST_NO','BSPT_FRST_RDT_STRT_YMD']],how='left',on='PT_SBST_NO')

    regn = pd.read_excel(f'/mnt/synthetic_data/data/processed/3_postprocess/CLRC_TRTM_CASB_{args.epsilon}.xlsx')
    regn['PT_SBST_NO'] = regn['PT_SBST_NO'].astype('str')

    regn_info = []
    for i in regn['PT_SBST_NO'].unique():
        start = regn[regn['CSTR_NT'] == 1].groupby(by='PT_SBST_NO').get_group(i)['CSTR_STRT_YMD'].iloc[0]
        end = regn[regn['CSTR_NT'] == 1].groupby(by='PT_SBST_NO').get_group(i)['CSTR_END_YMD'].iloc[-1]
        regn_info.append([i,start,end])
        
    regn_info_pd = pd.DataFrame(regn_info,columns=['PT_SBST_NO','CSTR_STRT_YMD','CSTR_END_YMD'])

    a = data.copy()
    #dead_ymd = pd.merge(a['PT_SBST_NO'],dead[['PT_SBST_NO','BSPT_DEAD_YMD']], on='PT_SBST_NO', how='left')['BSPT_DEAD_YMD']
    #oprt_ymd = pd.merge(a['PT_SBST_NO'],oprt[['PT_SBST_NO','OPRT_YMD']], on='PT_SBST_NO', how='left')['OPRT_YMD']
    #rdt_ymd = pd.merge(a['PT_SBST_NO'],rdt[['PT_SBST_NO','RDT_STRT_YMD']], on='PT_SBST_NO', how='left')['RDT_STRT_YMD']
    regn_strt_ymd = pd.merge(a['PT_SBST_NO'],regn_info_pd[['PT_SBST_NO','CSTR_STRT_YMD']], on='PT_SBST_NO', how='left')['CSTR_STRT_YMD']
    regn_end_ymd = pd.merge(a['PT_SBST_NO'],regn_info_pd[['PT_SBST_NO','CSTR_END_YMD']], on='PT_SBST_NO', how='left')['CSTR_END_YMD']

    data['BSPT_FRST_ANCN_TRTM_STRT_YMD'] = regn_strt_ymd
    data = pd.concat([head,data])

    data['CENTER_CD'] = 00000
    data['IRB_APRV_NO'] = '2-2222-02-22'
    data['CRTN_DT'] = '0200.0'
    data['OPRT_SEQ'] = 1

    data['PT_SBST_NO'] = data['PT_SBST_NO'].astype('str')

    def encode(x):
        if x == 'C18' :
            return 'colon'
        elif x == 'C19' :
            return "rectosigmoid junction"
        elif x == 'C20' :
            return "rectum"
        
    data['BSPT_FRST_DIAG_NM'] = data['BSPT_FRST_DIAG_CD']
    data['BSPT_FRST_DIAG_NM'] = data['BSPT_FRST_DIAG_CD'].apply(encode)

    data.to_excel(OUTPUT_PATH.joinpath(f'{file_name}_{args.epsilon}.xlsx'))

if __name__ == "__main__":
    main()