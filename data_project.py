# src/data_project.py
"""
Data Project Module implementing OOP and SOLID principles for sales data analysis.
All plotting functions accept outdir so they don't hardcode 'outputs/'.
"""
from __future__ import annotations
import os
import logging
from dataclasses import dataclass
from typing import Tuple, Optional, List

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
df = pd.read_excel(r"C:\Users\braha\OneDrive\Desktop\programs\Entrans\sales.xlsx", nrows=5)
print(df.columns.tolist())
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
sns.set()

@dataclass
class AnalysisConfig:
    age_bins: List[int] = (0, 18, 25, 35, 45, 60, 200)
    age_labels: List[str] = ("0-18", "19-25", "26-35", "36-45", "46-60", "61+")


class DataLoader:
    """Handles loading and saving data."""
    def __init__(self, file_path: str):
        self.file_path = file_path

    def load_excel(self) -> pd.DataFrame:
        """Loads Excel file into DataFrame."""
        logger.info("Loading Excel file: %s", self.file_path)
        return pd.read_excel(self.file_path, engine="openpyxl")

    def save_pickle(self, df: pd.DataFrame, output_path: str) -> None:
        """Saves DataFrame as pickle."""
        os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
        df.to_pickle(output_path)
        logger.info("Saved pickle: %s", output_path)


class DataPreprocessor:
    """Preprocess data: handle nulls, datatypes, compute Revenue/Profit defaults, and age groups."""
    def __init__(self, config: Optional[AnalysisConfig] = None):
        self.config = config or AnalysisConfig()

    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        df.columns = [str(c).strip() for c in df.columns]
        required = [
        "Date", "Customer_Age", "Customer_Gender", "Product_Category",
        "Sub_Category", "Product", "Order_Quantity", "Unit_Price", "Revenue"]
        missing = [c for c in required if c not in df.columns]
        if missing:
            raise KeyError(f"Missing required columns: {missing}")
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
        df["Customer_Age"] = pd.to_numeric(df["Customer_Age"], errors="coerce")
        df["Order_Quantity"] = pd.to_numeric(df["Order_Quantity"], errors="coerce").fillna(0).astype(int)
        df["Unit_Price"] = pd.to_numeric(df["Unit_Price"], errors="coerce").fillna(0.0)
        df["Revenue"] = pd.to_numeric(df["Revenue"], errors="coerce").fillna(df["Order_Quantity"] * df["Unit_Price"])
        if "Profit" not in df.columns:
            df["Profit"] = df["Revenue"] * 0.10
        else:
            df["Profit"] = pd.to_numeric(df["Profit"], errors="coerce").fillna(df["Revenue"] * 0.10)
        if "Age_Group" not in df.columns and "Customer_Age" in df.columns:
            df["Age_Group"] = pd.cut(
            df["Customer_Age"].fillna(-1),
            bins=list(self.config.age_bins),
            labels=list(self.config.age_labels),
            include_lowest=True
        )
        logger.info("✅ Data cleaned successfully with columns: %s", df.columns.tolist())
        return df


class DataAnalyzer:
    """Performs analysis and visualization."""
    def __init__(self, df: pd.DataFrame):
        self.df = df

    def summary_statistics(self) -> pd.DataFrame:
        return self.df.select_dtypes(include="number").agg(["mean", "median", "std", "min", "max"]).T

    def category_counts(self) -> Tuple[int, int, int]:
        return (int(self.df["Product_Category"].nunique()),
                int(self.df["Sub_Category"].nunique()),
                int(self.df["Product"].nunique()))

    def plot_histogram_age(self, outdir: str):
        os.makedirs(outdir, exist_ok=True)
        outpath = os.path.join(outdir, "customer_age_hist.png")
        plt.figure(figsize=(8, 5))
        sns.histplot(self.df["Customer_Age"].dropna(), kde=False, bins=15)
        plt.title("Customer Age Distribution")
        plt.xlabel("Age")
        plt.ylabel("Count")
        plt.tight_layout()
        plt.savefig(outpath)
        plt.close()
        logger.info("Saved histogram: %s", outpath)

    def profit_by_category(self, outdir: str):
        os.makedirs(outdir, exist_ok=True)
        outpath = os.path.join(outdir, "profit_by_category.png")
        profit_df = self.df.groupby('Product_Category')['Profit'].sum().sort_values()
        plt.figure(figsize=(8, 5))
        profit_df.plot(kind='barh')
        plt.title('Profit by Product Category')
        plt.xlabel('Profit')
        plt.tight_layout()
        plt.savefig(outpath)
        plt.close()
        logger.info("Saved profit-by-category plot: %s", outpath)

    def plot_gender_distribution(self, outdir: str):
        os.makedirs(outdir, exist_ok=True)
        outpath = os.path.join(outdir, "gender_distribution.png")
        counts = self.df["Customer_Gender"].value_counts()
        plt.figure(figsize=(6,6))
        counts.plot(kind="pie", autopct="%1.1f%%")
        plt.title("Gender Distribution")
        plt.ylabel("")
        plt.tight_layout()
        plt.savefig(outpath)
        plt.close()
        logger.info("Saved gender distribution: %s", outpath)

    def plot_agegroup_vs_revenue(self, outdir: str):
        os.makedirs(outdir, exist_ok=True)
        outpath = os.path.join(outdir, "agegroup_revenue.png")
        grp = self.df.groupby("Age_Group")["Revenue"].sum().reset_index()
        plt.figure(figsize=(8,5))
        sns.barplot(data=grp, x="Age_Group", y="Revenue")
        plt.title("Revenue by Age Group")
        plt.tight_layout()
        plt.savefig(outpath)
        plt.close()
        logger.info("Saved agegroup vs revenue: %s", outpath)

    def plot_monthly_trends(self, start: str, end: str, outdir: str):
        os.makedirs(outdir, exist_ok=True)
        outpath = os.path.join(outdir, "monthly_trends.png")
        df = self.df.dropna(subset=["Date"]).copy()
        df["YearMonth"] = df["Date"].dt.to_period("M").astype(str)
        mask = (df["YearMonth"] >= start) & (df["YearMonth"] <= end)
        df = df.loc[mask]
        if df.empty:
            logger.warning("No data found between %s and %s", start, end)
        grp = df.groupby("YearMonth")[["Revenue", "Profit"]].sum().reset_index()
        plt.figure(figsize=(10, 5))
        plt.plot(grp["YearMonth"], grp["Revenue"], marker="o", label="Revenue")
        plt.plot(grp["YearMonth"], grp["Profit"], marker="o", label="Profit")
        plt.xticks(rotation=45)
        plt.legend()
        plt.title(f"Monthly Revenue & Profit: {start} to {end}")
        plt.tight_layout()
        plt.savefig(outpath)
        plt.close()
        logger.info("Saved monthly trends: %s", outpath)


    def plot_profit_margin_scatter(self, outdir: str):
        os.makedirs(outdir, exist_ok=True)
        outpath = os.path.join(outdir, "profit_margin_scatter.png")
        df = self.df.copy()
        df["Profit_Margin"] = df["Profit"] / df["Revenue"].replace({0: pd.NA})
        res = df.groupby("Product")["Profit_Margin"].mean().reset_index()
        plt.figure(figsize=(10,5))
        sns.scatterplot(data=res, x="Product", y="Profit_Margin")
        plt.xticks(rotation=90)
        plt.title("Average Profit Margin per Product")
        plt.tight_layout()
        plt.savefig(outpath)
        plt.close()
        logger.info("Saved profit margin scatter: %s", outpath)
