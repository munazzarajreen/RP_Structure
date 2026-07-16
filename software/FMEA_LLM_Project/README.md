# FMEA LLM Framework

A modular framework for benchmarking Large Language Models for FMEA and FMECA generation.

## Features

- Modular architecture
- FMEA and FMECA support
- Multiple prompt strategies
- Multiple LLM support
  - Llama 3.1
  - Mistral
  - Qwen2-VL (planned)
- Automatic JSON parsing
- Schema validation
- Component coverage evaluation
- Hallucination detection
- RPN validation
- Experiment logging
- Experiment database
- Decision engine

## Project Structure

```
src/
    configure_experiment.py
    input_loader.py
    prompt_builder/
    llm_engine.py
    output_parser.py
    evaluation_engine.py
    decision_engine.py
    experiment_database.py
    experiment_storage.py

data/
    input/

outputs/

main.py
```

## Current Status

Version 0.1

Current capabilities

- Prompt generation
- LLM inference
- Structured parsing
- Evaluation
- Experiment database

Planned work

- Benchmark datasets
- RAG integration
- Fine-tuning
- Multi-model benchmarking
- Research paper experiments
