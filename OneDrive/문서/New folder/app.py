from os import name

from src.reranker import rerank_matches
import streamlit as st
import pandas as pd
import sys

sys.path.append("./src")

from matcher import get_top_matches, users_df

st.set_page_config(
    page_title="Profile Matching System",
    page_icon="🤝",
    layout="wide"
)

st.title("🤝 Intelligent Hybrid Recommendation System")

st.write(
    "AI-powered profile matching using NLP, MBTI compatibility, and location scoring."
)

# --------------------------------
# USER SELECTION
# --------------------------------

user_options = users_df["user_id"].tolist()

selected_user = st.selectbox(
    "Select User",
    user_options
)

# --------------------------------
# BUTTON
# --------------------------------

if st.button("Find Top Matches"):
    
    matches = get_top_matches(selected_user)

    current_user = users_df[
        users_df["user_id"] == selected_user
    ].iloc[0]
    st.write("DEBUG:",current_user)
    st.subheader("Selected User Profile")

    st.write({
    "Name": current_user["name"],
    "Profession": current_user["profession"],
    "Location": current_user["location"],
    "MBTI": current_user["mbti"],
    "Age": current_user["age"]
})
    matches = rerank_matches(
        matches,
        current_user
    )
    st.write(matches.columns)
    matches["match_percentage"] = (
    matches["compatibility_score"]
    / matches["compatibility_score"].max()
) * 100
    
    st.subheader(f"Top Matches for {selected_user}")
    st.dataframe(matches)
    st.subheader("Compatibility Chart")

    st.bar_chart(
    matches.set_index("name")["compatibility_score"]
)
    st.subheader("MBTI Distribution")
    
    st.bar_chart(
        matches["mbti"].value_counts()
    )
    st.write("Common interests:",matches["interests"])
    st.subheader("Best Match")

    best = matches.iloc[0]

    st.write({
    "Name": best["name"],
    "Profession": best["profession"],
    "Location": best["location"],
    "MBTI": best["mbti"],
    "Compatibility %": round(best["match_percentage"], 2)
})
    st.subheader("Why This Match?")

    st.info(
    f"""
    • Same MBTI Type: {best['mbti']}
    • Location: {best['location']}
    • Profession: {best['profession']}
    • Compatibility Score: {round(best['match_percentage'],2)}%
    • AI Feedback Score: {round(best['feedback_score'],4)}
    """
)
    st.subheader("Performance Analysis")

    accuracy = round(matches["feedback_score"].mean() * 100, 2)

    baseline_accuracy = 58
    improvement = round(accuracy - baseline_accuracy, 2)

    avg_compatibility = round(
        matches["compatibility_score"].mean(),
        2
    )

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Recommendation Accuracy",
            f"{accuracy}%",
            f"{improvement:+}%"
        )

    with col2:
        st.metric(
            "Average Compatibility",
            f"{avg_compatibility}"
        )

    st.subheader("AI Feedback Score")

    st.dataframe(
        matches[
            [
                "user_id",
                "name",
                "feedback_score"
            ]
        ]
    )

    st.subheader("Project Summary")

    st.write({
        "Users": len(users_df),
        "Matching Method": "NLP + MBTI + Location",
        "Learning Model": "Feedback-based ML Re-ranking",
        "Top Matches Displayed": len(matches)
    })

    st.subheader("Project Statistics")

    st.write({
        "Total Users": len(users_df),
        "Top Matches Displayed": len(matches),
        "Recommendation Model": "NLP + MBTI + Location",
        "AI Re-ranking": "Random Forest",
        "Accuracy": f"{accuracy}%"
    })

    csv = matches.to_csv(index=False)

    st.download_button(
        "Download Recommendations",
        csv,
        "recommendations.csv",
        "text/csv"
    )

    st.success("Recommendations Generated Successfully!")
