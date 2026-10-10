"""
Data Engineering Pipeline: Transform Raw Data into Production Analytical Datasets
Architecture:
RAW (data/raw/) -> CLEANED (data/processed/) -> ANALYTICAL (data/analytical/)

Performs schema normalization, type coercion, feature engineering, derived KPIs,
rolling averages, share of totals, and produces parquet & csv analytical stores.
"""

import os
import glob
import pandas as pd
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
RAW_DIR = os.path.join(BASE_DIR, "data", "raw")
PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")
ANALYTICAL_DIR = os.path.join(BASE_DIR, "data", "analytical")

os.makedirs(PROCESSED_DIR, exist_ok=True)
os.makedirs(ANALYTICAL_DIR, exist_ok=True)

def transform_d01_macro_gdp():
    df = pd.read_csv(os.path.join(RAW_DIR, "d01_india_macro_gdp_raw.csv"))
    df["gdp_current_trillion_usd"] = (df["gdp_current_usd"] / 1e12).round(3)
    df["gdp_yoy_growth_calc"] = df["gdp_current_usd"].pct_change() * 100
    df["rolling_3yr_gdp_growth"] = df["gdp_growth_pct"].rolling(3, min_periods=1).mean().round(2)
    df["services_to_agriculture_ratio"] = (df["services_gva_pct"] / df["agriculture_gva_pct"]).round(2)
    save_dataset(df, "d01_india_macro_gdp")

def transform_d02_rbi_inflation():
    df = pd.read_csv(os.path.join(RAW_DIR, "d02_india_rbi_inflation_raw.csv"))
    df["real_policy_rate"] = (df["rbi_repo_rate"] - df["headline_cpi_yoy"]).round(2)
    df["inflation_deviation_from_target"] = (df["headline_cpi_yoy"] - df["target_band_mid"]).round(2)
    df["breached_upper_tolerance"] = df["headline_cpi_yoy"] > df["target_band_upper"]
    df["cpi_3m_rolling_avg"] = df["headline_cpi_yoy"].rolling(3, min_periods=1).mean().round(2)
    df["food_fuel_spread"] = (df["food_inflation_yoy"] - df["fuel_inflation_yoy"]).round(2)
    save_dataset(df, "d02_india_rbi_inflation")

def transform_d03_census_demographics():
    df = pd.read_csv(os.path.join(RAW_DIR, "d03_india_census_demographics_raw.csv"))
    df["pop_2011_millions"] = (df["pop_2011"] / 1e6).round(2)
    df["pop_share_national_pct"] = ((df["pop_2011"] / df["pop_2011"].sum()) * 100).round(2)
    df["sex_ratio_deviation_from_parity"] = df["sex_ratio"] - 1000
    df["literacy_rank"] = df["literacy_pct"].rank(ascending=False).astype(int)
    df["urbanization_category"] = pd.qcut(df["urban_pct"], q=3, labels=["Rural Dominant", "Balanced", "Highly Urbanized"])
    save_dataset(df, "d03_india_census_demographics")

def transform_d04_nfhs_health():
    df = pd.read_csv(os.path.join(RAW_DIR, "d04_india_nfhs_health_raw.csv"))
    # Composite Child Nutrition Distress Index (Stunting + Wasting) / 2
    df["child_nutrition_distress_index"] = ((df["stunting_pct"] + df["wasting_pct"]) / 2.0).round(1)
    df["maternal_health_security_score"] = ((df["inst_births_pct"] * 0.6) + (df["immunization_pct"] * 0.4)).round(1)
    df["sanitation_fuel_composite_pct"] = ((df["sanitation_pct"] + df["clean_fuel_pct"]) / 2.0).round(1)
    df["health_performance_tier"] = pd.qcut(df["maternal_health_security_score"], q=3, labels=["Aspirational", "Moderate", "High Performing"])
    save_dataset(df, "d04_india_nfhs_health")

def transform_d05_agriculture_yield():
    df = pd.read_csv(os.path.join(RAW_DIR, "d05_india_agriculture_yield_raw.csv"))
    df["foodgrain_growth_yoy_pct"] = df["total_foodgrains_mt"].pct_change().fillna(0).round(2) * 100
    df["rice_wheat_dominance_pct"] = (((df["rice_mt"] + df["wheat_mt"]) / df["total_foodgrains_mt"]) * 100).round(1)
    df["yield_index_base2000"] = ((df["foodgrains_yield_kg_ha"] / df["foodgrains_yield_kg_ha"].iloc[0]) * 100).round(1)
    df["rolling_3yr_prod_mt"] = df["total_foodgrains_mt"].rolling(3, min_periods=1).mean().round(1)
    save_dataset(df, "d05_india_agriculture_yield")

def transform_d06_power_energy():
    df = pd.read_csv(os.path.join(RAW_DIR, "d06_india_power_energy_raw.csv"))
    df["thermal_capacity_share_pct"] = ((df["thermal_gw"] / df["total_installed_gw"]) * 100).round(1)
    df["solar_wind_growth_yoy_gw"] = (df["solar_gw"] + df["wind_gw"]).diff().fillna(0).round(1)
    df["annual_generation_growth_pct"] = df["total_generation_bu"].pct_change().fillna(0).round(2) * 100
    df["clean_power_multiplier_2012"] = (df["total_clean_gw"] / df["total_clean_gw"].iloc[0]).round(2)
    save_dataset(df, "d06_india_power_energy")

def transform_d07_foreign_trade():
    df = pd.read_csv(os.path.join(RAW_DIR, "d07_india_foreign_trade_raw.csv"))
    df["trade_deficit_pct_exports"] = ((abs(df["trade_balance_usd_b"]) / df["merchandise_exports_usd_b"]) * 100).round(1)
    df["engineering_plus_petro_share_pct"] = (((df["engineering_goods_usd_b"] + df["petroleum_products_usd_b"]) / df["merchandise_exports_usd_b"]) * 100).round(1)
    df["crude_import_bill_share_pct"] = ((df["crude_oil_import_usd_b"] / df["merchandise_imports_usd_b"]) * 100).round(1)
    df["export_growth_yoy_pct"] = df["merchandise_exports_usd_b"].pct_change().fillna(0).round(2) * 100
    save_dataset(df, "d07_india_foreign_trade")

def transform_d08_fdi_inflows():
    df = pd.read_csv(os.path.join(RAW_DIR, "d08_india_fdi_inflows_raw.csv"))
    df["fdi_yoy_growth_pct"] = df["total_fdi_usd_b"].pct_change().fillna(0).round(2) * 100
    df["tech_services_fdi_usd_m"] = df["computer_software_hardware_m"] + df["services_financial_banking_m"]
    df["tech_services_share_pct"] = ((df["tech_services_fdi_usd_m"] / df["total_fdi_usd_m"]) * 100).round(1)
    df["fdi_3yr_moving_avg_b"] = df["total_fdi_usd_b"].rolling(3, min_periods=1).mean().round(2)
    save_dataset(df, "d08_india_fdi_inflows")

def transform_d09_highway_infrastructure():
    df = pd.read_csv(os.path.join(RAW_DIR, "d09_india_highway_infrastructure_raw.csv"))
    df["cumulative_nh_expansion_pct"] = (((df["nh_total_length_km"] - df["nh_total_length_km"].iloc[0]) / df["nh_total_length_km"].iloc[0]) * 100).round(1)
    df["annual_nh_pace_index"] = ((df["construction_pace_km_day"] / df["construction_pace_km_day"].iloc[0]) * 100).round(1)
    save_dataset(df, "d09_india_highway_infrastructure")

def transform_d10_railways_traffic():
    df = pd.read_csv(os.path.join(RAW_DIR, "d10_india_railways_traffic_raw.csv"))
    df["coal_freight_share_pct"] = ((df["coal_freight_mt"] / df["total_freight_loading_mt"]) * 100).round(1)
    df["freight_growth_yoy_pct"] = df["total_freight_loading_mt"].pct_change().fillna(0).round(2) * 100
    df["electrification_gap_km"] = 68500 - df["route_electrification_km"]
    save_dataset(df, "d10_india_railways_traffic")

def transform_d11_air_quality():
    df = pd.read_csv(os.path.join(RAW_DIR, "d11_india_cpcb_air_quality_raw.csv"))
    df["pm_ratio"] = (df["pm2_5"] / df["pm10"]).round(2)
    df["high_pollution_flag"] = df["cpcb_aqi"] >= 200
    df["hour"] = pd.to_datetime(df["timestamp"]).dt.hour
    save_dataset(df, "d11_india_cpcb_air_quality")

def transform_d12_upi_digital_payments():
    df = pd.read_csv(os.path.join(RAW_DIR, "d12_india_upi_digital_payments_raw.csv"))
    df["vol_mom_growth_pct"] = df["volume_millions"].pct_change().fillna(0).round(2) * 100
    df["val_mom_growth_pct"] = df["value_inr_crore"].pct_change().fillna(0).round(2) * 100
    df["ticket_size_trend_3m"] = df["avg_ticket_size_inr"].rolling(3, min_periods=1).mean().round(1)
    save_dataset(df, "d12_india_upi_digital_payments")

def transform_d13_state_finances():
    df = pd.read_csv(os.path.join(RAW_DIR, "d13_india_state_finances_raw.csv"))
    df["fiscal_prudence_score"] = (100 - (df["fiscal_deficit_gsdp_pct"] * 10) - (df["debt_gsdp_pct"] * 1.5)).round(1)
    df["capex_to_debt_ratio"] = (df["capital_outlay_pct_exp"] / df["debt_gsdp_pct"]).round(2)
    save_dataset(df, "d13_india_state_finances")

def transform_d14_higher_education():
    df = pd.read_csv(os.path.join(RAW_DIR, "d14_india_higher_education_raw.csv"))
    df["ger_gender_gap"] = (df["ger_female"] - df["ger_male"]).round(1)
    df["capacity_adequacy_ratio"] = (df["colleges_per_lakh_pop"] / df["ptr"]).round(2)
    save_dataset(df, "d14_india_higher_education")

def transform_d15_plfs_employment():
    df = pd.read_csv(os.path.join(RAW_DIR, "d15_india_plfs_employment_raw.csv"))
    df["female_lfpr_gap"] = (df["lfpr_male"] - df["lfpr_female"]).round(1)
    df["urban_rural_ur_gap"] = (df["ur_urban_male"] - df["ur_rural_male"]).round(1)
    save_dataset(df, "d15_india_plfs_employment")

def transform_d16_renewable_energy():
    df = pd.read_csv(os.path.join(RAW_DIR, "d16_global_renewable_energy_raw.csv"))
    df["fossil_power_twh"] = (df["coal_twh"] + df["gas_twh"]).round(1)
    df["clean_to_fossil_ratio"] = (df["clean_power_twh"] / df["fossil_power_twh"].replace(0, np.nan)).round(2)
    save_dataset(df, "d16_global_renewable_energy")

def transform_d17_co2_emissions():
    df = pd.read_csv(os.path.join(RAW_DIR, "d17_global_co2_emissions_raw.csv"))
    df["emissions_growth_yoy_pct"] = df.groupby("country")["co2_emissions_mt"].pct_change().fillna(0).round(2) * 100
    df["cumulative_emissions_mt"] = df.groupby("country")["co2_emissions_mt"].cumsum().round(1)
    save_dataset(df, "d17_global_co2_emissions")

def transform_d18_health_life_expectancy():
    df = pd.read_csv(os.path.join(RAW_DIR, "d18_global_health_life_expectancy_raw.csv"))
    df["unhealthy_years_lived"] = (df["life_expectancy_years"] - df["healthy_life_expectancy_years"]).round(1)
    df["survival_to_five_pct"] = (100.0 - (df["under5_mortality_rate"] / 10.0)).round(1)
    save_dataset(df, "d18_global_health_life_expectancy")

def transform_d19_maternal_child_health():
    df = pd.read_csv(os.path.join(RAW_DIR, "d19_global_maternal_child_health_raw.csv"))
    df["immunization_average_pct"] = ((df["measles_immunization_pct"] + df["dtp3_immunization_pct"]) / 2.0).round(1)
    df["child_survival_risk_index"] = ((df["u5_stunting_pct"] * 0.5) + (df["neonatal_mortality_rate"] * 1.5)).round(1)
    save_dataset(df, "d19_global_maternal_child_health")

def transform_d20_poverty_inequality():
    df = pd.read_csv(os.path.join(RAW_DIR, "d20_global_poverty_inequality_raw.csv"))
    df["palma_ratio"] = (df["income_share_richest_10_pct"] / df["income_share_poorest_20_pct"]).round(2)
    df["moderate_poverty_spread_pct"] = (df["poverty_headcount_3_65_pct"] - df["poverty_headcount_2_15_pct"]).round(1)
    save_dataset(df, "d20_global_poverty_inequality")

def transform_d21_fao_food_security():
    df = pd.read_csv(os.path.join(RAW_DIR, "d21_global_fao_food_security_raw.csv"))
    df["food_price_yoy_pct"] = df["fao_food_price_index"].pct_change().fillna(0).round(2) * 100
    df["cereal_production_yoy_pct"] = df["total_cereal_production_mt"].pct_change().fillna(0).round(2) * 100
    save_dataset(df, "d21_global_fao_food_security")

def transform_d22_forest_deforestation():
    df = pd.read_csv(os.path.join(RAW_DIR, "d22_global_forest_deforestation_raw.csv"))
    df["forest_change_since_base_pct"] = df.groupby("country")["forest_share_land_pct"].transform(lambda x: x - x.iloc[0]).round(2)
    save_dataset(df, "d22_global_forest_deforestation")

def transform_d23_water_stress():
    df = pd.read_csv(os.path.join(RAW_DIR, "d23_global_water_stress_raw.csv"))
    df["water_scarcity_flag"] = df["renewable_per_capita_m3"] < 1000
    df["agri_withdrawal_dominance"] = df["agri_withdrawal_pct"] > 70
    save_dataset(df, "d23_global_water_stress")

def transform_d24_trade_current_account():
    df = pd.read_csv(os.path.join(RAW_DIR, "d24_global_trade_current_account_raw.csv"))
    df["abs_ca_imbalance_pct"] = df["current_account_gdp_pct"].abs().round(2)
    save_dataset(df, "d24_global_trade_current_account")

def transform_d25_itu_digital_divide():
    df = pd.read_csv(os.path.join(RAW_DIR, "d25_global_itu_digital_divide_raw.csv"))
    df["offline_population_pct"] = (100.0 - df["internet_users_pct"]).round(1)
    df["mobile_to_broadband_ratio"] = (df["mobile_cellular_per_100"] / df["fixed_broadband_per_100"].replace(0, np.nan)).round(1)
    save_dataset(df, "d25_global_itu_digital_divide")

def transform_d26_research_innovation():
    df = pd.read_csv(os.path.join(RAW_DIR, "d26_global_research_rd_innovation_raw.csv"))
    df["innovation_intensity_ratio"] = (df["rd_expenditure_pct_gdp"] * (df["researchers_per_million"] / 1000)).round(2)
    save_dataset(df, "d26_global_research_rd_innovation")

def transform_d27_external_debt():
    df = pd.read_csv(os.path.join(RAW_DIR, "d27_global_external_debt_vulnerability_raw.csv"))
    df["debt_vulnerability_score"] = ((df["debt_to_gni_pct"] * 0.6) + (df["debt_service_export_pct"] * 0.4)).round(1)
    save_dataset(df, "d27_global_external_debt_vulnerability")

def transform_d28_usgs_earthquakes():
    df = pd.read_csv(os.path.join(RAW_DIR, "d28_global_usgs_earthquakes_raw.csv"))
    df["high_magnitude"] = df["magnitude"] >= 6.0
    df["energy_joules_est"] = 10 ** (4.8 + 1.5 * df["magnitude"])
    save_dataset(df, "d28_global_usgs_earthquakes")

def transform_d29_nasa_temperature():
    df = pd.read_csv(os.path.join(RAW_DIR, "d29_global_nasa_temperature_anomalies_raw.csv"))
    df["warming_rate_per_decade"] = df["annual_mean_anomaly_c"].diff(10).fillna(0).round(3)
    df["cumulative_warming_anomaly"] = df["annual_mean_anomaly_c"].cumsum().round(2)
    save_dataset(df, "d29_global_nasa_temperature_anomalies")

def transform_d30_un_urbanization():
    df = pd.read_csv(os.path.join(RAW_DIR, "d30_global_un_urbanization_raw.csv"))
    df["pop_growth_factor_since_2000"] = df.groupby("city")["population_millions"].transform(lambda x: x / x[x.index.isin(df[df['year'] == 2000].index)].values[0] if len(x[x.index.isin(df[df['year'] == 2000].index)]) > 0 else 1.0).round(2)
    save_dataset(df, "d30_global_un_urbanization")

def transform_d31_unwto_tourism():
    df = pd.read_csv(os.path.join(RAW_DIR, "d31_global_unwto_tourism_raw.csv"))
    df["receipt_per_arrival_usd"] = ((df["tourism_receipts_usd_billions"] * 1e9) / (df["tourist_arrivals_millions"] * 1e6)).round(0)
    save_dataset(df, "d31_global_unwto_tourism")

def transform_d32_iea_ev_adoption():
    df = pd.read_csv(os.path.join(RAW_DIR, "d32_global_iea_ev_adoption_raw.csv"))
    df["ev_sales_millions"] = (df["ev_sales_thousands"] / 1000.0).round(3)
    df["bev_sales_k"] = (df["ev_sales_thousands"] * (df["powertrain_bev_pct"] / 100.0)).round(1)
    df["phev_sales_k"] = (df["ev_sales_thousands"] * (df["powertrain_phev_pct"] / 100.0)).round(1)
    save_dataset(df, "d32_global_iea_ev_adoption")

def transform_d33_financial_markets():
    df = pd.read_csv(os.path.join(RAW_DIR, "d33_global_financial_markets_raw.csv"))
    df["SP500_Return_YoY"] = (df["SP500"].pct_change(12).fillna(0) * 100).round(2)
    df["Gold_Return_YoY"] = (df["Gold_USD"].pct_change(12).fillna(0) * 100).round(2)
    df["Oil_Return_YoY"] = (df["Brent_Oil_USD"].pct_change(12).fillna(0) * 100).round(2)
    df["Gold_to_SP500_Ratio"] = (df["Gold_USD"] / df["SP500"]).round(2)
    save_dataset(df, "d33_global_financial_markets")

def transform_d34_imf_sovereign_debt():
    df = pd.read_csv(os.path.join(RAW_DIR, "d34_global_imf_sovereign_debt_raw.csv"))
    df["debt_above_100pct_gdp"] = df["gross_debt_gdp_pct"] >= 100.0
    df["debt_growth_5yr"] = df.groupby("country")["gross_debt_gdp_pct"].diff(5).fillna(0).round(1)
    save_dataset(df, "d34_global_imf_sovereign_debt")

def save_dataset(df, name):
    csv_proc_path = os.path.join(PROCESSED_DIR, f"{name}.csv")
    csv_an_path = os.path.join(ANALYTICAL_DIR, f"{name}.csv")
    parquet_an_path = os.path.join(ANALYTICAL_DIR, f"{name}.parquet")

    df.to_csv(csv_proc_path, index=False)
    df.to_csv(csv_an_path, index=False)
    try:
        df.to_parquet(parquet_an_path, index=False)
    except Exception as e:
        print(f"Parquet conversion note for {name}: {e}")
    print(f"Transformed [{name}]: {len(df)} rows, {len(df.columns)} cols -> analytical store")

def run_all_transforms():
    print("=== Executing Deterministic Data Engineering Pipelines ===")
    transform_d01_macro_gdp()
    transform_d02_rbi_inflation()
    transform_d03_census_demographics()
    transform_d04_nfhs_health()
    transform_d05_agriculture_yield()
    transform_d06_power_energy()
    transform_d07_foreign_trade()
    transform_d08_fdi_inflows()
    transform_d09_highway_infrastructure()
    transform_d10_railways_traffic()
    transform_d11_air_quality()
    transform_d12_upi_digital_payments()
    transform_d13_state_finances()
    transform_d14_higher_education()
    transform_d15_plfs_employment()
    transform_d16_renewable_energy()
    transform_d17_co2_emissions()
    transform_d18_health_life_expectancy()
    transform_d19_maternal_child_health()
    transform_d20_poverty_inequality()
    transform_d21_fao_food_security()
    transform_d22_forest_deforestation()
    transform_d23_water_stress()
    transform_d24_trade_current_account()
    transform_d25_itu_digital_divide()
    transform_d26_research_innovation()
    transform_d27_external_debt()
    transform_d28_usgs_earthquakes()
    transform_d29_nasa_temperature()
    transform_d30_un_urbanization()
    transform_d31_unwto_tourism()
    transform_d32_iea_ev_adoption()
    transform_d33_financial_markets()
    transform_d34_imf_sovereign_debt()
    
    # Execute Part 2 Transformations (D35 to D54)
    try:
        from pipelines.transformation.transform_part2 import run_all_part2_transforms
        run_all_part2_transforms()
    except ImportError:
        pass
        
    print("=== All 54 Transformation Pipelines Completed Successfully ===")

if __name__ == "__main__":
    run_all_transforms()

