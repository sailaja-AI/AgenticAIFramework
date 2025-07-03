from fastapi import FastAPI
from pydantic import BaseModel
import os
import subprocess
from transformers import pipeline
from rl_patch_agent import suggest_patch_rl_agent

app = FastAPI()

# Load CodeBERT
classifier = pipeline("text-classification", model="microsoft/codebert-base", tokenizer="microsoft/codebert-base", truncation=True)

# Request Model
class CodeInput(BaseModel):
    code: str

# Run Semgrep on-the-fly
def run_semgrep_on_code(code_text):
    os.makedirs("temp", exist_ok=True)
    with open("temp/code_file.py", "w", encoding="utf-8") as f:
        f.write(code_text)
    result = subprocess.run(
        ["semgrep", "--config=p/owasp-top-ten", "temp/code_file.py"],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    return result.stdout.decode('utf-8', errors='replace')

# CodeBERT vulnerability prediction
def predict_vulnerability(code_text):
    result = classifier(code_text[:2000])[0]
    label_map = {"LABEL_0": "safe", "LABEL_1": "vulnerable"}
    return label_map.get(result["label"], "unknown")

# Endpoint
@app.post("/analyze/")
def analyze_code(input: CodeInput):
    semgrep_result = run_semgrep_on_code(input.code)
    transformer_result = predict_vulnerability(input.code)
    rl_suggestion = suggest_patch_rl_agent(input.code)

    return {
        "semgrep_analysis": semgrep_result,
        "transformer_prediction": transformer_result,
        "rl_patch_suggestion": rl_suggestion
    }
