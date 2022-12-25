import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import re
import sys
import numpy as np
if len(sys.argv) == 1:
    print("No file was dropped\n")
    print("please Drag and Drop the file")
    exit()

first = sys.argv[1]
second = sys.argv[2]
corpus1 = pd.read_csv(first, encoding='latin-1')
corpus2 = pd.read_csv(second, encoding='latin-1')
namer1 = corpus1.columns[1]
namer2 = corpus2.columns[1]
def get_date_format(date): # get the date format
    if re.match(r"^\d{4}-\d{2}-\d{2}$", date):
        return "%Y-%m-%d"
    elif re.match(r"^\d{2}-\d{2}-\d{4}$", date):
        return "%d-%m-%Y"
    elif re.match(r"^\d{2}/\d{2}/\d{4}$", date):
        return "%m/%d/%Y"
    elif re.match(r"^\d{4}/\d{2}/\d{2}$", date):
        return "%Y/%d/%m"
    elif re.match(r"^\d{4}\d{2}\d{2}$", date):
        return "%Y%m%d"
    elif re.match(r"^\d{2}\d{2}\d{4}$", date):
        return "%d%m%Y"
    elif re.match(r"^\d{4}/\d{2}/\d{4}$", date):
        return "%Y/%m/%d"
    elif re.match(r"^\d{2} \w{3} \d{4}$", date):
        return "%d %b %Y"
    elif re.match(r"^\d{2} \w{4,9} \d{4}$", date):
        return "%d %B %Y"
    else:
        return None
corpus1['Date'] = pd.to_datetime(corpus1['Date'], format=get_date_format(corpus1['Date'][0]))
corpus2['Date'] = pd.to_datetime(corpus2['Date'], format=get_date_format(corpus2['Date'][0]))
def removeNan(df): # remove nan from the top based on the first column
    h = df.columns[1]
    for i in range(len(df)):
        if df[h][i] == df[h][i]:
            return df[i:]

def removenanfromlast(df): # remove nan from the bottom based on the first column
    h = df.columns[1]
    for i in range(len(df))[::-1]:
        if df[h][i] == df[h][i]:
            return df[:i+1]

def get_df_name(df): # get the name of the file
    name = Path(df).stem
    return name

def interpolatetwopoints(df1, df2): # interpolate between two points
    newdf1 = corpus1.set_index('Date')
    newdf2 = corpus2.set_index('Date')
    thenewdf = newdf1.join(newdf2, how='outer')
    thenewdf = removeNan(thenewdf) # remove nan from the top based on the first column
    thenewdf = removenanfromlast(thenewdf) # remove nan from the bottom
    #firsto = get_df_name(first)
    #secondo = get_df_name(second)
    thenewdf = thenewdf.interpolate(method='linear')
    #thenewdf.to_csv(r"C:\Users\MrM\Desktop\New Intership\Interpolated_" +firsto +"_"+ secondo+".csv", index=True)
    return thenewdf


interpoo = pd.DataFrame(interpolatetwopoints(corpus1, corpus2))
interpoo= interpoo.dropna()
firsto = get_df_name(first)
secondo = get_df_name(second)
interpoo.to_csv(r".\Interpolated_" +firsto +"_"+ secondo+".csv", index=True)
