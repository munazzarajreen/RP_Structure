from pathlib import Path
from src.experiment_config import ExperimentConfig


def generate_experiment_id():
    outputs_folder = Path("outputs")
    outputs_folder.mkdir(exist_ok=True)

    existing_ids = []

    for folder in outputs_folder.iterdir():
        if folder.is_dir() and folder.name.startswith("EXP"):
            try:
                number = int(folder.name.replace("EXP", ""))
                existing_ids.append(number)
            except ValueError:
                pass

    next_number = max(existing_ids, default=0) + 1
    return f"EXP{next_number:03d}"


def choose_analysis_type():
    print("===================================")
    print("FMEA / FMECA Generation and Evaluation")
    print("===================================")
    print()
    print("Choose Analysis Type")
    print("1. FMEA")
    print("2. FMECA")

    choice = input("Enter your choice: ")

    if choice == "1":
        return "fmea"
    if choice == "2":
        return "fmeca"

    raise ValueError("Invalid analysis type. Choose 1 or 2.")


def choose_input_type():
    print()
    print("Choose Input Type")
    print("1. System Description")
    print("2. System Description + Component List")
    print("3. Image / P&ID Diagram")

    choice = input("Enter your choice: ")

    if choice == "1":
        return "system_description"
    if choice == "2":
        return "system_description_with_components"
    if choice == "3":
        return "image"

    raise ValueError("Invalid input type. Choose 1, 2, or 3.")


def choose_prompt_style():
    print()
    print("Choose Prompt Style")
    print("1. Minimal")
    print("2. Structured")
    print("3. Constrained")

    choice = input("Enter your choice: ")

    if choice == "1":
        return "minimal"
    if choice == "2":
        return "structured"
    if choice == "3":
        return "constrained"

    raise ValueError("Invalid prompt style. Choose 1, 2, or 3.")


def choose_model():
    print()
    print("Choose Model")
    print("1. LLaMA")
    print("2. Mistral")
    print("3. Qwen2-VL")

    choice = input("Enter your choice: ")

    if choice == "1":
        return "llama"
    if choice == "2":
        return "mistral"
    if choice == "3":
        return "qwen"

    raise ValueError("Invalid model. Choose 1, 2, or 3.")


def configure_experiment():
    experiment_id = generate_experiment_id()
    analysis_type = choose_analysis_type()
    input_type = choose_input_type()
    prompt_style = choose_prompt_style()
    model_name = choose_model()

    return ExperimentConfig(
        experiment_id=experiment_id,
        analysis_type=analysis_type,
        input_type=input_type,
        prompt_style=prompt_style,
        model_name=model_name
    )