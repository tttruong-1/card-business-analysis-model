import sys
import os
import pathlib
import numpy as np
import pandas as pd

def main(in_directory, out_directory):
    input_path = pathlib.Path(in_directory)
    output_path = pathlib.Path(out_directory)

    data = pd.read_csv(input_path)
    
    print("Original Data:")
    print(data)
    print()

    # notes is for data gatherer so no need to include in anaylsis
    data = data.drop(columns=['notes'])

    # empty values default to noon (12pm)
    time = data['show time'].fillna('12:00')

    # convert to time date object on 'sold date' and 'purchase date'
    sold_dates = data['sold date'].fillna("2026-04-01") # default date to start of semester if empty
    data['sold date'] = pd.to_datetime(sold_dates.astype(str) + ' ' + time)

    purchased_dates = data['purchased date'].fillna("2026-04-01") # default date to start of semester if empty
    data['purchased date'] = pd.to_datetime(purchased_dates.astype(str) + " 12:00:00")

    # no longer need show time as it is included in sold dates
    data = data.drop(columns=['show time'])

    print("Dates Columns:")
    print(data[['purchased date', 'sold date']].head())
    print()

    # if cost has no value then default to 70% of sold cost (which is the standard purchasing rate of buyers)
    data['cost'] = np.where(data['cost'] == 0, data['sold'] * 0.70, data['cost'])

    print("Just Cost:")
    print(data[['cost', 'sold']].head())
    print()

    print("Sample Cleaned Data:")
    print(data)

    # output cleaned data to new file
    os.makedirs(output_path, exist_ok=True)
    data.to_csv(output_path / "cleaned_data.csv", index=False)

    print()
    print()
    print("Data cleaned and saved to new .csv file cleaned_data")


if __name__=='__main__':
    in_directory = sys.argv[1]
    out_directory = "cleaned"
    main(in_directory, out_directory)
