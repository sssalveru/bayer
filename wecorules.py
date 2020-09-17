import pandas as pd
import numpy as np
data = pd.read_csv("C:\\Users\\Sampreeth Salveru\\Downloads\\AG_Discrete_DS06-Jul-2020.csv")

# WECO Rule 1
def weco1(col, ucl, lcl):
    if np.isnan(ucl) == False and np.isnan(lcl) == False:
        y = np.array(data[col].dropna())
        rule1 = np.array([])
        for i in range(0,len(y)):
            if(y[i] > ucl or y[i] < lcl):
                rule1 = np.append(rule1, i)
        rule1 = rule1.astype(np.int)
        return rule1
    elif np.isnan(ucl) == True and np.isnan(lcl) == False:
        y = np.array(data[col].dropna())
        rule1 = np.array([])
        for i in range(0,len(y)):
            if(y[i] < lcl):
                rule1 = np.append(rule1, i)
        rule1 = rule1.astype(np.int)
        return rule1
    elif np.isnan(ucl) == False and np.isnan(lcl) == True:
        y = np.array(data[col].dropna())
        rule1 = np.array([])
        for i in range(0,len(y)):
            if(y[i] > ucl):
                rule1 = np.append(rule1, i)
        rule1 = rule1.astype(np.int)
        return rule1
    else: 
        return []

# WECO Rule 4
def weco4(col, mean):
    if np.isnan(mean) == True:
        return []
    else:
        x = data[col].dropna()
        anomalies = x - mean
        signs = np.sign(anomalies)
        signs = np.array(signs)
        A = signs.cumsum()
        A[8:] -= A[:-8]
        rule4 = (np.abs(A)==8).nonzero()[0]
        return rule4

# WECO Rule 5
def weco5(col):
    x = data[col].dropna()
    nub = np.sign(np.diff(x)).astype(np.int8)
    N = 6
    C = nub.cumsum()
    C[N:] -= C[:-N]
    rule5 =(np.abs(C)==N).nonzero()[0]
    return rule5
