# Day 33 — Merging & Combining Data with pandas

## Objective
Combine data from multiple DataFrames using merge and concat operations — the core skill for building unified financial datasets from multiple sources.

## Files
| File | Description |
|------|-------------|
| `day33_input.xlsx` | Practice dataset — 3 sheets: Holdings, MarketPrices, Transactions |
| `day33_practice.py` | Full working code covering all 8 concepts + P&L report |
| `day33_output.xlsx` | Generated output — 4 sheets: PnL_Report, Inner_Join, Left_Join, Concat_Txns |

## Concepts Covered
- `pd.merge()` — inner, left, right, outer joins on a common key
- `left_on` / `right_on` — merging when key column names differ
- `suffixes` — handling duplicate column names after merge
- `pd.concat()` — vertical row stacking and horizontal column stacking

## Key Takeaway
> Use `merge()` when combining two tables via a shared key (like SQL JOIN).  
> Use `concat()` when stacking similarly-structured tables (same columns or same rows).

## Portfolio Connection
The P&L report builder (holdings + live prices → gain/loss per stock) is a direct component of the **Phase 7 Financial Dashboard** project.

## Run
```bash
# Place day33_input.xlsx in the same directory, then:
python day33_practice.py
```
