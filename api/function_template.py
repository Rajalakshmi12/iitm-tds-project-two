import subprocess
import os
import hashlib
import subprocess

# Q1
def q1_code_vsc():
    return check_prettier()
    # return "Success Raji Project 2 you got 100"
    
    
def check_prettier():
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    folder_path = os.path.join(current_dir, 'README.md')

    # Check if the folder exists
    if os.path.isdir(folder_path):
        return f"The folder '{folder_path}' exists."
    else:
        return f"The folder '{folder_path}' does not exist."
    return f'Working Directory: {current_dir} File Path: {file_path}'

    try:
        # prettier_bin = "/vercel/path0/api/node_modules/.bin/prettier"
        if not (os.path.exists(prettier_bin)):
            result = subprocess.run(
                ["npx", "prettier", "--version"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                shell=True)
        else:   
            result = subprocess.run(
                [prettier_bin, "--version"], 
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                shell=True)   

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

        formatted_file = "api/formatted_readme.md"
        
        # Run Prettier and store formatted output in a new file
        result = subprocess.run(
            ["npx", "-y", "prettier@3.4.2", "--stdin-filepath", formatted_file],
            input=content,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            shell=True)
        
        if result.stderr:
            return "Error: Prettier processing failed"
        
        # Save formatted content
        with open(formatted_file, "w", encoding="utf-8") as f:
            f.write(result.stdout)
        
        # Compute SHA-256 hash using Python (cross-platform)
        sha256_hash = hashlib.sha256(result.stdout.encode()).hexdigest()
        return f'{sha256_hash}'
    
    except Exception as e:
        return str(e)

def q3_readme_shasum():
    file_path = 'api/README.md'
    
    if not os.path.exists(file_path):
        return "Error: File not found"
    
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    sha256_hash = calculate_sha256(content)
    return({"answer": sha256_hash})
    
    