import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from mbti import get_mbti_score

# ----------------------------------
# LOAD DATA
# ----------------------------------

users_df = pd.read_csv("data/users.csv")

# ----------------------------------
# LOAD MODEL
# ----------------------------------
# ----------------------------------
# CREATE COMBINED PROFILE TEXT
# ----------------------------------

users_df["profile_text"] = (
    users_df["professional_summary"] + " "
    + users_df["about_me"] + " "
    + users_df["interests"]
)

# ----------------------------------
# GENERATE EMBEDDINGS
# ----------------------------------

vectorizer = TfidfVectorizer()

embeddings = vectorizer.fit_transform(
    users_df["profile_text"]
)

# ----------------------------------
# LOCATION SCORE
# ----------------------------------

def get_location_score(loc1, loc2):
    if loc1 == loc2:
        return 100
    return 50

# ----------------------------------
# RECOMMEND FUNCTION
# ----------------------------------

def get_top_matches(user_id, top_n=5):

    user_row = users_df[
        users_df["user_id"] == user_id
    ].iloc[0]

    user_index = user_row.name

    scores = []

    for idx, candidate in users_df.iterrows():

        if candidate["user_id"] == user_id:
            continue

        # Semantic Similarity
        text_score = cosine_similarity(
        embeddings[user_index],
        embeddings[idx]
        )[0][0]

        text_score = text_score * 100

        # MBTI Score
        mbti_score = get_mbti_score(
            user_row["mbti"],
            candidate["mbti"]
        )

        # Location Score
        location_score = get_location_score(
            user_row["location"],
            candidate["location"]
        )

        # Final Score
        total_score = (
            (0.5 * text_score)
            + (0.3 * mbti_score)
            + (0.2 * location_score)
        )

        scores.append({
            "user_id": candidate["user_id"],
            "name": candidate["name"],
            "profession": candidate["profession"],
            "mbti": candidate["mbti"],
            "location": candidate["location"],
            "compatibility_score":
                round(total_score, 2),
                "interests": candidate["interests"]
        })

    results = pd.DataFrame(scores)
    print("Scores generated:",len(scores))
    return results.sort_values(
        by="compatibility_score",
        ascending=False
    ).head(top_n)

# ----------------------------------
# TEST
# ----------------------------------
print("The File reached the end successfully")
if __name__ == "__main__":
    

    test_user = "U001"

    matches = get_top_matches(test_user)

    print("\nTop Matches For", test_user)
    print(matches)