import re

def extract_total(text):
    """Extract total amount from receipt text"""
    # Find all amounts with pattern: number.number (like 1.100.00 or 1,028.20)
    # This regex looks for numbers with separators
    amount_pattern = r'(\d+[.,]\d{2,3}[.,]?\d{2})'  # Matches XXX.XXX.XX or XXX,XXX.XX
    amounts = re.findall(amount_pattern, text)
    
    if amounts:
        cleaned_amounts = []
        for amount in amounts:
            # Normalize: for Thai receipts, last comma/dot is decimal separator
            # Pattern: 1.100.00 means 1100.00, pattern: 1,028.20 means 1028.20
            parts = re.split(r'[.,]', amount)
            
            if len(parts) == 3:
                # Format like 1.100.00 or 1,028.20
                # The last part is always cents, parts before are thousands
                try:
                    # Remove separators except last one, treat as decimal
                    normalized = ''.join(parts[:-1]) + '.' + parts[-1]
                    value = float(normalized)
                    cleaned_amounts.append((value, amount))
                except ValueError:
                    continue
            elif len(parts) == 2:
                try:
                    value = float(amount.replace(',', '.'))
                    cleaned_amounts.append((value, amount))
                except ValueError:
                    continue
        
        if cleaned_amounts:
            # Return the largest amount (most likely the total)
            cleaned_amounts.sort(reverse=True)
            return cleaned_amounts[0][1]  # Return original format
    
    return None

def extract_date(text):
    """Extract date from receipt text"""
    patterns = [
        r'(\d{2})/(\d{2})/(\d{4})',  # DD/MM/YYYY
        r'(\d{2})-(\d{2})-(\d{2})',  # DD-MM-YY
        r'(\d{2})/(\d{2})/(\d{2})',  # DD/MM/YY
        r'(\d{1,2})\s+[a-z]+\s+(\d{4})',  # D Month YYYY
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(0)
    
    # If no structured date found, try to extract at least the time or invoice date
    # Look for time patterns like HH:MM
    time_match = re.search(r'(\d{2}):(\d{2})', text)
    if time_match:
        return f"Time: {time_match.group(0)}"
    
    return None

def extract_data(text):
    """Extract structured data from receipt OCR text"""
    return {
        "date": extract_date(text),
        "total": extract_total(text)
    }
