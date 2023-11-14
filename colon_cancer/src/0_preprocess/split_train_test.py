import pandas as pd
import numpy as np

org = pd.read_pickle('/mnt/synthetic_data/data/processed/0_preprocess/D0.pkl')

dead_idx = (org[org['DEAD_NFRM_DEAD']==1]['PT_SBST_NO'].unique())
surv_idx = np.setdiff1d(org['PT_SBST_NO'].unique(),dead_idx)


train_dead_idx = np.random.choice(dead_idx, int(len(dead_idx)/2))
train_surv_idx = np.random.choice(surv_idx, int(len(surv_idx)/2))

test_dead_idx = np.setdiff1d(dead_idx, train_dead_idx)
test_surv_idx = np.setdiff1d(surv_idx, train_surv_idx)

train_df = pd.concat([org[org['PT_SBST_NO'].isin(train_dead_idx)],org[org['PT_SBST_NO'].isin(train_surv_idx)]])
test_df = pd.concat([org[org['PT_SBST_NO'].isin(test_dead_idx)],org[org['PT_SBST_NO'].isin(test_surv_idx)]])

train_df.to_pickle('/mnt/synthetic_data/data/processed/0_preprocess/D0_train.pkl')
test_df.to_pickle('/mnt/synthetic_data/data/processed/0_preprocess/D0_test.pkl')