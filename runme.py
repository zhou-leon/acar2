
import subprocess
import sys
import os
import json
import webbrowser

# Load config.json
CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'config.json')
with open(CONFIG_PATH, 'r') as f:
    config = json.load(f)
backend_cfg = config.get('backend', {})
frontend_cfg = config.get('frontend', {})

# Backend command
backend_cmd = [
    sys.executable,
    os.path.join('backend', 'app.py')
]

# Frontend command
frontend_cmd = [
    sys.executable,
    os.path.join('frontend', 'main.py')
]


print(f"Starting Flask backend on {backend_cfg.get('host')}:{backend_cfg.get('port')}")

# Use the same environment for both processes
env = os.environ.copy()
backend_proc = subprocess.Popen(backend_cmd, env=env)

print(f"Starting ReactPy frontend on {frontend_cfg.get('host')}:{frontend_cfg.get('port')}")
frontend_proc = subprocess.Popen(frontend_cmd, env=env)

# Open frontend page in default web browser
frontend_url = f"http://{frontend_cfg.get('host', '127.0.0.1')}:{frontend_cfg.get('port', 8000)}"
print(f"Opening frontend page: {frontend_url}")
webbrowser.open(frontend_url)

try:
    backend_proc.wait()
    frontend_proc.wait()
except KeyboardInterrupt:
    print("Shutting down servers...")
    backend_proc.terminate()
    frontend_proc.terminate()