# orthogonal_try_catch_payroll.py
import json

# --- Components remain simple, focused, and orthogonal ---

def fetch_all_employees(db_filepath):
    try:
        with open(db_filepath, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"[CRITICAL] DB Read Failure: {e}")
        return []

def calculate_net_pay(hours, rate, tax_rate):
    """Simple math. If hours is 'forty', Python will naturally 
    throw a TypeError here."""
    if hours < 0 or rate < 0:
        raise ValueError("Hours and rates cannot be negative.")
        
    gross = hours * rate
    tax = gross * tax_rate
    return {"gross": gross, "tax": tax, "net": gross - tax}

def format_currency(amount):
    return f"${amount:,.2f}"

def generate_report_string(name, financial_data):
    # If name is empty, we deliberately raise an error to enforce our rule
    if not name or not name.strip():
        raise KeyError("Employee name cannot be blank.")
        
    return (
        f"Employee: {name:<15} | "
        f"Gross: {format_currency(financial_data['gross']):>10} | "
        f"Tax: {format_currency(financial_data['tax']):>9} | "
        f"Net: {format_currency(financial_data['net']):>10}"
    )

def write_report_file(filepath, content):
    with open(filepath, "w") as f:
        f.write(content)


# --- The Orchestrator (Using the second Try/Catch approach) ---
def run_payroll_pipeline(db_path, tax_rate, output_path):
    raw_employees = fetch_all_employees(db_path)
    report_lines = []
    
    for emp in raw_employees:
        # THE SECOND APPROACH: Wrap the execution of the pipeline step
        try:
            # 1. Accessing data might throw KeyError (e.g. Ian missing hours_worked)
            hours = emp["hours_worked"]
            rate = emp["hourly_rate"]
            name = emp["name"]
            
            # 2. Math might throw TypeError (Fiona's 'forty') or ValueError (negatives)
            financials = calculate_net_pay(hours, rate, tax_rate)
            
            # 3. String generation might throw KeyError (Blank name)
            line = generate_report_string(name, financials)
            report_lines.append(line)
            
        except KeyError as e:
            # Catches completely missing dictionary attributes or blank names
            print(f"[SKIP] Record ID {emp.get('id')} failed: Missing key or required field {e}")
            
        except TypeError as e:
            # Catches mixed types like attempting to multiply a string by a float
            print(f"[SKIP] Employee '{emp.get('name')}' failed: Data type mismatch ({e})")
            
        except ValueError as e:
            # Catches business logic errors raised by calculate_net_pay
            print(f"[SKIP] Employee '{emp.get('name')}' failed: Invalid values logic ({e})")
            
        except Exception as e:
            # A catch-all safety net for anything we didn't explicitly foresee
            print(f"[SKIP] Unexpected critical failure on record {emp.get('id')}: {e}")

    # Write whatever successfully made it through the gauntlet
    full_report = "\n".join(report_lines)
    write_report_file(output_path, full_report)
    print(f"\nPipeline finished. Output written to {output_path}")


if __name__ == "__main__":
    run_payroll_pipeline("employee_db.json", 0.20, "orthogonal_report.txt")
