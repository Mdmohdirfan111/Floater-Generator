import pandas as pd
import numpy as np
import calendar
import random
from datetime import datetime, timedelta

# Step 1: Load file
file_name = input("Enter the file name (with .csv or .xlsx): ").strip()
if file_name.endswith(".csv"):
    df = pd.read_csv(file_name)
else:
    df = pd.read_excel(file_name)

# Clean column names by stripping whitespace
df.columns = df.columns.str.strip()

# Step 2: Ask month & year
month_name = input("Enter the month name (e.g., May): ").strip().capitalize()
year = int(input("Enter the year (e.g., 2025): "))
month_number = list(calendar.month_name).index(month_name)
num_days = calendar.monthrange(year, month_number)[1]
all_dates = pd.date_range(f"{year}-{month_number:02d}-01", f"{year}-{month_number:02d}-{num_days}", freq="D")

# Step 3: Ask total monthly achievement percentage
monthly_target_percent = float(input("Enter the total monthly achievement % (e.g. 95): "))

# Step 4: Determine week-off days (1 Mon–Fri per week)
weekoffs = []
week_starts = [d for d in all_dates if d.weekday() == 0]  # Mondays
for week_start in week_starts:
    week_days = [week_start + timedelta(days=i) for i in range(5)
                 if (week_start + timedelta(days=i)).month == month_number]
    if week_days:
        weekoffs.append(random.choice(week_days))

# Step 5: Get working days (excluding weekoffs)
working_days = [d for d in all_dates if d not in weekoffs]

# Step 6: Prepare random daily achievement percentages
random_percents = [random.uniform(75, 150) for _ in working_days]
avg_percent = sum(random_percents) / len(random_percents)
adjustment_ratio = monthly_target_percent / avg_percent
adjusted_percents = [min(p * adjustment_ratio, 150) for p in random_percents]

# Step 7: Generate daily records
daily_entries = []
monthly_tgt_running = 0
monthly_ach_running = 0

# ✅ Add working day entries
for date, daily_percent in zip(working_days, adjusted_percents):
    random_row = df.sample(n=1).iloc[0]
    outlet = random_row['Outlet Name']
    code = random_row['Counter Code']
    tgt = float(random_row['Daily Tgt'])
    brand = random_row['Brand']
    counter_today_tgt = random_row["Counter's Today's Tgt"]
    counter = random_row['Counter']
    mt_gt = random_row['MT/GT']
    counter_monthly_tgt = random_row["Counter's Mthly Tgt"]
    location = random_row['Location']
    
    ach = int(tgt * (daily_percent / 100))

    monthly_tgt_running += tgt
    monthly_ach_running += ach

    daily_entries.append({
        "Date": date.strftime("%Y-%m-%d"),
        "Day": date.strftime("%A"),
        "COUNTER CODE": code,
        "Store Name": outlet,
        "Location": location,
        "MT/GT": mt_gt,
        "Counter": counter,
        "Counter's Mthly Tgt": counter_monthly_tgt,
        "Counter's Today's Tgt": counter_today_tgt,
        "Today's Ach": ach,
        "Trainee BA's Cumulative Monthly Tgt": round(monthly_tgt_running),
        "Trainee BA's Cumulative Monthly Achvt": round(monthly_ach_running),
        "% Cumulative Achvmt": f"{(monthly_ach_running/monthly_tgt_running)*100:.1f}%"
    })

# ✅ Add week-off day entries
for date in weekoffs:
    daily_entries.append({
        "Date": date.strftime("%Y-%m-%d"),
        "Day": date.strftime("%A"),
        "COUNTER CODE": "-",
        "Store Name": "WEEK OFF",
        "Location": "-",
        "MT/GT": "-",
        "Counter": "-",
        "Counter's Mthly Tgt": "-",
        "Counter's Today's Tgt": "-",
        "Today's Ach": "-",
        "Trainee BA's Cumulative Monthly Tgt": "-",
        "Trainee BA's Cumulative Monthly Achvt": "-",
        "% Cumulative Achvmt": "-"
    })

# ✅ Sort by date
output_df = pd.DataFrame(daily_entries)
output_df['Date'] = pd.to_datetime(output_df['Date'])
output_df = output_df.sort_values(by='Date').reset_index(drop=True)
output_df['Date'] = output_df['Date'].dt.strftime('%Y-%m-%d')  # Format back to string

# ✅ Save to Excel
output_file = f"Daily_Achievement_{month_name}_{year}.xlsx"
output_df.to_excel(output_file, index=False)

# ✅ Summary
print(f"\n✅ Done! File saved as: {output_file}")
print(f"📅 Total Days: {len(all_dates)}")
print(f"📌 Week-offs Added: {len(weekoffs)}")
print(f"📈 Records Generated: {len(output_df)}")
