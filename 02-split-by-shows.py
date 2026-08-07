import os
import pathlib
import pandas as pd

def main(in_directory, out_directory):
    input_path = pathlib.Path(in_directory)
    output_path = pathlib.Path(out_directory)

    data = pd.read_csv(input_path)

    os.makedirs(output_path, exist_ok=True)

    show = data['show']
    for show_name, group in data.groupby(show):
        print("---------------------")

        # ensure theres enough entries from a show (> 5) to make a seperate file for
        if len(group) < 6:
            print(f"Not enough entries for {show_name}. Skipped")
            print()
            continue

        # make a filename from show name
        filename = (
            "".join(c for c in str(show_name) if c.isalnum() or c in (" ", "_", "-")).rstrip().replace(" ", "_")
        )

        print(f"Show name: {show_name}")
        print(f"File name: {filename}")
        print(group)
        print()

        # output to new file
        file_path = output_path / f"{filename}.csv"
        group.to_csv(file_path, index=False)
        print(f"Successfully Exported show.")
        print()


    print()
    print()
    print("Data split by shows and saved to each .csv file")


if __name__=='__main__':
    in_directory = "cleaned/cleaned_data.csv"
    out_directory = "split"
    main(in_directory, out_directory)
