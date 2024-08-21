import subprocess
import sys

interpreter = sys.executable

if __name__ == "__main__":
    subprocess.run([interpreter, "test_load.py"])
    subprocess.run([interpreter, "test_available.py"])
