import streamlit as st
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score


# -------------------------------
# Load Dataset
# -------------------------------
df = pd.read_csv(
    "SMSSpamCollection",
    sep="\t",
    names=["label", "message"]
)

# Convert labels
df["label"] = df["label"].map({
    "ham": 0,
    "spam": 1
})

# Separate input and output
X = df["message"]
y = df["label"]

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# TF-IDF
vectorizer = TfidfVectorizer(
    lowercase=True,
    stop_words="english"
)

X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

# Train model
model = MultinomialNB()
model.fit(X_train_tfidf, y_train)

# Predictions
y_pred = model.predict(X_test_tfidf)

# Metrics
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)


# -------------------------------
# User Interface
# -------------------------------

st.set_page_config(
    page_title="Spam Mail Detector",
    page_icon="📩",
    layout="centered"
)

st.title("📩 Spam Mail Detector")
st.write("Enter a message below to determine whether it is spam or ham.")

st.divider()

message = st.text_area(
    "Enter your message:",
    placeholder="Example: Congratulations! You have won a free prize..."
)

if st.button("🔍 Check Message", use_container_width=True):

    if message.strip() == "":
        st.warning("Please enter a message.")

    else:
        message_tfidf = vectorizer.transform([message])
        prediction = model.predict(message_tfidf)[0]

        if prediction == 1:
            st.error("🚨 SPAM MESSAGE")
            st.write("This message has been classified as spam.")

        else:
            st.success("✅ HAM MESSAGE")
            st.write("This message appears to be legitimate.")


st.divider()

st.subheader("📊 Model Performance")

col1, col2 = st.columns(2)
col3, col4 = st.columns(2)

with col1:
    st.metric("Accuracy", f"{accuracy * 100:.2f}%")

with col2:
    st.metric("Precision", f"{precision * 100:.2f}%")

with col3:
    st.metric("Recall", f"{recall * 100:.2f}%")

with col4:
    st.metric("F1 Score", f"{f1 * 100:.2f}%")

st.caption("Model: Multinomial Naive Bayes | Features: TF-IDF")