# ============================================================
# DAY 33 - Merging & Combining Data with pandas
# Topics: pd.merge(), pd.concat(), join types, real finance use
# ============================================================

import pandas as pd

# ── Load the three sheets from your input file ───────────────
holdings     = pd.read_excel("day33_input.xlsx", sheet_name="Holdings")
market       = pd.read_excel("day33_input.xlsx", sheet_name="MarketPrices")
transactions = pd.read_excel("day33_input.xlsx", sheet_name="Transactions")

print("=" * 55)
print("RAW DATA PREVIEW")
print("=" * 55)
print("\n[Holdings]\n",     holdings.head(3))
print("\n[MarketPrices]\n", market.head(3))
print("\n[Transactions]\n", transactions.head(3))


# ============================================================
# CONCEPT 1 — INNER JOIN
# Only rows that exist in BOTH DataFrames are kept.
# S007 (Bajaj Finance) has no market price → it DISAPPEARS.
# ============================================================
inner_merged = pd.merge(
    holdings,          # left DataFrame
    market,            # right DataFrame
    on="Stock_ID",     # the common key column
    how="inner"        # keep only matching rows
)

print("\n" + "=" * 55)
print("CONCEPT 1 — INNER JOIN (matched rows only)")
print("=" * 55)
print(inner_merged[["Stock_ID", "Company", "Buy_Price_INR", "Current_Price_INR", "Sector"]])
print(f"\nHoldings rows: {len(holdings)}  |  After inner merge: {len(inner_merged)}")
print("→ S007 (Bajaj Finance) dropped — no market price entry")


# ============================================================
# CONCEPT 2 — LEFT JOIN
# ALL rows from the LEFT DataFrame are kept.
# S007 appears with NaN in market price columns.
# ============================================================
left_merged = pd.merge(
    holdings,
    market,
    on="Stock_ID",
    how="left"         # keep ALL rows from left (holdings)
)

print("\n" + "=" * 55)
print("CONCEPT 2 — LEFT JOIN (all holdings kept)")
print("=" * 55)
print(left_merged[["Stock_ID", "Company", "Buy_Price_INR", "Current_Price_INR", "Sector"]])
print("\n→ S007 present with NaN — good for spotting missing data")


# ============================================================
# CONCEPT 3 — RIGHT JOIN
# ALL rows from the RIGHT DataFrame are kept.
# ============================================================
right_merged = pd.merge(
    holdings,
    market,
    on="Stock_ID",
    how="right"        # keep ALL rows from right (market)
)

print("\n" + "=" * 55)
print("CONCEPT 3 — RIGHT JOIN (all market prices kept)")
print("=" * 55)
print(right_merged[["Stock_ID", "Company", "Current_Price_INR", "Sector"]])


# ============================================================
# CONCEPT 4 — OUTER JOIN
# Keep ALL rows from BOTH DataFrames.
# NaN wherever no match exists on either side.
# ============================================================
outer_merged = pd.merge(
    holdings,
    market,
    on="Stock_ID",
    how="outer"        # keep everything
)

print("\n" + "=" * 55)
print("CONCEPT 4 — OUTER JOIN (complete picture)")
print("=" * 55)
print(outer_merged[["Stock_ID", "Company", "Buy_Price_INR", "Current_Price_INR"]])


# ============================================================
# CONCEPT 5 — DIFFERENT KEY NAMES (left_on / right_on)
# When the key columns have different names in each DataFrame.
# ============================================================
holdings_renamed = holdings.rename(columns={"Stock_ID": "ticker"})

different_key_merge = pd.merge(
    holdings_renamed,
    market,
    left_on="ticker",       # key column name in LEFT df
    right_on="Stock_ID",    # key column name in RIGHT df
    how="inner"
)

print("\n" + "=" * 55)
print("CONCEPT 5 — DIFFERENT KEY NAMES (left_on / right_on)")
print("=" * 55)
print(different_key_merge[["ticker", "Stock_ID", "Company", "Current_Price_INR"]].head(4))


# ============================================================
# CONCEPT 6 — SUFFIX HANDLING
# When both DataFrames share a non-key column name,
# pandas auto-adds suffixes to avoid confusion.
# ============================================================
holdings_copy = holdings.copy()
holdings_copy["Sector"] = "Unknown"           # both dfs now have "Sector"

suffix_merge = pd.merge(
    holdings_copy,
    market,
    on="Stock_ID",
    how="inner",
    suffixes=("_holdings", "_market")         # custom suffixes
)

print("\n" + "=" * 55)
print("CONCEPT 6 — SUFFIX HANDLING (duplicate column names)")
print("=" * 55)
print(suffix_merge[["Stock_ID", "Company", "Sector_holdings", "Sector_market"]].head(4))
print("→ Without suffixes pandas uses _x and _y by default")


# ============================================================
# CONCEPT 7 — pd.concat() VERTICAL STACKING
# Stack two DataFrames on top of each other (same columns).
# Classic use-case: combining BUY and SELL transaction logs.
# ============================================================
buy_txns  = transactions[transactions["Type"] == "BUY"].copy()
sell_txns = transactions[transactions["Type"] == "SELL"].copy()

combined_txns = pd.concat(
    [buy_txns, sell_txns],    # list of DataFrames to stack
    ignore_index=True          # reset index after stacking
)

print("\n" + "=" * 55)
print("CONCEPT 7 — pd.concat() VERTICAL (stack rows)")
print("=" * 55)
print(f"BUY count: {len(buy_txns)} | SELL count: {len(sell_txns)} | Combined: {len(combined_txns)}")
print(combined_txns[["Transaction_ID", "Stock_ID", "Type", "Quantity"]])


# ============================================================
# CONCEPT 8 — pd.concat() HORIZONTAL STACKING
# Stick two DataFrames side by side (same rows, new columns).
# ============================================================
left_part  = holdings[["Stock_ID", "Company", "Quantity"]].reset_index(drop=True)
right_part = market[["Stock_ID", "Current_Price_INR", "Sector"]].reset_index(drop=True)

horizontal = pd.concat(
    [left_part, right_part],
    axis=1                     # axis=1 means side-by-side (columns)
)

print("\n" + "=" * 55)
print("CONCEPT 8 — pd.concat() HORIZONTAL (add columns)")
print("=" * 55)
print(horizontal.head(5))
print("→ Useful for aligning pre-computed feature columns")


# ============================================================
# PRACTICAL TASK — Build a Portfolio P&L Report
# Merge holdings + market → calculate gain/loss per stock
# ============================================================
portfolio = pd.merge(holdings, market, on="Stock_ID", how="left")

portfolio["Invested_INR"]     = portfolio["Quantity"] * portfolio["Buy_Price_INR"]
portfolio["Current_Value_INR"]= portfolio["Quantity"] * portfolio["Current_Price_INR"]
portfolio["PnL_INR"]          = portfolio["Current_Value_INR"] - portfolio["Invested_INR"]
portfolio["PnL_Pct"]          = (portfolio["PnL_INR"] / portfolio["Invested_INR"]) * 100

print("\n" + "=" * 55)
print("PRACTICAL TASK — Portfolio P&L Report")
print("=" * 55)
report = portfolio[["Stock_ID", "Company", "Sector",
                     "Invested_INR", "Current_Value_INR",
                     "PnL_INR", "PnL_Pct"]].round(2)
print(report.to_string(index=False))

total_invested = portfolio["Invested_INR"].sum()
total_current  = portfolio["Current_Value_INR"].sum()
total_pnl      = portfolio["PnL_INR"].sum()

print(f"\nTotal Invested : ₹{total_invested:,.2f}")
print(f"Total Value    : ₹{total_current:,.2f}")
print(f"Total P&L      : ₹{total_pnl:,.2f}")
print(f"Overall Return : {(total_pnl/total_invested)*100:.2f}%")

# ── Export final report to Excel ─────────────────────────────
with pd.ExcelWriter("day33_output.xlsx", engine="openpyxl") as writer:
    report.to_excel(writer, sheet_name="PnL_Report",       index=False)
    inner_merged.to_excel(writer, sheet_name="Inner_Join", index=False)
    left_merged.to_excel(writer,  sheet_name="Left_Join",  index=False)
    combined_txns.to_excel(writer, sheet_name="Concat_Txns", index=False)

print("\n✅ Exported → day33_output.xlsx (4 sheets)")
