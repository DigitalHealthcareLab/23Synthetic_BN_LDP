
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

table_name = 'lung_oprt_nfrm'
file_name = config['file_name'][table_name]
input_path = Path(config['path_config']['input_path'])
output_path = Path(config['path_config']['output_path'])
columns = config['data_config']['required'][table_name.upper()]
prefix = config['data_config']['prefix'][table_name.upper()]

if not output_path.joinpath('0_preprocess').exists():
    output_path.joinpath('0_preprocess').mkdir(parents=True)

output_path = output_path.joinpath('0_preprocess')

#%%
oprt_nfrm = read_file(input_path, file_name)

#%% 
oprt_required = oprt_nfrm[columns.keys()]

#%%
oprt_required = convert_dates(oprt_required, config, table_name.upper())

#%%

oprt_required = oprt_required.rename(columns = {'OPRT_YMD':'TIME'})

#%%
oprt_required.sort_values(by=['PT_SBST_NO','TIME'])

#%%
duplicated_counts = oprt_required[['PT_SBST_NO','TIME']].duplicated().sum()
print(f'duplicated_counts : {duplicated_counts}')

#%%

oprt_final = oprt_required.set_index(['PT_SBST_NO','TIME'])

oprt_final = oprt_final.add_prefix(prefix)

oprt_final = remove_invalid_values(oprt_final)


#%%
oprt_final.to_pickle(output_path.joinpath(table_name + '.pkl'))

# %%
