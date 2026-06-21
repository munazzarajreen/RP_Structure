import os
import re
import json
from datetime import datetime

import torch
from PIL import Image
from transformers import AutoProcessor, Qwen2VLForConditionalGeneration

MODEL_ID = "Qwen/Qwen2-VL-7B-Instruct"
IMAGE_PATH = "assets/PID_diagram.png"

PROMPT = """
You are a safety engineer.

The uploaded image is a system diagram.

Task:
Analyze the diagram and generate a Failure Modes and Effects Analysis (FMEA) for the system.

Instructions:
- Identify components directly from the diagram
- Generate realistic component-level failure modes
- Describe effects on other components
- Describe effects on the whole system
- Include detection methods
- Include compensating provisions and remarks
- Return exactly 25 rows
- Return ONLY valid JSON
- Do not return markdown
- Do not return explanations

Output format:
{
  "rows": [
    {
      "component": "...",
      "failure_mode": "...",
      "effect_on_other_components": "...",
      "effect_on_whole_system": "...",
      "detection_method": "...",
      "compensating_provisions_and_remarks": "..."
    }
  ]
}
""".strip()


def extract_json_block(text: str) -> str:
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1 or end <= start:
        raise ValueError("No valid JSON object found in model output.")
    return text[start:end + 1].strip()


def main():
    if not os.path.exists(IMAGE_PATH):
        raise FileNotFoundError(f"Image not found: {IMAGE_PATH}")

    os.makedirs("runs", exist_ok=True)
    run_id = datetime.now().strftime("%Y%m%d_%H%M%S")

    raw_path = f"runs/{run_id}_vlm_s1_raw.txt"
    json_path = f"runs/{run_id}_vlm_s1_output.json"
    error_path = f"runs/{run_id}_vlm_s1_error.txt"

    print("Loading image...")
    image = Image.open(IMAGE_PATH).convert("RGB")

    print("Loading processor...")
    processor = AutoProcessor.from_pretrained(MODEL_ID)

    print("Loading model...")
    model = Qwen2VLForConditionalGeneration.from_pretrained(
        MODEL_ID,
        torch_dtype=torch.float16,
        device_map="auto",
    )

    messages = [
        {
            "role": "user",
            "content": [
                {"type": "image", "image": image},
                {"type": "text", "text": PROMPT},
            ],
        }
    ]

    text = processor.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True,
    )

    inputs = processor(
        text=[text],
        images=[image],
        padding=True,
        return_tensors="pt",
    ).to(model.device)

    print("Generating FMEA...")
    with torch.no_grad():
        generated_ids = model.generate(
            **inputs,
            max_new_tokens=3000,
            do_sample=False,
        )

    generated_ids_trimmed = [
        out_ids[len(in_ids):]
        for in_ids, out_ids in zip(inputs.input_ids, generated_ids)
    ]

    output_text = processor.batch_decode(
        generated_ids_trimmed,
        skip_special_tokens=True,
        clean_up_tokenization_spaces=True,
    )[0]

    with open(raw_path, "w", encoding="utf-8") as f:
        f.write(output_text)

    print("\n===== RAW OUTPUT START =====\n")
    print(output_text[:4000])
    print("\n===== RAW OUTPUT END =====\n")

    try:
        json_text = extract_json_block(output_text)
        data = json.loads(json_text)

        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        print(f"Saved:\n- {raw_path}\n- {json_path}")

    except Exception as e:
        with open(error_path, "w", encoding="utf-8") as f:
            f.write(f"ERROR:\n{e}\n\nRAW OUTPUT:\n{output_text}")

        print(f"Parsing failed: {e}")
        print(f"Saved:\n- {raw_path}\n- {error_path}")


if __name__ == "__main__":
    main()