from pathlib import Path


class StateManager:

    def __init__(self):

        self.state_file = (
            Path(__file__).parent /
            "last_processed.txt"
        )

        if not self.state_file.exists():
            self.state_file.write_text("")

    def get_last_id(self):

        value = self.state_file.read_text().strip()

        return value if value else None

    def save_last_id(self, announcement_id):

        self.state_file.write_text(
            str(announcement_id)
        )