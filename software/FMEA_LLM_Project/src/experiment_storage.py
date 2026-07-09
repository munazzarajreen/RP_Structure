from dataclasses import asdict
from pathlib import Path
import json


class ExperimentStorage:
    def __init__(self, experiment_config):
        self.experiment_config = experiment_config
        self.experiment_folder = Path("outputs") / experiment_config.experiment_id
        self.experiment_folder.mkdir(parents=True, exist_ok=True)

    def save_config(self):
        config_path = self.experiment_folder / "config.json"

        with open(config_path, "w", encoding="utf-8") as file:
            json.dump(asdict(self.experiment_config), file, indent=4)

    def save_prompt(self, prompt):
        prompt_path = self.experiment_folder / "prompt.txt"

        with open(prompt_path, "w", encoding="utf-8") as file:
            file.write(prompt)

    def save_response(self, response):
        raw_response_path = self.experiment_folder / "response_raw.txt"
        metadata_path = self.experiment_folder / "response.json"

        raw_response = response.get("raw_response", "")

        metadata = {
            key: value
            for key, value in response.items()
            if key != "raw_response"
        }

        with open(raw_response_path, "w", encoding="utf-8") as file:
            file.write(raw_response)

        with open(metadata_path, "w", encoding="utf-8") as file:
            json.dump(metadata, file, indent=4)

    def save_parsed_output(self, parsed_output):
        parsed_output_path = self.experiment_folder / "parsed_output.json"

        with open(parsed_output_path, "w", encoding="utf-8") as file:
            json.dump(parsed_output, file, indent=4)

    def save_evaluation(self, evaluation_result):
        evaluation_path = self.experiment_folder / "evaluation.json"

        with open(evaluation_path, "w", encoding="utf-8") as file:
            json.dump(evaluation_result, file, indent=4)

    def save_decision(self, decision_result):
        decision_path = self.experiment_folder / "decision.json"

        with open(decision_path, "w", encoding="utf-8") as file:
            json.dump(decision_result, file, indent=4)