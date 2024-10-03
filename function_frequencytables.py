import numpy as np
import warnings

from functions_base import *

warnings.filterwarnings('ignore')

def plot_frenquencytable(path_results,df,variables,bins,time,n_intervals,point,depth):

    if len(variables) == 3:
        name_columnVar=[]
        for v in range(len(variables)):
            if variables[v] in ['Hm0','Tp']:
                name_columnVar.append(variables[v])
                # Create intervals for speed and period
                range_start, bin_width,range_end = parse_range_string(bins[v])
                absolute_intervals=np.arange(range_start,range_end+bin_width,bin_width)
                # Classify speed and period in the intervals
                df= cut_df_absolute(df, absolute_intervals, df.loc[:][variables[v]])   

            else:
                name_columnDir=variables[v]
                # Create intervals for directions
                direction_intervals, labels = create_directions_intervals(n_intervals)
                # Classify directions in the intervals                
                df = cut_df_directions(df, direction_intervals, df.loc[:][variables[v]])

        
        #Create Height and Period 
        for n in name_columnVar:        
            # Create the cross table
            cross_table = create_cross_table(df, df.loc[:][n+'_intervals'], df.iloc[:][name_columnDir+'_intervals'])        
            # Make correction for N direction
            cross_table = join_north_directions(cross_table,direction_intervals,n_intervals)
            # Calculate porcentage
            cross_table = calculate_percentage(cross_table, len(df))
            # Sum rows and columns
            cross_table = sum_rows_and_columns(cross_table,'Frequency')
            # Cumulative sum for rows and columns
            cross_table = cumulative_rows_and_columns(cross_table,'Cumulative Frequency')
            # Round the DataFrame
            cross_table = round_df(cross_table)
            # Treat vertical index
            cross_table = treat_vertical_index(cross_table)
        
            print('Create '+time+' '+n+'xMWD Frequency Table')
            plot_heat_map(cross_table,n,name_columnDir,False,path_results,time,point,depth)

        df_intervals=df
        # Create the cross table
        cross_table = create_cross_table(df, df.loc[:]['Hm0_intervals'], df.iloc[:]['Tp_intervals'])        
        # Calculate porcentage
        cross_table = calculate_percentage(cross_table, len(df))
        # Sum rows and columns
        cross_table = sum_rows_and_columns(cross_table,'Frequency')
        # Cumulative sum for rows and columns
        cross_table = cumulative_rows_and_columns(cross_table,'Cumulative Frequency')
        # Round the DataFrame
        cross_table = round_df(cross_table)
        # Treat vertical index
        cross_table = treat_vertical_index(cross_table)
        # Treat horizontal index
        cross_table = treat_horizontal_index(cross_table)

        print('Create '+time+' Hm0xTp Frequency Table')
        plot_heat_map(cross_table,'Hm0','Tp',False,path_results,time,point,depth)
        

    else:
        for v in range(len(variables)):
            if variables[v] in ['Wind Speed','Current Speed','Hm0']:
                name_columnVar=variables[v]
                # Create intervals for speed
                range_start, bin_width,range_end = parse_range_string(bins[v])
                absolute_intervals=np.arange(range_start,range_end+bin_width,bin_width)
                # Classify speed in the intervals
                df= cut_df_absolute(df, absolute_intervals, df.loc[:][variables[v]])   
            else:
                name_columnDir=variables[v]
                # Create intervals for directions
                direction_intervals, labels = create_directions_intervals(n_intervals)
                # Classify directions in the intervals                    
                df = cut_df_directions(df, direction_intervals, df.loc[:][variables[v]])

        df_intervals=df
        # Create the cross table
        cross_table = create_cross_table(df, df.loc[:][name_columnVar+'_intervals'], df.iloc[:][name_columnDir+'_intervals'])        
        # Make correction for N direction
        cross_table = join_north_directions(cross_table,direction_intervals,n_intervals)
        # Calculate porcentage
        cross_table = calculate_percentage(cross_table, len(df))
        # Sum rows and columns
        cross_table = sum_rows_and_columns(cross_table,'Frequency')
        # Cumulative sum for rows and columns
        cross_table = cumulative_rows_and_columns(cross_table,'Cumulative Frequency')
        # Round the DataFrame
        cross_table = round_df(cross_table)
        # Treat vertical index
        cross_table = treat_vertical_index(cross_table)
        
        print('Create '+time+' '+name_columnVar+'x' +name_columnDir+' Frequency Table')
        plot_heat_map(cross_table,name_columnVar,name_columnDir,False,path_results,time,point,depth)
    
    return df_intervals