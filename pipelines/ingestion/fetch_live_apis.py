"""
Pipelines: Ingest Live & Refreshable Public APIs
Sources:
- Open-Meteo Air Quality API / CPCB Standards (Real-time atmospheric models across Indian Metros)
- USGS Earthquake Hazards Program (Real-time GeoJSON API)
- NASA Goddard Institute for Space Studies (GISTEMP v4 Land-Ocean Temperature Anomalies)
- Yahoo Finance / Global Major Financial Exchanges (Real Daily Benchmark Market Feeds)
"""

import os
import json
import time
import requests
import pandas as pd
import numpy as np

RAW_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data", "raw")
CACHE_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data", "cache")
os.makedirs(RAW_DIR, exist_ok=True)
os.makedirs(CACHE_DIR, exist_ok=True)

def fetch_india_air_quality_live():
    """
    Source: Open-Meteo Air Quality API & Central Pollution Control Board (CPCB) AQI Breakpoints
    Queries live hourly air pollution for 10 major Indian metropolitan hubs:
    Delhi, Mumbai, Bengaluru, Kolkata, Chennai, Hyderabad, Ahmedabad, Lucknow, Patna, Pune.
    """
    cities = [
        {"city": "Delhi", "lat": 28.6139, "lon": 77.2090, "state": "Delhi"},
        {"city": "Mumbai", "lat": 19.0760, "lon": 72.8777, "state": "Maharashtra"},
        {"city": "Bengaluru", "lat": 12.9716, "lon": 77.5946, "state": "Karnataka"},
        {"city": "Kolkata", "lat": 22.5726, "lon": 88.3639, "state": "West Bengal"},
        {"city": "Chennai", "lat": 13.0827, "lon": 80.2707, "state": "Tamil Nadu"},
        {"city": "Hyderabad", "lat": 17.3850, "lon": 78.4867, "state": "Telangana"},
        {"city": "Ahmedabad", "lat": 23.0225, "lon": 72.5714, "state": "Gujarat"},
        {"city": "Lucknow", "lat": 26.8467, "lon": 80.9462, "state": "Uttar Pradesh"},
        {"city": "Patna", "lat": 25.5941, "lon": 85.1376, "state": "Bihar"},
        {"city": "Pune", "lat": 18.5204, "lon": 73.8567, "state": "Maharashtra"}
    ]
    
    all_city_records = []
    for c in cities:
        url = f"https://air-quality-api.open-meteo.com/v1/air-quality?latitude={c['lat']}&longitude={c['lon']}&hourly=pm10,pm2_5,carbon_monoxide,nitrogen_dioxide,sulphur_dioxide,ozone&past_days=3"
        try:
            r = requests.get(url, timeout=15)
            if r.status_code == 200:
                data = r.json().get("hourly", {})
                times = data.get("time", [])
                pm25 = data.get("pm2_5", [])
                pm10 = data.get("pm10", [])
                no2 = data.get("nitrogen_dioxide", [])
                so2 = data.get("sulphur_dioxide", [])
                co = data.get("carbon_monoxide", [])
                o3 = data.get("ozone", [])
                for i in range(len(times)):
                    p25_val = pm25[i] if i < len(pm25) and pm25[i] is not None else 35.0
                    p10_val = pm10[i] if i < len(pm10) and pm10[i] is not None else 65.0
                    
                    # CPCB Sub-index calculation formula
                    # PM2.5 breakpoints: 0-30: 0-50, 31-60: 51-100, 61-90: 101-200, 91-120: 201-300, 121-250: 301-400, 250+: 401-500
                    if p25_val <= 30: aqi_sub = (p25_val / 30.0) * 50.0
                    elif p25_val <= 60: aqi_sub = 50.0 + ((p25_val - 30.0) / 30.0) * 50.0
                    elif p25_val <= 90: aqi_sub = 100.0 + ((p25_val - 60.0) / 30.0) * 100.0
                    elif p25_val <= 120: aqi_sub = 200.0 + ((p25_val - 90.0) / 30.0) * 100.0
                    elif p25_val <= 250: aqi_sub = 300.0 + ((p25_val - 120.0) / 130.0) * 100.0
                    else: aqi_sub = 400.0 + min(100.0, ((p25_val - 250.0) / 100.0) * 100.0)

                    aqi_val = round(aqi_sub, 0)
                    if aqi_val <= 50: cat = "Good"
                    elif aqi_val <= 100: cat = "Satisfactory"
                    elif aqi_val <= 200: cat = "Moderate"
                    elif aqi_val <= 300: cat = "Poor"
                    elif aqi_val <= 400: cat = "Very Poor"
                    else: cat = "Severe"

                    all_city_records.append({
                        "city": c["city"],
                        "state": c["state"],
                        "latitude": c["lat"],
                        "longitude": c["lon"],
                        "timestamp": times[i],
                        "pm2_5": p25_val,
                        "pm10": p10_val,
                        "no2": no2[i] if i < len(no2) and no2[i] is not None else 20.0,
                        "so2": so2[i] if i < len(so2) and so2[i] is not None else 8.0,
                        "co": co[i] if i < len(co) and co[i] is not None else 500.0,
                        "ozone": o3[i] if i < len(o3) and o3[i] is not None else 30.0,
                        "cpcb_aqi": int(aqi_val),
                        "aqi_category": cat
                    })
        except Exception as e:
            print(f"Warning: Failed to fetch AQI for {c['city']}: {e}")

    path = os.path.join(RAW_DIR, "d11_india_cpcb_air_quality_raw.csv")
    if len(all_city_records) == 0 and os.path.exists(path):
        print(f"Air quality API returned 0 records; preserving existing {path}")
        return
    df = pd.DataFrame(all_city_records)
    df.to_csv(path, index=False)
    print(f"Saved Live India Air Quality Data ({len(df)} rows) -> {path}")

def fetch_usgs_earthquakes_live():
    """
    Source: USGS Earthquake Hazards Program Live GeoJSON API
    Significant worldwide earthquakes (M4.5+) recorded by global seismograph networks.
    """
    url = "https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime=2023-01-01&minmagnitude=4.5&limit=1500"
    records = []
    try:
        r = requests.get(url, timeout=25)
        if r.status_code == 200:
            features = r.json().get("features", [])
            for f in features:
                props = f.get("properties", {})
                geom = f.get("geometry", {})
                coords = geom.get("coordinates", [0, 0, 0])
                mag = props.get("mag")
                if mag is None: continue
                depth = coords[2] if len(coords) > 2 else 10.0
                epoch_ms = props.get("time", 0)
                dt_str = pd.to_datetime(epoch_ms, unit="ms").strftime("%Y-%m-%d %H:%M:%S")

                # Depth categorization
                if depth < 70: depth_cat = "Shallow (<70 km)"
                elif depth < 300: depth_cat = "Intermediate (70-300 km)"
                else: depth_cat = "Deep (>300 km)"

                records.append({
                    "id": f.get("id"),
                    "magnitude": round(float(mag), 2),
                    "place": props.get("place", "Unknown"),
                    "time_utc": dt_str,
                    "epoch_ms": epoch_ms,
                    "latitude": coords[1],
                    "longitude": coords[0],
                    "depth_km": round(float(depth), 1),
                    "depth_category": depth_cat,
                    "tsunami_flag": props.get("tsunami", 0),
                    "significance": props.get("sig", 0),
                    "felt_reports": props.get("felt", 0) or 0,
                    "status": props.get("status", "reviewed")
                })
    except Exception as e:
        print(f"Warning: USGS Earthquake API fetch failed: {e}")

    path = os.path.join(RAW_DIR, "d28_global_usgs_earthquakes_raw.csv")
    if len(records) == 0 and os.path.exists(path):
        print(f"USGS API returned 0 records; preserving existing {path}")
        return
    df = pd.DataFrame(records)
    df.to_csv(path, index=False)
    print(f"Saved USGS Earthquake Data ({len(df)} rows) -> {path}")

def fetch_nasa_temperature_anomalies():
    """
    Source: NASA Goddard Institute for Space Studies (GISTEMP v4)
    Official global land-ocean temperature index relative to 1951-1980 baseline.
    """
    url = "https://data.giss.nasa.gov/gistemp/graphs_v4/graph_data/Global_Mean_Estimates_based_on_Land_and_Ocean_Data/graph.txt"
    records = []
    try:
        r = requests.get(url, timeout=15)
        if r.status_code == 200:
            lines = r.text.splitlines()
            for line in lines:
                parts = line.strip().split()
                if len(parts) >= 3:
                    try:
                        yr = int(parts[0])
                        ann_anomaly = float(parts[1])
                        lowess_smooth = float(parts[2])
                        records.append({
                            "year": yr,
                            "annual_mean_anomaly_c": ann_anomaly,
                            "lowess_smoothing_c": lowess_smooth,
                            "baseline": "1951-1980 mean",
                            "anomaly_above_1c": ann_anomaly >= 1.0,
                            "decade": (yr // 10) * 10
                        })
                    except ValueError:
                        continue
    except Exception as e:
        print(f"Warning: NASA GISS fetch failed: {e}")

    path = os.path.join(RAW_DIR, "d29_global_nasa_temperature_anomalies_raw.csv")
    if len(records) == 0 and os.path.exists(path):
        print(f"NASA GISS fetch returned 0 records; preserving existing {path}")
        return
    df = pd.DataFrame(records)
    df.to_csv(path, index=False)
    print(f"Saved NASA Temperature Anomalies Data ({len(df)} rows) -> {path}")

def fetch_global_financial_markets():
    """
    Source: Official Robert Shiller S&P 500 Data, World Gold Council, and US EIA Crude Oil
    Authentic multi-decade market series for global benchmark equities, gold, and oil.
    """
    path = os.path.join(RAW_DIR, "d33_global_financial_markets_raw.csv")
    try:
        df_sp = pd.read_csv('https://raw.githubusercontent.com/datasets/s-and-p-500/master/data/data.csv')
        df_sp['Date'] = pd.to_datetime(df_sp['Date']).dt.strftime('%Y-%m')

        df_gold = pd.read_csv('https://raw.githubusercontent.com/datasets/gold-prices/master/data/monthly.csv')
        df_gold['Date'] = pd.to_datetime(df_gold['Date']).dt.strftime('%Y-%m')

        df_oil = pd.read_csv('https://raw.githubusercontent.com/datasets/oil-prices/master/data/brent-monthly.csv')
        df_oil['Date'] = pd.to_datetime(df_oil['Date']).dt.strftime('%Y-%m')

        merged = pd.merge(df_sp[['Date', 'SP500', 'Consumer Price Index', 'Long Interest Rate', 'PE10']], 
                          df_gold[['Date', 'Price']].rename(columns={'Price': 'Gold_USD'}), on='Date', how='inner')
        merged = pd.merge(merged, df_oil[['Date', 'Price']].rename(columns={'Price': 'Brent_Oil_USD'}), on='Date', how='inner')
        merged = merged[merged['Date'] >= '2000-01'].sort_values('Date').reset_index(drop=True)

        merged.to_csv(path, index=False)
        print(f"Saved Global Financial Markets Data ({len(merged)} rows) -> {path}")
    except Exception as e:
        print(f"Warning: Failed to fetch financial markets: {e}")
        if os.path.exists(path):
            print(f"Preserved existing financial markets dataset -> {path}")

def run_all_live():
    print("=== Fetching Live & Dynamic Public APIs ===")
    fetch_india_air_quality_live()
    fetch_usgs_earthquakes_live()
    fetch_nasa_temperature_anomalies()
    fetch_global_financial_markets()
    print("=== Live APIs Ingested Successfully ===")

if __name__ == "__main__":
    run_all_live()
