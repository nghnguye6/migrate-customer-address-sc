# Customer Address Cleanup Tool

This script is used to compare customer addresses **before** and **after** importing orders into Shopify.  
It helps identify and separate newly added addresses (often automatically created by Shopify during order import) from the original customer addresses.

---

## 🧰 Requirements

Make sure you have Python 3 installed and a virtual environment set up.

---

## 🚀 Usage Instructions

### Step 1: Activate the Virtual Environment

Open your terminal, navigate to the project directory, and activate the virtual environment:

```bash
source bin/activate

### Step 2: Run the Migration Script

Use the following command to run the script:

python3 script.py <customer_addresses_before.csv> <customer_addresses_after.csv> <records_per_file>

Parameters:

- <customer_addresses_before.csv> – CSV file containing customer addresses before importing orders.

- <customer_addresses_after.csv> – CSV file containing customer addresses after importing orders.

- <records_per_file> – Number of records per output file (e.g., 2000 or unlimited).

Example:

python3 script.py customers_before.csv customers_after.csv 2000

This will generate one or more output files, each containing up to 2000 rows of address changes.