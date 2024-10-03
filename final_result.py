import pandas as pd
import os
import warnings
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont

warnings.filterwarnings("ignore")

############################## Functions ###########################
def create_folders_results(points,variable):

    if variable in ['Wind Speed','Current Speed']:
        variable = variable.split(' ')[0]
        
    path_resultsFinal='./Results Final/'+points+'/'+variable+'/'
    if not os.path.exists(path_resultsFinal):    
        os.makedirs(path_resultsFinal)
    return path_resultsFinal

def create_folders_results_depth(points,variable,depth):
    
    path_resultsFinal='./Results Final/'+points+'/'+variable+'/'+depth+'/'
    if not os.path.exists(path_resultsFinal):    
        os.makedirs(path_resultsFinal)
    return path_resultsFinal
    
def draw_units(variable):

    if variable in ['Air Temperature','Sea Water Temperature']:
        var_txt=' [°C]'
    elif variable in ['Wind','Current']:
        var_txt=' [m/s]'
    elif variable in ['Hm0','Hmax','Water Level']:
        var_txt=' [m]'

    return var_txt

def get_path_omni(depth,df,i,variable):

    if str(depth) =='nan':
        path='./Results/'+df.loc[i]['Points']+'/'+variable+'/Omnidirectional/'
        path_resultsFinal=create_folders_results(df.loc[i]['Points'],variable)
    else:
        path='./Results/'+df.loc[i]['Points']+'/'+variable+'/'+depth+'/Omnidirectional/'
        path_resultsFinal=create_folders_results_depth(df.loc[i]['Points'],variable,depth)
        
    return path, path_resultsFinal        

def get_path_dir(depth,df,i,variable,direction):

    if str(depth) =='nan':
        path='./Results/'+df.loc[i]['Points']+'/'+variable+'/Directional/dfs_'+direction+'/'
        path_resultsFinal=create_folders_results(df.loc[i]['Points'],variable)

    else:
        path='./Results/'+df.loc[i]['Points']+'/'+variable+'/'+depth+'/Directional/dfs_'+direction+'/'
        path_resultsFinal=create_folders_results_depth(df.loc[i]['Points'],variable,depth)
        
    return path, path_resultsFinal     

def get_path_extreme(depth,points,variable):

    variable=check_var(variable)
    if str(depth) =='nan':
        path_resultsExtreme='./Results Final/'+points+'/'+variable+'/'
    else:    
        path_resultsExtreme='./Results Final/'+points+'/'+variable+'/'+depth+'/'
    
    return path_resultsExtreme

def check_var(variable):
    
    if variable in ['Wind Speed','Current Speed']:  
        variable=variable.split(' ')[0]
    else:
        variable=variable
        
    return variable

def check_var_inverse(variable):
    
    if variable in ['Wind','Current']:  
        variable=variable + ' Speed'
    else:
        variable=variable
        
    return variable

def check_for_completetable(path):
    file_path=path+'ExtremeAnalysisTable_complete.txt'
    if os.path.exists(file_path):
        os.remove(file_path)

def check_for_txt(path_resultsExtreme):

    path=path_resultsExtreme+path_resultsExtreme.split('/')[2]+'_ExtremeAnalysisTable_'+check_var_inverse(path_resultsExtreme.split('/')[3])+'_'+name_dir_list[file]+'.txt'
    if os.path.exists(path):
        exists_or_not=1
    else:
        exists_or_not=0

    return exists_or_not

############################## Main Function ########################
# Read excel
df=pd.read_csv('Extreme_Analysis.csv',sep=';')

#Create images and table for variables
for i in range(len(df)):

    if df.index[i]==0:
        pass #if index 0 skip line
    else:
        variable=check_var(df.loc[i]['Variable'])

        if df.loc[i]['Direction'][0] =='O':#Omnidirectional
            
            path,path_resultsFinal= get_path_omni(df.loc[i]['Depth'],df,i,variable)
            nameimg=df.loc[i]['Points']+'_ExtremeAnalysis_'+df.loc[i]['Variable']+'_'+df.loc[i]['Direction']
            nameTable=df.loc[i]['Points']+'_ExtremeAnalysisTable_'+df.loc[i]['Variable']+'_'+df.loc[i]['Direction']
            
            if df.loc[i]['Distribution']== 'not':
                pass
            else:
                #Work on Image 
                img=Image.open(path+df.loc[i]['Distribution']+'.png')
                img=img.resize((810,810))
                font=ImageFont.truetype('arial.ttf',12)
            
                #Add units in image
                var_txt=draw_units(variable)
                ImageDraw.Draw(img).text((50, 765),str(variable)+' units:'+var_txt,font=font, fill =(0, 0, 0))
                
                #Adds distribution Info
                ImageDraw.Draw(img).text((50, 780), "Distribution Type: "+df.loc[i]['Distribution'],font=font, fill =(0, 0, 0))
                #ImageDraw.Draw(img).text((50, 795), "Inter Event Type: 36h",font=font, fill =(0, 0, 0))
                #ImageDraw.Draw(img).text((250, 780), "Threshold: "+str(df.loc[i]['Threshold'])+ var_txt,font=font, fill =(0, 0, 0))
                ImageDraw.Draw(img).text((50, 795), "Confidence Level: 5 and 95%",font=font, fill =(0, 0, 0))
                
                #Get table with df
                df_table=pd.read_csv(path+df.loc[i]['Distribution']+'.txt',sep='\t',index_col=0)
                df_table=df_table.round(2)

                plt.figure(figsize=(10,5))
                plt.axis('off')
                plt.margins(x=0)
                
                #Save All
                img.save(path_resultsFinal+ nameimg+'.png')
                df_table.to_csv(path_resultsFinal+nameTable+'.txt')
            
        else:#Directional
        
            path,path_resultsFinal= get_path_dir(df.loc[i]['Depth'],df,i,variable,df.loc[i]['Direction'])
            nameimg=df.loc[i]['Points']+'_ExtremeAnalysis_'+df.loc[i]['Variable']+'_'+df.loc[i]['Direction']
            nameTable=df.loc[i]['Points']+'_ExtremeAnalysisTable_'+df.loc[i]['Variable']+'_'+df.loc[i]['Direction']

            if df.loc[i]['Distribution']== 'not':
                pass
            else:
                #Work on Image 
                img=Image.open(path+df.loc[i]['Distribution']+'.png')
                img=img.resize((810,810))
                font=ImageFont.truetype('arial.ttf',12)
                
                #Add units in image
                var_txt=draw_units(variable)
                ImageDraw.Draw(img).text((50, 765),str(variable)+' units:'+var_txt,font=font, fill =(0, 0, 0))
                
                #Adds distribution Info
                ImageDraw.Draw(img).text((50, 780), "Distribution Type: "+df.loc[i]['Distribution'],font=font, fill =(0, 0, 0))
                ImageDraw.Draw(img).text((50, 795), "Inter Event Type: 36h",font=font, fill =(0, 0, 0))
                ImageDraw.Draw(img).text((250, 780), "Threshold: "+str(df.loc[i]['Threshold'])+ var_txt,font=font, fill =(0, 0, 0))
                ImageDraw.Draw(img).text((250, 795), "Confidence Level: 5 and 95%",font=font, fill =(0, 0,0))

                #Get table with df
                df_table=pd.read_csv(path+df.loc[i]['Distribution']+'.txt',sep='\t',index_col=0)
                df_table=df_table.round(2)

                plt.figure(figsize=(10,5))
                plt.axis('off')
                plt.margins(x=0)
                    
                #Save All
                img.save(path_resultsFinal+ nameimg+'.png')
                df_table.to_csv(path_resultsFinal+nameTable+'.txt')

#Check if Complete table was created

#Create extreme table
path_resultsExtreme_list=[]
name_dir_list=[]

#Get path for each variable
for i in range(len(df)):
    if df.loc[i]['Variable'] =='Hmax':
        pass
    else:
        path_resultsExtreme=get_path_extreme(df.loc[i]['Depth'],df.loc[i]['Points'],df.loc[i]['Variable'])
        path_resultsExtreme_list.append(path_resultsExtreme)
        name_dir_list.append(df.loc[i]['Direction'])


for path_resultsExtreme in path_resultsExtreme_list:

    df_extreme=pd.DataFrame()
    name_list=[]
    check_for_completetable(path_resultsExtreme)
    files = [os.path.join(path_resultsExtreme, f) for f in os.listdir(path_resultsExtreme) if f.endswith('.txt')]

    for file in range(len(files)):

        binary=check_for_txt(path_resultsExtreme)
        if binary == 0:
            pass
        else:
            df_table=pd.read_csv(path_resultsExtreme+path_resultsExtreme.split('/')[2]+'_ExtremeAnalysisTable_'+check_var_inverse(path_resultsExtreme.split('/')[3])+'_'+name_dir_list[file]+'.txt',index_col=0)
            df_return_value=df_table.loc[:,'return value']
            df_extreme = pd.concat([df_extreme, df_return_value], axis=1)
            name_list.append(name_dir_list[file])
    
    #Organiza dataframe
    df_extreme.columns=name_list
    north_column = df_extreme.copy().pop(df_extreme.columns[-1]) 
    df_extreme.insert(1, north_column.name, north_column) 

    #Create extreme table for all directions needed
    df_extreme = df_extreme.pop(df_extreme.columns[-1])  # Remove column 'B'
    df_extreme = df_extreme.T
    df_extreme.index = df_extreme.index.set_names('Directional Sectors[N°]')

    df_extreme.to_csv(path_resultsExtreme+'ExtremeAnalysisTable_complete.txt',sep='\t')
    
print("Done!")