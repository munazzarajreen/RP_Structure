def build(config):
    constraints = []

    if config.prompt_style == "constrained":
        constraints.append("Constraints:")
        constraints.append("- Return only valid JSON.")
        constraints.append("- Do not include explanations outside the JSON.")
        constraints.append("- Each row must describe one failure mode.")
        constraints.append("- Use technical and concise wording.")

        if config.input_type == "system_description_with_components":
            constraints.append("- Use only the provided components.")
            constraints.append("- Do not invent additional components.")

        if config.analysis_type == "fmeca":
            constraints.append("- Severity, occurrence, and detection must be integers from 1 to 10.")
            constraints.append("- Calculate RPN as severity × occurrence × detection.")

    if not constraints:
        return ""

    return "\n".join(constraints)