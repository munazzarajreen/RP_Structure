def build(config, experiment_input):
    if config.input_type == "system_description":
        return f"""
System Description:
{experiment_input["system_description"]}
""".strip()

    if config.input_type == "system_description_with_components":
        components = "\n".join(
            f"- {component}" for component in experiment_input["component_list"]
        )

        return f"""
System Description:
{experiment_input["system_description"]}

Component List:
{components}
""".strip()

    if config.input_type == "image":
        return """
Input:
A system diagram / P&ID image is provided to the vision-language model.
Analyze the visible components and system structure.
""".strip()

    raise ValueError(f"Unknown input type: {config.input_type}")