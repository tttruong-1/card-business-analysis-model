import pathlib
import numpy as np
import pandas as pd

INVESTMENT_OUTPUT_TEMPLATE = (
    "Average return on investment: {avg_roi:.2g}%\n"
    "Average daily return: {avg_daily_roi:.2f}% per day"
)

def calculate_stats(data):
    data = data.copy()

    data["profit"] = data["sold"] - data["cost"]
    data["sold date"] = pd.to_datetime(data["sold date"])
    data["purchased date"] = pd.to_datetime(data["purchased date"])

    # calculate time elapsed in days
    data["days hold"] = (data["sold date"] - data["purchased date"]).dt.total_seconds() / (24 * 3600)

    # calculate roi as percent
    data["roi"] = (data["profit"] / data["cost"]) * 100

    # calculate daily roi
    days = data["days hold"].replace(0, np.nan)
    data["daily_roi"] = data["roi"] / days

    # calculate avgerage roi and daily roi
    avg_roi = data["roi"].mean()
    avg_daily_roi = data["daily_roi"].mean()

    metrics = {
        "avg_roi": avg_roi,
        "avg_daily_roi": avg_daily_roi
    }

    top_20 = data.nlargest(20, "roi")

    return metrics, top_20

def print_stats(title, metrics, top_20):
    print("---------------------")
    print(f"Investment Stats on: {title}")
    print()
    print(INVESTMENT_OUTPUT_TEMPLATE.format(**metrics))
    print()

    for i, (_, row) in enumerate(top_20.iterrows(), start=1):
        print(
            f"{i:2d}. {row['item']} ({row['product type']}): "
            f"Cost ${row['cost']:.2f} | Sold ${row['sold']:.2f} | "
            f"Profit ${row['profit']:.2f} | ROI: {row['roi']:.2f}%"
        )

    print()
    print()

def main(in_directory, split_directory):
    input_path = pathlib.Path(in_directory)
    split_path = pathlib.Path(split_directory)

    data = pd.read_csv(input_path)

    # investment stats for all sales
    metrics, top_20 = calculate_stats(data)
    print_stats("All Items", metrics, top_20)

    # investment stats of each show
    if split_path.exists():
        for csv_file in sorted(split_path.glob("*.csv")):
            show_data = pd.read_csv(csv_file)
            show_stats, top_20 = calculate_stats(show_data)
            print_stats(csv_file.stem, show_stats, top_20)


    print("All stats successfully calculated!")


if __name__=='__main__':
    in_directory = "cleaned/cleaned_data.csv"
    split_directory = "split"
    main(in_directory, split_directory)
