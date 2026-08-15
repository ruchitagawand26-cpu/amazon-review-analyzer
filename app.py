import streamlit as st
import pandas as pd
import string
# Load dataset
df = pd.read_csv("amazon_reviews.csv")

# Page configuration
st.set_page_config(
    page_title="Amazon Review Analyzer",
    page_icon="🛒",
    layout="wide"
)

# Title
st.title("Amazon Product Review Analyzer")
st.write("Analyze Amazon customer reviews, ratings and sentiments.")

# Create sentiment column
def get_sentiment(rating):
    if rating >= 4:
        return "Positive"
    elif rating == 3:
        return "Neutral"
    else:
        return "Negative"

df["RATING"] = pd.to_numeric(df["RATING"], errors="coerce")
df["Sentiment"] = df["RATING"].apply(get_sentiment)

# Dashboard
st.subheader("Overall Dashboard")

total_reviews = len(df)
average_rating = df["RATING"].mean()

positive = (df["Sentiment"] == "Positive").sum()
neutral = (df["Sentiment"] == "Neutral").sum()
negative = (df["Sentiment"] == "Negative").sum()

positive_percent = positive / total_reviews * 100
neutral_percent = neutral / total_reviews * 100
negative_percent = negative / total_reviews * 100

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Reviews", total_reviews)
col2.metric("Average Rating", f"{average_rating:.2f} ⭐")
col3.metric("Positive", f"{positive_percent:.1f}%")
col4.metric("Negative", f"{negative_percent:.1f}%")
