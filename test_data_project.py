import pandas as pd
import pytest
from src.data_project import DataProject


def sample_df():
    return pd.DataFrame({
        "Order_ID": [1, 2, 3, 4],
        "Order_Date": ["2023-01-15", "2023-02-20", "2023-03-05", "2023-03-28"],
        "Customer_Age": [22, 34, 56, 41],
        "Customer_Gender": ["M", "F", "M", "F"],
        "Product_Category": ["A", "B", "A", "C"],
        "Sub_Category": ["a1", "b1", "a2", "c1"],
        "Product": ["p1", "p2", "p1", "p3"],
        "Quantity": [2, 1, 3, 4],
        "Unit_Price": [100, 150, 200, 50],
        "Revenue": [200, 150, 600, 200],
        "Profit": [20, 15, 60, 20]
    })


def test_preprocess_types(tmp_path):
    df = sample_df()
    path = tmp_path / "data.xlsx"
    df.to_excel(path, index=False)

    dp = DataProject()
    dp.load_from_excel(str(path))
    processed = dp.preprocess()

    assert pd.api.types.is_datetime64_any_dtype(processed["Order_Date"])
    assert "Age_Group" in processed.columns


def test_counts(tmp_path):
    df = sample_df()
    path = tmp_path / "data2.xlsx"
    df.to_excel(path, index=False)

    dp = DataProject()
    dp.load_from_excel(str(path))
    dp.preprocess()

    cat, sub, prod = dp.counts()
    assert cat == 3
    assert sub == 4
    assert prod == 3


def test_summary_statistics(tmp_path):
    df = sample_df()
    path = tmp_path / "data3.xlsx"
    df.to_excel(path, index=False)

    dp = DataProject()
    dp.load_from_excel(str(path))
    dp.preprocess()
    stats = dp.summary_statistics()

    assert "mean" in stats.columns
    assert "Quantity" in stats.index


def test_monthly_trends(tmp_path):
    df = sample_df()
    path = tmp_path / "data4.xlsx"
    df.to_excel(path, index=False)

    dp = DataProject()
    dp.load_from_excel(str(path))
    dp.preprocess()

    out = tmp_path / "trend.png"
    dp.plot_monthly_trends("2023-01", "2023-03", str(out))
    assert out.exists()
