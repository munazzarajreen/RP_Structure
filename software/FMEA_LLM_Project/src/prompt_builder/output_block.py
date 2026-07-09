def build(config):
    if config.prompt_style == "minimal":
        return """
Output:
Provide the analysis in a clear and understandable format.
""".strip()

    if config.prompt_style == "structured":
        return """
Output:
Return the result in JSON format.
""".strip()

    if config.prompt_style == "constrained":
        if config.analysis_type == "fmea":
            return """
Output:
Return only valid JSON with the following fields:
component
function
failure_mode
cause
effect_on_other_components
effect_on_whole_system
detection_method
recommended_action
""".strip()

        if config.analysis_type == "fmeca":
            return """
Output:
Return only valid JSON with the following fields:
component
function
failure_mode
cause
effect_on_other_components
effect_on_whole_system
severity
occurrence
detection
rpn
recommended_action
""".strip()

    raise ValueError(f"Unknown prompt style: {config.prompt_style}")