
from pathlib import Path
import sys

backend_path = Path(__file__).parent.absolute()
sys.path.append(backend_path.parent.joinpath('access').as_posix())

# Load backend config from config.json
CONFIG_PATH = backend_path.joinpath('../config.json')
with open(CONFIG_PATH, 'r') as f:
    config = json.load(f)
backend_cfg = config.get('backend', {})