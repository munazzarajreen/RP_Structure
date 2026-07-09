import json
import re

from src.schemas import get_required_fields


class OutputParser:
    def parse(self, llm_response, config):
        raw_response = llm_response.get("raw_response", "")

        cleaned_text = self._remove_markdown_code_blocks(raw_response)
        json_text = self._extract_json_text(cleaned_text)

        result = {
            "model_name": llm_response.get("model_name"),
            "parser_status": "failed",
            "json_valid": False,
            "rows": [],
            "missing_fields": [],
            
        }

        try:
            data = json.loads(json_text)
            result["json_valid"] = True
        except json.JSONDecodeError as error:
            result["parser_error"] = str(error)
            return result

        rows = self._normalize_rows(data)
        result["rows"] = rows

        missing_fields = self._check_required_fields(
            rows,
            config.analysis_type
        )

        result["missing_fields"] = missing_fields

        if len(missing_fields) == 0 and len(rows) > 0:
            result["parser_status"] = "success"
        elif len(rows) > 0:
            result["parser_status"] = "success_with_missing_fields"
        else:
            result["parser_status"] = "success_but_no_rows_found"

        return result

    def _remove_markdown_code_blocks(self, text):
        text = text.strip()
        text = re.sub(r"^```json\s*", "", text)
        text = re.sub(r"^```\s*", "", text)
        text = re.sub(r"\s*```$", "", text)
        return text.strip()

    def _extract_json_text(self, text):
        text = text.strip()

        first_array = text.find("[")
        first_object = text.find("{")

        if first_array == -1 and first_object == -1:
            return text

        if first_array == -1:
            start = first_object
        elif first_object == -1:
            start = first_array
        else:
            start = min(first_array, first_object)

        last_array = text.rfind("]")
        last_object = text.rfind("}")

        end = max(last_array, last_object)

        return text[start:end + 1]

    def _normalize_rows(self, data):
        if isinstance(data, list):
            return data

        if isinstance(data, dict):
            possible_keys = [
                "FMEA_Results",
                "FMECA_Results",
                "FMEA",
                "FMECA",
                "results",
                "rows",
            ]

            for key in possible_keys:
                if key in data and isinstance(data[key], list):
                    return data[key]

        return []

    def _check_required_fields(self, rows, analysis_type):
        required_fields = get_required_fields(analysis_type)

        missing_fields = []

        for index, row in enumerate(rows):
            for field in required_fields:
                if field not in row:
                    missing_fields.append({
                        "row": index + 1,
                        "missing_field": field
                    })

        return missing_fields