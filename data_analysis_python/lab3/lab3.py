#####################
# ЗАДАНИЕ 1
#####################
import numpy as np

def function(int_list):
    n_list = np.array(int_list)

    n_list[n_list < 0] = 0
    n_list[n_list > 0] *= 4
    n_list.sort()
    n_list = n_list[::-1]

    return n_list[0] + n_list[1]

#####################
# ЗАДАНИЕ 2
#####################
import numpy as np

def function(temperature1, temperature2):
    temp1_list = np.array(temperature1)
    temp2_list = np.array(temperature2)

    temps_list = np.hstack((temp1_list[::3], temp2_list[::3]))
    mas_temp = temps_list[temps_list > 0]

    max, min, mean, std = int(mas_temp.max()), int(mas_temp.min()), int(mas_temp.mean()), int(mas_temp.std())

    return max + min + mean + std

#####################
# ЗАДАНИЕ 3
#####################
import numpy as np

def function(a, b, c):
    A = np.array([
        [1, 0, 1, 0],
        [4, 0, 1, -2],
        [a, b, 0, c],
        [-1, 1, -2, 1]
    ])

    B = np.array([2, 0, 5, -2])

    solution_vector = np.linalg.solve(A, B)

    return int(solution_vector.sum())

#####################
# ЗАДАНИЕ 4
#####################
import pandas as pd

def series_data(name, index):
    s = pd.Series([x for x in range(1, 1001, 2)], name=name)
    s.index += 1

    part = s.loc[index:]

    part[part.index % 2 != 0] *= 5
    part[part.index % 2 == 0] += 7

    s.loc[index:] = part

    return max(s[index], s[index + 1], s[index + 7])

#####################
# ЗАДАНИЕ 5
#####################
import pandas as pd

def frame_data(values, indices):
    df = pd.DataFrame(values, index=indices)

    df = df.sort_index()
    df *= 2
    df.iloc[0] += df.iloc[1]

    return df.iloc[1, -1]

#####################
# ЗАДАНИЕ 6
#####################
import pandas as pd

def sellers(n):
    df = pd.read_csv('tranzaktions.csv', sep='\t')

    seller_n = f'seller_{n}'
    seller_data = df[df['Продавец'] == seller_n]

    sum_n = seller_data['Цена (млн)'].sum()
    avg_n = round(seller_data['Цена (млн)'].mean())

    avg2_n = round(
        seller_data.loc[
            seller_data['Цена (млн)'] >= 2,
            'Цена (млн)'
        ].mean()
    )

    return sum_n + avg_n + avg2_n

sel_n = sellers(2)
print(sel_n)
#####################
# ЗАДАНИЕ 7
#####################
import pandas as pd

def cmp_series(n):
    transaction = ['100', -20, 300, 'bank', -450, 200, 'error', 0, 130.5, 50, '12']

    t = pd.Series(transaction)

    t = pd.to_numeric(t, errors='coerce')
    t = t.dropna()

    t = t[t % 1 == 0]
    t = t * n

    positive = t[t > 0]
    negative = t[t < 0]

    return abs(negative.sum()) + positive.sum()

#####################
# ЗАДАНИЕ 8
#####################
import numpy as np
import pandas as pd

def f(n):
    np.random.seed(n)

    s = pd.Series(np.random.normal(size=200))
    s = pd.Series(s.values ** 2, index = s.index + 2)
    
    count = (s > 2).sum()
    sum_cond = s[(s < 2) & (s.index % 2 !=0)].sum()
    
    return int(count + sum_cond)

#####################
# ЗАДАНИЕ 9
#####################
import numpy as np
import pandas as pd

np.random.seed(10)

df = pd.read_csv("CreditCardTransaction.csv")
dfs = df.sample(n=10_000)

top_3_departments = dfs['Department'].value_counts().nlargest(3)
transaction_median = dfs.loc[(dfs['Year'] == 2022) & (dfs['Month'].isin([1, 2])), 'TrnxAmount'].median()
dfs['MedianTrnxDiff'] = abs(transaction_median) - dfs["TrnxAmount"].abs()
index_val = int(dfs['MedianTrnxDiff'].iloc[67])
print(index_val)