print("🔥 CLEAN BACKEND RUNNING")

from fastapi import FastAPI, Body
from pydantic import BaseModel
import pickle, sqlite3, os
from fastapi.middleware.cors import CORSMiddleware
from hashlib import sha256

from app.utils import preprocess, get_sentiment, get_priority, check_alert

app = FastAPI()

# -------- CORS --------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------- PATHS --------
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, "database.db")

MODEL_CAT_PATH = os.path.join(BASE_DIR, "models", "model_category.pkl")
VEC_CAT_PATH = os.path.join(BASE_DIR, "models", "vectorizer_category.pkl")

MODEL_PRI_PATH = os.path.join(BASE_DIR, "models", "model_priority.pkl")
VEC_PRI_PATH = os.path.join(BASE_DIR, "models", "vectorizer_priority.pkl")

# -------- LOAD MODEL --------
model_cat = pickle.load(open(MODEL_CAT_PATH, "rb"))
vec_cat = pickle.load(open(VEC_CAT_PATH, "rb"))

model_pri = pickle.load(open(MODEL_PRI_PATH, "rb"))
vec_pri = pickle.load(open(VEC_PRI_PATH, "rb"))

# -------- DB --------
conn = sqlite3.connect(DB_PATH, check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS complaints (
id INTEGER PRIMARY KEY AUTOINCREMENT,
text TEXT,
category TEXT,
priority TEXT,
sentiment TEXT,
status TEXT
)
""")

# -------- LOGIN SYSTEM --------
users = {
    "admin": {
        "password": sha256("admin123".encode()).hexdigest(),
        "role": "admin"
    },
    "user": {
        "password": sha256("user123".encode()).hexdigest(),
        "role": "user"
    }
}

@app.post("/login")
def login(data: dict = Body(...)):
    username = data.get("username")
    password = sha256(data.get("password").encode()).hexdigest()

    if username in users and users[username]["password"] == password:
        return {"status": "success", "role": users[username]["role"]}
    return {"status": "fail"}

# -------- MODEL --------
class Complaint(BaseModel):
    text: str

@app.post("/analyze")
def analyze(data: Complaint):

    clean = preprocess(data.text)

    # CATEGORY
    cat_vec = vec_cat.transform([clean])
    category = model_cat.predict(cat_vec)[0]

    # PRIORITY (ML)
    pri_vec = vec_pri.transform([clean])
    priority = model_pri.predict(pri_vec)[0]

    # SENTIMENT
    sentiment = get_sentiment(data.text)

    # RULE BOOST
    if any(w in data.text.lower() for w in ["fire","shock","danger","accident"]):
        priority = "High"

    # ALERT
    alert = check_alert(priority)

    # SAVE DB
    cursor.execute("""
    INSERT INTO complaints(text,category,priority,sentiment,status)
    VALUES(?,?,?,?,?)
    """,(data.text,category,priority,sentiment,"Pending"))

    conn.commit()

    return {
        "category": category,
        "priority": priority,
        "sentiment": sentiment,
        "alert": alert
    }

# -------- FETCH --------
@app.get("/complaints")
def get_all():
    cursor.execute("SELECT * FROM complaints ORDER BY id DESC")
    return cursor.fetchall()

# -------- UPDATE --------
@app.put("/update/{cid}")
def update(cid: int, status: str):
    cursor.execute("UPDATE complaints SET status=? WHERE id=?", (status, cid))
    conn.commit()
    return {"msg": "updated"}