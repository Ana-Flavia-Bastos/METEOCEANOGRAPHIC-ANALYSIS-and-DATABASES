import re
import numpy as np
import pandas as pd
import seaborn as sns
import warnings
from matplotlib.colors import ListedColormap
import matplotlib.pyplot as plt
from matplotlib import gridspec, cm
from windrose import WindroseAxes

warnings.filterwarnings('ignore')

def parse_range_string(range_string):
    input_range = re.match(r'\[([-+]?[0-9]*\.?[0-9]+):([-+]?[0-9]*\.?[0-9]+):([-+]?[0-9]*\.?[0-9]+)]', range_string)
    if input_range:
        return tuple(map(float, input_range.groups()))
    else:
        raise ValueError("Formato invalido. Insira no formato: '[start:bin_width:end]'.")
    
def organize_bins(variables,bins):

    if variables not in ['Wind Direction','Current Direction','MWD']:
        range_start, bin_width, range_end = parse_range_string(bins)
    else:
        range_end = 360
        bin_width=float(bins.split(':')[1])
        if bins == '[0:45:360]':
            range_end=337.5
            range_start = -22.5
        elif bins == '[0:22.5:360]':
            range_end=348.75
            range_start= -11.25
        elif bins == '[0:15:360]':
            range_end=352.5
            range_start= -7.5

    return range_start, bin_width, range_end

def organized_North_values(df,dfs_month,variables):

    df[variables]=np.where(df[variables].values>=348.749999,df[variables]-360,df[variables])
    for i in range(len(dfs_month)):
        dfs_month[i][variables]=np.where(dfs_month[i][variables].values>=348.75,dfs_month[i][variables]-360,dfs_month[i][variables])

    return df,dfs_month

def create_directions_intervals(n_interval):
    # Create intervals for directions 
    n_interval = int(n_interval)
    if n_interval == 8:
        direction_intervals_left = np.array([0.,22.5,67.5,112.5,157.5,202.5,247.5,282.5,337.5])
        direction_intervals_right = np.array([22.5,67.5,112.5,157.5,202.5,247.5,282.5,337.5,360.])
        #labels = ['N_start','NE','E','SE','S','SW','W','NW','N_end']
        labels = ['[0-22.5)','[22.5 - 67.5)','[67.5 - 112.5)','[112.5 - 157.5)','[157.5 - 202.5)','[202.5 - 247.5)','[247.5 - 282.5)','[282.5 - 337.5)','[337.5 - 360)']
    elif n_interval == 16:
        direction_intervals_left = np.array([0.,11.25,33.75,56.25,78.75,101.25,123.75,146.25,168.75,191.25,213.75,236.25,258.75,281.25,303.75,326.25,348.75])
        direction_intervals_right = np.array([11.25,33.75,56.25,78.75,101.25,123.75,146.25,168.75,191.25,213.75,236.25,258.75,281.25,303.75,326.25,348.75,360])
        #labels = ['N_start','NNE','NE','ENE','E','ESE','SE','SSE','S','SSW','SW','WSW','W','WNW','NW','NNW','N_end']
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
    return direction_intervals, labels

def cut_df_absolute(df, absolute_intervals, column_to_cut):
    # Cut DataFrame according absolute intervals
    cutted_column = pd.cut(x=column_to_cut,
                           bins=absolute_intervals,
                           right=False)
    df[column_to_cut.name+'_intervals'] = cutted_column
    return df

def cut_df_directions(df, direction_intervals, column_to_cut):
    # Cut DataFrame according directions intervals
    cutted_column = pd.cut(x=column_to_cut,
                           bins=direction_intervals,
                           include_lowest=True)
    df[column_to_cut.name+'_intervals'] = cutted_column
    return df

def create_cross_table(df, vertical_column, horizontal_column):
    # Create cross table
    cross_table = pd.crosstab(index=vertical_column,
                              columns=horizontal_column,
                              dropna=False)
    cross_table.index = cross_table.index.astype(str)
    cross_table.columns = cross_table.columns.astype(str)
    return cross_table

def join_north_directions(cross_table,direction_intervals,n_interval):
    if int(n_interval) == 16:
        bin_n='['+ str(360-(360+((360/int(n_interval))/2))) +','+str(direction_intervals[0])[6:11]+')'
    else:
        bin_n='['+ str(360-(360+((360/int(n_interval))/2))) +','+str(direction_intervals[0])[6:11]
    # Sum frquency in N direction
    cross_table[bin_n] = cross_table[str(direction_intervals[0])]+cross_table[str(direction_intervals[-1])]
    del cross_table[str(direction_intervals[0])]
    del cross_table[str(direction_intervals[-1])]
    first_column = cross_table.pop(bin_n)
    cross_table.insert(0,bin_n,first_column)

    return cross_table

def calculate_percentage(cross_table, ts_len):    
    # Calculate percentage
    cross_table = (cross_table/ts_len)
    return cross_table

def sum_rows_and_columns(cross_table,freq):
    # Sum rows and columns of the DataFrame
    cross_table.loc[freq,:] = cross_table.sum(axis=0)
    cross_table.loc[:,freq] = cross_table.sum(axis=1)
    return cross_table

def cumulative_rows_and_columns(cross_table,acum_freq):
    # Sum rows and columns of the DataFrame
    cross_table.loc[acum_freq,:]= cross_table.iloc[-1,:-1].cumsum()
    cross_table.loc[:,acum_freq] = cross_table.iloc[:-2,-1].cumsum()
    return cross_table

def round_df(cross_table):
    # Round DataFrame
    cross_table = round(cross_table, 10)
    return cross_table

def treat_vertical_index(cross_table):
    # Treat vertical index plotting
    cross_table.index.name = '%'
    cross_table_index = list(cross_table.index)
    # Loop over the index
    for i in range(len(cross_table_index)):
        if i < (len(cross_table_index)-3):
            cross_table_index[i] = cross_table_index[i]
        elif i == (len(cross_table.index)-3):
            cross_table_index[i] = '>= '+cross_table.index[i][1:5].replace(',','')
            #index_to_df = index_to_df.replace('.','')
        #if i == 0:
        #    cross_table_index[i] = cross_table.index[i].replace('[','(')
    cross_table.index = cross_table_index
    return cross_table

def treat_horizontal_index(cross_table):
    # Treat horizontal index
    cross_table_index = list(cross_table.columns)
    # Loop over the index
    for i in range(len(cross_table_index)):
        if i == (len(cross_table.columns)-3):
            index_to_df = '> '+cross_table.columns[i][1:5].replace(',','')
            #index_to_df = index_to_df.replace('.','')  
            cross_table_index[i] = index_to_df
        if i == 0:
            cross_table_index[i] = cross_table.columns[i].replace('[','(')
    cross_table.columns = cross_table_index
    return cross_table

def plot_heat_map(cross_table, x_axis_name, y_axis_name, period,path_results,time,point,depth):
    
    # Plot heat map
    plot_cmap = cm.get_cmap('Blues')
    # Create figure and axis
    fig = plt.figure(figsize=(15, 9)) 
    gs = gridspec.GridSpec(2,2,width_ratios=[8, 1],height_ratios=[8, 1]) 
    fig.suptitle(point+' '+depth+'\nFrequency Table - '+x_axis_name+' X '+y_axis_name+' - '+time)
    plt.rc('font', size=9)
    # Main heat map
    ax0 = plt.subplot(gs[0])
    plot_table = cross_table.iloc[0:-2,0:-2]
    if x_axis_name in ['Wind Speed','Current Speed']:
        plot_table.index.name = x_axis_name + ' [m/s]'
    elif x_axis_name in['Hm0','Hmax']:
        plot_table.index.name = x_axis_name + ' [m]'
    elif x_axis_name in ['Tp']:
        plot_table.index.name = x_axis_name + ' [s]'

    if y_axis_name in ['Wind Speed','Current Speed']:
       plot_table.columns.name = y_axis_name + ' [m/s]'
    elif y_axis_name in ['Hm0','Hmax']:
        plot_table.columns.name = y_axis_name + ' [m]'
    elif y_axis_name in ['Wind Direction','MWD']:
        plot_table.columns.name = y_axis_name + ' [°N-from]'
    elif  y_axis_name in ['Current Direction']:
        plot_table.columns.name = y_axis_name + ' [°N-to]'
    elif y_axis_name in ['Tp']:
        plot_table.columns.name = y_axis_name + ' [s]'

    sns.heatmap(plot_table,annot=True,fmt='.2%',cmap=plot_cmap,linecolor='white',linewidths=0.2,cbar=False, ax=ax0)
    sns.heatmap(plot_table,mask=cross_table.iloc[0:-2,0:-2]!=0.,annot=True,annot_kws={'color':'lightgrey'},fmt='.2%',cmap=ListedColormap(['white']),linecolor='white',linewidths=0.08,cbar=False,ax=ax0)
    ax0.xaxis.tick_top()
    ax0.xaxis.set_label_position('top')
    ax0.tick_params(axis='x',labelrotation=45,length=0)
    if period == True:
        ax0.tick_params(axis='x',length=0,labelsize=8)
    ax0.tick_params(axis='y',labelrotation=360,length=0)
    # Column heat map
    plot_table = cross_table.iloc[0:-2,-2:]
    plot_table.index.name = None
    plot_table.columns.name = None
    ax1 = plt.subplot(gs[1])
    sns.heatmap(plot_table,annot=True,fmt='.2%',cmap=ListedColormap(['white']),linecolor='white',linewidths=0.2,cbar=False,ax=ax1,yticklabels=False)
    ax1.xaxis.tick_top()
    ax1.xaxis.set_label_position('top')
    ax1.tick_params(axis='x',labelrotation=45,length=0)
    # Row heat map    
    plot_table = cross_table.iloc[-2:,0:-2]
    plot_table.index.name = None
    plot_table.columns.name = None
    ax2 = plt.subplot(gs[2])
    sns.heatmap(plot_table,annot=True,fmt='.2%',cmap=ListedColormap(['white']),linecolor='white',linewidths=0.2,cbar=False,ax=ax2,xticklabels=False)
    ax2.tick_params(axis='y',length=0)
    # Save to file
    plt.tight_layout()
    fig.savefig(path_results+point+'_FrequencyTable_'+x_axis_name+' vs. '+y_axis_name+'_'+time+'.png')

def plot_rose(dfs_intervals,nsector,variables,bins,time,path_results,point,depth):

    if len(variables)==3:
        #Organizing correct order of variables
        name_columnVar=[]
        title=[]
        bins_l=[]
        for v in range(len(variables)):
            if variables[v] in ['Wind Speed','Current Speed']:
                name_columnVar.append(variables[v])
                bins_l.append(bins[v])
                title.append(variables[v] + ' [m/s]')
            elif variables[v] in ['Hm0']:
                name_columnVar.append(variables[v])
                bins_l.append(bins[v])
                title.append(variables[v] + ' [m]')
            elif variables[v] in ['Tp']:
                name_columnVar.append(variables[v])
                title.append(variables[v] + ' [s]')
                bins_l.append(bins[v])
            else:
                name_dir=variables[v]

        # Plot rose for each variable
        for n in range(len(name_columnVar)):

            plot_cmap = cm.get_cmap('Blues')
            range_start, bin_width,range_end = parse_range_string(bins_l[n])
            bin=np.arange(range_start,range_end+bin_width,bin_width)
            for i in range(len(dfs_intervals)):
                df=dfs_intervals[i]
                absolute_column=df.loc[:][name_columnVar[n]]
                direction_column=df.loc[:]['MWD']
                # Plot rose
                fig, axs = plt.subplots(figsize=(15, 9))
                axs.axis('off')
                ax = WindroseAxes.from_ax(theta_labels=['E','NE','N','NW','W','SW','S','SE'],fig=fig)
                ax.bar(direction=direction_column,
                        var=absolute_column,
                        bins=bin,
                        nsector=nsector,
                        cmap=cm.get_cmap(plot_cmap),
                        normed=True,
                        opening=.9,
                        edgecolor='black')

                ax.legend(loc='center left',bbox_to_anchor=(1.05, 0.5),title=title[n],fontsize=12)
                fig.text(0.5, 0.5, '%', color='black',
                    bbox=dict(facecolor='black', edgecolor='black', boxstyle='circle', color='lightgray'))
                plt.title(point+' '+depth+'\nRose Plot - '+name_columnVar[n]+' - '+time[i])

                print('Create '+time[i]+' '+name_columnVar[n]+' Rose Plot')
                fig.savefig(path_results+point+'_RosePlot_'+name_columnVar[n]+' vs. '+name_dir+'_'+time[i]+'.png',bbox_inches='tight',pad_inches=0.1)
    
    else:

        #Organizing correct order of variables
        for v in range(len(variables)):
            if variables[v] not in ['Wind Direction','Current Direction','MWD']:
                b=v
                n=variables[v]
                if variables[v] in ['Wind Speed','Current Speed']:
                    title=variables[v] + ' [m/s]'
                elif variables[v] in ['Hm0']:
                    title=variables[v] +' [m]'
                elif variables[v] in ['Tp']:
                    title=variables[v] + ' [s]' 
            else:
                n_dir= variables[v]

        plot_cmap = cm.get_cmap('Blues')
        range_start, bin_width,range_end = parse_range_string(bins[b])
        bin=np.arange(range_start,range_end+bin_width,bin_width)
        for i in range(len(dfs_intervals)):
            df=dfs_intervals[i]
            absolute_column=df.loc[:][n]
            direction_column=df.loc[:][n_dir]
            # Plot rose
            fig, axs = plt.subplots(figsize=(15, 9))
            axs.axis('off')
            ax = WindroseAxes.from_ax(theta_labels=['E','NE','N','NW','W','SW','S','SE'],fig=fig)
            ax.bar(direction=direction_column,
                    var=absolute_column,
                    bins=bin,
                    nsector=nsector,
                    cmap=cm.get_cmap(plot_cmap),
                    normed=True,
                    opening=.9,
                    edgecolor='black')

            ax.legend(loc='center left',bbox_to_anchor=(1.05, 0.5),title=title,fontsize=12)
            fig.text(0.5, 0.5, '%', color='black',
                bbox=dict(facecolor='black', edgecolor='black', boxstyle='circle', color='lightgray'))
            plt.title(point+' '+depth+'\nRose Plot - '+n+' - '+time[i])

            print('Create '+time[i]+' '+n+' Rose Plot')
            fig.savefig(path_results+point+'_RosePlot_'+n+' vs. '+n_dir+'_'+time[i]+'.png',bbox_inches='tight',pad_inches=0.1)
        