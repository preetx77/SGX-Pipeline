import sys
from pathlib import Path

# Fix path issues - remove conflicting paths
project_root = str(Path(__file__).parent)
sys.path = [p for p in sys.path if 'calchas' not in p]
sys.path.insert(0, project_root)

from scraper.sgx_client import SGXClient

def main():

    client = SGXClient()
    client.print_summary("OILTEK INTERNATIONAL LIMITED")

if __name__ == "__main__":
    main()