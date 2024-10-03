Folders:
Omnidirectional-> local of omnidirectional dfs0s files to run “main_extrermeanalysis.ipynb”
backup -> jupiter codes backup
separate_byDirection -> function to create directional dfs0 if directional analysis is needed
Extreme_Analysis.csv -> User input data for extreme analysis script
main_extrermeanalysis.ipynb -> main function for extreme analysis script (jupiter file)
select_Threshold.ipynb -> function generates the stability an residual life images to define the threshold.
 

#Running:
1) If need, pip install -r Requirements.txt

2) Transfer dfs0 of interess to Omnidirectional folder

3) If directional extreme analysis is needed you must run (separate_byDirection.py) to create the separated dfs0, otherwise continue to next step;

4) Use the selected_Threshold.ipynb to generate the stability an residual life images to define the threshold.
	- Change the file name of dfs0 in file

5) Complete the first columns 4 columns of Extreme_Analysis.csv

	Index=> binary variable (0=pass - 1=Do it)
	Point=> Name for Point of interess
	Depth=> Name for Depth along water column (Current and Sea Water Temperature) 
			total sea state,wind,swell components (Wave)
			others variables the cel should remain empty
	File => Name of the correspondent dfs0 on omnidirectional folder (without extension .dfs0)
			In case of Wave analysis of Hm0 and Hmax, for Hmax use:Wave_Hmax_TSS
	Variable => Choose one of the variable for extreme analysis
				[Wind Speed
				 Current Speed
				 Air Temperature
				 Hm0
				 Hmax	
				 Sea Water Temperature
				 Water Level]
	Direction => Choose between Omnidirectional or the range of direction, for example: [348.75 - 11.25)
	Threshold=> Threshold used for extreme analysis (Tip: use the images from folder Threshold)

6) a)Use main_extremeanalysis.ipynb to generete extreme analysis -> this calculate using 7 types of distribution: Exponentional, Generalized Pareto, Truncated Pareto, 	Pareto,Lognorm,Generalized Extreme Value,Pearson3

   b)Select the best Distribution for each case using the images and complete the last column of Extreme Analysis.csv
	*use not if the available data is to few
7) Run final_result.py to organize data for apêndices

#################################
To use jupyter notebook:
	
	1-Run jupyter notebook in cmd
	2- In VScode Select kernal (localhost):
		-Select another kernel (top-right)
		-Select Existing Jupyter Server
		-Copy url open in VScode open window