from fastapi import FastAPI
from pydantic import BaseModel
from groq import Groq
import os

app = FastAPI()

# 🔐 API KEY iz Railway (NE upisuješ ručno!)
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

MODEL = "llama-3.3-70b-versatile"

SYSTEM = """
Ti si moj djed.

Govoriš mirno, toplo i jednostavno.
Ponekad kažeš "sinko".
Daješ životne savjete.
Ne koristiš moderne izraze.
"""

STYLE = """
- "Ma slušaj sinko, sve se to na kraju posloži."
- "Ne treba žuriti, svaka stvar dođe na svoje."
- "Bitno je da si ti zdrav, ostalo ćemo lako."
"""

class Request(BaseModel):
    prompt: str

@app.post("/chat")
def chat(req: Request):
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM},
            {"role": "system", "content": STYLE},
            {"role": "user", "content": req.prompt}
        ],
        temperature=0.8
    )

    return {"reply": response.choices[0].message.content}