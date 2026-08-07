import sys
import pathlib
import pandas as pd

BUSINESS_OUTPUT_TEMPLATE = (
    "Tax Rate: {tax:.3g}\n"
    "Total Revenue: ${total_sales:.2f}\n"
    "Total Taxes: ${total_taxes:.2f}\n"
    "Total Profits: ${total_profits:.2f}\n"
    "Total Profit Margin: {total_profits_margin:.3g}\n"
    "Average Selling Price: ${avg_selling_price:.3g}\n"
    "Median Selling Price: ${med_selling_price:.3g}\n"
    "Average Profit per Item: ${avg_profit_per_item:.3g}\n"
    "Peak of Sale times: {peak_sale_times:.3g}:00\n"
    "Amount of Sales: {amount_sales:.0f}\n"
    "Amount of Sales Over $100: {sales_over_100:.0f}\n"
    "Amount of Sales Between $50-$99: {sales_between_50_99:.0f}\n"
    "Amount of Sales Below $50: {sales_below_50:.0f}"
)

INVENTORY_OUTPUT_TEMPLATE = (
    "Set with Highest Sales: {highest_set_sales}\n"
    "Total Profit from Highest Set: ${profit_from_highest_set:.3g}\n"
    "Type with Highest Sales: {type_highest_sales}\n"
    "Amount of Card Sales: {amount_card_sales:.0f}\n"
    "Amount of Sealed Sales: {amount_sealed_sales:.0f}\n"
    "Amount of Graded Card Sales: {amount_graded_sales:.0f}\n"
    "Total Card Profits: ${total_card_profits:.2f}\n"
    "Total Sealed Profits: ${total_sealed_profits:.2f}\n"
    "Total Graded Card Profits: ${total_graded_profits:.2f}\n"
    "Average Card Profit: ${avg_card_profit:.3g}\n"
    "Average Sealed Profit: ${avg_sealed_profit:.3g}\n"
    "Average Graded Card Profit: ${avg_graded_profit:.3g}"
)

def calculate_sales(data, tax_rate):
    data = data.copy()
    data["profit"] = (data["sold"] * (1 - tax_rate)) - data["cost"]
    data["taxes"] = data["sold"] * tax_rate

    return data

def calculate_stats(data, tax_rate):
    data = calculate_sales(data, tax_rate)
    tax = tax_rate

    # business metrics
    total_sales = data["sold"].sum()
    total_taxes = data["taxes"].sum()
    total_profits = data["profit"].sum()
    total_profits_margin = total_profits / total_sales

    avg_selling_price = data["sold"].mean()
    med_selling_price = data["sold"].median()
    avg_profit_per_item = data["profit"].mean()

    data["sold date"] = pd.to_datetime(data["sold date"])
    peak_sale_times = data["sold date"].dt.hour.mode()[0]

    amount_sales = len(data)
    sales_over_100 = (data["sold"] > 100).sum()
    sales_between_50_99 = ((data["sold"] >= 50) & (data["sold"] < 100)).sum()
    sales_below_50 = (data["sold"] < 50).sum()

    # inventory metrics
    highest_set_sales = data.groupby("set")["sold"].sum().idxmax()
    profit_from_highest_set = data[data["set"] == highest_set_sales]["profit"].sum()
    type_highest_sales = data.groupby("product type")["sold"].sum().idxmax()

    amount_card_sales = len(data[data["product type"] == "card"])
    amount_sealed_sales = len(data[data["product type"] == "sealed"])
    amount_graded_sales = len(data[data["product type"] == "graded card"])

    total_card_profits = data[data["product type"] == "card"]["profit"].sum()
    total_sealed_profits = data[data["product type"] == "sealed"]["profit"].sum()
    total_graded_profits = data[data["product type"] == "graded card"]["profit"].sum()

    avg_card_profit = data[data["product type"] == "card"]["profit"].mean()
    avg_sealed_profit = data[data["product type"] == "sealed"]["profit"].mean()
    avg_graded_profit = data[data["product type"] == "graded card"]["profit"].mean()

    return {
        "tax": tax,
        "total_sales": total_sales,
        "total_taxes": total_taxes,
        "total_profits": total_profits,
        "total_profits_margin": total_profits_margin,
        "avg_selling_price": avg_selling_price,
        "med_selling_price": med_selling_price,
        "avg_profit_per_item": avg_profit_per_item,
        "peak_sale_times": peak_sale_times,
        "amount_sales": amount_sales,
        "sales_over_100": sales_over_100,
        "sales_between_50_99": sales_between_50_99,
        "sales_below_50": sales_below_50,
        "highest_set_sales": highest_set_sales,
        "profit_from_highest_set": profit_from_highest_set,
        "type_highest_sales": type_highest_sales,
        "amount_card_sales": amount_card_sales,
        "amount_sealed_sales": amount_sealed_sales,
        "amount_graded_sales": amount_graded_sales,
        "total_card_profits": total_card_profits,
        "total_sealed_profits": total_sealed_profits,
        "total_graded_profits": total_graded_profits,
        "avg_card_profit": avg_card_profit,
        "avg_sealed_profit": avg_sealed_profit,
        "avg_graded_profit": avg_graded_profit
    }

def print_stats(title, metrics):
    print("---------------------")
    print(f"Stats for show: {title}")
    print()
    print(BUSINESS_OUTPUT_TEMPLATE.format(**metrics))
    print()
    print(INVENTORY_OUTPUT_TEMPLATE.format(**metrics))
    print()
    print()

def main(in_directory, split_directory, tax_rate):
    input_path = pathlib.Path(in_directory)
    split_path = pathlib.Path(split_directory)

    data = pd.read_csv(input_path)

    # all sales
    metrics = calculate_stats(data, tax_rate)
    print_stats("All Sales", metrics)

    # sales of each show
    if split_path.exists():
        for csv_file in sorted(split_path.glob("*.csv")):
            show_data = pd.read_csv(csv_file)
            show_stats = calculate_stats(show_data, tax_rate)
            print_stats(csv_file.stem, show_stats)


    print("All stats successfully calculated!")


if __name__=='__main__':
    in_directory = "cleaned/cleaned_data.csv"
    split_directory = "split"
    tax = float(sys.argv[1])
    main(in_directory, split_directory, tax)
