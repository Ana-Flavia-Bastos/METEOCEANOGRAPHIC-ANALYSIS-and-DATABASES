import seaborn as sns
from matplotlib.ticker import FuncFormatter
import numpy as np
import matplotlib.pyplot as plt

from functions_base_portuguese import *

#Plot Histogram
def probability_histogram(df,path_results,variables,bins,time,point,depth,histogram_data):

    range_start, bin_width, range_end = organize_bins(variables,bins)
    
    bins_list = []
    counts_list = []
    cumulative_list = []
    

    if variables == ['Nível médio da Água','Altura Significativa']:
        variables_n= variables + ' [m]'
    elif variables == 'Período':
        variables_n= variables + ' [s]'
    elif variables in ['Direção média de Ondas','Direção do Vento']:
        variables_n= variables + ' [°N-de]'
    elif variables in ['Direção da Corrente']:
        variables_n= variables + ' [°N-para]'
    elif variables in ['Velocidade do Vento','Velocidade da Corrente']:
        variables_n= variables + ' [m/s]'
    elif variables in ['Temperatura do Ar','Temperatura da Água']:
        variables_n= variables + ' [°C]'

    fig, ax = plt.subplots()
    ax_cumulative = ax.twinx()
    ax.grid(True, color='lightgray', linewidth=0.5, zorder=0)
    ax_cumulative.grid(False)

    #Histograma
    sns.histplot(df[variables], binwidth=bin_width, binrange=(range_start, range_end), kde=False, stat='percent',
                    shrink=0.4, color='slategrey', edgecolor='black', alpha=1, ax=ax, zorder=3)
            
    #Linha cumulativa
    bin = np.arange(range_start,range_end+bin_width,bin_width)
    bin = bin.round(2)
    counts, _ = np.histogram(df[variables], bins=bin, range=(range_start, range_end))
    total_count = np.sum(counts)
    cumulative_counts = np.cumsum(counts) / total_count * 100
    cumulative_counts=np.insert(cumulative_counts,0,0)
    hist_percent = counts / total_count * 100
    
    # Append data to the lists
    bins_list.extend([f'[{bin[i]}-{bin[i + 1]}]' for i in range(len(bin) - 1)])
    counts_list.extend(hist_percent.tolist())
    #cumulative_list.extend(cumulative_counts.tolist())


    #Plot da linha cumulativa
    bin_midpoints = bin[:-1] + bin_width / 2
    bin_midpoints=np.insert(bin_midpoints,0,range_start)
    ax_cumulative.plot(bin_midpoints, cumulative_counts, color='dodgerblue', linestyle='-', linewidth=2, alpha=1,
                        zorder=4)
    
    ax.set_xlabel(variables_n, color='black') 
    ax.set_ylabel('Probabilidade [%]', color='black')
    ax_cumulative.set_ylabel('Acumulada [%]', color='black')
    ax.set_title(point+' '+depth+' \n '+f'Histograma - {variables} - {time}')

    # Adjust the y-ticks on the twin axes to match the original axes
    ax.set_yticks(np.linspace(0, ax.get_ybound()[1], 11))
    ax_cumulative.set_yticks(np.arange(0, 101, 10))
    ax.set_xticks(np.arange(range_start,ax.get_xbound()[1],bin_width),labels=np.arange(range_start,ax.get_xbound()[1],bin_width),rotation=45)

    ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f'{x:.0f}'))
    ax_cumulative.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f'{x:.0f}'))
    
    ax_cumulative.spines['bottom'].set_color('black')
    ax_cumulative.spines['left'].set_color('black')
    ax_cumulative.spines['right'].set_color('black')
    ax_cumulative.spines['top'].set_color('black')

    ax.set_xlim(range_start,range_end)
    ax.set_ylim(0)
    ax_cumulative.set_ylim(0,100)

    print('Criando histograma ' +time+' da variável ' +variables)
    fig.savefig(path_results+point+'_DadosHistograma_'+variables +'_'+time+'.png',bbox_inches='tight')
    
    # Store the data lists in the histogram_data dictionary
    histogram_data[time] = {
        'Intervalos': bins_list,
        'Anual': counts_list,
        #'Accum': cumulative_list
    }
    