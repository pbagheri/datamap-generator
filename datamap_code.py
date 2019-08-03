# -*- coding: utf-8 -*-
"""
Created on Sun Nov 19 11:57:26 2017

@author: Payam
"""
from pandas import read_excel, read_csv, Series,  DataFrame, notnull
from numpy import nan as npnan
from os import path
#from cx_Freeze import setup, Executable

dir_path = path.dirname(path.dirname(path.abspath(__file__)))
print(dir_path)


maptab = read_excel(dir_path + '\\0_input_data\\maptab.xlsx', skiprows=[0])
maptab.rename(columns = {'Value': 'features', 'Unnamed: 1': 'values', 'Label': 'labels'}, inplace = True)
maptab.head()

datamap_pre = read_csv(dir_path + '/0_input_data/variables.csv', header=None, encoding = "ISO-8859-1")
datamap_pre.head()

datamap = datamap_pre[[0,1]]
datamap[2] = npnan
datamap[3] = datamap_pre[2]

datamap[1].replace(to_replace={'Numeric':'integer', 'String':'string'},inplace=True)

# Here the the blocks (variaables and their associates levels) are read and the 
# information about the number of levels for each variable recorded in blocks 
ind = Series(maptab.features[notnull(maptab.features)].index)
lst = int(maptab.index.max()) + 1
ind_sh = ind.shift(-1)
ind_sh.iloc[ind_sh.index.max()] = lst
blocks = ind_sh-ind

maptab.head()

# An empty dataframe to contain datamap info
mapdic = DataFrame(columns=range(int(2*max(blocks))), index=range(len(ind)))

# populates the maptab by the levels of their values for each variable in each row
for i in ind.index:
    lis = maptab[['values','labels']].iloc[ind[i]:int(ind[i]+blocks[i])].values.reshape(1,int(2*(blocks[i])))
    lis = lis.tolist()
    lis = lis[0]
    lis += [npnan] * (int(2*max(blocks)) - len(lis))
    mapdic.iloc[i] = lis

mapdic[int(2*max(blocks))] = list(maptab.features[maptab.features.notnull()])

# the dataframe that is going to contain the final datamap
final_datamap = DataFrame(columns=range(int(4+2*max(blocks))), index=range(datamap.shape[0]))
final_datamap[[0,1,2,3]] = datamap

# reads through the variables and adds datamap data to whichever variavle that has 
# levels and values for levels.
for c in range(len(final_datamap[0])):
    if mapdic[int(2*max(blocks))].isin(final_datamap.iloc[c]).sum():
        print(c)
        final_datamap.iloc[c:c+1,list(range(4,int(2*max(blocks)+4)))] = mapdic[list(range(0,int(2*max(blocks))))][mapdic[int(2*max(blocks))]==final_datamap[0][c]].values.tolist() 
    else:
        final_datamap.iloc[c:c+1,list(range(4,int(2*max(blocks)+4)))] = DataFrame(columns=range(0,int(2*max(blocks))), index=range(0,1))

final_datamap[0] = final_datamap[0].apply(lambda x: x.lower())   

final_datamap.to_csv(dir_path + '\\0_output\\datamap.csv', index=False, header=False)  
