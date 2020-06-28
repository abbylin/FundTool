import pandas as pd
import numpy as np
import tushare as ts
import matplotlib.pyplot as plt
import matplotlib.pyplot as savefig
import numpy as np
import os

StockCode_File = 'StockCode.txt'
StockDataPath_Extend = '/StockData'

df = pd.DataFrame([[1.4, np.nan], [7.1, -4.5],
                   [np.nan, np.nan], [0.75, -1.3]],
                  index=['a', 'b', 'c', 'd'],
                  columns=['one', 'two'])
print(df)
print(df['two'].sum())
print(df['two'].mean())

current_path = os.getcwd()
data_file = current_path + StockDataPath_Extend + "/" + "招商银行/" + "600036.SH.csv"
if os.path.exists(data_file):
    dataform = pd.read_csv(data_file, nrows=30)
    print(dataform)
    for row in dataform.itertuples(index=True, name='Pandas'):
        print(getattr(row, "Index"))
        print(row['close'])
