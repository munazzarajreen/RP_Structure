class EvaluationEngine:

    def evaluate(self, parsed_output, experiment_input=None, config=None):
        rows = parsed_output.get("rows", [])
        missing_fields = parsed_output.get("missing_fields", [])

        evaluation = {
            "evaluation_status": "completed",

            "json_valid": parsed_output.get("json_valid", False),
            "parser_status": parsed_output.get("parser_status"),
            "parser_success": parsed_output.get("parser_status") == "success",

            "row_count": len(rows),
            "missing_fields_count": len(missing_fields),
            "missing_fields": missing_fields,

            "schema_compliance": len(missing_fields) == 0,

            "component_check_enabled": False,
            "expected_components": [],
            "generated_components": [],
            "covered_components": [],
            "missing_components": [],
            "hallucinated_components": [],
            "component_coverage_percent": None,
            "hallucination_rate_percent": None,

            "rpn_check_enabled": False,
            "rpn_correct_count": 0,
            "rpn_incorrect_count": 0,
            "rpn_accuracy_percent": None,
            "invalid_rpn_rows": []
        }

        generated_components = [
            row.get("component")
            for row in rows
            if row.get("component")
        ]

        evaluation["generated_components"] = generated_components

        # Component coverage and hallucination check
        if experiment_input and experiment_input.get("component_list"):
            evaluation["component_check_enabled"] = True

            expected_components = experiment_input["component_list"]
            evaluation["expected_components"] = expected_components

            expected_lower = [component.lower() for component in expected_components]
            generated_lower = [component.lower() for component in generated_components]

            covered_components = []
            missing_components = []

            for component in expected_components:
                if component.lower() in generated_lower:
                    covered_components.append(component)
                else:
                    missing_components.append(component)

            hallucinated_components = []

            for component in generated_components:
                if component.lower() not in expected_lower:
                    hallucinated_components.append(component)

            evaluation["covered_components"] = covered_components
            evaluation["missing_components"] = missing_components
            evaluation["hallucinated_components"] = hallucinated_components

            if len(expected_components) > 0:
                evaluation["component_coverage_percent"] = round(
                    len(covered_components) / len(expected_components) * 100,
                    2
                )

            if len(generated_components) > 0:
                evaluation["hallucination_rate_percent"] = round(
                    len(hallucinated_components) / len(generated_components) * 100,
                    2
                )

        # RPN check for FMECA
        if config and config.analysis_type == "fmeca":
            evaluation["rpn_check_enabled"] = True

            correct_count = 0
            incorrect_count = 0
            invalid_rows = []

            for index, row in enumerate(rows):
                severity = row.get("severity")
                occurrence = row.get("occurrence")
                detection = row.get("detection")
                rpn = row.get("rpn")

                if not all(isinstance(value, int) for value in [severity, occurrence, detection, rpn]):
                    incorrect_count += 1
                    invalid_rows.append({
                        "row": index + 1,
                        "reason": "Severity, occurrence, detection, or RPN is missing or not an integer."
                    })
                    continue

                expected_rpn = severity * occurrence * detection

                if rpn == expected_rpn:
                    correct_count += 1
                else:
                    incorrect_count += 1
                    invalid_rows.append({
                        "row": index + 1,
                        "severity": severity,
                        "occurrence": occurrence,
                        "detection": detection,
                        "expected_rpn": expected_rpn,
                        "actual_rpn": rpn
                    })

            evaluation["rpn_correct_count"] = correct_count
            evaluation["rpn_incorrect_count"] = incorrect_count
            evaluation["invalid_rpn_rows"] = invalid_rows

            if len(rows) > 0:
                evaluation["rpn_accuracy_percent"] = round(
                    correct_count / len(rows) * 100,
                    2
                )

        return evaluation