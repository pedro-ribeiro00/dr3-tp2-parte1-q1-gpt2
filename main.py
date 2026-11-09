from contextlib import asynccontextmanager
from threading import Lock
from fastapi import FastAPI, HTTPException
from pydantic import Field, BaseModel
from transformers import pipeline
from schemas import TextRequest

class GenerateRequest(TextRequest):
    max_new_tokens: int = Field(default=60, ge=1, le=150)

class GenerateResponse(BaseModel):
    generated_text: str

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.generator = pipeline("text-generation", model="openai-community/gpt2", device=-1)
    app.state.lock = Lock()
    yield

app = FastAPI(title="Parte 1 - Q1 - GPT-2", lifespan=lifespan)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/generate", response_model=GenerateResponse)
def generate(data: GenerateRequest):
    generator = app.state.generator
    tokens = generator.tokenizer.encode(data.text, add_special_tokens=False)
    if len(tokens) + data.max_new_tokens > generator.model.config.n_positions:
        raise HTTPException(422, "Entrada e continuação excedem a janela do GPT-2.")
    try:
        with app.state.lock:
            result = generator(data.text, max_new_tokens=data.max_new_tokens,
                               do_sample=True, temperature=0.8, top_p=0.95,
                               pad_token_id=generator.tokenizer.eos_token_id,
                               return_full_text=True)
        return {"generated_text": result[0]["generated_text"]}
    except RuntimeError as exc:
        raise HTTPException(503, "Falha de inferência local.") from exc
