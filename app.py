import streamlit as st
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import joblib

# --- Load data and models once and cache them for speed ---
@st.cache_data(show_spinner=True)
def load_retail_data():
    df = pd.read_csv("online_retail.csv")
    # Prepare customer-product matrix for similarity calculation
    customer_product = df.pivot_table(
        index='CustomerID',
        columns='Description',
        values='Quantity',
        aggfunc='sum'
    ).fillna(0)
    product_matrix = customer_product.T
    similarity = cosine_similarity(product_matrix)
    sim_df = pd.DataFrame(similarity, index=product_matrix.index, columns=product_matrix.index)
    product_list = sorted(product_matrix.index.tolist())
    return sim_df, product_list

@st.cache_resource(show_spinner=True)
def load_models():
    scaler = joblib.load("scaler.joblib")
    kmeans = joblib.load("kmeans.joblib")
    return scaler, kmeans

# Load data and models
product_similarity_df, product_list = load_retail_data()
scaler, kmeans = load_models()

# Map cluster index to segment label
cluster_labels = {
    0: 'High-Value',
    1: 'Regular',
    2: 'Occasional',
    3: 'At-Risk'
}

# Set page config
st.set_page_config(page_title="Shopper Spectrum", layout="wide")

# Custom CSS for dark mode with black background and light text
page_bg = """
<style>
    /* Page background */
    .reportview-container, .main .block-container {
        background-color: #000000;
        color: #FFFFFF;
    }
    /* Header and text colors */
    h1, h2, h3, h4, h5, h6, p, span, label {
        color: #FFFFFF;
    }
    /* Sidebar */
    .css-1d391kg, .css-1v3fvcr {
        background-color: #121212;
        color: white;
    }
    /* Buttons text */
    div.stButton > button {
        color: white;
        background-color: #212121;
        border: 1px solid #444444;
    }
    /* Cards styling */
    .recommendation-card {
        border: 1px solid #555555;
        padding: 15px;
        margin-bottom: 15px;
        border-radius: 8px;
        background-color: #1a1a1a;
        box-shadow: 2px 2px 8px rgba(255, 255, 255, 0.1);
        font-size: 16px;
        color: #ffffff;
    }
    /* Selectbox text */
    div[role="listbox"] > div {
        background-color: #121212 !important;
        color: #fff !important;
    }
    /* Number input and other inputs */
    input, textarea {
        background-color: #1a1a1a !important;
        color: #fff !important;
        border: 1px solid #555 !important;
    }
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

st.title("🛒 Shopper Spectrum: Product Recommendation & Customer Segmentation")

menu = st.sidebar.selectbox("Choose Module", ["Product Recommendation", "Customer Segmentation"])

if menu == "Product Recommendation":
    st.header("Product Recommendation")

    product_input = st.selectbox("Select a product:", product_list)

    if st.button("Get Recommendations"):
        if not product_input:
            st.warning("Please select a product.")
        else:
            sim_scores = product_similarity_df.loc[product_input].sort_values(ascending=False)
            recommendations = sim_scores.iloc[1:6].index.tolist()

            st.subheader(f"Top 5 Similar Products to '{product_input}':")
            for i, prod in enumerate(recommendations, 1):
                st.markdown(f"""
                    <div class="recommendation-card">
                        <strong>{i}. {prod}</strong>
                    </div>
                    """, unsafe_allow_html=True)

elif menu == "Customer Segmentation":
    st.header("Customer Segmentation")

    recency = st.number_input("Recency (days since last purchase):", min_value=0, value=30)
    frequency = st.number_input("Frequency (# of purchases):", min_value=0, value=5)
    monetary = st.number_input("Monetary (total spend):", min_value=0.0, value=100.0, format="%.2f")

    if st.button("Predict Cluster"):
        input_data = np.array([[recency, frequency, monetary]])
        scaled = scaler.transform(input_data)
        cluster = kmeans.predict(scaled)[0]
        label = cluster_labels.get(cluster, f"Cluster {cluster}")
        st.success(f"Predicted Customer Segment: **{label}**")
