# A tiny FastAPI server that loads a SentenceTransformer once
# and answers any text you send it.
# -------------------------------------------------
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
import numpy as np
import uvicorn

app = FastAPI(title="RenPy‑NLP Bridge")

model = SentenceTransformer('all-mpnet-base-v2')


CANNED = [
    "Ah, you are going to the market! I will go with you. From Ur came the best toy-maker, have you heard? They have animal figures on wheels, and new whistles!",
    "Oh, you do not tell you, keep your secrets, Shibtu!",
    "Do not be mad at me! I am your friend.",
    "I am sorry you do not tell me."
]
jumps = ['market', 'market', 'market', 'market']

CANNED_EMB = model.encode(CANNED, normalize_embeddings=True)

class Query(BaseModel):
    text: str

@app.post("/reply")
def get_reply(payload: Query):

    q_vec = model.encode([payload.text], normalize_embeddings=True)[0]

    # Cosine similarity
    sims = np.dot(CANNED_EMB, q_vec)
    best_idx = int(np.argmax(sims))

    return {
        "reply": CANNED[best_idx],
        "score": float(sims[best_idx]),
        "jump_loc": jumps[best_idx]
    }

# Run the server, localhost
if __name__ == "__main__":
    uvicorn.run("nlp_service:app", host="127.0.0.1", port=8000, log_level="info")