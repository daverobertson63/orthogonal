# monolithic_db_payroll.py
import json

def process_database_payroll(db_filepath, tax_rate, output_filepath):
    # 1. Tightly Coupled DB Fetching
    try:
        with open(db_filepath, "r") as f:
            employees = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Database error: {e}")
        return

    processed_records = []
    
    # 2. Iterating, validating, and calculating all in one place
    for emp in employees:
        # Validation logic mixed with processing
        if emp["hours_worked"] < 0 or emp["hourly_rate"] < 0:
            print(f"Skipping employee {emp['name']}: Invalid negative values.")
            continue
            
        # Math calculation
        gross = emp["hours_worked"] * emp["hourly_rate"]
        tax = gross * tax_rate
        net = gross - tax
        
        # Duplicated string formatting (DRY Violation)
        formatted_gross = f"${gross:,.2f}"
        formatted_tax = f"${tax:,.2f}"
        formatted_net = f"${net:,.2f}"
        
        record_string = f"Employee: {emp['name']} | Gross: {formatted_gross} | Tax: {formatted_tax} | Net: {formatted_net}"
        processed_records.append(record_string)
        
    # 3. Tightly Coupled Output File Writing
    report_content = "\n".join(processed_records)
    with open(output_filepath, "w") as f:
        f.write(report_content)
    
    print("Database processing and report generation complete.")

# Triggering the monolithic function
process_database_payroll("employee_db.json", 0.20, "payroll_report.txt")
