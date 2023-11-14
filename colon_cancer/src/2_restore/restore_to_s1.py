
#%%
import pandas as pd
from pathlib import Path
import argparse
import pickle
import os, sys
import numpy as np


PROJ_PATH = Path('/home/dogu86/colon_synthesis_2')
sys.path.append(PROJ_PATH.joinpath('src').as_posix())

from MyModule.utils import *
config = load_config()

#%%
PROJ_PATH = Path(config['path_config']['project_path'])
INPUT_PATH = Path('/mnt/synthetic_data/data/processed/1_apply_bayesian/produce_data/D0_train/')
OUTPUT_PATH = Path('/mnt/synthetic_data/data/processed/2_restore/restore_to_s1/D0_train')

if not OUTPUT_PATH.exists() :
    OUTPUT_PATH.mkdir(parents=True)
    
#%%
def create_dummy():
    '''
    dummy data frame will serve as a frame for the original D0 
    '''
    D0_path = Path('/mnt/synthetic_data/data/processed/0_preprocess/D0_train.pkl')
    dummy = pd.read_pickle(D0_path).iloc[0:0].copy()
    return dummy

dummy = create_dummy()

#%%
def load_csv_data(path, patient_number):
    '''
    path : path to single csv
    '''
    df = pd.read_csv(path)
    
    df['PT_SBST_NO'] = patient_number
    global dummy
    local_dummy = dummy.copy()
    return pd.concat([local_dummy, df], ignore_index=True)
    

#%%
def load_synthetic_data(path):
    '''
    path : path to the whole folder
    ''' 
    all_files = sorted(path.iterdir())
    get_csv = lambda x : x.as_posix()[-3:] == 'csv'
    get_pt_number = lambda x : x.as_posix().split('_')[-1][:-4]
    all_csv_files = list(filter(get_csv, all_files))
    all_pt_number = list(map(get_pt_number, all_csv_files))
    all_synthetic_datas = list(map(load_csv_data, all_csv_files, all_pt_number))
    return all_synthetic_datas
#%%
encoding_path = Path('/mnt/synthetic_data/data/processed/0_preprocess/encoding.pkl')

with open(encoding_path, 'rb') as f:
    encoding = pickle.load(f)

def reverse_encoding(encoding):
    encoding.pop('PT_SBST_NO')
    def reverse(book):
        return {v : k for k,v in book.items()}
    return {k : reverse(book) for k, book in encoding.items()}
    

#%%
def main():


    parser = argparse.ArgumentParser()
    parser.add_argument('--epsilon','-e', help='enter epsilons')
    args = parser.parse_args()
    


    pkl_path = Path('/mnt/synthetic_data/data/processed/1_apply_bayesian/produce_data/D0_train/')
    pkl_path = pkl_path.joinpath('epsilon'+str(args.epsilon))
    pkls = (os.listdir(pkl_path))
    
    for pkl in pkls:
        if '.csv' not in pkl:
            temp = pkl_path.joinpath(pkl)
            temp_df = pd.read_pickle(temp)
    
            temp_df.to_csv(pkl_path.joinpath(pkl.split('.')[0]+'.csv'))

    path = INPUT_PATH.joinpath(f'epsilon{args.epsilon}')
    
    all_data_in_list = load_synthetic_data(path)
    S1 = pd.concat(all_data_in_list)
    
    encoding_path = Path('/mnt/synthetic_data/data/processed/0_preprocess/encoding.pkl')
    with open(encoding_path, 'rb') as f:
        encoding = pickle.load(f)
    
    encoding_rev = reverse_encoding(encoding)
    S1 = S1.replace(encoding_rev)
    
    days = pd.to_timedelta(S1.TIME, 'days')
    date = pd.to_datetime('2222/02/22', format='%Y/%m/%d')
    date = date + days
    
    S1['TIME'] = date
    
    with open(OUTPUT_PATH.joinpath(f'S1_{args.epsilon}.pkl'),'wb') as f:
        pickle.dump(S1, f)

if __name__ == '__main__':
    main()
    

