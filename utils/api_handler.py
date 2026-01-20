import requests

BASE_URL = "https://dummyjson.com/products"


def fetch_all_products():
    """
    Fetches all products from DummyJSON API
    Returns: list of product dictionaries
    """
    try:
        response = requests.get(f"{BASE_URL}?limit=100", timeout=10)
        response.raise_for_status()
        data = response.json()
        print("API Status: Successfully fetched products")
        return data.get("products", [])
    except requests.exceptions.RequestException as e:
        print(f"API Error: {e}")
        return []


def create_product_mapping(api_products):
    """
    Creates a mapping of product IDs to product info
    """
    product_mapping = {}

    for product in api_products:
        product_mapping[product["id"]] = {
            "title": product.get("title"),
            "category": product.get("category"),
            "brand": product.get("brand"),
            "rating": product.get("rating")
        }

    return product_mapping


def enrich_sales_data(transactions, product_mapping):
    """
    Enriches transaction data with API product information
    """
    enriched_transactions = []

    for tx in transactions:
        enriched = tx.copy()

        # Extract numeric ID from ProductID (P101 → 101)
        try:
            numeric_id = int(tx["ProductID"][1:])
        except:
            numeric_id = None

        if numeric_id in product_mapping:
            api_data = product_mapping[numeric_id]
            enriched["API_Category"] = api_data["category"]
            enriched["API_Brand"] = api_data["brand"]
            enriched["API_Rating"] = api_data["rating"]
            enriched["API_Match"] = True
        else:
            enriched["API_Category"] = None
            enriched["API_Brand"] = None
            enriched["API_Rating"] = None
            enriched["API_Match"] = False

        enriched_transactions.append(enriched)

    return enriched_transactions


def save_enriched_data(enriched_transactions, filename="data/enriched_sales_data.txt"):
    """
    Saves enriched transactions back to file
    """
    headers = [
        "TransactionID", "Date", "ProductID", "ProductName",
        "Quantity", "UnitPrice", "CustomerID", "Region",
        "API_Category", "API_Brand", "API_Rating", "API_Match"
    ]

    with open(filename, "w", encoding="utf-8") as file:
        file.write("|".join(headers) + "\n")

        for tx in enriched_transactions:
            row = [
                str(tx.get("TransactionID")),
                str(tx.get("Date")),
                str(tx.get("ProductID")),
                str(tx.get("ProductName")),
                str(tx.get("Quantity")),
                str(tx.get("UnitPrice")),
                str(tx.get("CustomerID")),
                str(tx.get("Region")),
                str(tx.get("API_Category")),
                str(tx.get("API_Brand")),
                str(tx.get("API_Rating")),
                str(tx.get("API_Match")),
            ]
            file.write("|".join(row) + "\n")

    print(f"Enriched data saved to {filename}")
