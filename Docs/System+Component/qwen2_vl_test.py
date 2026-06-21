import os
import torch
from PIL import Image
from transformers import AutoProcessor, Qwen2VLForConditionalGeneration

MODEL_ID = "Qwen/Qwen2-VL-7B-Instruct"
IMAGE_PATH = "assets/PID_diagram.png"

PROMPT = """
You are a safety engineer.

Analyze the uploaded system diagram.

Task:
1. Identify the main components visible in the diagram.
2. Identify the main sections of the system.
3. Briefly describe how the system appears to operate.

Return only plain text.
Do not return JSON.
Do not return markdown.
""".strip()


def main():
    if not os.path.exists(IMAGE_PATH):
        raise FileNotFoundError(f"Image not found: {IMAGE_PATH}")

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

    print("Generating response...")
    with torch.no_grad():
        generated_ids = model.generate(
            **inputs,
            max_new_tokens=800,
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

    print("\n===== MODEL OUTPUT START =====\n")
    print(output_text)
    print("\n===== MODEL OUTPUT END =====\n")


if __name__ == "__main__":
    main()
    