# Sales Data Analysis (Python OOP + SOLID)

## Overview
A Python project that performs data preprocessing, analysis, and visualization on sales data using **OOP** principles and **SOLID** design.

### Key Features
- Load and preprocess Excel sales data using pandas
- Generate visualizations (histogram, bar chart, pie chart, line plot, scatter plot)
- Save preprocessed data as a pickle
- Unit tests for core functionalities
- Follows best practices (naming, docstrings, type hints)

---

## Tasks Implemented
1. Import data from Excel → DataFrame  
2. Preprocess (nulls, data types)  
3. Save as Pickle  
4. Analyze and visualize using Seaborn/Matplotlib  

### Analysis Includes
- (a) Summary statistics  
- (b) Product category/sub-category/product counts  
- (c) Histogram for customer age  
- (d) Box plots for revenue across age groups (optional extension)  
- (e) Pie chart for gender distribution  
- (f) Revenue by age group  
- (g) Profit by product category  
- (h) Monthly revenue and profit trend (user input)  
- (i) Profit margin scatter plot per product  

---

## Run Instructions
```bash
# 1. Create virtual environment
python -m venv venv
source venv/bin/activate     # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run analysis
python run_analysis.py --file path/to/sales.xlsx --outdir outputs

# 4. Run tests
pytest -q
