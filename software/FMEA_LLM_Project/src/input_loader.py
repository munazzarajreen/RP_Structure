from pathlib import Path


class InputLoader:
    def __init__(self):
        self.input_folder = Path("data/input")

    def _read_text_file(self, file_name):
        file_path = self.input_folder / file_name

        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        text = file_path.read_text(encoding="utf-8")

        if not text.strip():
            raise ValueError(f"File is empty: {file_path}")

        return text

    def load_text_input(self):
        system_description = self._read_text_file("system_description.txt")

        return {
            "input_type": "system_description",
            "system_description": system_description,
            "component_list": None,
            "image_path": None
        }

    def load_text_with_components_input(self):
        system_description = self._read_text_file("system_description.txt")
        component_text = self._read_text_file("component_list.txt")

        components = [
            line.strip()
            for line in component_text.splitlines()
            if line.strip()
        ]

        return {
            "input_type": "system_description_with_components",
            "system_description": system_description,
            "component_list": components,
            "image_path": None
        }

    def load_image_input(self):
        image_path = self.input_folder / "pid_diagram.png"

        if not image_path.exists():
            raise FileNotFoundError(f"Image file not found: {image_path}")

        return {
            "input_type": "image",
            "system_description": None,
            "component_list": None,
            "image_path": image_path
        }