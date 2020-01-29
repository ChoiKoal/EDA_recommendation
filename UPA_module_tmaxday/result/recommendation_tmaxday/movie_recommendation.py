import surprise
import os
import pandas as pd
from surprise import SVD
from surprise import Dataset
from surprise import dump
from surprise.model_selection import cross_validate
from surprise import accuracy
from surprise.model_selection import KFold
import matplotlib.pyplot as plt
import numpy as np
from surprise.model_selection import KFold

data = surprise.Dataset.load_builtin('ml-100k')
df = pd.DataFrame(data.raw_ratings, columns=["user", "item", "rate", "id"])
del df["id"]
df_table = df.set_index(["user", "item"]).unstack()
data_array = df_table.values

matA = np.array(data_array).astype(np.float64)
print (data_array)
U, s, V = np.linalg.svd(matA, full_matrices = True)

print (U, s*V)

bsl_options = {
    'method': 'als',
    'n_epochs': 5,
    'reg_u': 12,
    'reg_i': 5
}
algo = surprise.BaselineOnly(bsl_options)

np.random.seed(0)
acc = np.zeros(3)
cv = KFold(3)
for i, (trainset, testset) in enumerate(cv.split(data)):
    algo.fit(trainset)
    predictions = algo.test(testset)
    acc[i] = surprise.accuracy.rmse(predictions, verbose=True)
acc.mean()