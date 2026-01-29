from langchain_core.tools import tool

# Mock Standard Rates (DSR - Delhi Schedule of Rates)
STANDARD_RATES = {
    "concrete m20": 6500,  # Per cubic meter
    "steel reinforcement": 75, # Per kg
    "brickwork": 5500, # Per cubic meter
    "plastering": 450 # Per square meter
}

@tool
def unit_converter(value: float, from_unit: str, to_unit: str) -> str:
    """
    Converts construction units directly.
    Supported: feet to meters, sqft to sqm, inch to mm.
    """
    try:
        if from_unit == "feet" and to_unit == "meters":
            return str(value * 0.3048)
        elif from_unit == "meters" and to_unit == "feet":
            return str(value / 0.3048)
        elif from_unit == "sqft" and to_unit == "sqm":
            return str(value * 0.092903)
        elif from_unit == "inch" and to_unit == "mm":
            return str(value * 25.4)
        else:
            return "Conversion not supported in this beta tool."
    except Exception as e:
        return f"Error: {e}"

@tool
def check_compliance(item: str, quoted_rate: float) -> str:
    """
    Checks if a quoted rate is within 10% of the Standard Schedule of Rates (DSR).
    Returns a compliance warning or approval.
    """
    item = item.lower()
    found_key = None
    for key in STANDARD_RATES:
        if key in item:
            found_key = key
            break
            
    if not found_key:
        return "Item not found in Standard Schedule of Rates."
        
    std_rate = STANDARD_RATES[found_key]
    diff = abs(quoted_rate - std_rate)
    percent_diff = (diff / std_rate) * 100
    
    if percent_diff > 10:
        return f"⚠️ NON-COMPLIANT: Rate {quoted_rate} deviates by {percent_diff:.2f}% from Standard ({std_rate})."
    else:
        return f"✅ COMPLIANT: Rate is within acceptable limits of Standard ({std_rate})."

expert_tools = [unit_converter, check_compliance]
