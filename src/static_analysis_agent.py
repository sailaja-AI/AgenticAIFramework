import subprocess

def run_semgrep(path):
    result = subprocess.run(['semgrep', '--config=p/owasp-top-ten', path], capture_output=True, text=True)
    return result.stdout

output = run_semgrep("./src")
print(output)
