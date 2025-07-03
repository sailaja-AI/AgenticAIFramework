def suggest_patch_rl_agent(code_text: str) -> str:
    """
    Stub function: Returns a generic security suggestion.
    """
    if "SELECT * FROM" in code_text or "user_input" in code_text:
        return "Use parameterized queries instead of string concatenation."
    return "No patch required. Code looks safe."
