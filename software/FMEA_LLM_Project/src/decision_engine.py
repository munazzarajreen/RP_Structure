class DecisionEngine:
    def decide(self, evaluation_result):
        return {
            "decision_status": "dummy_decision_success",
            "sufficiency": "not_decided_yet",
            "recommendation": "Real sufficiency rules will be added later.",
            "based_on": evaluation_result["evaluation_status"]
        }