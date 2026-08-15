import streamlit as st
import pandas as pd

# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="Amazon Review Analyzer",
    page_icon="🛒",
    layout="wide"
)

# ==================================================
# CUSTOM CSS
# ==================================================

st.markdown("""
<style>

.main {
    background-color: #f8f9fa;
}

.title {
    font-size: 42px;
    font-weight: 700;
    text-align: center;
    margin-bottom: 5px;
}

.subtitle {
    text-align: center;
    font-size: 18px;
    color: #666;
    margin-bottom: 30px;
}

.section {
    font-size: 25px;
    font-weight: 600;
    margin-top: 30px;
    margin-bottom: 15px;
}

</style>
""", unsafe_allow_html=True)

# ==================================================
# LOAD DATASET
# ==================================================

raw = pd.read_csv("amazon_reviews.csv")

# ==================================================
# FIX CSV STRUCTURE
# ==================================================

columns = list(raw.columns)

rating_columns = columns[3:]

clean_data = []

for _, row in raw.iterrows():

    sr_no = row[columns[0]]
    product = row[columns[1]]

    rating = None

    for col in rating_columns:

        value = str(row[col]).strip()

        if value in ["1", "2", "3", "4", "5"]:
            rating = int(value)
            break

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

df = pd.DataFrame(
    clean_data,
    columns=["SR.NO.", "PRODUCT", "REVIEW", "RATING"]
)

# Remove invalid ratings
df = df.dropna(subset=["RATING"])

df["RATING"] = pd.to_numeric(df["RATING"])

# ==================================================
# SENTIMENT ANALYSIS
# ==================================================

def get_sentiment(rating):

    if rating >= 4:
        return "Positive"

    elif rating == 3:
        return "Neutral"

    else:
        return "Negative"


df["Sentiment"] = df["RATING"].apply(get_sentiment)

# ==================================================
# HEADER
# ==================================================

st.markdown(
    '<div class="title">🛒 Amazon Product Review Analyzer</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Analyze customer reviews, ratings and sentiments</div>',
    unsafe_allow_html=True
)

st.divider()

# ==================================================
# SIDEBAR
# ==================================================

st.sidebar.title("🔍 Filters")

products = ["All Products"] + sorted(
    df["PRODUCT"].unique().tolist()
)

selected_product = st.sidebar.selectbox(
    "Select Product",
    products
)

if selected_product != "All Products":

    filtered_df = df[
        df["PRODUCT"] == selected_product
    ]

else:

    filtered_df = df.copy()

st.sidebar.info(
    "Use the filter to analyze reviews for a specific product."
)

# ==================================================
# DASHBOARD
# ==================================================

st.markdown(
    '<div class="section">📊 Overall Dashboard</div>',
    unsafe_allow_html=True
)

total_reviews = len(filtered_df)

average_rating = filtered_df["RATING"].mean()

positive = (
    filtered_df["Sentiment"] == "Positive"
).sum()

neutral = (
    filtered_df["Sentiment"] == "Neutral"
).sum()

negative = (
    filtered_df["Sentiment"] == "Negative"
).sum()

if total_reviews > 0:

    positive_percent = positive / total_reviews * 100
    neutral_percent = neutral / total_reviews * 100
    negative_percent = negative / total_reviews * 100

else:

    positive_percent = 0
    neutral_percent = 0
    negative_percent = 0

# ==================================================
# METRICS
# ==================================================

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric(
    "📝 Total Reviews",
    total_reviews
)

col2.metric(
    "⭐ Average Rating",
    f"{average_rating:.2f}"
)

col3.metric(
    "😊 Positive",
    f"{positive_percent:.1f}%"
)

col4.metric(
    "😐 Neutral",
    f"{neutral_percent:.1f}%"
)

col5.metric(
    "😞 Negative",
    f"{negative_percent:.1f}%"
)

st.divider()

# ==================================================
# CHARTS
# ==================================================

chart1, chart2 = st.columns(2)

with chart1:

    st.markdown(
        "### ⭐ Rating Distribution"
    )

    rating_counts = (
        filtered_df["RATING"]
        .value_counts()
        .sort_index()
    )

    st.bar_chart(rating_counts)

with chart2:

    st.markdown(
        "### 😊 Sentiment Distribution"
    )

    sentiment_counts = (
        filtered_df["Sentiment"]
        .value_counts()
    )

    st.bar_chart(sentiment_counts)

# ==================================================
# PRODUCT ANALYSIS
# ==================================================

st.markdown(
    '<div class="section">🛍️ Product-wise Analysis</div>',
    unsafe_allow_html=True
)

product_counts = (
    filtered_df["PRODUCT"]
    .value_counts()
)

st.bar_chart(product_counts)

# ==================================================
# AVERAGE RATING BY PRODUCT
# ==================================================

st.markdown(
    "### ⭐ Average Rating by Product"
)

product_rating = (
    filtered_df
    .groupby("PRODUCT")["RATING"]
    .mean()
    .sort_values(ascending=False)
)

st.bar_chart(product_rating)

# ==================================================
# CUSTOMER REVIEWS
# ==================================================

st.markdown(
    '<div class="section">📝 Customer Reviews</div>',
    unsafe_allow_html=True
)

display_df = filtered_df[
    ["PRODUCT", "REVIEW", "RATING", "Sentiment"]
]

st.dataframe(
    display_df,
    width="stretch",
    hide_index=True
)

# ==================================================
# DOWNLOAD DATASET
# ==================================================

st.markdown(
    '<div class="section">📥 Download Data</div>',
    unsafe_allow_html=True
)

csv_data = filtered_df.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    label="📥 Download Cleaned Dataset",
    data=csv_data,
    file_name="amazon_reviews_cleaned.csv",
    mime="text/csv"
)

# ==================================================
# PROJECT INFORMATION
# ==================================================

st.divider()

with st.expander("ℹ️ About This Project"):

    st.write(
        """
        **Amazon Product Review Analyzer**

        This mini project analyzes Amazon customer reviews
        using Python and Pandas.

        **Features:**
        - Review and rating analysis
        - Sentiment classification
        - Product-wise analysis
        - Rating distribution
        - Interactive product filtering
        - Cleaned dataset download

        **Sentiment Rules:**
        - ⭐ 4–5 → Positive
        - ⭐ 3 → Neutral
        - ⭐ 1–2 → Negative
        """
    )

st.caption(
    "Amazon Product Review Analyzer • Mini Project"
)
