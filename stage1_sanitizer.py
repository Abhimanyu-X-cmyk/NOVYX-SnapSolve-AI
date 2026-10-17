import re

def clean_math_input(raw_text: str) -> dict:
    # 1. Strip spaces and lowercase
    text = raw_text.strip().lower()
    
    # 2. Remove common prefixes
    for prefix in ["solve:", "solve", "find:", "calculate:"]:
        if text.startswith(prefix):
            text = text[len(prefix):].strip()
            
    # 3. Standardize math symbols
    text = text.replace("×", "*").replace("÷", "/").replace("−", "-").replace("^", "**")
    text = text.replace(" ", "")
    
    # 4. Validation checks
    if not text:
        return {"original": raw_text, "cleaned": "", "is_valid": False, "error": "Empty input"}
    
    if text.count("=") != 1:
        return {"original": raw_text, "cleaned": text, "is_valid": False, "error": "Must contain exactly one '=' sign"}
        
    if re.search(r"(\+{2,}|\-{2,}|/{2,}|\*{3,})", text):
        return {"original": raw_text, "cleaned": text, "is_valid": False, "error": "Invalid consecutive operators"}

    # 5. Insert implicit multiplication (2x -> 2*x, 2(x) -> 2*(x), (a)(b) -> (a)*(b))
    text = re.sub(r"(\d)([a-z])", r"\1*\2", text)
    text = re.sub(r"(\d)(\()", r"\1*\2", text)
    text = re.sub(r"(\))(\()", r"\1*\2", text)
    
    return {
        "original": raw_text,
        "cleaned": text,
        "is_valid": True,
        "error": None
    }

if __name__ == "__main__":
    test_equations = [
        "Solve: 2x + 3 = 9",
        "x^2 - 4 = 0",
        "2(x + 3) = 10",
        "(x + 1)(x - 1) = 0",
        "2x ++ 3 = 9"
    ]
    print("--- Running NOVYX Stage 1 Tests ---")
    for eq in test_equations:
        res = clean_math_input(eq)
        print(f"Input: {res['original']}  -->  Cleaned: {res['cleaned']} | Valid: {res['is_valid']}")
