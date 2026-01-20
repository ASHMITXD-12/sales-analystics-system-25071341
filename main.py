from utils.file_handler import read_sales_data
from utils.data_processor import (
    parse_transactions,
    validate_and_filter,
    calculate_total_revenue,
    region_wise_sales,
    top_selling_products,
    customer_analysis,
    daily_sales_trend,
    find_peak_sales_day,
    low_performing_products,
    generate_sales_report
)
from utils.api_handler import (
    fetch_all_products,
    create_product_mapping,
    enrich_sales_data,
    save_enriched_data
)


DATA_FILE = "data/sales_data.txt"
ENRICHED_FILE = "data/enriched_sales_data.txt"
REPORT_FILE = "output/sales_report.txt"


def main():
    print("=" * 50)
    print("SALES ANALYTICS SYSTEM")
    print("=" * 50)

    try:
        # [1/10] Read sales data
        print("\n[1/10] Reading sales data...")
        raw_lines = read_sales_data(DATA_FILE)
        print("✓ Successfully read sales data")

        # [2/10] Parse and clean
        print("\n[2/10] Parsing and cleaning data...")
        parsed_data = parse_transactions(raw_lines)
        print(f"✓ Parsed {len(parsed_data)} records")

        # [3/10] Display filter options
        print("\n[3/10] Filter options available:")
        print("Regions: North, South, East, West")
        print("Amount Range: 100 – 10,00,000")

        # [4/10] Validate transactions
        print("\n[4/10] Validating transactions...")
        valid_data, invalid_count, summary = validate_and_filter(parsed_data)
        print(f"✓ Valid: {summary['final_count']}, Invalid: {invalid_count}")

        # [5/10] Analytics (Part 2)
        print("\n[5/10] Analyzing sales data...")
        calculate_total_revenue(valid_data)
        region_wise_sales(valid_data)
        top_selling_products(valid_data)
        customer_analysis(valid_data)
        daily_sales_trend(valid_data)
        find_peak_sales_day(valid_data)
        low_performing_products(valid_data)
        print("✓ Analysis completed")

        # [6/10] Fetch API data
        print("\n[6/10] Fetching product data from API...")
        api_products = fetch_all_products()
        product_mapping = create_product_mapping(api_products)

        # [7/10] Enrich sales data
        print("\n[7/10] Enriching sales data...")
        enriched_data = enrich_sales_data(valid_data, product_mapping)
        enriched_count = sum(1 for tx in enriched_data if tx["API_Match"])
        print(f"✓ Enriched {enriched_count} transactions")

        # [8/10] Save enriched data
        print("\n[8/10] Saving enriched data...")
        save_enriched_data(enriched_data, ENRICHED_FILE)
        print(f"✓ Saved to {ENRICHED_FILE}")

        # [9/10] Generate report
        print("\n[9/10] Generating report...")
        generate_sales_report(
            valid_data,
            enriched_data,
            output_file=REPORT_FILE
        )
        print(f"✓ Report saved to {REPORT_FILE}")

        # [10/10] Complete
        print("\n[10/10] Process Complete")
        print("=" * 50)
        print("✓ All tasks completed successfully")
        print("=" * 50)

    except Exception as e:
        print("\n❌ An unexpected error occurred:")
        print(str(e))
        print("The application did not terminate abruptly.")


if __name__ == "__main__":
    main()
