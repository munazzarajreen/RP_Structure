def build(config):
    if config.analysis_type == "fmea":
        return """
Task:
Generate a Failure Modes and Effects Analysis (FMEA) for the given system.
""".strip()

    if config.analysis_type == "fmeca":
        return """
Task:
Generate a Failure Modes, Effects and Criticality Analysis (FMECA) for the given system.
""".strip()

    raise ValueError(f"Unknown analysis type: {config.analysis_type}")