import os
import json
from datetime import datetime

from rouge_score import rouge_scorer


references = [
    "Pump: Vane wheel breakage",
    "Pump: Leakage from casing",
    "Pump: Vane wheel jammed",
    "Pump: Pump wear",
    "Filter: Blockage",
    "Filter: Rupture",
    "Unload valve: Failure to unload",
    "Unload valve: Continuous return to reservoir",
    "Check valve: Failure to open",
    "Check valve: Failure to close",
    "Pressure gauge: Incorrect reading",
    "Relief valves: Failure to open",
    "Relief valves: Failure to close",
    "Accumulator bladder: Ruptured",
    "Dump valve: Leakage",
    "Servo-valves: Null position drift/offset",
    "Servo-valves: Failure in closed mode",
    "Servo-valves: Failure in open mode",
    "Actuators: Housing leakage",
    "Actuators: Housing or seal rupture",
    "Piping and seals: Leakage",
    "Piping and seals: Rupture",
    "Reservoir: Leakage: total fluid loss",
    "Reservoir: Leakage: slow fluid loss",
    "Heat exchanger: Oil leakage",
    "Heat exchanger: Insufficient cooling",
]

candidates = [
    "Pump: Insufficient flow rate",
    "Pump: Insufficient flow rate",
    "Pump: Insufficient flow rate",
    "Pump: Insufficient flow rate",
    "Filter: Clogging",
    "Filter: Contamination of hydraulic fluid",
    "Unload valve: Inability to regulate pressure",
    "Unload valve: Sticking",
    "Check valve: Backflow",
    "Check valve: Inability to seal",
    "Pressure gauge: Inaccurate pressure reading",
    "Relief valves: Inability to regulate pressure",
    "Relief valves: Inability to regulate pressure",
    "Accumulator bladder: Loss of pressure",
    "Dump valve: Inability to release pressure",
    "Servo-valves: Inability to control flow",
    "Servo-valves: Inability to control flow",
    "Servo-valves: Inability to control flow",
    "Actuators: Inability to move limb",
    "Actuators: Inability to move limb",
    "Piping and seals: Leakage",
    "Piping and seals: Leakage",
    "Reservoir: Insufficient fluid level",
    "Reservoir: Insufficient fluid level",
    "Heat exchanger: Inability to regulate temperature",
    "Heat exchanger: Inability to regulate temperature",
]


def main():
    if len(references) != len(candidates):
        raise ValueError(
            f"Length mismatch: {len(references)} references vs {len(candidates)} candidates"
        )

    os.makedirs("runs", exist_ok=True)
    run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = f"runs/{run_id}_rouge_l_results.json"

    print(f"Computing ROUGE-L for {len(references)} aligned pairs...")

    scorer = rouge_scorer.RougeScorer(["rougeL"], use_stemmer=True)

    pair_results = []
    f1_scores = []
    precision_scores = []
    recall_scores = []

    for i, (ref, cand) in enumerate(zip(references, candidates), start=1):
        scores = scorer.score(ref, cand)["rougeL"]

        precision_scores.append(scores.precision)
        recall_scores.append(scores.recall)
        f1_scores.append(scores.fmeasure)

        row = {
            "id": i,
            "reference": ref,
            "candidate": cand,
            "rougeL_precision": round(scores.precision, 4),
            "rougeL_recall": round(scores.recall, 4),
            "rougeL_f1": round(scores.fmeasure, 4),
        }
        pair_results.append(row)

    mean_precision = sum(precision_scores) / len(precision_scores)
    mean_recall = sum(recall_scores) / len(recall_scores)
    mean_f1 = sum(f1_scores) / len(f1_scores)

    print("\n=== Mean ROUGE-L ===")
    print(f"Precision: {mean_precision:.4f}")
    print(f"Recall:    {mean_recall:.4f}")
    print(f"F1:        {mean_f1:.4f}")

    result = {
        "num_pairs": len(references),
        "mean_rougeL_precision": round(mean_precision, 4),
        "mean_rougeL_recall": round(mean_recall, 4),
        "mean_rougeL_f1": round(mean_f1, 4),
        "pairs": pair_results,
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"\nSaved results to: {output_path}")


if __name__ == "__main__":
    main()