"""
LLM Wrapper (Low-Resource, Open-Source)

Uses Phi-3 Mini for CPU-only inference.
Optimized for 8GB RAM systems.
"""

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
import torch

MODEL_NAME = "google/flan-t5-base"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

model = AutoModelForSeq2SeqLM.from_pretrained(
    MODEL_NAME,
    device_map="cpu",
    dtype=torch.float32,
    low_cpu_mem_usage=True
)

generator = pipeline(
    "text2text-generation",
    model=model,
    tokenizer=tokenizer,
#    device=-1,   # CPU
)

SYSTEM_PROMPT = """
You are a university admissions assistant.

Rules:
- Answer ONLY using the provided context.
- If the answer is not present, say:
  "I don’t have that information in my knowledge base."
- Do NOT give advice, predictions, or opinions.
- Do NOT include private or personal data.
- Keep answers factual and concise.
"""

def generate_answer(context: str, question: str) -> str:
    prompt = f"""
<System>
{SYSTEM_PROMPT}
</System>

Context:
{context}

Question:
{question}

Answer:
"""

    output = generator(
        prompt,
        max_new_tokens=150,
        temperature=0.2,
        do_sample=False,
        pad_token_id=tokenizer.eos_token_id,
    )

    text = output[0]["generated_text"]
    return text.split("Answer:")[-1].strip()
