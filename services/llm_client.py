from transformers import pipeline

# Initialize text generation pipeline with GPT-2 model (small, fast, no sentencepiece)
generator = pipeline("text-generation", model="gpt2")

def get_prediction(prompt: str) -> str:
    outputs = generator(prompt, max_new_tokens=200)
    generated_text = outputs[0]["generated_text"]
    # Remove the prompt text from generated output if present
    if generated_text.startswith(prompt):
        generated_text = generated_text[len(prompt):]
    return generated_text.strip()
