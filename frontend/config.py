from pathlib import Path
import json

frontend_path = Path(__file__).parent.absolute()

# Load frontend config from config.json
CONFIG_PATH = frontend_path.parent.joinpath('config.json')
with open(CONFIG_PATH, 'r') as f:
    config = json.load(f)
frontend_cfg = config.get('frontend', {})
backend_cfg = config.get('backend', {})

API_BASE = f"http://{backend_cfg.get('host', '127.0.0.1')}:{backend_cfg.get('port', 5000)}"
THEME = frontend_cfg.get('theme', 'apple-glass')