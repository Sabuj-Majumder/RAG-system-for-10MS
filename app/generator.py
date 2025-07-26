import subprocess

def query_mistral(prompt: str) -> str:
    result = subprocess.run(
        ["ollama", "run", "mistral", "--temperature", "0"],
        input=prompt.encode(),
        stdout=subprocess.PIPE
    )
    return result.stdout.decode().strip()
