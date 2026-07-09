FMEA_REQUIRED_FIELDS = [
    "component",
    "function",
    "failure_mode",
    "cause",
    "effect_on_other_components",
    "effect_on_whole_system",
    "detection_method",
    "recommended_action",
]


FMECA_REQUIRED_FIELDS = [
    "component",
    "function",
    "failure_mode",
    "cause",
    "effect_on_other_components",
    "effect_on_whole_system",
    "severity",
    "occurrence",
    "detection",
    "rpn",
    "recommended_action",
]


def get_required_fields(analysis_type):
    if analysis_type == "fmea":
        return FMEA_REQUIRED_FIELDS

    if analysis_type == "fmeca":
        return FMECA_REQUIRED_FIELDS

    raise ValueError(f"Unknown analysis type: {analysis_type}")