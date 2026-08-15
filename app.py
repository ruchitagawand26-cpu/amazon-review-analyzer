import streamlit as st
import pandas as pd
import string

# Load analyzed dataset
df = pd.read_csv("amazon_reviews.csv")

# Page configuration
st.set_page_config(
    page_title="Amazon Review Analyzer",
    page_icon="🛒",
    layout="wide"
)

# Title
st.title("🛒 Amazon Product Review Analyzer")
st.write("Analyze Amazon customer reviews, ratings and sentiments.")

# ---------------- DASHBOARD ----------------

st.subheader("📊 Overall Dashboard")

total_reviews = len(df)
df["RATING"] = pd.to_numeric(df["RATING"],errors="coerce")
average_rating = df["RATING"].mean()

positive = (df["sentiment"] == "Positive").sum()
neutral = (df["sentiment"] == "Neutral").sum()
negative = (df["sentiment"] == "Negative").sum()

positive_percent = positive / total_reviews * 100
neutral_percent = neutral / total_reviews * 100
negative_percent = negative / total_reviews * 100

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Reviews", total_reviews)
col2.metric("Average Rating", f"{average_rating:.2f} ⭐")
col3.metric("Positive", f"{positive_percent:.1f}% 😊")
col4.metric("Negative", f"{negative_percent:.1f}% 😞")

# ---------------- SENTIMENT CHART ----------------

st.subheader("📈 sentiment Distribution")

sentiment_counts = df["sentiment"].value_counts()

st.bar_chart(sentiment_counts)

# ---------------- PRODUCT ANALYSIS ----------------

st.subheader("🛍️ Product Analysis")

product_rating = df.groupby("Product")["Rating"].mean()

st.write("Average Rating by Product")

st.bar_chart(product_rating)

# ---------------- REVIEW ANALYZER ----------------

st.subheader("🔍 Analyze Your Own Review")

review = st.text_area(
    "Enter an Amazon review:",
    placeholder="Example: The product is excellent and I am very happy with it!"
)

if st.button("Analyze Review"):

    if review.strip() == "":
        st.warning("Please enter a review first.")

    else:
        # Clean the review
        clean_review = review.lower()
        clean_review = clean_review.translate(
            str.maketrans("", "", string.punctuation)
        )

        # Simple keyword-based sentiment
        positive_words = [
            "good", "great", "excellent", "amazing",
            "love", "best", "happy", "perfect",
            "awesome", "nice", "satisfied"
        ]

        negative_words = [
            "bad", "worst", "poor", "terrible",
            "hate", "awful", "disappointed",
            "waste", "broken", "useless"
        ]

        words = clean_review.split()

        positive_score = sum(word in positive_words for word in words)
        negative_score = sum(word in negative_words for word in words)

        if positive_score > negative_score:
            sentiment = "Positive"
            st.success("😊 Positive Review")

        elif negative_score > positive_score:
            sentiment = "Negative"
            st.error("😞 Negative Review")

        else:
            sentiment = "Neutral"
            st.info("😐 Neutral Review")

        st.write("**Your Review:**", review)
        st.write("**Predicted Sentiment:**", sentiment)

# ---------------- PRODUCT SELECTOR ----------------

st.subheader("📋 View Product Reviews")

selected_product = st.selectbox(
    "Select a product:",
    df["PRODUCT"].unique()
)

product_data = df[df["PRODUCT"] == selected_product]

st.dataframe(
    product_data[["Review", "Rating", "Sentiment"]],
    width="stretch"
)
