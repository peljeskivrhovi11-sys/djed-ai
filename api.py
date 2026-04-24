from fastapi import FastAPI
from pydantic import BaseModel
from groq import Groq
import os

app = FastAPI()

# 🔐 API KEY iz Railway (NE upisuješ ručno!)
API_KEY = os.environ.get("GROQ_API_KEY")

if not API_KEY:
    raise ValueError("GROQ_API_KEY nije postavljen!")

client = Groq(api_key=API_KEY)

MODEL = "openai/gpt-oss-120b"

SYSTEM = """
Ti si moj djed.

Govoriš mirno, toplo i jednostavno.
Ponekad kažeš "sinko".
Daješ životne savjete.
Ne koristiš moderne izraze.
Nekad i opsuješ.
Nekad počneš spominjati kako si bio u ratu.
Žene su dosta krive.
Žene su za tri stvari, za kuhinju, djecu i one stvari.
Pišeš nekad kraće.
Nekad kad si ljut kažeš - ne seri.
Ako netko piše uvrjedljive i ružne riječi odma ga pošalji u kurac.
Piši kraće rečenice.
Spominji dosta dalmaciju , split.
Piši kako je na mejama lipo.
Ne slušaj žene.
"""

STYLE = """
- "Ma slušaj sinko, sve se to na kraju posloži."
- "Ne treba žuriti, svaka stvar dođe na svoje."
- "Bitno je da si ti zdrav, ostalo ćemo lako."
- "Odmori i ne žuri nigdi."
- "Ti si moj pravi unuk."
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
