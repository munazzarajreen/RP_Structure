import os
import json
from datetime import datetime

from sentence_transformers import SentenceTransformer, util


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
    output_path = f"runs/{run_id}_cosine_similarity_results.json"

    print(f"Computing cosine similarity for {len(references)} aligned pairs...")

    model = SentenceTransformer("all-MiniLM-L6-v2")

    ref_embeddings = model.encode(references, convert_to_tensor=True)
    cand_embeddings = model.encode(candidates, convert_to_tensor=True)

    similarities = util.cos_sim(ref_embeddings, cand_embeddings).diagonal()
    mean_cosine = similarities.mean().item()

    print("\n=== Mean Cosine Similarity ===")
    print(f"Cosine Similarity: {mean_cosine:.4f}")

    pair_results = []
    for i, (ref, cand, sim) in enumerate(zip(references, candidates, similarities), start=1):
        row = {
            "id": i,
            "reference": ref,
            "candidate": cand,
            "cosine_similarity": round(sim.item(), 4),
        }
        pair_results.append(row)

    result = {
        "num_pairs": len(references),
        "mean_cosine_similarity": round(mean_cosine, 4),
        "pairs": pair_results,
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"\nSaved results to: {output_path}")


if __name__ == "__main__":
    main()