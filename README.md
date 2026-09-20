# Nassau Candy Distributor — Shipping Route Efficiency Analysis

A data analytics project that analyzes factory-to-customer shipping performance using order and shipment data.

## Features

* Factory-to-customer route analysis
* Shipping lead-time analysis
* State and regional performance analysis
* Shipping mode comparison
* Interactive Streamlit dashboard
* Route and order-level drill-down
* Filters for date, region, state, ship mode, and delay threshold

## Tech Stack

* Python
* Pandas
* NumPy
* Plotly
* Streamlit

## Project Structure

```text
nassau_project/
├── data/
│   ├── Nassau_Candy_Distributor.csv
│   └── cleaned_data.csv
├── .streamlit/
│   └── config.toml
├── clean_data.py
├── analyze.py
├── app.py
├── state_codes.py
├── requirements.txt
└── README.md
```

## How to Run

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Clean the data

```bash
python clean_data.py
```

### 3. Run analysis (Optional)

```bash
python analyze.py
```

### 4. Start the dashboard

```bash
streamlit run app.py
```

The dashboard will open at:

```text
http://localhost:8501
```

## Data Limitation

The source dataset contains an unusual date difference:

* Order Date: 2024–2025
* Ship Date: 2026–2030

This results in unusually large calculated shipping lead times. Therefore, absolute lead-time values should be interpreted carefully. However, relative comparisons between routes, regions, states, and shipping modes can still be analyzed.

## Project Goal

To analyze shipping performance and identify route efficiency, geographic patterns, and potential delivery delays across the Nassau Candy distribution network.

## Author

**Dipanshu Kharera**

B.Tech — Artificial Intelligence & Machine Learning
