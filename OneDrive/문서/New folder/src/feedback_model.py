from joblib import dump
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# -----------------------------
# LOAD DATA
# -----------------------------

users_df = pd.read_csv("../data/users.csv")
feedback_df = pd.read_csv("../data/feedback.csv")
print("Users:", len(users_df))
print("Feedback:", len(feedback_df))
print(feedback_df.head())
# -----------------------------
# CREATE FEATURES
# -----------------------------
print("Users:", len(users_df))
print("Feedback:", len(feedback_df))

print("\nFeedback Columns:")
print(feedback_df.columns.tolist())

print("\nFirst 5 Rows:")
print(feedback_df.head())
features = []

for _, row in feedback_df.iterrows():

    user = users_df[
        users_df["user_id"] == row["user_id"]
    ].iloc[0]

    matched = users_df[
        users_df["user_id"] == row["matched_user_id"]
    ].iloc[0]
same_location = int(
    user["location"] == matched["location"]
)

same_profession = int(
    user["profession"] == matched["profession"]
)

same_mbti = int(
    user["mbti"] == matched["mbti"]
)

interest_overlap = len(
    set(user["interests"].split(", "))
    &
    set(matched["interests"].split(", "))
)

experience_gap = abs(
    user["experience_years"]
    - matched["experience_years"]
)

age_gap = abs(
    user["age"]
    - matched["age"]
)
features.append({
    "same_location": same_location,
    "same_profession": same_profession,
    "same_mbti": same_mbti,
    "interest_overlap": interest_overlap,
    "experience_gap": experience_gap,
    "age_gap": age_gap,
    "action": row["action"]
})
print("Features list length:", len(features))
X = pd.DataFrame(
    features,
    columns=[
        "same_location",
        "same_profession",
        "same_mbti"
    ]
)

y = feedback_df["action"]

# -----------------------------
# TRAIN MODEL
# -----------------------------
print("Features rows:", len(X))
print("Target rows:", len(y))
print(X.head())
print(y.head())
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

model = LogisticRegression()

model.fit(X_train, y_train)

predictions = model.predict(X_test)

accuracy = accuracy_score(
    y_test,
    predictions
)

print("\nModel Accuracy:", round(accuracy * 100, 2), "%")

dump(model, "../models/feedback_model.pkl")

print("Model saved successfully!")
# -----------------------------
# PREFERENCE FUNCTION
# -----------------------------

def predict_acceptance(
        same_location,
        same_profession,
        same_mbti):

    probability = model.predict_proba([
        [
            same_location,
            same_profession,
            same_mbti
        ]
    ])[0][1]

    return round(probability * 100, 2)