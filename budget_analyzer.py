import pandas as pd

# -----------------------------
# 1️⃣ Load Data
# -----------------------------
file_name = "transactions.csv"
df = pd.read_csv(file_name)

# -----------------------------
# 2️⃣ Basic Cleaning
# -----------------------------
df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")
df.dropna(inplace=True)

# -----------------------------
# 3️⃣ Categorize Spending
# -----------------------------
# If category missing, try to infer from Description (optional)
df["Category"] = df["Category"].fillna("Other")

# -----------------------------
# 4️⃣ Summarize Spending
# -----------------------------
summary = df.groupby("Category")["Amount"].sum().reset_index()
summary = summary.sort_values(by="Amount", ascending=False)

# Calculate total income, expenses, balance
total_income = df[df["Amount"] > 0]["Amount"].sum()
total_expense = df[df["Amount"] < 0]["Amount"].sum() * -1
balance = total_income - total_expense

# -----------------------------
# 5️⃣ Export to Excel
# -----------------------------
output_file = "budget_report.xlsx"
with pd.ExcelWriter(output_file, engine="openpyxl") as writer:
    df.to_excel(writer, sheet_name="Transactions", index=False)
    summary.to_excel(writer, sheet_name="Summary", index=False)
    pd.DataFrame({
        "Total Income": [total_income],
        "Total Expense": [total_expense],
        "Balance": [balance]
    }).to_excel(writer, sheet_name="Overview", index=False)

print(f"✅ Budget report saved as {output_file}")

