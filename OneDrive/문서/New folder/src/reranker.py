import pandas as pd
from joblib import load

model = load("models/feedback_model.pkl")

def rerank_matches(matches, current_user):

    reranked = []

    for _, row in matches.iterrows():

        same_location = int(
            current_user["location"] == row["location"]
        )

        same_profession = int(
            current_user["profession"] == row["profession"]
        )

        same_mbti = int(
            current_user["mbti"] == row["mbti"]
        )

        X = [[
            same_location,
            same_profession,
            same_mbti
        ]]

        score = model.predict_proba(X)[0][1]

        row = row.copy()

        row["feedback_score"] = score

        reranked.append(row)

    reranked_df = pd.DataFrame(reranked)

    reranked_df = reranked_df.sort_values(
        by="feedback_score",
        ascending=False
    )

    return reranked_df