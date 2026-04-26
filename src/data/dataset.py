import pandas as pd
import random

categories = {
    "electricity": {
        "keywords": [
            "bijli", "light", "power", "electricity",
            "current", "voltage", "transformer", "meter","dp"
        ],
        "phrases": [
            "nahi aa rahi",
            "bar bar cut ho rahi hai",
            "fluctuation ho raha hai",
            "transformer kharab hai",
            "meter ka issue hai",
            "current nahi aa raha",
            "power failure ho gaya hai",
            "shock lagne ka danger hai",
            "faat gaya"
        ]
    },

    "water": {
        "keywords": [
            "pani", "water", "supply", "pipeline", "tap", "jal"
        ],
        "phrases": [
            "nahi aa raha",
            "pressure bahut kam hai",
            "pipeline leak ho rahi hai",
            "ganda pani aa raha hai",
            "supply band hai",
            "water issue hai",
            "tap se pani nahi aa raha"
        ]
    },

    "sanitation": {
        "keywords": [
            "kooda", "garbage", "waste", "drain", "nala", "safai"
        ],
        "phrases": [
            "nahi uthaya gaya",
            "overflow ho raha hai",
            "bahut badbu aa rahi hai",
            "drain block ho gaya hai",
            "kachra jama hai",
            "cleaning nahi hui",
            "area ganda hai"
        ]
    },

    "roads": {
        "keywords": [
            "road", "sadak", "pothole", "construction", "street"
        ],
        "phrases": [
            "toot gayi hai",
            "bahut kharab condition me hai",
            "bade potholes hai",
            "accident ka danger hai",
            "road damage hai",
            "kaam adhura hai",
            "construction incomplete hai"
        ]
    },

    "public": {
        "keywords": [
            "noise", "awaz", "parking", "crowd", "traffic"
        ],
        "phrases": [
            "bahut zyada hai",
            "control nahi ho raha",
            "illegal parking ho rahi hai",
            "disturbance create ho raha hai",
            "traffic jam ho raha hai",
            "log bahut shor kar rahe hai"
        ]
    }
}

locations = [
    "near school", "colony me", "market me",
    "ghar ke paas", "near hospital", "main road pe",
    "society me", "area me"
]

prefix = [
    "", "please help,", "complaint:", "urgent:",
    "bahut problem hai,", "serious issue,"
]

suffix = [
    "", "please fix asap", "jaldi solve kare",
    "immediate action needed", "bahut dikkat ho rahi hai"
]

# Priority keywords
high_words = ["danger", "accident", "shock", "fire", "urgent", "serious"]

data = []

for _ in range(7500):   # increased data

    category = random.choice(list(categories.keys()))

    keyword = random.choice(categories[category]["keywords"])
    phrase = random.choice(categories[category]["phrases"])
    loc = random.choice(locations)

    pre = random.choice(prefix)
    suf = random.choice(suffix)

    text = f"{pre} {keyword} {phrase} {loc} {suf}".strip()
    text = " ".join(text.split())

    # -------- ADD REALISTIC NOISE --------
    if random.random() < 0.15:
        text = text.replace("hai", "h").replace("problem", "prblm")

    # -------- SENTIMENT --------
    if any(w in text.lower() for w in high_words):
        sentiment = "Negative"
    else:
        sentiment = random.choice(["Negative", "Neutral"])

    # -------- PRIORITY --------
    if any(w in text.lower() for w in ["danger", "accident", "shock", "fire"]):
        priority = "High"
    elif "urgent" in text.lower():
        priority = "High"
    else:
        priority = "High" if sentiment == "Negative" and random.random() > 0.65 else "Normal"

    data.append([text, category, priority, sentiment])

df = pd.DataFrame(data, columns=["text", "category", "priority", "sentiment"])

df = df.sample(frac=1).reset_index(drop=True)

df.to_csv("advanced_dataset.csv", index=False)

print("🔥 PRO DATASET READY:", len(df))