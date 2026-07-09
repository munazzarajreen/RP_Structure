import time
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer


class LLMEngine:

    def __init__(self):

        self.model_map = {
            "llama": "meta-llama/Llama-3.1-8B-Instruct",
            "mistral": "mistralai/Mistral-7B-Instruct-v0.3",
        }

    def generate(self, config, prompt):

        if config.model_name == "qwen":
            return {
                "model_name": "qwen",
                "model_id": "Qwen2-VL",
                "raw_response": "Qwen2-VL integration will be added later.",
                "generation_time_sec": 0,
                "input_tokens": 0,
                "output_tokens": 0,
                "total_tokens": 0
            }

        if config.model_name not in self.model_map:
            raise ValueError(f"Unsupported model: {config.model_name}")

        model_id = self.model_map[config.model_name]

        # ----------------------------
        # Load tokenizer
        # ----------------------------

        tokenizer = AutoTokenizer.from_pretrained(model_id)

        # ----------------------------
        # Load model
        # ----------------------------

        model = AutoModelForCausalLM.from_pretrained(
            model_id,
            torch_dtype=torch.float16,
            device_map="auto"
        )

        messages = [
            {
                "role": "user",
                "content": prompt
            }
        ]

        input_text = tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )

        inputs = tokenizer(
            input_text,
            return_tensors="pt"
        ).to(model.device)

        input_token_count = inputs["input_ids"].shape[1]

        # ----------------------------
        # Measure inference time
        # ----------------------------

        start_time = time.time()

        outputs = model.generate(
            **inputs,
            max_new_tokens=2048,
            do_sample=False
        )

        end_time = time.time()

        generation_time = round(end_time - start_time, 3)

        # ----------------------------
        # Decode output
        # ----------------------------

        generated_tokens = outputs[0][inputs["input_ids"].shape[-1]:]

        response = tokenizer.decode(
            generated_tokens,
            skip_special_tokens=True
        )

        output_token_count = len(generated_tokens)

        total_tokens = input_token_count + output_token_count

        tokens_per_second = round(
            output_token_count / generation_time,
            2
        ) if generation_time > 0 else 0

        # ----------------------------
        # GPU Memory
        # ----------------------------

        gpu_memory_gb = None

        if torch.cuda.is_available():

            gpu_memory_gb = round(
                torch.cuda.max_memory_allocated() / (1024 ** 3),
                2
            )

        return {

            "model_name": config.model_name,

            "model_id": model_id,

            "generation_time_sec": generation_time,

            "input_tokens": input_token_count,

            "output_tokens": output_token_count,

            "total_tokens": total_tokens,

            "tokens_per_second": tokens_per_second,

            "gpu_memory_gb": gpu_memory_gb,

            "raw_response": response

        }