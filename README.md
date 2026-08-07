System librares required:
-python 3.8+
-pandas
-numpy
-scipy
-matplotlib


System requires data of the form:
product	type	set	cost	sale	current market value 	show time	purchased date	sold date	notes

The format makes inputting easier to go from 
	show -> discord -> .csv -> system


To run the system:

1. Put raw .csv data into raw data folder

2. Test the data by running 00-load-validate-data.py with command
	python3 00-load-validate-data.py raw_data/{...}

3. Clean any missing values and set datetime object with date columns with command
	python3 01-clean-missing-values.py raw_data/{...}

4. The final cleaning phase is to split the cleaned data by each show for statistical analysis. Do this by running
	python3 02-split-by-shows.py

5. Start calculating business statistics with command
	python3 03-anaylize-sales.py {tax_rate}

6. Calculate stats related to investments for anaylsis with command
	python3 04-analyize-increase-in-value.py

7. Display plots of sales over time with command
	python3 05-generate-plots-all-sales.py

8. Generate plots of each show with command
	python3 06-generate-plots-per-shows.py
