"""Manual authentication helper for NotebookLM CLI.

This script helps you authenticate with NotebookLM CLI manually,
which avoids Unicode encoding issues in the Windows console.
"""

import subprocess
import sys
import os

print("=" * 60)
print("NotebookLM CLI Authentication Helper")
print("=" * 60)
print()
print("This will open Chrome for you to sign in to NotebookLM.")
print("After signing in and granting permissions, Chrome will close.")
print()
print("Press Enter to start authentication...")
input()

try:
    # Set UTF-8 encoding environment
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    
    # Run authentication in a way that redirects output to avoid encoding errors
    print("\nOpening Chrome for authentication...")
    print("(If Chrome doesn't open, you may need to reinstall notebooklm-mcp-cli)")
    print()
    
    result = subprocess.run(
        ["nlm", "login"],
        env=env,
        timeout=120
    )
    
    if result.returncode == 0:
        print("\n" + "=" * 60)
        print("✓ Authentication complete!")
        print("=" * 60)
        print()
        
        # Verify authentication
        print("Verifying authentication...")
        check_result = subprocess.run(
            ["nlm", "login", "--check"],
            capture_output=True,
            text=True,
            env=env
        )
        
        if check_result.returncode == 0 and "authenticated" in check_result.stdout.lower():
            print("✓ Authentication verified successfully!")
            print()
            print("You can now run the automation script:")
            print("  python src\\main.py")
        else:
            print("⚠ Warning: Could not verify authentication")
            print("Please try running: nlm login --check")
    else:
        print("\n⚠ Authentication may have failed")
        print("Please try again or check the error message above")
        
except subprocess.TimeoutExpired:
    print("\n⚠ Authentication timed out")
    print("Make sure you completed the sign-in process in Chrome")
    
except FileNotFoundError:
    print("\n✗ Error: 'nlm' command not found")
    print()
    print("Please install notebooklm-mcp-cli:")
    print("  npm install -g notebooklm-mcp-cli")
    sys.exit(1)
    
except Exception as e:
    print(f"\n✗ Error: {e}")
    sys.exit(1)

print()
print("Press Enter to exit...")
input()
