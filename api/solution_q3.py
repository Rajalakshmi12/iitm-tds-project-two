import subprocess
import os
import hashlib
from function_template import check_prettier
import subprocess

def check_prettier():
    """Check if Prettier is installed and accessible."""

    try:
        # Run Prettier using the globally installed `npx`
        result = subprocess.run(
            ["npx", "prettier", "--version"],  # Use global npx
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            shell=True  # Required on Windows
        )

        if result.returncode == 0:
            print(f"Prettier Found: {result.stdout.strip()}")
            return True
        else:
            print(f"Prettier Error: {result.stderr.strip()}")
            return False
    except FileNotFoundError:
        print("`npx` not found in system PATH. Ensure Node.js is installed.")
        return False
    except Exception as e:
        print(f"Exception in check_prettier(): {e}")
        return False

def calculate_sha256(content):
    """Runs Prettier on the content and computes the SHA-256 hash."""
    try:
        if not check_prettier():
            return "Error: Prettier is not installed"
    
        formatted_file = "formatted_readme.md"
        
        # Run Prettier and store formatted output in a new file
        result = subprocess.run(
            ["npx", "-y", "prettier@3.4.2", "--stdin-filepath", formatted_file],
            input=content,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            shell=True  # Ensures execution in Vercel/Linux
        )
        
        if result.stderr:
            print("Prettier Error:", result.stderr)
            return "Error: Prettier processing failed"
        
        # Save formatted content
        with open(formatted_file, "w", encoding="utf-8") as f:
            f.write(result.stdout)
        
        # Compute SHA-256 hash using Python (cross-platform)
        sha256_hash = hashlib.sha256(result.stdout.encode()).hexdigest()
        print(sha256_hash)

        return sha256_hash
    except Exception as e:
        return str(e)

def q3_readme_shasum():
    file_path = 'README.md'
    if not os.path.exists(file_path):
        return "Error: File not found"
    
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    sha256_hash = calculate_sha256(content)
    print({"answer": sha256_hash})

if __name__ == "__main__":
    q3_readme_shasum()