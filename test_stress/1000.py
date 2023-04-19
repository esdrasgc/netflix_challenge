from scipy.linalg import svd, diagsvd
import pandas as pd
import numpy as np

def selecionar_K_primeiros_valores(u, s, vt, K):
    u_ = u[:, 0:K]
    s_ = s[:K]
    vt_ = vt[:K, :]
    return u_, s_, vt_

df = pd.read_csv('ratings_small.csv')
df = df.drop('timestamp', axis=1)
matrix = pd.pivot_table(df, values='rating', index='userId', columns='movieId')


for iteração in range(1000):
    b = matrix.copy()
    cont = 0
    indices = set()
    i = np.random.randint(0, b.shape[0])
    j = np.random.randint(0, b.shape[1])
    while cont < 1000:
        if np.isnan(b.iloc[i, j]):
            i = np.random.randint(0, b.shape[0])
            j = np.random.randint(0, b.shape[1])
        else:
            cont+=1
            indices.add((i, j))

    b.iloc[i, j] = np.random.randint(5, 51) / 10
    b = b.fillna(2.75)

    b = b.to_numpy()

    U, s, Vt = svd(b)

    U_, s_, Vt_ = selecionar_K_primeiros_valores(U, s, Vt, 20)

    B_ = U_ @ diagsvd(s_, U_.shape[1], Vt_.shape[0]) @ Vt_

    diferença = matrix.iloc[i, j] - B_[i, j]
    with open('test_stress/diferenças_1000.txt', 'a') as f:
        f.write(f'{diferença}\n')
