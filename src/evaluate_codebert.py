import pandas as pd
from sklearn.metrics import classification_report

# Load
df = pd.read_csv("../data/codebert_predictions.csv", encoding="utf-8")
print(df.head())

# Map predicted labels
label_map = {
    "LABEL_0": "safe",
    "LABEL_1": "vulnerable"
}
df["predicted_label_mapped"] = df["predicted_label"].map(label_map).fillna("unknown")

# True vs predicted
y_true = df["label"]
y_pred = df["predicted_label_mapped"]

print("✅ Classification Report")
print(classification_report(y_true, y_pred, zero_division=0))
