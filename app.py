import streamlit as st
import pandas as pd

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Amazon Review Analyzer",
    page_icon="🛒",
    layout="wide"
)

# --------------------------------------------------
# LOAD CSV
# --------------------------------------------------

raw = pd.read_csv("amazon_reviews.csv")

# --------------------------------------------------
# FIX THE BROKEN CSV STRUCTURE
# --------------------------------------------------

# Get the original columns
columns = list(raw.columns)

# First 3 columns are:
# SR.NO. | PRODUCT | REVIEW
base_columns = columns[:3]

# All remaining columns may contain the rating
rating_columns = columns[3:]

clean_data = []

for _, row in raw.iterrows():

    sr_no = row[columns[0]]
    product = row[columns[1]]

    # Find the rating from all columns after PRODUCT
    rating = None
    rating_position = None

    for i, col in enumerate(rating_columns):

        value = str(row[col]).strip()

        if value in ["1", "2", "3", "4", "5"]:
            rating = int(value)
            rating_position = i
            break

    # Collect review text
    review_parts = []

    for col in columns[2:]:
        value = str(row[col]).strip()

        if value == "nan":
            continue

        if value in ["1", "2", "3", "4", "5"]:
            break

        review_parts.append(value)

    review = " ".join(review_parts)

    clean_data.append([
        sr_no,
        product,
        review,
        rating
    ])

# Create clean dataframe
df = pd.DataFrame(
    clean_data,
    columns=["SR.NO.", "PRODUCT", "REVIEW", "RATING"]
)

# Remove rows without ratings
df = df.dropna(subset=["RATING"])

# Make sure ratings are numbers
df["RATING"] = pd.to_numeric(df["RATING"])

# --------------------------------------------------
# SENTIMENT ANALYSIS
# --------------------------------------------------

def get_sentiment(rating):

    if rating >= 4:
        return "Positive"

    elif rating == 3:
        return "Neutral"

    else:
        return "Negative"


df["Sentiment"] = df["RATING"].apply(get_sentiment)

# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title("🛒 Amazon Product Review Analyzer")

st.write(
    "Analyze Amazon customer reviews, ratings and sentiments."
)

# --------------------------------------------------
# OVERALL DASHBOARD
# --------------------------------------------------

st.subheader("📊 Overall Dashboard")

total_reviews = len(df)

average_rating = df["RATING"].mean()

positive = (df["Sentiment"] == "Positive").sum()

neutral = (df["Sentiment"] == "Neutral").sum()

negative = (df["Sentiment"] == "Negative").sum()

positive_percent = positive / total_reviews * 100

neutral_percent = neutral / total_reviews * 100

negative_percent = negative / total_reviews * 100

# --------------------------------------------------
# METRICS
# --------------------------------------------------

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

# --------------------------------------------------
# RATING ANALYSIS
# --------------------------------------------------

st.subheader("⭐ Rating Analysis")

rating_counts = (
    df["RATING"]
    .value_counts()
    .sort_index()
)

st.bar_chart(rating_counts)

# --------------------------------------------------
# SENTIMENT ANALYSIS
# --------------------------------------------------

st.subheader("😊 Sentiment Analysis")

sentiment_counts = df["Sentiment"].value_counts()

st.bar_chart(sentiment_counts)

# --------------------------------------------------
# PRODUCT ANALYSIS
# --------------------------------------------------

st.subheader("🛍️ Product-wise Analysis")

product_counts = df["PRODUCT"].value_counts()

st.bar_chart(product_counts)

# --------------------------------------------------
# CUSTOMER REVIEWS
# --------------------------------------------------

st.subheader("📝 Customer Reviews")

st.dataframe(
    df,
    width="stretch"
)
