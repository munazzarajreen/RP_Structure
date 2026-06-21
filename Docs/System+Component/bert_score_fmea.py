import os
import json
from datetime import datetime

from bert_score import score


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
    output_path = f"runs/{run_id}_bert_score_results.json"

    print(f"Computing BERTScore for {len(references)} aligned pairs...")

    # model_type can be changed if needed, but this default is commonly used
    P, R, F1 = score(
        candidates,
        references,
        lang="en",
        model_type="microsoft/deberta-xlarge-mnli",
        verbose=True,
        device="cuda"  # use GPU if available
    )

    mean_precision = P.mean().item()
    mean_recall = R.mean().item()
    mean_f1 = F1.mean().item()

    print("\n=== Mean BERTScore ===")
    print(f"Precision: {mean_precision:.4f}")
    print(f"Recall:    {mean_recall:.4f}")
    print(f"F1:        {mean_f1:.4f}")

    pair_results = []
    for i, (ref, cand, p, r, f1) in enumerate(zip(references, candidates, P, R, F1), start=1):
        row = {
            "id": i,
            "reference": ref,
            "candidate": cand,
            "precision": round(p.item(), 4),
            "recall": round(r.item(), 4),
            "f1": round(f1.item(), 4),
        }
        pair_results.append(row)

    result = {
        "num_pairs": len(references),
        "mean_precision": round(mean_precision, 4),
        "mean_recall": round(mean_recall, 4),
        "mean_f1": round(mean_f1, 4),
        "pairs": pair_results,
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"\nSaved results to: {output_path}")


if __name__ == "__main__":
    main()