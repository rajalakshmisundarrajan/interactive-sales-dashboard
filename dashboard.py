# ================================
# 📊 Interactive Sales Dashboard
# ================================

import os
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

# -------------------------------
# ⚙️ CONFIGURATION
# -------------------------------
DATA_PATH = "sales_data.csv"
OUTPUT_DIR = "visualizations"

sns.set_style("whitegrid")
sns.set_palette("Set2")

# -------------------------------
# 📁 CREATE OUTPUT FOLDER
# -------------------------------
def create_output_dir():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)


# -------------------------------
# 📥 LOAD DATA
# -------------------------------
def load_data(path):
    try:
        df = pd.read_csv(path)
        print("✅ Data loaded successfully")
        return df
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        exit()


# -------------------------------
# 🧹 DATA CLEANING
# -------------------------------
def preprocess_data(df):
    df = df.copy()

    # Drop missing values
    df.dropna(inplace=True)

    # Convert Date column
    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'])

    # Feature engineering
    if 'Date' in df.columns:
        df['Month'] = df['Date'].dt.to_period('M').astype(str)

    print("✅ Data preprocessing completed")
    return df


# -------------------------------
# 📈 SALES TREND (LINE PLOT)
# -------------------------------
def plot_sales_trend(df):
    if 'Month' not in df.columns:
        return

    monthly_sales = df.groupby('Month')['Total_Sales'].sum().reset_index()

    plt.figure(figsize=(10, 5))
    sns.lineplot(data=monthly_sales, x='Month', y='Total_Sales', marker='o')
    plt.xticks(rotation=45)
    plt.title("Monthly Sales Trend")

    path = os.path.join(OUTPUT_DIR, "sales_trend.png")
    plt.savefig(path, bbox_inches='tight')
    plt.close()

    print("📈 Sales trend saved")


# -------------------------------
# 📊 CATEGORY PERFORMANCE (BAR)
# -------------------------------
def plot_category_performance(df):
    if 'Product' not in df.columns:
        return

    plt.figure(figsize=(8, 5))
    sns.barplot(data=df, x='Product', y='Total_Sales', estimator=sum)
    plt.title("Sales by Product")

    path = os.path.join(OUTPUT_DIR, "category_sales.png")
    plt.savefig(path, bbox_inches='tight')
    plt.close()

    print("📊 Category performance saved")


# -------------------------------
# 📦 PRICE DISTRIBUTION (BOX)
# -------------------------------
def plot_price_distribution(df):
    if 'Product' not in df.columns or 'Price' not in df.columns:
        return

    plt.figure(figsize=(8, 5))
    sns.boxplot(x='Product', y='Price', data=df)
    plt.title("Price Distribution by Product")

    path = os.path.join(OUTPUT_DIR, "price_distribution.png")
    plt.savefig(path, bbox_inches='tight')
    plt.close()

    print("📦 Price distribution saved")


# -------------------------------
# 🔥 CORRELATION HEATMAP
# -------------------------------
def plot_correlation_heatmap(df):
    numeric_df = df.select_dtypes(include=np.number)

    if numeric_df.empty:
        return

    plt.figure(figsize=(8, 6))
    sns.heatmap(numeric_df.corr(), annot=True)
    plt.title("Feature Correlation Heatmap")

    path = os.path.join(OUTPUT_DIR, "correlation_heatmap.png")
    plt.savefig(path, bbox_inches='tight')
    plt.close()

    print("🔥 Heatmap saved")


# -------------------------------
# ✨ INTERACTIVE PLOT (PLOTLY)
# -------------------------------
def interactive_scatter(df):
    required_cols = {'Total_Sales', 'Price', 'Product'}
    if not required_cols.issubset(df.columns):
        return

    fig = px.scatter(
        df,
        x='Total_Sales',
        y='Price',
        color='Product',
        size='Quantity' if 'Quantity' in df.columns else None,
        hover_data=df.columns
    )

    fig.write_html(os.path.join(OUTPUT_DIR, "interactive_scatter.html"))
    print("✨ Interactive chart saved")


# -------------------------------
# 🧠 MAIN FUNCTION
# -------------------------------
def main():
    print("🚀 Starting Sales Dashboard...")

    create_output_dir()

    df = load_data(DATA_PATH)
    df = preprocess_data(df)

    plot_sales_trend(df)
    plot_category_performance(df)
    plot_price_distribution(df)
    plot_correlation_heatmap(df)
    interactive_scatter(df)

    print("🎯 Dashboard generation completed!")


# -------------------------------
# ▶️ ENTRY POINT
# -------------------------------
if __name__ == "__main__":
    main()