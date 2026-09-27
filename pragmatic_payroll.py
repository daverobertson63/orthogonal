# orthogonal_db_payroll.py
import json

# --- Component 1: Database Layer & Sanitization ---
def fetch_all_employees(db_filepath):
    """Its ONLY job is to safely read data from the file system.
    If the file doesn't exist or is corrupted JSON, it returns an empty list."""
    try:
        with open(db_filepath, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"[DB ERROR] Could not read file: {e}")
        return []


# --- Component 2: Validation & Type Conversion Layer ---
def sanitize_and_validate_employee(emp):
    """
    Validates and cleans a single employee record.
    Returns a cleaned dictionary if valid, or None if it should be skipped.
    """
    # Trap 1: Missing name or empty name string
    name = emp.get("name", "").strip()
    if not name:
        print(f"[VALIDATION WARNING] Skipping ID {emp.get('id')}: Missing employee name.")
        return None

    # Trap 2: Missing fields entirely (like Ian missing hours_worked)
    if "hours_worked" not in emp or "hourly_rate" not in emp:
        print(f"[VALIDATION WARNING] Skipping {name}: Missing required payroll fields.")
        return None

    # Trap 3: Type conversion (handling Hannah's "35.00" and catching Fiona's "forty")
    try:
        hours = float(emp["hours_worked"])
        rate = float(emp["hourly_rate"])
    except (ValueError, TypeError):
        print(f"[TYPE ERROR] Skipping {name}: Invalid numeric values for hours/rate.")
        return None

    # Trap 4: Logical business rules (Negative numbers or impossible hours)
    if hours < 0 or rate < 0:
        print(f"[BUSINESS RULE] Skipping {name}: Hours ({hours}) or Rate ({rate}) cannot be negative.")
        return None
        
    if hours > 140: # Extraneous case check (e.g., Kevin Bacon working 168 hours)
        print(f"[BUSINESS RULE] Skipping {name}: Suspiciously high hours worked ({hours}).")
        return None

    # If it passes everything, return the safely sanitized data
    return {"name": name, "hours": hours, "rate": rate}


# --- Component 3: Pure Business Logic ---
def calculate_net_pay(hours, rate, tax_rate):
    """Pure math. Completely insulated from strings, bad data, and files."""
    gross = hours * rate
    tax = gross * tax_rate
    return {"gross": gross, "tax": tax, "net": gross - tax}


# --- Component 4: Presentation Layer (DRY Representation) ---
def format_currency(amount):
    """Single authoritative rule for how money looks."""
    return f"${amount:,.2f}"


def generate_report_string(name, financial_data):
    """Combines name and financials into a standard display format."""
    return (
        f"Employee: {name:<15} | "
        f"Gross: {format_currency(financial_data['gross']):>10} | "
        f"Tax: {format_currency(financial_data['tax']):>9} | "
        f"Net: {format_currency(financial_data['net']):>10}"
    )


# --- Component 5: Output Layer ---
def write_report_file(filepath, content):
    """Handles file writing exclusively."""
    with open(filepath, "w") as f:
        f.write(content)


# --- The Orchestrator (The Pipe) ---
def run_payroll_pipeline(db_path, tax_rate, output_path):
    """Coordinates independent modules like an production assembly line."""
    raw_employees = fetch_all_employees(db_path)
    report_lines = []
    
    for raw_emp in raw_employees:
        # Run through our validation filter first!
        sanitized_emp = sanitize_and_validate_employee(raw_emp)
        if not sanitized_emp:
            continue  # Safely skip bad records without breaking the loop!
            
        # Run the math on the guaranteed clean data
        financials = calculate_net_pay(
            sanitized_emp["hours"], 
            sanitized_emp["rate"], 
            tax_rate
        )
        
        line = generate_report_string(sanitized_emp["name"], financials)
        report_lines.append(line)
        
    full_report = "\n".join(report_lines)
    write_report_file(output_path, full_report)
    print(f"\nPipeline finished. Output written to {output_path}")


if __name__ == "__main__":
    run_payroll_pipeline("employee_db.json", 0.20, "orthogonal_report.txt")
