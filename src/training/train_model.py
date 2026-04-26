import pandas as pd
import re
import pickle
import os

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# -------- PATHS --------
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

DATA_PATH = os.path.join(BASE_DIR, "data", "advanced_dataset.csv")

MODEL_CAT_PATH = os.path.join(BASE_DIR, "models", "model_category.pkl")
VEC_CAT_PATH = os.path.join(BASE_DIR, "models", "vectorizer_category.pkl")

MODEL_PRI_PATH = os.path.join(BASE_DIR, "models", "model_priority.pkl")
VEC_PRI_PATH = os.path.join(BASE_DIR, "models", "vectorizer_priority.pkl")


# -------- LOAD DATA --------
df = pd.read_csv(DATA_PATH)

# -------- PREPROCESS --------
def preprocess(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9 ]', ' ', text)
    return text

df["clean"] = df["text"].apply(preprocess)

# -------- TRAIN / TEST SPLIT --------
X_train, X_test, y_train, y_test = train_test_split(
    df["clean"], df["category"], test_size=0.2, random_state=42
)

# -------- CATEGORY MODEL --------
vec_cat = TfidfVectorizer(max_features=5000)
X_train_vec_cat = vec_cat.fit_transform(X_train)
X_test_vec_cat = vec_cat.transform(X_test)

model_cat = LogisticRegression(max_iter=300)
model_cat.fit(X_train_vec_cat, y_train)

y_pred_cat = model_cat.predict(X_test_vec_cat)
acc_cat = accuracy_score(y_test, y_pred_cat)

print(f"✅ Category Accuracy: {acc_cat*100:.2f}%")

# -------- PRIORITY MODEL --------
vec_pri = TfidfVectorizer(max_features=3000)
X_vec_pri = vec_pri.fit_transform(df["clean"])

model_pri = LogisticRegression(max_iter=300)
model_pri.fit(X_vec_pri, df["priority"])

print("✅ Priority Model Trained")

# -------- SAVE MODELS --------
pickle.dump(model_cat, open(MODEL_CAT_PATH, "wb"))
pickle.dump(vec_cat, open(VEC_CAT_PATH, "wb"))

pickle.dump(model_pri, open(MODEL_PRI_PATH, "wb"))
pickle.dump(vec_pri, open(VEC_PRI_PATH, "wb"))

print("🔥 ALL MODELS SAVED SUCCESSFULLY")