# Card Business Analysis Model

A model programmed in Python using pandas and data science concepts to analyze business statistics of Pokemon Trading card sales. Is primarily used for card vendors to track sales, calculate statistics and make informed business decisions and predictions with visuals.

## Key Features

- Prints business related statistics of sales from card shows. Outputs the averages, popular sets, popular types of products and profits.
- Creates graphical visualizations of statistics to aid in analysis.
- Divides sales by shows to see individual stats.

## System librares required

- python 3.8+
- pandas
- numpy
- scipy
- matplotlib

## .csv file format

Files must include rows ordered as:
```bash
product	type	set	cost	sale	current market value 	show time	purchased date	sold date	notes
```

```bash
The format makes inputting easier to go from:
	show -> discord -> .csv -> system
```

## To run the system

1. Put raw .csv data into raw data folder

2. Test the data by running 00-load-validate-data.py with command
```bash
	python3 00-load-validate-data.py raw_data/{...}
```

3. Clean any missing values and set datetime object with date columns with command
```bash
	python3 01-clean-missing-values.py raw_data/{...}
```

4. The final cleaning phase is to split the cleaned data by each show for statistical analysis. Do this by running
```bash
	python3 02-split-by-shows.py
```

5. Start calculating business statistics with command
```bash
	python3 03-anaylize-sales.py {tax_rate}
```

6. Calculate stats related to investments for anaylsis with command
```bash
	python3 04-analyize-increase-in-value.py
```

7. Display plots of sales over time with command
```bash
	python3 05-generate-plots-all-sales.py
```

8. Generate plots of each show with command
```bash
	python3 06-generate-plots-per-shows.py
```
