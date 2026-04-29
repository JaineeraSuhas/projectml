# IDCFSS Data Cleaning Configuration Guide

Welcome to the **Intelligent Data Cleaning & Feature Selection System (IDCFSS)**. If you've just uploaded a dataset and feel a bit lost about what happens next, this guide will walk you through the entire pipeline step-by-step.

## 1. What Happens After Inserting the Dataset?

Once you upload your CSV or Excel file, the system immediately gets to work behind the scenes:
1. **Data Profiling**: The backend analyzes your dataset to understand its shape (rows and columns) and calculates critical statistics.
2. **Health Check**: It scans for missing values (nulls/empty cells), detects potential outliers (anomalies), and identifies the data types of each column (e.g., numerical vs. categorical text).
3. **Report Generation**: The frontend then displays a summary of your data's health, telling you exactly which columns need attention before you can use the data for machine learning.

From here, you enter the **Data Cleaning Pipeline**, moving step-by-step through different cleaning configurations.

---

## 2. Understanding Each Cleaning Feature

Here is a breakdown of every feature available in the cleaning pipeline and why you need it:

### A. Missing Value Handling (Imputation)
Real-world data is rarely perfect; it often has blanks or missing entries. Machine learning models cannot process missing data.
*   **Drop Rows**: Completely deletes any row that has a missing value. Best used when you have plenty of data and very few missing values.
*   **Mean/Median/Mode Imputation**: Fills missing numerical values with the average (Mean), middle value (Median), or most frequent value (Mode) of that column.
*   **KNN Imputation**: Uses an algorithm (K-Nearest Neighbors) to guess the missing value based on other similar rows in your dataset. (Highly accurate but slower).

### B. Outlier Detection
Outliers are extreme values that don't fit the normal pattern (e.g., an age of 150 years). They can severely confuse machine learning models.
*   **Z-Score**: Identifies values that are statistically too far from the average.
*   **IQR (Interquartile Range)**: Focuses on the middle 50% of your data and removes values that fall drastically outside of it.
*   **Isolation Forest**: An AI-based method that isolates anomalies by randomly splitting the data. Great for complex datasets.
*   **Action**: Once detected, you can either **Drop** the outlier rows or **Cap/Clip** them (replacing the extreme value with a maximum allowed threshold).

### C. Categorical Encoding
Machine learning models only understand numbers. They do not understand words like "Red", "Green", or "Blue". Encoding translates text into numbers.
*   **Label Encoding**: Assigns a unique number to each category (e.g., Red=1, Green=2, Blue=3). Best for ordinal data where order matters (e.g., Low, Medium, High).
*   **One-Hot Encoding**: Creates a new binary column for every single category (e.g., `is_red`, `is_green`). Best for nominal data where order does not matter.
*   **Target Encoding**: Replaces the category with the average value of your target prediction. Powerful for categorical columns with hundreds of unique values (like Zip Codes).

### D. Feature Scaling (Normalization)
If one column is measured in millions (like Salary) and another in single digits (like Years of Experience), the model might unfairly prioritize the larger numbers.
*   **Standard Scaler**: Centers the data around 0 with a standard deviation of 1.
*   **MinMax Scaler**: Shrinks all values to fit perfectly between 0 and 1.
*   **Robust Scaler**: Similar to Standard, but specifically designed to not be influenced by outliers.

---

## 3. The Final Step: Intelligent Feature Selection

**What is it?**
Not all columns in your dataset are actually useful for making predictions. In fact, having too many useless columns (noise) makes your model slower and less accurate. Feature Selection uses AI to rank your columns and pick only the most important ones.

**How to use it:**
1.  **Select a Target Variable**: This is the most crucial step. You must tell the system *what* you are trying to predict (e.g., "House Price", "Customer Churn", "Spam or Not Spam").
2.  **Choose a Selection Method**:
    *   **Random Forest / XGBoost**: Trains a quick tree-based model to see which columns it relies on the most. (Best overall choice).
    *   **Mutual Information**: Measures the statistical dependency between each column and your target variable.
    *   **Lasso Regression**: Uses math to shrink the importance of useless columns down to exactly zero.
3.  **Set the Number of Features**: Decide how many columns you want to keep (e.g., "Keep the top 10 features").
4.  **Execute**: The system will discard the useless columns and output your finalized, perfectly optimized dataset.

**After Feature Selection**, your data is fully prepared. You can now download the clean CSV, view the final Data Quality Report, and export the Python code pipeline!
