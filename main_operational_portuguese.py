import pandas as pd
import mikeio
import warnings

from functions_operational_portuguese import *

warnings.filterwarnings('ignore')

# Read excel
df=pd.read_csv('operacional_info.csv',sep=';', encoding='latin-1')

#Organize Excel Data
points=(list(dict.fromkeys(df['Point'])))
typeanalysis = get_typeanalysis_dfs0(points,df) #Type Analysis
variables,bins,depths,depths_complete,dfs0 = get_variables_bins_depth_dfs0(points,typeanalysis,df)#Variable, Bin, Depth, Dfs0

#n_intervals=input("Indique em quantos setores direcionais as variaveis devem ser divididas (Opções:8;16;24): ") # número de setores direcionais
n_intervals=16

#Paths
path_dfs0='./dfs0/'

#Create folders Results for each type analysis for each point  
create_folders_results_points(points) 
create_folders_results_analysis(typeanalysis,points)
create_folders_results_depth(typeanalysis,depths,points)

for p in range(len(points)):

    print('\nCriando resultados do '+points[p])

    #Create Stats ans Histograms and Frequecy Table
    for i in range(len(typeanalysis[p])):

        print('\n'+typeanalysis[p][i])
        
        for d in range(len(depths[p][i])):
        
            ds=mikeio.read(path_dfs0+dfs0[p][i][d])
            df=ds.to_dataframe()
            dfs_month=separate_month(df)
            df=df.drop(['date','month'], axis=1)
            
            if typeanalysis[p][i]=='Onda':
            
                print('\nCriando resultados de Onda.\n')                
                depth_wa=check_depth(depths[p][i],d)
                variable_wa=variables[p][i]
                path_results='./Resultados/'+points[p]+'/Onda/'           
                create_stats_table(df,path_results,variable_wa,dfs_month,points[p],depth_wa)
                create_histogram(df,dfs_month,variable_wa,bins[p][i],path_results,points[p],depth_wa)
                dfs_intervals=create_frequencytable(df,variable_wa,dfs_month,bins[p][i],path_results,n_intervals,points[p],depth_wa)
                create_roseplot(dfs_intervals,n_intervals,variable_wa,bins[p][i],path_results,points[p],depth_wa)
                
            elif typeanalysis[p][i]=='Vento':
                
                print('\nCriando resultados do Vento.')
                depth_wi=check_depth(depths[p][i],d)
                variable_wi=variables[p][i]
                path_results='./Resultados/'+points[p]+'/Vento/'
                create_stats_table(df,path_results,variable_wi,dfs_month,points[p],depth_wi)
                create_histogram(df,dfs_month,variable_wi,bins[p][i],path_results,points[p],depth_wi)
                dfs_intervals=create_frequencytable(df,variable_wi,dfs_month,bins[p][i],path_results,n_intervals,points[p],depth_wi)
                create_roseplot(dfs_intervals,n_intervals,variable_wi,bins[p][i],path_results,points[p],depth_wi)

            elif typeanalysis[p][i]=='Correntes':
            
                depth_c=check_depth(depths[p][i],d)
                variable_c,bins_c=rearrange_fordepth(variables[p][i],bins[p][i],depths_complete[p][i])
                print('\nCriando resultado Correntes' +str(depth_c[d]))
                path_results='./Resultados/'+points[p]+'/Correntes/'+depth_c+'/'
                create_stats_table(df,path_results,variable_c[d],dfs_month,points[p],depth_c)
                create_histogram(df,dfs_month,variable_c[d],bins_c[d],path_results,points[p],depth_c)
                dfs_intervals=create_frequencytable(df,variable_c[d],dfs_month,bins_c[d],path_results,n_intervals,points[p],depth_c)
                create_roseplot(dfs_intervals,n_intervals,variable_c[d],bins_c[d],path_results,points[p],depth_c)

            elif typeanalysis[p][i]=='Temperatura do Ar':
            
                print('\nCriando resultados de Temperatura do Ar.')
                depth_at=check_depth(depths[p][i],d)
                variable_at=variables[p][i]
                path_results='./Resultados/'+points[p]+'/Temperatura do Ar/'
                create_stats_table(df,path_results,variable_at,dfs_month,points[p],depth_at)
                create_histogram(df,dfs_month,variable_at,bins[p][i],path_results,points[p],depth_at)

            elif typeanalysis[p][i]=='Temperatura do Água':
            
                depth_swt=check_depth(depths[p][i],d)
                variable_swt,bins_swt=rearrange_fordepth(variables[p][i],bins[p][i],depths_complete[p][i])
                print('\nCriando resultados da Temperatura da Água '+str(depth_swt[d]))
                path_results='./Resultados/'+points[p]+'/Temperatura da Água/'+depth_swt+'/'
                create_stats_table(df,path_results,variable_swt[d],dfs_month,points[p],depth_swt)
                create_histogram(df,dfs_month,variable_swt[d],bins_swt[d],path_results,points[p],depth_swt)

            elif typeanalysis[p][i]=='Nível médio da Água':

                print('\nCriando resultados do Nível médio da Água')
                depth_wl=check_depth(depths[p][i],d)
                variable_wl=variables[p][i]
                path_results='./Results/'+points[p]+'/Nível médio da Água/'
                create_histogram(df,dfs_month,variable_wl,bins[p][i],path_results,points[p],depth_wl)
     
print('Done!')