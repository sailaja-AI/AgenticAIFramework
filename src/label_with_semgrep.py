import pandas as pd
import subprocess
import os

def run_semgrep_on_snippet(code_text: str) -> str:
    os.makedirs("temp", exist_ok=True)
    with open("temp/snippet.py", "w", encoding="utf-8") as f:
        f.write(code_text)
    
    result = subprocess.run(
        ["semgrep", "--config=p/owasp-top-ten", "temp/snippet.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    semgrep_output = result.stdout.decode('utf-8', errors='replace')
    
    return "vulnerable" if "severity" in semgrep_output.lower() else "safe"

# Load sample dataset
df = pd.read_csv("../data/sample_dataset.csv", encoding="utf-8")

# LIMIT rows for faster demo
df = df.head(500)

# Apply labeling
df["label"] = df["code"].apply(run_semgrep_on_snippet)

# Optional preprocessing
df["clean_code"] = df["code"].apply(lambda x: x.lower().strip())

# Save
df.to_csv("../data/labeled_preprocessed.csv", index=False, encoding="utf-8")
print("✅ Saved data/labeled_preprocessed.csv")
