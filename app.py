import streamlit as st
import pandas as pd

# -------------------------------
# PAGE CONFIGURATION
# -------------------------------

st.set_page_config(
    page_title="Amazon Review Analyzer",
    page_icon="🛒",
    layout="wide"
)

# -------------------------------
# LOAD DATASET
# -------------------------------

df = pd.read_csv("amazon_reviews.csv")

# Keep only the required columns
df = df[["SR.NO.", "PRODUCT", "REVIEW", "RATING"]]

# -------------------------------
# CLEAN RATING
# -------------------------------

df["RATING"] = pd.to_numeric(
    df["RATING"],
    errors="coerce"
)

# Remove rows where rating is missing
df = df.dropna(subset=["RATING"])

# -------------------------------
# SENTIMENT ANALYSIS
# -------------------------------

def get_sentiment(rating):

    if rating >= 4:
        return "Positive"

    elif rating == 3:
        return "Neutral"

    else:
        return "Negative"


df["Sentiment"] = df["RATING"].apply(get_sentiment)

# -------------------------------
# TITLE
# -------------------------------

st.title("🛒 Amazon Product Review Analyzer")

st.write(
    "Analyze Amazon customer reviews, ratings and sentiments."
)

# -------------------------------
# DASHBOARD
# -------------------------------

st.subheader("📊 Overall Dashboard")

total_reviews = len(df)

average_rating = df["RATING"].mean()

positive = (df["Sentiment"] == "Positive").sum()

neutral = (df["Sentiment"] == "Neutral").sum()

negative = (df["Sentiment"] == "Negative").sum()

positive_percent = positive / total_reviews * 100

neutral_percent = neutral / total_reviews * 100

negative_percent = negative / total_reviews * 100

# -------------------------------
# METRICS
# -------------------------------

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Reviews",
    total_reviews
)

col2.metric(
    "Average Rating",
    f"{average_rating:.2f} ⭐"
)

col3.metric(
    "Positive",
    f"{positive_percent:.1f}%"
)

col4.metric(
    "Negative",
    f"{negative_percent:.1f}%"
)

# -------------------------------
# RATING ANALYSIS
# -------------------------------

st.subheader("⭐ Rating Analysis")

rating_counts = df["RATING"].value_counts().sort_index()

st.bar_chart(rating_counts)

# -------------------------------
# SENTIMENT ANALYSIS
# -------------------------------

st.subheader("😊 Sentiment Analysis")

sentiment_counts = df["Sentiment"].value_counts()

st.bar_chart(sentiment_counts)

# -------------------------------
# PRODUCT ANALYSIS
# -------------------------------

st.subheader("🛍️ Product-wise Analysis")

product_counts = df["PRODUCT"].value_counts()

st.bar_chart(product_counts)

# -------------------------------
# CUSTOMER REVIEWS
# -------------------------------

st.subheader("📝 Customer Reviews")

st.dataframe(
    df,
    width="stretch"
)
