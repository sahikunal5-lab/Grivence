import pickle
import re
import os

# -------- PATHS --------
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

MODEL_CAT_PATH = os.path.join(BASE_DIR, "models", "model_category.pkl")
VEC_CAT_PATH = os.path.join(BASE_DIR, "models", "vectorizer_category.pkl")

MODEL_PRI_PATH = os.path.join(BASE_DIR, "models", "model_priority.pkl")
VEC_PRI_PATH = os.path.join(BASE_DIR, "models", "vectorizer_priority.pkl")

# -------- LOAD MODELS --------
model_cat = pickle.load(open(MODEL_CAT_PATH, "rb"))
vec_cat = pickle.load(open(VEC_CAT_PATH, "rb"))

model_pri = pickle.load(open(MODEL_PRI_PATH, "rb"))
vec_pri = pickle.load(open(VEC_PRI_PATH, "rb"))

# -------- PREPROCESS --------
def preprocess(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9 ]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# -------- SENTIMENT --------
def get_sentiment(text):
    negative_words = ["problem","issue","bad","dirty","leakage","broken","urgent"]
    return "Negative" if any(w in text.lower() for w in negative_words) else "Neutral"

# -------- RULE BOOST --------
def rule_priority(text, ml_priority):
    text = text.lower()

    if any(w in text for w in ["fire","shock","danger","accident"]):
        return "High"

    return ml_priority

# -------- LOOP --------
while True:
    text = input("\nEnter complaint (type 'exit' to quit): ")

    if text.lower() == "exit":
        break

    clean = preprocess(text)

    # CATEGORY
    cat_vec = vec_cat.transform([clean])
    category = model_cat.predict(cat_vec)[0]

    # PRIORITY (ML)
    pri_vec = vec_pri.transform([clean])
    priority = model_pri.predict(pri_vec)[0]

    # RULE BOOST
    priority = rule_priority(text, priority)

    # SENTIMENT
    sentiment = get_sentiment(text)

    # OUTPUT
    print("\n🔍 RESULT")
    print("👉 Category :", category)
    print("👉 Priority :", priority)
    print("👉 Sentiment:", sentiment)