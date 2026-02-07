
import subprocess
import sys
import venv
import os

def run_command(command):
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ Success: {command}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed: {command}")
        print(f"Error: {e.stderr}")
        return False

# 1. Create venv
if not os.path.exists(".venv3"):
    print("Creating .venv3...")
    venv.create(".venv3", with_pip=True)

# 2. Activate command prefix
activate_cmd = ". .venv3/bin/activate"

# 3. Upgrade pip
run_command(f"{activate_cmd} && pip install --upgrade pip")

# 4. Install critical packages one by one
packages = ["numpy", "scipy", "pandas", "scikit-learn", "lightgbm", "shap"]
for pkg in packages:
    print(f"Installing {pkg}...")
    if not run_command(f"{activate_cmd} && pip install {pkg} --no-cache-dir"):
        print(f"⚠️ Failed to install {pkg}. Trying without dependencies...")
        run_command(f"{activate_cmd} && pip install {pkg} --no-deps --no-cache-dir")

# 5. Verify import
validation_script = "import lightgbm; print('LightGBM Loaded Successfully')"
run_command(f"{activate_cmd} && python3 -c \"{validation_script}\"")
