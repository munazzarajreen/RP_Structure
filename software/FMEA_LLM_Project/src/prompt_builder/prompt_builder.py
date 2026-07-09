from src.prompt_builder.system_role import build as build_system_role
from src.prompt_builder.task_block import build as build_task_block
from src.prompt_builder.input_block import build as build_input_block
from src.prompt_builder.output_block import build as build_output_block
from src.prompt_builder.constraint_block import build as build_constraint_block


class PromptBuilder:
    def build(self, config, experiment_input):
        blocks = [
            build_system_role(config),
            build_task_block(config),
            build_input_block(config, experiment_input),
            build_output_block(config),
            build_constraint_block(config),
        ]

        final_prompt = "\n\n".join(block for block in blocks if block.strip())

        return final_prompt