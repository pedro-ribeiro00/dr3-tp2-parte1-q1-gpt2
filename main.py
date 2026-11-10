from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator
from transformers import pipeline

app = FastAPI()
gerador = pipeline("text-generation", model="openai-community/gpt2", device=-1)


class Entrada(BaseModel):
    text: str = Field(min_length=1, max_length=20000)

    @field_validator("text")
    @classmethod
    def validar_texto(cls, texto):
        if not texto.strip():
            raise ValueError("Informe um texto.")
        return texto

@app.post("/generate")
def gerar(entrada: Entrada):
    tokens = gerador.tokenizer.encode(entrada.text, add_special_tokens=False)
    if len(tokens) + 60 > gerador.model.config.n_positions:
        raise HTTPException(422, "Texto maior que o limite do GPT-2.")
    resultado = gerador(entrada.text, max_new_tokens=60, do_sample=True,
                        pad_token_id=gerador.tokenizer.eos_token_id)
    return {"generated_text": resultado[0]["generated_text"]}
