from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import cohere

app = FastAPI()

# ------------------- CORS -------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------- COHERE CLIENT -------------------
co = cohere.Client("Q0E43l3hbG1y8zdhSkiU6DTaVMVFPTIqVEm7CCU9")

# ------------------- SYSTEM PROMPT -------------------
system_prompt = """
You are an Elevator Specialist.
You answer only elevator-related questions in ONLY 3 lines.
If unrelated, reply in Telugu: "నేను కేవలం ఎలివేటర్‌ సంబంధిత ప్రశ్నలకు మాత్రమే సమాధానం చెప్పగలను."
If user asks nothing, greet them in Telugu.
If user asks for a page, return this format ONLY:

{"navigate": "<page>", "message": "<short Telugu answer>"}

Valid pages:
/home, /services, /products, /contact, /about, /gallery, /clients, /careers
"""

# ------------------- REQUEST BODY -------------------
class ChatRequest(BaseModel):
    question: str


# ============================
# 🚀 CHAT API WITH PAGE NAVIGATION
# ============================
@app.post("/chat")
def ask_bot(req: ChatRequest):
    q = req.question.lower().strip()

    if q == "":
        return {
            "answer": "హలో! ఎలివేటర్‌ సంబంధిత ఏ ప్రశ్నకైనా నేను సహాయం చేస్తాను.",
            "navigate": None
        }

    # -------- PAGE TRIGGER KEYWORDS --------
    PAGE_MAP = {
        "home": "/",
        "service": "/services",
        "installation": "/services",
        "repair": "/services",
        "maintain": "/services",

        "product": "/products",
        "model": "/products",

        "gallery": "/gallery",
        "photos": "/gallery",

        "client": "/clients",
        "brand": "/clients",

        "career": "/careers",
        "job": "/careers",

        "contact": "/contact",
        "phone": "/contact",
        "call": "/contact",

        "about": "/about",
        "company": "/about",
    }

    for key, route in PAGE_MAP.items():
        if key in q:
            return {
                "answer": "మీరు కోరిన పేజీని తెరవుతున్నాను...",
                "navigate": route
            }

    # ------- AI CALL (FREE TIER SAFE) -------
    final_prompt = f"{system_prompt}\nUser: {req.question}"

    response = co.chat(
        model="command-r7b-12-2024",
        message=final_prompt
    )

    return {
        "answer": response.text,
        "navigate": None
    }


# -------------------
# ROOT TEST ROUTE
# -------------------
@app.get("/")
def root():
    return {"message": "Chatbot API Running Successfully!"}
