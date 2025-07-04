import pandas as pd, pytz

SRC_FILE   = "scrape.csv"              # Kaggle file
DST_FILE   = "ff_news_mt5.csv"         # what MT5 will read
BROKER_TZ  = pytz.timezone("Africa/Nairobi")   # broker/server time zone
IMPACT_MAP = {"High": 3, "Medium": 2, "Low": 1}

# 1️⃣  Load & make all column names lower-case (avoids typo headaches)
df = pd.read_csv(SRC_FILE)
df.columns = df.columns.str.lower()    # now it's 'datetime', 'impact', etc.

# 2️⃣  Convert the UTC timestamp to broker time
df["timestamp"] = (
    pd.to_datetime(df["datetime"], utc=True)   # Kaggle’s times are in UTC
      .dt.tz_convert(BROKER_TZ)
)

# 3️⃣  Keep only what the EA needs & map impact → numbers
out = (df.assign(impact=df["impact"].map(IMPACT_MAP))
         [["timestamp", "currency", "impact", "event"]])

# 4️⃣  Format as  YYYY.MM.DD HH:MM  (MT5-friendly) and export
out["timestamp"] = out["timestamp"].dt.strftime("%Y.%m.%d %H:%M")
out.to_csv(DST_FILE, index=False, encoding="utf-8")

print(f"✔  Saved {DST_FILE} — ready for Strategy Tester")
