import pandas as pd
from transformers import pipeline

# Load labeled dataset
df = pd.read_csv("../data/labeled_preprocessed.csv", encoding="utf-8")

# Limit rows for demo
df = df.head(5)

# Truncate code to first 512 tokens (approx 2000 chars is safe)
def truncate_code(code, max_chars=2000):
    return code[:max_chars]

# Load CodeBERT
classifier = pipeline(
    "text-classification",
    model="microsoft/codebert-base",
    tokenizer="microsoft/codebert-base",
    truncation=True,  # just in case
)

# Run predictions safely
def safe_predict(text):
    try:
        result = classifier(truncate_code(text))[0]
        return result['label']
    except Exception as e:
        print("⚠️ Error:", e)
        return "error"

# Apply prediction
df["predicted_label"] = df["code"].apply(safe_predict)

# Save results
df.to_csv("../data/codebert_predictions.csv", index=False, encoding="utf-8")
print("✅ Saved data/codebert_predictions.csv")
