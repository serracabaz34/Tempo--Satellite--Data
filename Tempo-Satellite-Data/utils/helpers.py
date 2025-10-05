# utils/helpers.py
import traceback

def log_error(msg):
    print(f"[ERROR] {msg}")
    traceback.print_exc()