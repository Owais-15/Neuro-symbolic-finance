import subprocess
import sys
import os

import shutil

def run_command(command):
    """Run a shell command and print output."""
    print(f"Running: {command}")
    try:
        result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stderr}")
        sys.exit(1)

def main():
    print("🚀 Starting GitHub Release Automation...")
    
    # 1. Clean Slate (The Nuclear Option)
    if os.path.exists(".git"):
        print("Found existing .git. Removing to ensure clean history (no secrets)...")
        # On Windows, sometimes .git files are read-only, so we might need a handler, 
        # but standard rmtree usually works or we can use shell command.
        try:
            shutil.rmtree(".git")
        except PermissionError:
             run_command("rmdir /s /q .git") # Windows fallback

    # 2. Initialize Git
    run_command("git init")

    # 3. Configure Identity
    print("\n👤 Configuring Git Identity (Required for Commit)...")
    email = input("Enter your email (for git config): ").strip()
    name = input("Enter your name (for git config): ").strip()
    
    if email:
        run_command(f'git config user.email "{email}"')
    if name:
        run_command(f'git config user.name "{name}"')

    # 4. Stage files
    run_command("git add .")

    # 3. Commit
    try:
        run_command('git commit -m "v1.0: Neuro-Symbolic Framework Release"')
    except:
        print("Nothing to commit or already committed.")

    # 4. Get Remote URL
    repo_url = input("\n🔗 Enter your GitHub Repository URL: ").strip()
    if not repo_url:
        print("Error: URL cannot be empty.")
        sys.exit(1)

    # 5. Rename branch to main
    run_command("git branch -M main")

    # 6. Add Remote
    try:
        run_command(f"git remote add origin {repo_url}")
    except:
        print("Remote 'origin' might already exist. Updating URL...")
        run_command(f"git remote set-url origin {repo_url}")

    # 7. Push
    print("\n⬆️ Pushing to GitHub...")
    run_command("git push -u origin main")

    print("\n✅ Successfully pushed to GitHub!")

if __name__ == "__main__":
    main()
