def parse_transactions(raw_lines):
  
    transactions = []

    for line in raw_lines:
        parts = [p.strip() for p in line.split("|")]

        if len(parts) != 8:
            continue

        txn_id, date, prod_id, prod_name, qty, price, cust_id, region = parts

        try:
            qty = int(qty)
            price = float(price.replace(",", ""))
        except:
            continue

        prod_name = prod_name.replace(",", "")

        transactions.append({
            "TransactionID": txn_id,
            "Date": date,
            "ProductID": prod_id,
            "ProductName": prod_name,
            "Quantity": qty,
            "UnitPrice": price,
            "CustomerID": cust_id,
            "Region": region
        })

    return transactions


def validate_and_filter(transactions, region=None, min_amount=None, max_amount=None):

    valid_transactions = []
    invalid_count = 0

    regions = set()
    amounts = []

    for tx in transactions:
        amount = tx["Quantity"] * tx["UnitPrice"]
        regions.add(tx["Region"])
        amounts.append(amount)

        if (
            not tx["TransactionID"].startswith("T")
            or not tx["ProductID"].startswith("P")
            or not tx["CustomerID"].startswith("C")
            or tx["Quantity"] <= 0
            or tx["UnitPrice"] <= 0
            or not tx["Region"]
        ):
            invalid_count += 1
            continue

        if region and tx["Region"] != region:
            continue
        if min_amount and amount < min_amount:
            continue
        if max_amount and amount > max_amount:
            continue

        valid_transactions.append(tx)

    print(f"Available regions: {sorted(regions)}")
    if amounts:
        print(f"Transaction amount range: {min(amounts):.2f} - {max(amounts):.2f}")

    summary = {
        "total_input": len(transactions),
        "invalid": invalid_count,
        "final_count": len(valid_transactions)
    }

    return valid_transactions, invalid_count, summary

def calculate_total_revenue(transactions):

    return sum(tx["Quantity"] * tx["UnitPrice"] for tx in transactions)

def region_wise_sales(transactions):
    region_data = {}
    total_revenue = calculate_total_revenue(transactions)

    for tx in transactions:
        region = tx["Region"]
        revenue = tx["Quantity"] * tx["UnitPrice"]

        if region not in region_data:
            region_data[region] = {
                "total_sales": 0.0,
                "transaction_count": 0
            }

        region_data[region]["total_sales"] += revenue
        region_data[region]["transaction_count"] += 1

    for region in region_data:
        region_data[region]["percentage"] = (
            region_data[region]["total_sales"] / total_revenue * 100
            if total_revenue > 0 else 0
        )

    # Sort by total_sales descending
    sorted_regions = dict(
        sorted(
            region_data.items(),
            key=lambda x: x[1]["total_sales"],
            reverse=True
        )
    )

    return sorted_regions

def top_selling_products(transactions, n=5):
    product_data = {}

    for tx in transactions:
        name = tx["ProductName"]
        qty = tx["Quantity"]
        revenue = qty * tx["UnitPrice"]

        if name not in product_data:
            product_data[name] = {"quantity": 0, "revenue": 0.0}

        product_data[name]["quantity"] += qty
        product_data[name]["revenue"] += revenue

    sorted_products = sorted(
        product_data.items(),
        key=lambda x: x[1]["quantity"],
        reverse=True
    )

    return [
        (name, data["quantity"], data["revenue"])
        for name, data in sorted_products[:n]
    ]

def customer_analysis(transactions):
    customer_data = {}

    for tx in transactions:
        cust = tx["CustomerID"]
        amount = tx["Quantity"] * tx["UnitPrice"]
        product = tx["ProductName"]

        if cust not in customer_data:
            customer_data[cust] = {
                "total_spent": 0.0,
                "purchase_count": 0,
                "products_bought": set()
            }

        customer_data[cust]["total_spent"] += amount
        customer_data[cust]["purchase_count"] += 1
        customer_data[cust]["products_bought"].add(product)

    result = {}

    sorted_customers = sorted(
        customer_data.items(),
        key=lambda x: x[1]["total_spent"],
        reverse=True
    )

    for cust, data in sorted_customers:
        result[cust] = {
            "total_spent": data["total_spent"],
            "purchase_count": data["purchase_count"],
            "avg_order_value": (
                data["total_spent"] / data["purchase_count"]
                if data["purchase_count"] > 0 else 0
            ),
            "products_bought": list(data["products_bought"])
        }

    return result

def daily_sales_trend(transactions):
    daily_data = {}

    for tx in transactions:
        date = tx["Date"]
        revenue = tx["Quantity"] * tx["UnitPrice"]
        cust = tx["CustomerID"]

        if date not in daily_data:
            daily_data[date] = {
                "revenue": 0.0,
                "transaction_count": 0,
                "customers": set()
            }

        daily_data[date]["revenue"] += revenue
        daily_data[date]["transaction_count"] += 1
        daily_data[date]["customers"].add(cust)


    sorted_daily = dict(sorted(daily_data.items()))

    for date in sorted_daily:
        sorted_daily[date]["unique_customers"] = len(sorted_daily[date]["customers"])
        del sorted_daily[date]["customers"]

    return sorted_daily

def find_peak_sales_day(transactions):
    daily = daily_sales_trend(transactions)

    peak_date = None
    peak_revenue = 0
    peak_count = 0

    for date, data in daily.items():
        if data["revenue"] > peak_revenue:
            peak_revenue = data["revenue"]
            peak_date = date
            peak_count = data["transaction_count"]

    return peak_date, peak_revenue, peak_count

def low_performing_products(transactions, threshold=10):
    product_data = {}

    for tx in transactions:
        name = tx["ProductName"]
        qty = tx["Quantity"]
        revenue = qty * tx["UnitPrice"]

        if name not in product_data:
            product_data[name] = {"quantity": 0, "revenue": 0.0}

        product_data[name]["quantity"] += qty
        product_data[name]["revenue"] += revenue

    low_products = [
        (name, data["quantity"], data["revenue"])
        for name, data in product_data.items()
        if data["quantity"] < threshold
    ]

    return sorted(low_products, key=lambda x: x[1])

from datetime import datetime

def generate_sales_report(
    transactions,
    enriched_transactions,
    output_file="output/sales_report.txt"
):



    total_transactions = len(transactions)
    total_revenue = sum(tx["Quantity"] * tx["UnitPrice"] for tx in transactions)
    avg_order_value = total_revenue / total_transactions if total_transactions else 0

    dates = [tx["Date"] for tx in transactions]
    date_range = f"{min(dates)} to {max(dates)}" if dates else "N/A"

  
    region_data = {}
    for tx in transactions:
        region = tx["Region"]
        revenue = tx["Quantity"] * tx["UnitPrice"]

        if region not in region_data:
            region_data[region] = {"sales": 0, "count": 0}

        region_data[region]["sales"] += revenue
        region_data[region]["count"] += 1

    for region in region_data:
        region_data[region]["percentage"] = (
            region_data[region]["sales"] / total_revenue * 100
            if total_revenue > 0 else 0
        )

    region_data = dict(
        sorted(region_data.items(), key=lambda x: x[1]["sales"], reverse=True)
    )


    product_data = {}
    for tx in transactions:
        name = tx["ProductName"]
        qty = tx["Quantity"]
        revenue = qty * tx["UnitPrice"]

        if name not in product_data:
            product_data[name] = {"qty": 0, "revenue": 0}

        product_data[name]["qty"] += qty
        product_data[name]["revenue"] += revenue

    top_products = sorted(
        product_data.items(),
        key=lambda x: x[1]["qty"],
        reverse=True
    )[:5]

    
    customer_data = {}
    for tx in transactions:
        cust = tx["CustomerID"]
        amount = tx["Quantity"] * tx["UnitPrice"]

        customer_data[cust] = customer_data.get(cust, 0) + amount

    top_customers = sorted(
        customer_data.items(),
        key=lambda x: x[1],
        reverse=True
    )[:5]

 
    daily_data = {}
    for tx in transactions:
        date = tx["Date"]
        revenue = tx["Quantity"] * tx["UnitPrice"]
        cust = tx["CustomerID"]

        if date not in daily_data:
            daily_data[date] = {
                "revenue": 0,
                "count": 0,
                "customers": set()
            }

        daily_data[date]["revenue"] += revenue
        daily_data[date]["count"] += 1
        daily_data[date]["customers"].add(cust)

    daily_data = dict(sorted(daily_data.items()))

    
    enriched_count = sum(1 for tx in enriched_transactions if tx["API_Match"])
    enrichment_rate = (
        enriched_count / len(enriched_transactions) * 100
        if enriched_transactions else 0
    )

    failed_products = sorted(
        {tx["ProductID"] for tx in enriched_transactions if not tx["API_Match"]}
    )

 
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("SALES ANALYTICS REPORT\n")
        f.write("======================\n")
        f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Records Processed: {total_transactions}\n\n")

        f.write("OVERALL SUMMARY\n")
        f.write("----------------\n")
        f.write(f"Total Revenue: {total_revenue:,.2f}\n")
        f.write(f"Total Transactions: {total_transactions}\n")
        f.write(f"Average Order Value: {avg_order_value:,.2f}\n")
        f.write(f"Date Range: {date_range}\n\n")

        f.write("REGION-WISE PERFORMANCE\n")
        f.write("------------------------\n")
        f.write("Region | Sales | % of Total | Transactions\n")
        for region, data in region_data.items():
            f.write(
                f"{region} | "
                f"{data['sales']:,.2f} | "
                f"{data['percentage']:.2f}% | "
                f"{data['count']}\n"
            )
        f.write("\n")

        f.write("TOP 5 PRODUCTS\n")
        f.write("----------------\n")
        f.write("Rank | Product | Quantity | Revenue\n")
        for i, (name, data) in enumerate(top_products, start=1):
            f.write(
                f"{i} | {name} | {data['qty']} | {data['revenue']:,.2f}\n"
            )
        f.write("\n")

        f.write("TOP 5 CUSTOMERS\n")
        f.write("----------------\n")
        f.write("Rank | CustomerID | Total Spent\n")
        for i, (cust, spent) in enumerate(top_customers, start=1):
            f.write(f"{i} | {cust} | {spent:,.2f}\n")
        f.write("\n")

        f.write("DAILY SALES TREND\n")
        f.write("------------------\n")
        f.write("Date | Revenue | Transactions | Unique Customers\n")
        for date, data in daily_data.items():
            f.write(
                f"{date} | "
                f"{data['revenue']:,.2f} | "
                f"{data['count']} | "
                f"{len(data['customers'])}\n"
            )
        f.write("\n")

        f.write("API ENRICHMENT SUMMARY\n")
        f.write("----------------------\n")
        f.write(f"Total Records Enriched: {enriched_count}\n")
        f.write(f"Success Rate: {enrichment_rate:.2f}%\n")
        if failed_products:
            f.write("Products not enriched:\n")
            for pid in failed_products:
                f.write(f"- {pid}\n")
