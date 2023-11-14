
#%%
import yaml
import pandas as pd
import pickle
from pathlib import Path
import numpy as np
import os, sys

project_path = Path(__file__).parents[2]
os.sys.path.append(project_path.as_posix())

from src.MyModule.utils import *
config = load_config()
#%%
table_name = 'lung_ex_plmn'
file_name = config['file_name'][table_name]
input_path = Path(config['path_config']['input_path'])
output_path = Path(config['path_config']['output_path'])
columns = config['data_config']['required'][table_name.upper()]
prefix = config['data_config']['prefix'][table_name.upper()]

if not output_path.joinpath('0_preprocess').exists():
    output_path.joinpath('0_preprocess').mkdir(parents=True)

output_path = output_path.joinpath('0_preprocess')
#%% load data
ex_plmn = read_file(input_path, file_name)

#%%  read data
ex_plmn_required = ex_plmn[columns.keys()].copy()

#%%
ex_plmn_required

#%%
ex_plmn_required['PLEX_RSLT_VL'] = ex_plmn_required['PLEX_RSLT_VL'].replace('o',0, regex=True)

#%%
ex_plmn_required['PLEX_RSLT_VL'] = ex_plmn_required.PLEX_RSLT_VL.replace('>|<','', regex=True)

ex_plmn_required = ex_plmn_required.replace('+++++', np.nan)
ex_plmn_required = ex_plmn_required.replace(':::::',np.nan)
ex_plmn_required['PLEX_RSLT_VL'] = ex_plmn_required.PLEX_RSLT_VL.replace('.', np.nan)

ex_plmn_required['PLEX_RSLT_VL'] = ex_plmn_required['PLEX_RSLT_VL'].astype('float32')



#%% convert dates
ex_plmn_required = convert_dates(ex_plmn_required, config=config, table_name=table_name.upper())
ex_plmn_required = ex_plmn_required.drop_duplicates()


#%%
ex_plmn_required = ex_plmn_required.rename(columns = {'PLEX_YMD':"TIME"})

duplicated_counts = ex_plmn_required[['PT_SBST_NO','TIME']].duplicated().sum()
print(f'duplicated_counts : {duplicated_counts}')

#%%
pivoted_ex_plmn = pd.pivot_table(ex_plmn_required, index=['PT_SBST_NO','TIME'], columns= 'PLEX_NM', values='PLEX_RSLT_VL')

#%%
duplicated_counts = pivoted_ex_plmn.reset_index()[['PT_SBST_NO','TIME']].duplicated().sum()
print(f'duplicated_counts : {duplicated_counts}')
#%% convert to time index 

pivoted_ex_plmn = pivoted_ex_plmn.add_prefix(prefix)


#%%
pivoted_ex_plmn.to_pickle(output_path.joinpath('lung_ex_plmn.pkl'))

#%%