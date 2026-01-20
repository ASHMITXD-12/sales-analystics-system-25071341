# Sales Analytics System

A Python-based Sales Data Analytics System that processes raw sales data, cleans and validates transactions, integrates external product data using an API, performs detailed analysis, and generates comprehensive business reports.

This project demonstrates core Python concepts such as file handling, error handling, data structures (lists & dictionaries), functions, API integration, and report generation.

---

## 📁 Project Structure
sales-analytics-system/
  ├── README.md
  ├── main.py
  ├── utils/
  │   ├── file_handler.py
  │   ├── data_processor.py
  │   └── api_handler.py
  ├── data/
  │   └── sales_data.txt (provided)
  ├── output/
  └── requirements.txt
## 🚀 Features

### ✔ File Handling & Data Cleaning
- Handles non-UTF encodings (utf-8, latin-1, cp1252)
- Skips headers and empty lines
- Cleans malformed fields and numeric formatting
- Filters invalid transactions

### ✔ Data Processing & Analysis
- Total revenue calculation
- Region-wise sales analysis
- Top-selling products
- Customer purchase analysis
- Daily sales trends and peak sales day
- Low-performing product identification

### ✔ API Integration
- Fetches product data from DummyJSON API
- Maps products using numeric IDs
- Enriches transaction data with category, brand, and rating
- Saves enriched data to file

### ✔ Report Generation
- Generates a detailed text-based business report
- Includes summaries, tables, and performance insights
- Outputs human-readable formatted report

### ✔ Main Application Workflow
- Step-by-step execution with console feedback
- Graceful error handling using try-except
- End-to-end execution via `main.py`

---

## 🛠️ Setup Instructions

### 1. Install Dependencies

Make sure Python 3 is installed, then run:

```bash
pip install -r requirements.txt

2️ Run the Application

From the root directory:

python main.py

📄 Output Files

Enriched Data:
data/enriched_sales_data.txt

Final Report:
output/sales_report.txt

Both files are generated automatically after successful execution.

🧠 Technologies Used

Python 3

Requests (API handling)

DummyJSON API
