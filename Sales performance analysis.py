import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error

# -----------------------------
# Utility Functions
# -----------------------------

def load_data(filepath):
    print("[INFO] Loading data from:", filepath)
    df = pd.read_csv(filepath)
    print("[INFO] Data loaded successfully. Shape:", df.shape)
    return df

def validate_data(df):
    print("[INFO] Validating dataset...")

    required_columns = ["Date", "Product", "Region", "Quantity", "Price"]
    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"[ERROR] Missing required column: {col}")

    print("[INFO] All required columns are present.")

    print("[INFO] Checking for missing values...")
    print(df.isnull().sum())

    return True

def preprocess_data(df):
    print("[INFO] Preprocessing data...")

    df = df.copy()

    # Convert Date column
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    # Drop rows with invalid dates
    df = df.dropna(subset=["Date"])

    # Handle missing numeric values
    df["Quantity"] = df["Quantity"].fillna(0)
    df["Price"] = df["Price"].fillna(0)

    # Ensure numeric types
    df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce").fillna(0)
    df["Price"] = pd.to_numeric(df["Price"], errors="coerce").fillna(0)

    # Feature Engineering
    df["Sales"] = df["Quantity"] * df["Price"]
    df["Year"] = df["Date"].dt.year
    df["Month"] = df["Date"].dt.month
    df["Month_Name"] = df["Date"].dt.strftime("%b")

    print("[INFO] Preprocessing completed. Shape:", df.shape)
    return df

# -----------------------------
# KPI Calculations
# -----------------------------

def calculate_kpis(df):
    print("[INFO] Calculating KPIs...")

    total_sales = df["Sales"].sum()
    total_orders = len(df)
    avg_order_value = df["Sales"].mean()

    kpis = {
        "Total Sales": total_sales,
        "Total Orders": total_orders,
        "Average Order Value": avg_order_value
    }

    for k, v in kpis.items():
        print(f"[KPI] {k}: {v:.2f}")

    return kpis

# -----------------------------
# Performance Analysis
# -----------------------------

def sales_by_product(df):
    result = df.groupby("Product")["Sales"].sum().sort_values(ascending=False)
    print("\n[INFO] Sales by Product:")
    print(result)
    return result

def sales_by_region(df):
    result = df.groupby("Region")["Sales"].sum().sort_values(ascending=False)
    print("\n[INFO] Sales by Region:")
    print(result)
    return result

def monthly_sales_trend(df):
    df["YearMonth"] = df["Date"].dt.to_period("M")
    trend = df.groupby("YearMonth")["Sales"].sum()
    print("\n[INFO] Monthly Sales Trend:")
    print(trend)
    return trend

# -----------------------------
# Visualization Functions
# -----------------------------

def plot_bar(series, title, xlabel, ylabel):
    plt.figure()
    series.plot(kind="bar")
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.tight_layout()
    plt.show()

def plot_line(series, title, xlabel, ylabel):
    plt.figure()
    series.plot()
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.tight_layout()
    plt.show()

# -----------------------------
# Product Performance Scoring
# -----------------------------

def product_performance_score(df):
    print("\n[INFO] Calculating product performance scores...")

    summary = df.groupby("Product").agg({
        "Sales": "sum",
        "Quantity": "sum"
    })

    # Normalize scores
    summary["Sales_Score"] = (summary["Sales"] - summary["Sales"].min()) / (summary["Sales"].max() - summary["Sales"].min())
    summary["Quantity_Score"] = (summary["Quantity"] - summary["Quantity"].min()) / (summary["Quantity"].max() - summary["Quantity"].min())

    summary["Performance_Score"] = 0.7 * summary["Sales_Score"] + 0.3 * summary["Quantity_Score"]

    summary = summary.sort_values("Performance_Score", ascending=False)

    print(summary)
    return summary

# -----------------------------
# Simple Sales Forecasting
# -----------------------------

def forecast_sales(monthly_sales):
    print("\n[INFO] Performing simple sales forecasting using Linear Regression...")

    # Prepare data
    y = monthly_sales.values
    X = np.arange(len(y)).reshape(-1, 1)

    model = LinearRegression()
    model.fit(X, y)

    # Predict next 3 periods
    future_X = np.arange(len(y), len(y) + 3).reshape(-1, 1)
    future_predictions = model.predict(future_X)

    print("[INFO] Forecast for next 3 periods:", future_predictions)

    # Plot
    plt.figure()
    plt.plot(X.flatten(), y, label="Historical Sales")
    plt.plot(future_X.flatten(), future_predictions, label="Forecast", linestyle="--")
    plt.title("Sales Forecast")
    plt.xlabel("Time Index")
    plt.ylabel("Sales")
    plt.legend()
    plt.tight_layout()
    plt.show()

    return future_predictions

# -----------------------------
# Main Pipeline
# -----------------------------

def main():
    print("======================================")
    print("   SALES PERFORMANCE ANALYSIS PIPELINE ")
    print("======================================\n")

    # Step 1: Load Data
    df = load_data("sales_data.csv")

    # Step 2: Validate Data
    validate_data(df)

    # Step 3: Preprocess Data
    df = preprocess_data(df)

    # Step 4: KPI Calculation
    calculate_kpis(df)

    # Step 5: Performance Analysis
    product_sales = sales_by_product(df)
    region_sales = sales_by_region(df)
    monthly_trend = monthly_sales_trend(df)

    # Step 6: Visualizations
    plot_bar(product_sales, "Sales by Product", "Product", "Total Sales")
    plot_bar(region_sales, "Sales by Region", "Region", "Total Sales")
    plot_line(monthly_trend, "Monthly Sales Trend", "Month", "Total Sales")

    # Step 7: Product Performance Scoring
    performance_table = product_performance_score(df)

    # Step 8: Forecasting
    forecast_sales(monthly_trend)

    print("\n[INFO] Analysis completed successfully!")

# Entry Point
if __name__ == "__main__":
    main()
