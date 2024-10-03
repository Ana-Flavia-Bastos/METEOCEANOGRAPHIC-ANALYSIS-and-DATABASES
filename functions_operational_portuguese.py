import pandas as pd
import numpy as np
import os
import warnings
import matplotlib.pyplot as plt

from functions_base_portuguese import *
from function_frequencytables_portuguese import *
from function_histogram_portuguese import *

warnings.filterwarnings('ignore')

######################################Create Folder for Results if does not exist############################################

def create_folders_results_points(points):
    for p in points:
        path='./Resultados/'+p+'/'
        if not os.path.exists(path):    
            os.makedirs(path)

def create_folders_results_analysis(typeanalysis,points):
    for p in range(len(points)):
        for ty in typeanalysis[p]:
            path='./Resultados/'+points[p]+'/'+ty+'/'
            if not os.path.exists(path):    
                os.makedirs(path)
                
def create_folders_results_depth(typeanalysis,depth,points):

    for p in range(len(points)):
        for i in range(len(typeanalysis[p])):
            if typeanalysis[p][i] in ['Corrente','Temperatura da Água']:
                for d in range(len(depth[p][i])):
                    path='./Results/'+points[p]+'/'+typeanalysis[p][i]+'/'+depth[p][i][d]
                    if not os.path.exists(path):    
                        os.makedirs(path)
                    
############################################Get Type analysis and Dfs0 by point###############################################

def get_typeanalysis_dfs0(points,df):

    typeanalysis=[]
    for p in points:
        typeanalysis_perpoint=[]    
        for d in range(len(df)):
            if df.loc[d]['Ponto']== p:
                typeanalysis_perpoint.append(df.loc[d]['Tipo Analise'])
        typeanalysis_l=list(dict.fromkeys(typeanalysis_perpoint))
        typeanalysis.append(typeanalysis_l)

    return typeanalysis

####################################### Get Variable and Bins and Depth by Type analysis ##########################################

def get_variables_bins_depth_dfs0(points,typeanalysis,df):
    variables=[]
    bins=[]
    depths=[]
    dfs0=[]
    depths_complete=[]
    for p in range(len(points)):
        variables_perpoint=[]
        bins_perpoint=[]
        depths_perpoint=[]
        depths_complete_perpoint=[]
        dfs0_perpoint=[]      
        for ty in typeanalysis[p]:
            variable_pertype=[]
            bins_pertype=[]
            depths_pertype=[]
            depths_complete_pertype=[]
            dfs0_pertype=[]
            for t in range(len(df)):
                if df.iloc[t]['Tipo Analise']==ty and df.iloc[t]['Ponto']==points[p]:
                    variable_pertype.append(df.iloc[t]['Variavel'])
                    bins_pertype.append(df.iloc[t]['Intervalos'])
                    depths_pertype.append(df.iloc[t]['Pronfundidade'])
                    depths_complete_pertype.append(df.iloc[t]['Profundidade'])
                    dfs0_pertype.append(df.iloc[t]['Dfs0'])
            dfs0_pertype=list(dict.fromkeys(dfs0_pertype))
            depths_pertype=list(dict.fromkeys(depths_pertype))
            variables_perpoint.append(variable_pertype)
            bins_perpoint.append(bins_pertype)
            depths_perpoint.append(depths_pertype)
            depths_complete_perpoint.append(depths_complete_pertype)
            dfs0_perpoint.append(dfs0_pertype)
        variables.append(variables_perpoint)
        bins.append(bins_perpoint)
        depths.append(depths_perpoint)
        depths_complete.append(depths_complete_perpoint)
        dfs0.append(dfs0_perpoint)
        
    return variables,bins,depths,depths_complete,dfs0

################################################### Check for multiple depths ##################################################

def check_depth(depths,d):

    if str(depths[0]) =='nan':
        depth_l=""
    else:
        depth_l=depths[d]
        
    return depth_l 

def rearrange_fordepth(variables,bins,alldepth):

    depth_c=list(dict.fromkeys(alldepth))
    rearrange_var=[]
    rearrange_bins=[]
    for depth in range(len(depth_c)):
        var_perdepth=[]
        bins_perdepth=[]
        for d in range(len(alldepth)):   
            if depth_c[depth] == alldepth[d]:
                var_perdepth.append(variables[d])
                bins_perdepth.append(bins[d])
        rearrange_var.append(var_perdepth)
        rearrange_bins.append(bins_perdepth)

    return rearrange_var,rearrange_bins
 
##############################################Separate Dataframe into months##################################################

def separate_month(df):
    #Index into separate columns
    df['date'] = df.index
    df['month'] = df['date'].dt.month

    g=df.groupby(df.month)
    dfs_month=[group for _,group in g]

    #Clean dataframes
    dfs=[]
    for df_m in dfs_month:
        df_m=df_m.drop(['date','month'], axis=1)
        dfs.append(df_m)
    
    return dfs
    
############################################## Add unit in variable text ##################################################

def get_unit(variables):

    if variables in ['Altura Significativa','Nível médio da Água']:
        variables_n= variables + ' [m]'
    elif variables == 'Período': 
        variables_n= variables + ' [s]'
    elif variables in ['Direção média de Ondas','Direção do Vento']:
        variables_n= variables + ' [°N-from]'
    elif variables in ['Direção da Corrente']:
        variables_n= variables + ' [°N-to]'
    elif variables in ['Velocidade do Vento','Velocidade da Corrente']:
        variables_n= variables + ' [m/s]'
    elif variables in ['Temperatura do Ar','Temperatura da Água']:
        variables_n= variables + ' [° C]'
        
    return variables_n 
############################################## Create Stats Table ##################################################

def create_stats_table(df,path_results,variables,dfs_month,point,depth):

    for v in range(len(variables)):
        if variables[v] not in ['Direção do Vento', 'Direção da Corrente', 'Direção média de Ondas']:
            #Get stats from annual data
            stats=df[variables[v]].describe(percentiles=[0.05,0.5,0.95]).round(2)

            #Get Stats for each month
            for df_month in dfs_month:
                stats_month=df_month[variables[v]].describe(percentiles=[0.05,0.5,0.95]).round(2)
                
                #Combine all stats into one data frame
                stats=pd.concat([stats, stats_month], axis=1)

            #Rename Columns     
            stats.columns=['Anual','Jan','Fev','Mar','Abr','Maio','Jun','Jul','Ago','Set','Out','Nov','Dez']
            stats=stats.round(2)
            #Create table
            plt.figure(figsize=(10,5))
            plt.axis('off')
            variable_n=get_unit(variables[v])
            plt.title(point+' '+depth+' \n '+variable_n)

            rcolors=plt.cm.Greys(np.full(len(stats.index),0.1))
            ccolors=plt.cm.Greys(np.full(len(stats.columns),0.1))

            plt.table(cellText=stats.values,
                        colLabels=stats.columns,
                        colColours=ccolors,
                        rowLabels=stats.index,
                        rowColours=rcolors,
                        loc='center',
                        cellLoc='center')

            #Save Table
            print('Criando Tabela de Estatística '+variables[v])
            stats.to_csv(path_results+point+depth+'_Estatistica_'+str(variables[v])+'.txt',sep='\t',index='False')
            plt.savefig(path_results+point+'_Estatistica_'+str(variables[v])+'.png',bbox_inches='tight')

############################################## Create Histograms Table ##################################################

#Loop for annual and monthly
def create_histogram(df, dfs_month, variables, bins, path_results,point,depth):
    
    for v in range(len(variables)):
        
        time = ['Annual', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    
        if variables[v] in ['Direção do Vento','Direção da Corrente','Direção média de Ondas']:
            df_copy=df.copy()
            dfs_month_copy=dfs_month.copy()
            df_copy,dfs_month_copy=organized_North_values(df_copy,dfs_month_copy,variables[v])
            histogram_data = {t: {} for t in time}

            probability_histogram(df_copy, path_results, variables[v], bins[v],'Anual', point, depth, histogram_data)

            for i, t in enumerate(time[1:], 1):
                probability_histogram(dfs_month_copy[i - 1], path_results, variables[v], bins[v], t, point, depth, histogram_data)
        else:
            histogram_data = {t: {} for t in time}

            probability_histogram(df, path_results, variables[v], bins[v],'Anual', point, depth, histogram_data)

            for i, t in enumerate(time[1:], 1):
                probability_histogram(dfs_month[i - 1], path_results, variables[v], bins[v], t, point, depth, histogram_data)
        
        df_annual = pd.DataFrame(histogram_data['Anual']).set_index('Intervalos')

        df_months = {}
        for month in time[1:]:
            df_months[month] = pd.DataFrame(histogram_data[month]).set_index('Intervalos')

        # Combine monthly and annual data into a single DataFrame
        df_combined = df_annual.copy()
        for month, data in df_months.items():
            df_combined[month] = data['Anual']

        # Add cumulative data for the annual DataFrame
        #df_combined['Accum'] = df_annual['Accum']

        # Reorder the columns
        columns_order =  ['Anual']+time[1:]
        df_combined = df_combined[columns_order]
        df_combined=df_combined.round(2)

        # Save DataFrame to Excel
        print('Criando dados do histogram '+variables[v])
        df_combined.to_csv(path_results+point+'_DadosHistograma_'+str(variables[v])+'.txt',sep='\t',index='False')
               
############################################## Create Frequency Table ################################################## 

#Loop for annual and monthly
def create_frequencytable(df,variables,dfs_month,bins,path_results,n_intervals,point,depth): 

    dfs_intervals=[]
    time=['Anual','Jan','Fev','Mar','Abr','Maio','Jun','Jul','Ago','Set','Out','Nov','Dez']
    
    df_intervals=plot_frenquencytable(path_results,df,variables,bins,time[0],n_intervals,point,depth)
    dfs_intervals.append(df_intervals)

    for t in range(1,len(time)):
        df_intervals=plot_frenquencytable(path_results,dfs_month[t-1],variables,bins,time[t],n_intervals,point,depth)
        dfs_intervals.append(df_intervals)
    return dfs_intervals
    
################################################ Create Rose Plot ###################################################### 

def create_roseplot(dfs_intervals,n_intervals,variables,bins,path_results,point,depth):
    
    time=['Anual','Jan','Fev','Mar','Abr','Maio','Jun','Jul','Ago','Set','Out','Nov','Dez']
    n_intervals = int(n_intervals)
    plot_rose(dfs_intervals,n_intervals,variables,bins,time,path_results,point,depth)
    