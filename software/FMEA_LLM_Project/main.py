from src.configure_experiment import configure_experiment
from src.experiment_runner import ExperimentRunner


def main():
    experiment_config = configure_experiment()

    runner = ExperimentRunner()
    runner.run(experiment_config)


if __name__ == "__main__":
    main()