# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
from datetime import datetime, time

df = pd.DataFrame(np.random.randn(5, 3), index=['one', 'two', 'three', 'four', 'five'], columns=list('ABC'))

print(df)
print()

# Выборка из ячейки dataframe
print(df.iat[0, 0])
print(df.at['one', 'A'])
print(df.iloc[0, 0])
print(df.loc['one', 'A'])

# Изменение ячейки dataframe
df.iat[0, 0] = 1
df.at['one', 'B'] = 2
df.iloc[0, 2] = 3
df.loc['two', 'A'] = 4

print()
print(df)
