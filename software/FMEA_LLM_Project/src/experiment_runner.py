from src.input_loader import InputLoader
from src.display import show_experiment_summary
from src.prompt_builder.prompt_builder import PromptBuilder
from src.experiment_storage import ExperimentStorage
from src.experiment_database import ExperimentDatabase
from src.llm_engine import LLMEngine
from src.output_parser import OutputParser
from src.evaluation_engine import EvaluationEngine
from src.decision_engine import DecisionEngine


class ExperimentRunner:

    def run(self, experiment_config):

        # Load input
        loader = InputLoader()

        if experiment_config.input_type == "system_description":
            experiment_input = loader.load_text_input()
        elif experiment_config.input_type == "system_description_with_components":
            experiment_input = loader.load_text_with_components_input()
        elif experiment_config.input_type == "image":
            experiment_input = loader.load_image_input()
        else:
            raise ValueError(f"Unknown input type: {experiment_config.input_type}")

        experiment_input["analysis_type"] = experiment_config.analysis_type

        show_experiment_summary(experiment_input)

        print()
        print("===================================")
        print("Experiment Configuration")
        print("===================================")
        print(experiment_config)
        print("===================================")

        # Build prompt
        prompt_builder = PromptBuilder()
        prompt = prompt_builder.build(experiment_config, experiment_input)

        # Save config and prompt
        storage = ExperimentStorage(experiment_config)
        storage.save_config()
        storage.save_prompt(prompt)

        print()
        print("Prompt saved successfully.")

        # Run LLM
        llm_engine = LLMEngine()
        llm_response = llm_engine.generate(experiment_config, prompt)
        storage.save_response(llm_response)

        print()
        print("===================================")
        print("LLM Response Summary")
        print("===================================")
        print(f"Model        : {llm_response.get('model_name')}")
        print(f"Model ID     : {llm_response.get('model_id')}")
        print("Raw response : Saved to response_raw.txt")
        print("Metadata     : Saved to response.json")
        print("===================================")

        # Parse output
        parser = OutputParser()
        parsed_output = parser.parse(llm_response, experiment_config)
        storage.save_parsed_output(parsed_output)

        print()
        print("===================================")
        print("Parser Summary")
        print("===================================")
        print(f"JSON valid     : {parsed_output.get('json_valid')}")
        print(f"Parser status  : {parsed_output.get('parser_status')}")
        print(f"Rows parsed    : {len(parsed_output.get('rows', []))}")
        print(f"Missing fields : {len(parsed_output.get('missing_fields', []))}")
        print("===================================")

        # Evaluate output
        evaluator = EvaluationEngine()
        evaluation = evaluator.evaluate(
            parsed_output,
            experiment_input,
            experiment_config
        )
        storage.save_evaluation(evaluation)

        print()
        print("Evaluation saved successfully.")

        # Save experiment summary to database
        database = ExperimentDatabase()
        database.save_result(
            experiment_config,
            llm_response,
            evaluation
        )

        print()
        print("Experiment result added to outputs/results.csv.")

        # Decide sufficiency
        decision_engine = DecisionEngine()
        decision = decision_engine.decide(evaluation)
        storage.save_decision(decision)

        print()
        print("Decision saved successfully.")