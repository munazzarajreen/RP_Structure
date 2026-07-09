from dataclasses import dataclass


@dataclass
class ExperimentConfig:
    experiment_id: str
    analysis_type: str      # fmea or fmeca
    input_type: str         # system_description, system_description_with_components, image
    prompt_style: str       # minimal, structured, constrained
    model_name: str         # llama, mistral, qwen