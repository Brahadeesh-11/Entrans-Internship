# run_analysis.py
"""
Runner script for Sales Data Analysis Project.
Usage:
    python run_analysis.py --file path/to/sales.xlsx --outdir outputs
"""
import argparse
import sys
import os

# Ensure project root is on sys.path so `src` imports work when running this script directly.
HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

from src.data_project import DataLoader, DataPreprocessor, DataAnalyzer

def main(file: str, outdir: str):
    os.makedirs(outdir, exist_ok=True)

    loader = DataLoader(file)
    try:
        df = loader.load_excel()
    except FileNotFoundError:
        print(f"ERROR: File not found: {file}")
        raise
    except Exception as e:
        print(f"ERROR: Could not read Excel file: {e}")
        raise

    pre = DataPreprocessor()
    try:
        df_clean = pre.clean_data(df)
    except KeyError as ke:
        print("ERROR: Required columns missing:", ke)
        raise
    except Exception as e:
        print("ERROR during preprocessing:", e)
        raise

    pickle_path = os.path.join(outdir, "sales_data.pkl")
    loader.save_pickle(df_clean, pickle_path)
    print(f"✅ Data saved as pickle at: {pickle_path}")

    analyzer = DataAnalyzer(df_clean)

    print("\n📊 Summary Statistics:")
    print(analyzer.summary_statistics().to_string())

    # Plots (all saved to outdir)
    analyzer.plot_histogram_age(outdir)
    analyzer.profit_by_category(outdir)
    analyzer.plot_gender_distribution(outdir)
    analyzer.plot_agegroup_vs_revenue(outdir)
    analyzer.plot_profit_margin_scatter(outdir)

    # Monthly trends - request start/end from user (or skip if not interactive)
    try:
        start = input("Enter start (YYYY-MM) or press Enter to skip: ").strip()
        if start:
            end = input("Enter end (YYYY-MM): ").strip()
            analyzer.plot_monthly_trends(start, end, outdir)
    except KeyboardInterrupt:
        print("\nSkipping monthly trends (interrupted).")

    print(f"\nAll outputs saved to: {os.path.abspath(outdir)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Sales Data Analysis Project")
    parser.add_argument("--file", required=True, help="Path to sales Excel file")
    parser.add_argument("--outdir", default="outputs", help="Directory to save results")
    args = parser.parse_args()
    main(args.file, args.outdir)
