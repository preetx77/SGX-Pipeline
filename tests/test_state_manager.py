import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from state.state_manager import StateManager

state = StateManager()

print()

print("Previous:", state.get_last_id())

state.save_last_id("TEST123")

print("Current :", state.get_last_id())

print()