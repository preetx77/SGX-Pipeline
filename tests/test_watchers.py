import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from watchers.sgx_watcher import SGXWatcher

watcher = SGXWatcher()

watcher.run_once()