import pandas as pd 
import numpy as np
import mikeio
import os
from mikeio import EUMUnit,EUMType,ItemInfo

######################################## Operational Functions #############################################
def create_direction_intervals(n_interval):
    if n_interval == 8:
        direction_intervals_left = np.array([0.,22.5,67.5,112.5,157.5,202.5,247.5,282.5,337.5])
        direction_intervals_right = np.array([22.5,67.5,112.5,157.5,202.5,247.5,282.5,337.5,360.])
        labels = ['[0-22.5)','[22.5 - 67.5)','[67.5 - 112.5)','[112.5 - 157.5)','[157.5 - 202.5)','[202.5 - 247.5)','[247.5 - 282.5)','[282.5 - 337.5)','[337.5 - 360)']
    elif n_interval == 16:
        direction_intervals_left = np.array([0.,11.25,33.75,56.25,78.75,101.25,123.75,146.25,168.75,191.25,213.75,236.25,258.75,281.25,303.75,326.25,348.75])
        direction_intervals_right = np.array([11.25,33.75,56.25,78.75,101.25,123.75,146.25,168.75,191.25,213.75,236.25,258.75,281.25,303.75,326.25,348.75,360])
        labels = ['[0 - 11.25)','[11.25 - 33.75)','[33.75 - 56.25)','[56.25 - 78.75)','[78.75 - 101.25)','[101.25 - 123.75)','[123.75 - 146.25)','[146.25 - 168.75)',
                '[168.75 - 191.25)','[191.25 - 213.75)','[213.75 - 236.25)','[236.25 - 258.75)','[258.75 - 281.25)','[281.25 - 303.75)','[303.75 - 326.25)','[326.25 - 348.75)','[348.75 - 360)']
    elif n_interval == 24:
        direction_intervals_left = np.array([0.,7.5,22.5,37.5,52.5,67.5,82.5,97.5,112.5,127.5,142.5,157.5,172.5,187.5,202.5,217.5,232.5,247.5,262.5,277.5,292.5,307.5,322.5,337.5,352.5])
        direction_intervals_right = np.array([7.5,22.5,37.5,52.5,67.5,82.5,97.5,112.5,127.5,142.5,157.5,172.5,187.5,202.5,217.5,232.5,247.5,262.5,277.5,292.5,307.5,322.5,337.5,352.5,360])
        labels=['[-7.5 - 7.5)','[7.5 - 22.5)','[22.5 - 37.5)','[37.5 - 52.5)','[52.5 - 67.5)','[67.5 - 82.5)','[82.5 - 97.5)','[97.5 - 112.5)','[112.5 - 127.5)','[127.5 - 142.5)','[142.5 - 157.5)','[157.5 - 172.5)',
                '[172.5 - 187.5)','[187.5 - 202.5)','[202.5 - 217.5)','[217.5 - 232.5)','[232.5 - 247.5)','[247.5 - 262.5)','[262.5 - 277.5)','[277.5 - 292.5)','[292.5 - 307.5)','[307.5 - 322.5)','[322.5 - 337.5)','[337.5 - 352.5)','[352.5 - 360)']
    direction_intervals = pd.IntervalIndex.from_arrays(left=direction_intervals_left,
                                                        right=direction_intervals_right,
                                                        closed='left')
    
    return direction_intervals,labels

def cut_df_directions(df, direction_intervals, column_to_cut):
# Cut DataFrame according directions intervals
    cutted_column = pd.cut(x=column_to_cut,
                            bins=direction_intervals,
                            include_lowest=True)
    df[column_to_cut.name+'_intervals'] = cutted_column

    return df

######################################## Main Function ################################################################

#Input file
file='Wave_TSS'#input .dfs0 for directional sectors(without extension)
path_input='./Omnidirectional/'
ds=mikeio.read(path_input+file+'.dfs0')
items=ds.items #Get items ds to dfs0 directional
df=ds.to_dataframe()

#Select number o sectors for directional intervals
n_interval = 16#int(input('How many directional sectors (options are 8,16,24): ')) #Options: 8,16,24

direction_intervals,labels=create_direction_intervals(n_interval)

#Identify the different directional intervals in dfs0
if file.split('_')[0] in ['Wind','Current']:
    variable=file.split('_')[0]+' Direction' #Options: Wind Direction, Currents Direction and MWD    
else:
    variable='MWD'#Options: Wind Direction, Currents Direction and MWD

column_to_cut=df.loc[:][variable]
df=cut_df_directions(df, direction_intervals, column_to_cut)

#Group the dfs0 by direction
g=df.groupby(variable+'_intervals',observed=False)
dfs_dir=[group for _,group in g]

#Create dfs0
path_results='./Directional/'+file+'/'

if not os.path.exists(path_results):    
    os.makedirs(path_results)
    
#Join North
df_north=pd.concat([dfs_dir[0].iloc[:,:-1],dfs_dir[-1].iloc[:,:-1]])
df_north.index=df_north.index.sort_values()
start_n=labels[0].split('-')[-1]
end_n=labels[-1].split('-')[0]
label_n=end_n+'-'+start_n
if df_north.empty:
    pass #in case the direction does not happen
else:
    df_north.to_dfs0(path_results+'dfs_'+label_n+'.dfs0',items=items)

#Creat other directions
for d in range(1,len(dfs_dir)-1):
    df_dir=dfs_dir[d]
    df_dir_new=df_dir.iloc[:,:-1]
    if df_dir_new.empty: 
        pass #in case the direction does not happen
    else:
        df_dir_new.to_dfs0(path_results+'dfs_'+labels[d]+'.dfs0',items=items)

print(file+' Directional created!')

print('Done!')