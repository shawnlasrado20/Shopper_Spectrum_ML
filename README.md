
# Shopper Spectrum: Customer Segmentation and Product Recommendations in E-Commerce

## Project Overview

**Shopper Spectrum** is an interactive data science project that analyzes e-commerce transaction data to segment customers based on their Recency, Frequency, and Monetary (RFM) purchasing behavior, and recommends products through an item-based collaborative filtering recommendation system.

This project provides:
- Data preprocessing and exploratory analysis
- Customer segmentation using KMeans clustering
- Product recommendation using cosine similarity
- A Streamlit web app to interactively get customer clusters and product recommendations


## Prerequisites

- Python 3.10+ installed on your machine
- [pip](https://pip.pypa.io/en/stable/installation/) package manager
- *(Optional but recommended)* A Python virtual environment tool such as `venv`

## Setup Instructions

### 1. Clone the repository

git clone https://github.com/your-username/ShopperSpectrum.git
cd ShopperSpectrum

### 2. Create and activate a virtual environment (optional but recommended)

On macOS/Linux:
python3 -m venv venv
source venv/bin/activate


On Windows:
python -m venv venv
venv\Scripts\activate

### 3. Install required packages

pip install -r requirements.txt


*If `requirements.txt` is missing, install packages manually:*

pip install streamlit pandas numpy scikit-learn joblib matplotlib seaborn


### 4. Prepare scaler and clustering models (if pre-saved models are not provided)

If you don’t have `scaler.joblib` and `kmeans.joblib`, run the training script to create them:

python train_model.py

*This script preprocesses the data, trains the scaler and KMeans models, then saves them for the app to use.*

### 5. Run the Streamlit App

Run the web app using:

streamlit run app.py

Your default web browser will open automatically showing the interactive Shopper Spectrum app with:

- **Product Recommendation:** Select a product to get the top 5 similar products recommended.
- **Customer Segmentation:** Input Recency, Frequency, and Monetary values to predict the customer segment.

## How to Use the Streamlit App

On loading, use the sidebar to select:

- **Product Recommendation:**  
  Choose a product from the dropdown to get item-based collaborative filtering recommendations.

- **Customer Segmentation:**  
  Enter RFM values manually and click **Predict Cluster** to see which customer segment you belong to.
