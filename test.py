import pandas as pd

data = pd.read_excel('result.xlsx', header=0,
                     names=['pp', 'pf', 'dp', 'ua', 'c', 'w', 'q', 'h', 'fai', 'vcs', 'vpx', 'ueq', 'heq'])

x = list(data.get('pp').astype(float))

print(x)