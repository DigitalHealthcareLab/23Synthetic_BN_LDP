#%%
import pandas as pd
import numpy as np
import pickle
import os, sys
from pathlib import Path
import argparse
import numpy as np
import math
import warnings

PROJ_PATH = Path('/home/dogu86/colon_synthesis_2')
sys.path.append(PROJ_PATH.joinpath('src').as_posix())

from MyModule.utils import *
config = load_config()

PROJ_PATH = Path(config['path_config']['project_path'])
INPUT_PATH = PROJ_PATH.joinpath('/mnt/synthetic_data/data/processed/2_restore/restore_to_db_form/D0')
OUTPUT_PATH = PROJ_PATH.joinpath('/mnt/synthetic_data/data/processed/3_postprocess/')

if not OUTPUT_PATH.exists() :
    OUTPUT_PATH.mkdir(parents=True)

file_name = "CLRC_TRTM_CASB"

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
    def encode_prps(x):
        if math.isnan(x):
            return np.nan
        if x == 2 :
            return 'Adjuvant'
        elif x == 1 :
            return "Neo-adjuvant"
        elif x == 3 :
            return "Palliative"
        elif x == 4 :
            return "Concurrent"
        elif x == 5 :
            return "Induction"
        elif x == 6 :
            return "Maintenance"
        elif x == 7 :
            return "Salvage"
        elif x == 8 :
            return "Consolidation"
        else :
            return "Other"

    def encode_regimen(x):
        if math.isnan(x):
            return np.nan
        if x == 1 :
            return "none"
        elif x == 2 :
            return "5-FU + leucovorin"
        elif x == 3 :
            return "capecitabline"
        elif x == 4 :
            return "S-1"
        elif x == 5 :
            return "UFT + leucovorin"
        elif x == 6:
            return "avastin + fluoropyrimidine"
        elif x == 7 :
            return "FOLFOX"
        elif x == 8 :
            return "FOLFOX + AVASTIN"
        elif x == 9 :
            return "FOLFOX + ERBITUX"
        elif x == 10 :
            return "XELOX"
        elif x == 11 :
            return "XELOX + AVASTIN"
        elif x == 12 :
            return "XELOX + ERBITUX"
        elif x == 13 :
            return "FOLFIRI"
        elif x == 14 : 
            return "FOLFIRI + AVASTIN"
        elif x == 15 :
            return "FOLFIRI + ERBITUX"
        else :
            return "Other"



    data = data.dropna(subset=['CSTR_REGN_CD','CSTR_PRPS_CD'])

    data['CSTR_PRPS_NM'] = data['CSTR_PRPS_CD'].apply(encode_prps)
    data['CSTR_REGN_NM'] = data['CSTR_REGN_CD'].apply(encode_regimen)

    data = data.rename(columns = {'TIME':'CSTR_STRT_YMD'})
    data['CSTR_END_YMD'] = data['CSTR_STRT_YMD'] + pd.to_timedelta(28, 'days')

    original_path = PROJ_PATH.joinpath(f'/mnt/synthetic_data/data/raw/{file_name}.xlsx')
    head = pd.read_excel(original_path, nrows=0)

    data = pd.concat([head, data])

    data['CENTER_CD'] = 00000
    data['IRB_APRV_NO'] = '2-2222-02-22'
    data['CRTN_DT'] = '2022-02-22'
    data['CSTR_SEQ'] = 1
    data['CSTR_CYCL_VL'] = 1

    dtypes = head.dtypes.to_dict()

    warnings.filterwarnings('ignore')

    whole_processed_arr = []
    for i in data['PT_SBST_NO'].unique():
    #for i in ['0']:
        group_0 = data.groupby(by='PT_SBST_NO').get_group(i)
        cnt = 0
        cycle_arr = []
        whole_data = []
        memorized = []
        for j in range(1,len(group_0)):
            try:
                prev = group_0.to_numpy().transpose()[6][j-1]+group_0.to_numpy().transpose()[10][j-1] 
                cur = group_0.to_numpy().transpose()[6][j]+group_0.to_numpy().transpose()[10][j] 
            except:
                print('Str Add error',i,j)

            if prev not in memorized:

                if prev==cur:
                    cycle_arr.append(group_0.to_numpy()[j-1])
                    cnt +=1   
                elif prev!=cur and cnt != 0:
                    whole_data.append(cycle_arr)
                    cycle_arr =[]
                    cnt = 0
                    memorized.append(prev)
                if cnt==12:
                    whole_data.append(cycle_arr)
                    cycle_arr=[]
                    cnt = 0
                    memorized.append(prev)
            else:
                pass

        temp_con_pd = pd.DataFrame(columns=head.columns)

        for k in range(len(whole_data)):
            if len(whole_data[k])>0:
                regn_info = pd.DataFrame(whole_data[k],columns=head.columns)
                regn_info['CSTR_CYCL_VL'] = np.arange(1,len(whole_data[k])+1,1)
                regn_info['CSTR_NT'] = k+1
                try:
                    regn_info['CSTR_STRT_YMD'].iloc[1:] = regn_info['CSTR_END_YMD'].iloc[0:-1]
                    regn_info['CSTR_END_YMD'] = regn_info['CSTR_STRT_YMD'] + pd.to_timedelta(28, 'days')

                except:
                    print('Date error : ',k)
                temp_con_pd = pd.concat([temp_con_pd,regn_info])

        
        if len(temp_con_pd)>0:
            whole_processed_arr.append(temp_con_pd)
            
    result = pd.concat(whole_processed_arr)
    result = result.astype(dtypes)

    result.to_excel(OUTPUT_PATH.joinpath(f'{file_name}_{args.epsilon}.xlsx'))
    pass

if __name__ == "__main__":
    main()