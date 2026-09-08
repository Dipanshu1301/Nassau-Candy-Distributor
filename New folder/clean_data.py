"""
STEP 1 & 2: Data Cleaning + Feature Engineering
Nassau Candy Distributor - Shipping Route Efficiency Analysis

Beginner note: run this file FIRST. It reads the raw CSV, cleans it,
adds new calculated columns (lead time, factory, route), and saves a
new file called cleaned_data.csv that the dashboard will use.
"""

import pandas as pd

# ---------------------------------------------------------
# 1. LOAD RAW DATA
# ---------------------------------------------------------
df = pd.read_csv("data/Nassau_Candy_Distributor.csv")
print(f"Raw rows loaded: {len(df)}")

# ---------------------------------------------------------
# 2. CLEAN DATES
#    Dates in the file are in DD-MM-YYYY text format, so we
#    tell pandas exactly how to read them.
# ---------------------------------------------------------
df["Order Date"] = pd.to_datetime(df["Order Date"], format="%d-%m-%Y", errors="coerce")
df["Ship Date"] = pd.to_datetime(df["Ship Date"], format="%d-%m-%Y", errors="coerce")

# Drop rows where dates could not be read at all
before = len(df)
df = df.dropna(subset=["Order Date", "Ship Date"])
print(f"Dropped {before - len(df)} rows with unreadable dates")

# ---------------------------------------------------------
# 3. CALCULATE SHIPPING LEAD TIME (days)
# ---------------------------------------------------------
df["Lead Time (Days)"] = (df["Ship Date"] - df["Order Date"]).dt.days

# Remove negative lead times (shipped before ordered = impossible)
before = len(df)
df = df[df["Lead Time (Days)"] >= 0]
print(f"Dropped {before - len(df)} rows with negative lead time")

# NOTE (data quality flag for the research paper):
# In this dataset, Ship Date years are far ahead of Order Date years
# (e.g. ordered in 2024, "shipped" in 2026-2030), giving lead times of
# 900-1600+ days. This is not realistic for real shipping and should be
# called out as a DATA LIMITATION in the report. For the dashboard/KPIs
# we still use the raw lead time as given, but we also create a
# "Lead Time (Capped)" version for readable charts.
df["Lead Time (Capped)"] = df["Lead Time (Days)"].clip(upper=30)

# ---------------------------------------------------------
# 4. STANDARDIZE GEOGRAPHIC FIELDS
# ---------------------------------------------------------
for col in ["City", "State/Province", "Region", "Country/Region"]:
    df[col] = df[col].astype(str).str.strip()

# ---------------------------------------------------------
# 5. MAP EACH PRODUCT TO ITS FACTORY (given in project brief)
# ---------------------------------------------------------
product_to_factory = {
    "Wonka Bar - Nutty Crunch Surprise": "Lot's O' Nuts",
    "Wonka Bar - Fudge Mallows": "Lot's O' Nuts",
    "Wonka Bar -Scrumdiddlyumptious": "Lot's O' Nuts",
    "Wonka Bar - Milk Chocolate": "Wicked Choccy's",
    "Wonka Bar - Triple Dazzle Caramel": "Wicked Choccy's",
    "Laffy Taffy": "Sugar Shack",
    "SweeTARTS": "Sugar Shack",
    "Nerds": "Sugar Shack",
    "Fun Dip": "Sugar Shack",
    "Fizzy Lifting Drinks": "Sugar Shack",
    "Everlasting Gobstopper": "Secret Factory",
    "Hair Toffee": "The Other Factory",
    "Lickable Wallpaper": "Secret Factory",
    "Wonka Gum": "Secret Factory",
    "Kazookles": "The Other Factory",
}

factory_coords = {
    "Lot's O' Nuts": (32.881893, -111.768036),
    "Wicked Choccy's": (32.076176, -81.088371),
    "Sugar Shack": (48.11914, -96.18115),
    "Secret Factory": (41.446333, -90.565487),
    "The Other Factory": (35.1175, -89.971107),
}

df["Factory"] = df["Product Name"].map(product_to_factory)
df["Factory Lat"] = df["Factory"].map(lambda f: factory_coords[f][0])
df["Factory Lon"] = df["Factory"].map(lambda f: factory_coords[f][1])

before = len(df)
df = df.dropna(subset=["Factory"])
print(f"Dropped {before - len(df)} rows with unmapped product/factory")

# ---------------------------------------------------------
# 6. DEFINE ROUTES
# ---------------------------------------------------------
df["Route (State)"] = df["Factory"] + " -> " + df["State/Province"]
df["Route (Region)"] = df["Factory"] + " -> " + df["Region"]

# ---------------------------------------------------------
# 7. SAVE CLEANED DATA
# ---------------------------------------------------------
df.to_csv("data/cleaned_data.csv", index=False)
print(f"Cleaned rows saved: {len(df)}")
print("Saved to data/cleaned_data.csv")