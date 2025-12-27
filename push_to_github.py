"""
Enhanced GitHub Push Script

Handles both initial push and updates to existing repository.
Includes security checks to prevent pushing sensitive data.
"""

import subprocess
import sys
import os
import shutil

def run_command(command, check=True):
    """Run a shell command and return output."""
    print(f"Running: {command}")
    try:
        result = subprocess.run(command, shell=True, check=check, text=True, capture_output=True)
        if result.stdout:
            print(result.stdout)
        return result
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stderr}")
        if check:
            sys.exit(1)
        return e

def check_sensitive_files():
    """Check for sensitive files before pushing."""
    print("\n🔒 Checking for sensitive files...")
    
    sensitive_patterns = ['.env', '*.key', '*.pem', '*secret*', '*password*']
    issues = []
    
    # Check if .env exists and is in .gitignore
    if os.path.exists('.env'):
        with open('.gitignore', 'r') as f:
            gitignore_content = f.read()
        
        if '.env' not in gitignore_content:
            issues.append("⚠️  .env file exists but NOT in .gitignore!")
        else:
            print("✅ .env is properly ignored")
    
    # Check git status for any sensitive files
    result = run_command("git status --porcelain", check=False)
    if result.returncode == 0:
        for line in result.stdout.split('\n'):
            if any(pattern.replace('*', '') in line.lower() for pattern in sensitive_patterns):
                if '.env' not in line:  # .env is already checked
                    issues.append(f"⚠️  Potential sensitive file: {line}")
    
    if issues:
        print("\n❌ SECURITY ISSUES FOUND:")
        for issue in issues:
            print(f"  {issue}")
        
        response = input("\nContinue anyway? (yes/no): ").strip().lower()
        if response != 'yes':
            print("Aborted for security.")
            sys.exit(1)
    else:
        print("✅ No sensitive files detected")

def main():
    print("="*80)
    print("🚀 GITHUB PUSH AUTOMATION - v2.0")
    print("="*80)
    
    # Check if this is an update or initial push
    is_update = os.path.exists(".git")
    
    if is_update:
        print("\n📦 Detected existing repository - will UPDATE")
        mode = "update"
    else:
        print("\n📦 No repository detected - will INITIALIZE")
        mode = "init"
    
    # Security check
    check_sensitive_files()
    
    if mode == "init":
        # Initial setup
        print("\n🔧 Initializing Git repository...")
        run_command("git init")
        
        # Configure identity
        print("\n👤 Configuring Git Identity...")
        email = input("Enter your email: ").strip()
        name = input("Enter your name: ").strip()
        
        if email:
            run_command(f'git config user.email "{email}"')
        if name:
            run_command(f'git config user.name "{name}"')
        
        # Get remote URL
        repo_url = input("\n🔗 Enter your GitHub Repository URL: ").strip()
        if not repo_url:
            print("Error: URL cannot be empty.")
            sys.exit(1)
        
        # Add remote
        run_command("git branch -M main")
        run_command(f"git remote add origin {repo_url}")
        
        # Initial commit
        commit_message = "v1.0: Initial release - Neuro-Symbolic Stock Predictor"
        
    else:
        # Update existing repository
        print("\n🔄 Updating existing repository...")
        
        # Check for uncommitted changes
        result = run_command("git status --porcelain", check=False)
        if not result.stdout.strip():
            print("✅ No changes to commit")
            response = input("Continue with push anyway? (yes/no): ").strip().lower()
            if response != 'yes':
                print("Aborted.")
                sys.exit(0)
        
        # Custom commit message
        print("\n📝 Commit message options:")
        print("  1. v2.0: Academic rigor improvements (Tier 1 fixes)")
        print("  2. Update: Documentation and code cleanup")
        print("  3. Custom message")
        
        choice = input("Select option (1-3): ").strip()
        
        if choice == "1":
            commit_message = "v2.0: Academic rigor improvements\n\n- Added formal research question and problem definition\n- Created comprehensive limitations section\n- Removed overclaiming language\n- Added ablation study (symbolic, ML, full system)\n- Improved documentation structure"
        elif choice == "2":
            commit_message = "Update: Documentation and code cleanup"
        else:
            commit_message = input("Enter custom commit message: ").strip()
            if not commit_message:
                commit_message = "Update project files"
    
    # Stage all changes
    print("\n📋 Staging files...")
    run_command("git add .")
    
    # Show what will be committed
    print("\n📊 Files to be committed:")
    run_command("git status --short")
    
    # Confirm
    response = input("\n✅ Proceed with commit and push? (y/n): ").strip().lower()
    if response not in ['y', 'yes']:
        print("Aborted.")
        sys.exit(0)
    
    # Commit
    print(f"\n💾 Committing: {commit_message.split(chr(10))[0]}...")
    try:
        run_command(f'git commit -m "{commit_message}"')
    except:
        print("⚠️  Nothing to commit or commit failed")
        response = input("Continue with push anyway? (yes/no): ").strip().lower()
        if response != 'yes':
            sys.exit(0)
    
    # Push
    print("\n⬆️  Pushing to GitHub...")
    if mode == "init":
        run_command("git push -u origin main")
    else:
        # Try normal push first
        result = run_command("git push", check=False)
        if result.returncode != 0:
            # If failed, might need force push (be careful!)
            print("\n⚠️  Normal push failed. This might require force push.")
            print("⚠️  WARNING: Force push will overwrite remote history!")
            response = input("Force push? (yes/no): ").strip().lower()
            if response == 'yes':
                run_command("git push --force")
            else:
                print("Aborted. Try: git pull --rebase origin main")
                sys.exit(1)
    
    print("\n" + "="*80)
    print("✅ SUCCESSFULLY PUSHED TO GITHUB!")
    print("="*80)
    
    # Show repository info
    result = run_command("git remote get-url origin", check=False)
    if result.returncode == 0:
        print(f"\n🔗 Repository: {result.stdout.strip()}")
    
    print("\n📊 Next steps:")
    print("  1. Visit your GitHub repository")
    print("  2. Verify all files are present")
    print("  3. Check that .env is NOT visible")
    print("  4. Create a release (optional)")
    print("  5. Share the link!")

if __name__ == "__main__":
    main()
