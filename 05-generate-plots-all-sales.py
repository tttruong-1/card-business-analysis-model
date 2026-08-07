import pathlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd

def plot_sales(data):
    plt.figure(figsize=(12, 5))


    # plot sales over time ($0 - $400)
    plt.subplot(1, 3, 1)
    plt.title(r"Sales Over Time (\$0 - \$400)")
    plt.xlabel("Date")
    plt.ylabel("Sold Price ($)")
    sales_400 = (data["sold"] >= 0) & (data["sold"] <= 400)
    plt.scatter(
        data.loc[sales_400, "sold date"],
        data.loc[sales_400, "sold"],
        color="teal",
        alpha=0.6,
        edgecolors="k",
        linewidth=0.5,
        s=35
    )
    plt.ylim(0, 400)
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
    plt.xticks(rotation=45)
    plt.grid(True, linestyle="--", alpha=0.4)


    # plot sales over time ($0 - $100)
    plt.subplot(1, 3, 2)
    plt.title(r"Sales Over Time (\$0 - \$100)")
    plt.xlabel("Date")
    plt.ylabel("Sold Price ($)")

    sales_100 = (data["sold"] >= 0) & (data["sold"] <= 100)

    plt.scatter(
        data.loc[sales_100, "sold date"],
        data.loc[sales_100, "sold"],
        color="darkcyan",
        alpha=0.6,
        edgecolors="black",
        linewidth=0.5,
        s=35,
    )

    plt.ylim(0, 100)
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
    plt.xticks(rotation=45)
    plt.grid(True, linestyle="--", alpha=0.4)


    # plot sales by product type
    type_sales = data.groupby("product type")["sold"].sum()

    plt.subplot(1, 3, 3)
    plt.title("Total Revenue by Product Type")
    plt.xlabel("Product Types")
    plt.ylabel("Total Revenue ($)")
    plt.bar(
        type_sales.index, type_sales.values, color="skyblue", edgecolor="black"
    )
    plt.grid(axis="y", linestyle="--", alpha=0.5)

    plt.tight_layout()
    plt.savefig("sales_analysis.png")
    plt.close()

def main(in_directory):
    input_path = pathlib.Path(in_directory)

    data = pd.read_csv(input_path)
    data["sold date"] = pd.to_datetime(data["sold date"])

    plot_sales(data)


    print("All plots successfully generated!")


if __name__=='__main__':
    in_directory = "cleaned/cleaned_data.csv"
    split_directory = "split"
    main(in_directory)
