import subprocess
import sys
import importlib.util

def install_package(package_name):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])

# Step 1: Check and install packaging
try:
    spec = importlib.util.find_spec("packaging")
    if spec is None:
        raise ImportError
except ImportError:
    print("Packaging not found. Installing packaging...")
    install_package("packaging")

# Step 2: Check Flask version and install if necessary
from packaging import version

spec = importlib.util.find_spec("flask")
if spec is None:
    print("Flask not found. Installing Flask 2.0.1...")
    install_package("flask==2.0.1")
else:
    flask = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(flask)
    flask_version = flask.__version__
    if version.parse(flask_version) < version.parse("2.0.1"):
        print(f"Flask {flask_version} found. Upgrading to Flask 2.0.1...")
        install_package("flask==2.0.1")
    else:
        print(f"Flask {flask_version} is already installed and meets the required version.")
