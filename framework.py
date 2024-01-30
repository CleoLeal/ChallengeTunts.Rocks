# importing as libraries
import pandas as pd #data manipulation and analysis library 
import numpy as np # data control
import math # librarie math to rounded

#caculating the avarage
def Average (n1, n2, n3) -> int:
    # calculating the average and ignore values NaN
    a = (n1 + n2 + n3) / 3

    # Rounded for up the average values
    rounded_avarage = a.apply(lambda x: np.ceil(x) if not pd.isna(x) else x)
    print(f'Avarege:{rounded_avarage}')
    return rounded_avarage

#calculating schools absences
def SchoolsAbsences(f) -> bool:
    max = 60 * 0.25
    if f > max: #if schools absences to bigger then maximum schools absences
        return True #return true 

#calculating NAF
def Naf(m) -> int:
    naf = math.ceil((50 - m) * 2)  # formula
    condition = math.ceil((m + naf)/2)
    print(f"Grade for final approval {condition}") 
    return condition