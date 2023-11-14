import pandas as pd
import numpy as np
import os, sys
from pathlib import Path
import argparse

OUTPUT_PATH = Path('/mnt/synthetic_data/lung/data/processed/3_postprocess/after_QC')

def date_correction(df, prior_col, late_col):
    drop_idx = df[df[late_col] < df[prior_col]].index
    return df.drop(drop_idx)

def bsnf_stage_correction(df):
    cond1 = df['BSPT_STAG_VL'] == 3
    cond2 = df['BSPT_T_STAG_VL'] == 3
    cond3 = df['BSPT_N_STAG_VL'] == 0
    drop_idx = df[cond1&cond2&cond3].index
    return df.drop(drop_idx)

def sgpt_correction(df):

    
    df.loc[df['SGPT_MTST_LN_CNT']==0, 'SGPT_PATL_N_STAG_VL'] = 0
    
    for i in [1,2,3]:
        df.loc[df['SGPT_MTST_LN_CNT']==i, 'SGPT_PATL_N_STAG_VL'] = 1
    

    cond1 = df['SGPT_MTST_LN_CNT'] >= 10
    cond2 = df['SGPT_PATL_N_STAG_VL'] == 0
    ln_drop = df[cond1 & cond2].index
    df = df.drop(ln_drop)
    

    return df


def ymd_correction(dead_df,df,target1, target2):
    temp = pd.merge(dead_df[['PT_SBST_NO','DEAD_YMD']],df[['PT_SBST_NO',target1]],
                    how='right',on='PT_SBST_NO')
    df_mod = df.drop(temp[temp[target1] > temp['DEAD_YMD']].index)    
    
    temp = pd.merge(dead_df[['PT_SBST_NO','DEAD_YMD']],df_mod[['PT_SBST_NO',target2]],
                    how='right',on='PT_SBST_NO')
    
    df_mod = df_mod.drop(temp[temp[target2] > temp['DEAD_YMD']].index)
    
    return df_mod


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--epsilon', '--e', help="epsilon values")
    args = parser.parse_args()

    bsnf = pd.read_excel(f'/mnt/synthetic_data/lung/data/processed/3_postprocess/LUNG_PT_BSNF_{args.epsilon}.xlsx')
    #sgpt = pd.read_excel(f'/mnt/synthetic_data/lung/data/processed/3_postprocess/LUNG_PTH_SRGC_{args.epsilon}.xlsx')
    #bpth = pd.read_excel(f'/mnt/synthetic_data/lung/data/processed/3_postprocess/LUNG_PTH_BPSY_{args.epsilon}.xlsx')
    #rdt = pd.read_excel(f'/mnt/synthetic_data/lung/data/processed/3_postprocess/LUNG_TRTM_RD_{args.epsilon}.xlsx')
    #regn = pd.read_excel(f'/mnt/synthetic_data/lung/data/processed/3_postprocess/LUNG_TRTM_CASB_{args.epsilon}.xlsx')
    dead = pd.read_excel(f'/mnt/synthetic_data/lung/data/processed/3_postprocess/LUNG_DEAD_NFRM_{args.epsilon}.xlsx')

    bsnf = date_correction(bsnf,'BSPT_FRST_RDT_STRT_YMD','BSPT_FRST_DIAG_YMD')
    bsnf = bsnf_stage_correction(bsnf)
    #sgpt = sgpt_correction(sgpt)
    #rdt = ymd_correction(dead, rdt, 'RDT_END_YMD','RDT_STRT_YMD')
    #regn = ymd_correction(dead, regn, 'CSTR_END_YMD','CSTR_STRT_YMD')

    bsnf.to_excel(OUTPUT_PATH.joinpath(f'LUNG_PT_BSNF_{args.epsilon}.xlsx'))
    #sgpt.to_excel(OUTPUT_PATH.joinpath(f'LUNG_PTH_SRGC_{args.epsilon}.xlsx'))
    #bpth.to_excel(OUTPUT_PATH.joinpath(f'LUNG_PTH_BPSY_{args.epsilon}.xlsx'))
    #rdt.to_excel(OUTPUT_PATH.joinpath(f'LUNG_TRTM_RD_{args.epsilon}.xlsx'))
    #regn.to_excel(OUTPUT_PATH.joinpath(f'LUNG_TRTM_CASB_{args.epsilon}.xlsx'))

if __name__=="__main__":
    main()