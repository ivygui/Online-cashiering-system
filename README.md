# Hawker Cash Register

A simple digital receipting system for a hawker stall, built with Streamlit. It works like the cash register of the past: every sale is keyed in as it happens, and the system keeps a clear record that can be checked at the end of the day.

**Why this exists:** many hawkers in Singapore now accept PayNow, PayLah and PayWave as well as cash. Because these payments do not pass through a cash drawer, it is hard to check that money received matches sales made. This app gives the stall owner a lightweight way to record each transaction and reconcile the day's totals by payment type.

The app was built using vibe coding. There is **no database**: all data is stored in a plain text file.

---

## Features

**Recording sales**
- Enter the sale amount, the amount rendered by the customer and the payment type (Cash, PayNow, PayLah, PayWave).
- Change is calculated automatically.
- A sale is rejected if the amount rendered is less than the sale amount.
- Undo the last transaction, and see the five most recent transactions.

**Reports**
- **Daily report:** full transaction listing, total sales, a revenue-goal progress bar, CSV download.
- **Monthly report:** sales summarised by day, month total, CSV download.
- **Payment type breakdown (optional requirement):** total sales by payment type, for a day and for a month, as a table and bar chart.

**Other**
- Staff PIN login with a lock button.
- English and Chinese interface.

---

## Requirements

- Python 3.9 or later
- Streamlit and Altair

```bash
pip install streamlit altair
```

## Running the app

```bash
streamlit run hawker_app3.py
```

The browser opens at `http://localhost:8501`. The default staff PIN is `1234`; change `APP_PASSWORD` near the top of `hawker_app3.py` before real use.

---

## Files

| File | Purpose |
|------|---------|
| `hawker_app3.py` | The Streamlit application |
| `sales_data.txt` | Transaction records (created automatically if missing) |

## Data format

`sales_data.txt` has a header line and one line per sale:

```
date,time,amount,tendered,change,payment_type
2026-09-24,15:30:30,6.0,10.0,4.0,Cash
```

Do not delete this file, and back it up regularly. Totals are based on the sale amount, not the amount rendered.

---

## Limitations

- Only the last transaction can be undone.
- The PIN is stored in the source code, which is fine for a demo but not for real use.
- The whole file is read on each page load, which suits a single small stall.
- Designed for one user at a time.

Any sample data in `sales_data.txt` is for demonstration only.
