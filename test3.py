import pandas as pd
import numpy as np

x = pd.DataFrame([[1,2,3],[1,2,3],[1,2,3]])
y = pd.DataFrame([[1,0,1],[1,0,1],[1,0,1]])
print(x)
print(y)
d = pd.DataFrame(np.where(x>y, 55, 0))
print(d)

'''
z = pd.DataFrame([range(-1,2) for x in range(0,3)])
print("\n",z)
z = pd.DataFrame(np.where(z<=x*y, 55, 0))
print("\n",z)
'''

