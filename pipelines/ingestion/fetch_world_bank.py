"""
Pipelines: Ingest World Bank World Development Indicators (WDI)
Primary Official Source: World Bank API (https://api.worldbank.org/v2/)
Authority: World Bank Group (Tier 1 International Statistical Body)
"""

import os
import json
import time
import requests
import pandas as pd

CACHE_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data", "cache")
RAW_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data", "raw")
os.makedirs(CACHE_DIR, exist_ok=True)
os.makedirs(RAW_DIR, exist_ok=True)

SESSION = requests.Session()
SESSION.headers.update({"User-Agent": "DV-Suite-Intelligence-Engine/1.0"})

def fetch_wb_indicator(indicator_code, country_code="IND", start_year=1990, end_year=2023, retries=3):
    cache_file = os.path.join(CACHE_DIR, f"wb_{country_code}_{indicator_code}.json")
    if os.path.exists(cache_file):
        try:
            with open(cache_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass

    url = f"https://api.worldbank.org/v2/country/{country_code}/indicator/{indicator_code}?format=json&date={start_year}:{end_year}&per_page=1000"
    for attempt in range(retries):
        try:
            resp = SESSION.get(url, timeout=25)
            if resp.status_code == 200:
                payload = resp.json()
                if len(payload) > 1 and payload[1]:
                    with open(cache_file, "w", encoding="utf-8") as f:
                        json.dump(payload[1], f)
                    return payload[1]
        except Exception as e:
            print(f"Warning: Attempt {attempt+1} failed for {indicator_code} ({country_code}): {e}")
            time.sleep(2)
    return []

def get_wb_dataframe(indicator_map, country_code="IND", start_year=1990, end_year=2023):
    """
    indicator_map: dict of {column_name: indicator_code}
    returns: DataFrame with columns ['year', col1, col2, ...]
    """
    records_by_year = {}
    for year in range(start_year, end_year + 1):
        records_by_year[year] = {"year": year, "country": country_code}

    for col_name, ind_code in indicator_map.items():
        data = fetch_wb_indicator(ind_code, country_code=country_code, start_year=start_year, end_year=end_year)
        for entry in data:
            try:
                y = int(entry.get("date"))
                val = entry.get("value")
                if y in records_by_year:
                    records_by_year[y][col_name] = val
            except (ValueError, TypeError):
                continue

    df = pd.DataFrame(list(records_by_year.values()))
    df = df.sort_values("year").reset_index(drop=True)
    return df

def run_world_bank_ingestion():
    print("=== Ingesting World Bank Official Indicators ===")
    
    # 1. India Macro GDP indicators
    macro_map = {
        "gdp_current_usd": "NY.GDP.MKTP.CD",
        "gdp_growth_pct": "NY.GDP.MKTP.KD.ZG",
        "gdp_per_capita_usd": "NY.GDP.PCAP.CD",
        "agriculture_gva_pct": "NV.AGR.TOTL.ZS",
        "industry_gva_pct": "NV.IND.TOTL.ZS",
        "services_gva_pct": "NV.SRV.TOTL.ZS",
        "gross_capital_formation_pct": "NE.GDI.TOTL.ZS",
        "inflation_cpi_pct": "FP.CPI.TOTL.ZG"
    }
    df_macro = get_wb_dataframe(macro_map, country_code="IND", start_year=1990, end_year=2023)
    macro_raw_path = os.path.join(RAW_DIR, "d01_india_macro_gdp_raw.csv")
    df_macro.to_csv(macro_raw_path, index=False)
    print(f"Saved India Macro GDP data ({len(df_macro)} rows) -> {macro_raw_path}")

    # 2. Global Development & Economic Comparison
    key_economies = ["USA", "CHN", "IND", "JPN", "DEU", "GBR", "BRA", "FRA"]
    gdp_comp_rows = []
    for c in key_economies:
        comp_map = {
            "gdp_usd": "NY.GDP.MKTP.CD",
            "gdp_growth": "NY.GDP.MKTP.KD.ZG",
            "gdp_per_capita": "NY.GDP.PCAP.CD",
            "co2_per_capita": "EN.ATM.CO2E.PC",
            "life_expectancy": "SP.DYN.LE00.IN",
            "rd_expenditure_pct": "GB.XPD.RSDV.GD.ZS",
            "internet_users_pct": "IT.NET.USER.ZS"
        }
        df_c = get_wb_dataframe(comp_map, country_code=c, start_year=2000, end_year=2023)
        gdp_comp_rows.append(df_c)
    
    if gdp_comp_rows:
        df_global_comp = pd.concat(gdp_comp_rows, ignore_index=True)
        global_raw_path = os.path.join(RAW_DIR, "global_wb_comparison_raw.csv")
        df_global_comp.to_csv(global_raw_path, index=False)
        print(f"Saved Global WB Comparison ({len(df_global_comp)} rows) -> {global_raw_path}")

if __name__ == "__main__":
    run_world_bank_ingestion()
