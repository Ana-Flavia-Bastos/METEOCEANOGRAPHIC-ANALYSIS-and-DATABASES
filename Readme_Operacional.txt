Folders:
dfs0 -> local of dfs0 files to run “main_operation.py”
Requirements.txt -> Python libraries to run source codes
operational_info.csv -> User input data for operational script
main_operation.py -> main function for operational script
function_operations.py -> functions for operational script
function_histogram.py -> function to create histograms 
function_frequencytables.py -> function to create frequency tables

Running:

1)      If need, pip install -r Requirements.txt

2)	Complete "operational_info.csv"
		Type analysis => Chosse one of the type analysis
				[Wind
				 Air Temperature
				 Wave
				 Sea Water Temperature
				 Current
				 Water Level]

		Variable => Choose one of the variables matching the type analysis
				[Wind Speed
				 Wind Direction
				 Air Temperature
				 Hm0
				 Tp
				 MWD
				 Sea Water Temperature
				 Current Speed
				 Current Direction]
		Point=> Name for Point of interess
		Depth=> Name for Depth along water column (Current and Sea Water Temperature) 
			total sea state,wind,swell components (Wave)
			others variables the cel should remain empty
		dfs0 => Name of the correspondent dfs0 data for type analysis (add extension .dfs0)
		bins => Intervals to be used [Start:Step:Stop)

3)	Run main_operation.py

4)	Dfs0 folder:
		The code will run for all the .dfs0 files in this folder. Keep just one type of variable per dfs0 (e.g waves).
		In the “dfs0_examples” folder, there is one type of .dfs0 for each one of the variables as a reference.
		- You must use the same type of items as the reference file.
		- The code needs the units to be (m/s, degree, Celsius)

5)	Intervals folder:
		-The intervals for each variable is estabilish in the excel under bins column 
		-The interval for direction sector is asked (optins are:8=45°, 16=22.5°, 24=15°)

6)	Results folder:
		All the outputs are generated in this folder and put into subfolders according with points and type analysis
