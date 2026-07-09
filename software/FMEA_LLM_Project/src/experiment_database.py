import csv
from pathlib import Path


class ExperimentDatabase:
    def __init__(self, database_path="outputs/results.csv"):
        self.database_path = Path(database_path)
        self.database_path.parent.mkdir(parents=True, exist_ok=True)

    def save_result(self, config, response_metadata, evaluation):
        row = {
            "experiment_id": config.experiment_id,
            "model_name": config.model_name,
            "analysis_type": config.analysis_type,
            "input_type": config.input_type,
            "prompt_style": config.prompt_style,

            "json_valid": evaluation.get("json_valid"),
            "parser_success": evaluation.get("parser_success"),
            "schema_compliance": evaluation.get("schema_compliance"),
            "row_count": evaluation.get("row_count"),
            "missing_fields_count": evaluation.get("missing_fields_count"),
            "component_coverage_percent": evaluation.get("component_coverage_percent"),
            "hallucination_rate_percent": evaluation.get("hallucination_rate_percent"),
            "rpn_accuracy_percent": evaluation.get("rpn_accuracy_percent"),

            "generation_time_sec": response_metadata.get("generation_time_sec"),
            "input_tokens": response_metadata.get("input_tokens"),
            "output_tokens": response_metadata.get("output_tokens"),
            "total_tokens": response_metadata.get("total_tokens"),
            "tokens_per_second": response_metadata.get("tokens_per_second"),
            "gpu_memory_gb": response_metadata.get("gpu_memory_gb"),
        }

        file_exists = self.database_path.exists()

        with open(self.database_path, "a", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=row.keys())

            if not file_exists:
                writer.writeheader()

            writer.writerow(row)