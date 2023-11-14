#%%

import yaml
import pandas as pd
import pickle
from pathlib import Path
import numpy as np
import os, sys
import re
from functools import reduce




project_path = Path(__file__).resolve()
project_path = project_path.parents[2]
os.sys.path.append(project_path.as_posix())

from src.MyModule.utils import *
config = load_config()

project_path = Path(config['path_config']['project_path'])
input_path = Path(config['path_config']['input_path'])
output_path = Path(config['path_config']['output_path'])
file_names = list(config['file_name'].keys())

preprocess_output = output_path.joinpath('0_preprocess')

#%%
def read_pkl(path):
    return pd.read_pickle(path)

#%%
def check_duplicates(df):
    counts = df[['PT_SBST_NO','TIME']].duplicated().sum()
    return counts


# %%
all_datas = [read_pkl(preprocess_output.joinpath(file +'.pkl')) for file in file_names]
all_datas = list(map(lambda data : data.reset_index(), all_datas))


print("Check Duplicates Once Again")
print(list(map(check_duplicates, all_datas)))

all_concated = reduce(lambda df1, df2 : pd.merge(df1, df2, how='outer', on=['PT_SBST_NO','TIME']), all_datas)

print(all_concated[all_concated['PT_BSNF_BSPT_AGE']<50].nunique())