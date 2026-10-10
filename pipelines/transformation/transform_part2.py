"""
Data Engineering Pipeline: Transform Part 2 Datasets (D35 to D54)
Produces cleaned, feature-engineered, and analytical datasets in CSV and Apache Parquet formats.
"""

import os
import pandas as pd
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
RAW_DIR = os.path.join(BASE_DIR, "data", "raw")
PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")
ANALYTICAL_DIR = os.path.join(BASE_DIR, "data", "analytical")

os.makedirs(PROCESSED_DIR, exist_ok=True)
os.makedirs(ANALYTICAL_DIR, exist_ok=True)

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

def transform_d35_gst_collections():
    df = pd.read_csv(os.path.join(RAW_DIR, "d35_india_gst_collections_raw.csv"))
    df["total_gst_lakh_crore"] = (df["total_gst_crore"] / 100000.0).round(3)
    df["cgst_sgst_combined"] = df["cgst_crore"] + df["sgst_crore"]
    df["igst_share_pct"] = ((df["igst_crore"] / df["total_gst_crore"]) * 100).round(2)
    df["cess_share_pct"] = ((df["cess_crore"] / df["total_gst_crore"]) * 100).round(2)
    df["rolling_3m_avg_crore"] = df["total_gst_crore"].rolling(3, min_periods=1).mean().round(1)
    df["period_str"] = df["year"].astype(str) + "-M" + df["month"].astype(str).str.zfill(2)
    save_dataset(df, "d35_india_gst_collections")

def transform_d36_pmjdy_inclusion():
    df = pd.read_csv(os.path.join(RAW_DIR, "d36_india_pmjdy_inclusion_raw.csv"))
    df["rural_share_pct"] = ((df["rural_beneficiaries_lakh"] / df["total_beneficiaries_lakh"]) * 100).round(2)
    df["women_share_pct"] = ((df["women_beneficiaries_lakh"] / df["total_beneficiaries_lakh"]) * 100).round(2)
    df["avg_deposit_per_account_inr"] = ((df["total_deposits_crore"] * 1e7) / (df["total_beneficiaries_lakh"] * 1e5)).round(1)
    df["rupay_card_penetration_pct"] = ((df["rupay_cards_issued_lakh"] / df["total_beneficiaries_lakh"]) * 100).round(2)
    df["deposit_density_tier"] = pd.qcut(df["avg_deposit_per_account_inr"], q=3, labels=["Emerging Balances", "Moderate Balances", "High Deposit Density"])
    save_dataset(df, "d36_india_pmjdy_inclusion")

def transform_d37_mgnregs_employment():
    df = pd.read_csv(os.path.join(RAW_DIR, "d37_india_mgnregs_employment_raw.csv"))
    df["persondays_per_household"] = (df["persondays_generated_lakh"] / df["households_worked_lakh"]).round(1)
    df["cost_per_personday_rs"] = ((df["total_expenditure_crore"] * 1e7) / (df["persondays_generated_lakh"] * 1e5)).round(1)
    df["women_inclusion_tier"] = pd.qcut(df["women_participation_pct"], q=3, labels=["Below Benchmark", "National Parity", "High Inclusion"])
    df["wage_deviation_from_avg"] = (df["avg_wage_rate_rs"] - df["avg_wage_rate_rs"].mean()).round(1)
    save_dataset(df, "d37_india_mgnregs_employment")

def transform_d38_civil_aviation():
    df = pd.read_csv(os.path.join(RAW_DIR, "d38_india_civil_aviation_raw.csv"))
    df["domestic_share_pct"] = ((df["domestic_passengers_million"] / df["total_passengers_million"]) * 100).round(2)
    df["pax_per_aircraft_movement"] = ((df["total_passengers_million"] * 1e6) / (df["aircraft_movements_million"] * 1e6)).round(1)
    df["pax_yoy_growth_pct"] = df["total_passengers_million"].pct_change().fillna(0).round(2) * 100
    df["cargo_per_airport_kt"] = ((df["cargo_tonnage_million_mt"] * 1000) / df["operating_airports_count"]).round(2)
    save_dataset(df, "d38_india_civil_aviation")

def transform_d39_major_ports():
    df = pd.read_csv(os.path.join(RAW_DIR, "d39_india_major_ports_raw.csv"))
    df["pol_share_pct"] = ((df["pol_oil_mmt"] / df["total_traffic_mmt"]) * 100).round(2)
    df["bulk_cargo_share_pct"] = (((df["iron_ore_mmt"] + df["coal_mmt"]) / df["total_traffic_mmt"]) * 100).round(2)
    df["container_share_pct"] = ((df["container_other_mmt"] / df["total_traffic_mmt"]) * 100).round(2)
    df["turnaround_efficiency_rank"] = df["avg_turnaround_hours"].rank().astype(int)
    save_dataset(df, "d39_india_major_ports")

def transform_d40_telecom_trai():
    df = pd.read_csv(os.path.join(RAW_DIR, "d40_india_telecom_trai_raw.csv"))
    df["rural_sub_share_pct"] = ((df["rural_sub_million"] / df["total_wireless_sub_million"]) * 100).round(2)
    df["broadband_penetration_pct"] = ((df["broadband_sub_million"] / df["total_wireless_sub_million"]) * 100).round(2)
    df["broadband_yoy_growth_pct"] = df["broadband_sub_million"].pct_change().fillna(0).round(2) * 100
    df["time_label"] = df["year"].astype(str) + "-Q" + df["quarter"].astype(str)
    save_dataset(df, "d40_india_telecom_trai")

def transform_d41_mining_minerals():
    df = pd.read_csv(os.path.join(RAW_DIR, "d41_india_mining_minerals_raw.csv"))
    df["total_bulk_minerals_mmt"] = df["iron_ore_million_mt"] + df["bauxite_million_mt"] + df["limestone_million_mt"]
    df["iron_ore_share_pct"] = ((df["iron_ore_million_mt"] / df["total_bulk_minerals_mmt"]) * 100).round(2)
    df["iron_ore_yoy_growth_pct"] = df["iron_ore_million_mt"].pct_change().fillna(0).round(2) * 100
    df["value_per_mt_iron_inr"] = ((df["total_metallic_value_billion_inr"] * 1e9) / (df["iron_ore_million_mt"] * 1e6)).round(1)
    save_dataset(df, "d41_india_mining_minerals")

def transform_d42_forest_cover_isfr():
    df = pd.read_csv(os.path.join(RAW_DIR, "d42_india_forest_cover_isfr_raw.csv"))
    df["dense_forest_sqkm"] = df["very_dense_forest_sqkm"] + df["mod_dense_forest_sqkm"]
    df["dense_canopy_ratio"] = ((df["dense_forest_sqkm"] / df["total_forest_sqkm"]) * 100).round(2)
    df["carbon_density_tonnes_per_sqkm"] = ((df["carbon_stock_million_tonnes"] * 1e6) / df["total_forest_sqkm"]).round(1)
    df["national_forest_share_pct"] = ((df["total_forest_sqkm"] / df["total_forest_sqkm"].sum()) * 100).round(2)
    df["ecological_zone_tier"] = pd.qcut(df["forest_cover_pct"], q=3, labels=["Sparse Canopy", "Balanced Woodlands", "Dense Forest Sanctuary"])
    save_dataset(df, "d42_india_forest_cover_isfr")

def transform_d43_petroleum_ppac():
    df = pd.read_csv(os.path.join(RAW_DIR, "d43_india_petroleum_ppac_raw.csv"))
    df["net_crude_deficit_mmt"] = (df["refinery_throughput_mmt"] - df["crude_production_mmt"]).round(1)
    df["diesel_share_pct"] = ((df["diesel_consumption_mmt"] / df["pol_consumption_mmt"]) * 100).round(2)
    df["petrol_to_diesel_ratio"] = (df["petrol_consumption_mmt"] / df["diesel_consumption_mmt"]).round(3)
    df["cooking_fuel_lpg_share_pct"] = ((df["lpg_consumption_mmt"] / df["pol_consumption_mmt"]) * 100).round(2)
    df["consumption_yoy_growth_pct"] = df["pol_consumption_mmt"].pct_change().fillna(0).round(2) * 100
    save_dataset(df, "d43_india_petroleum_ppac")

def transform_d44_ncrb_crime():
    df = pd.read_csv(os.path.join(RAW_DIR, "d44_india_ncrb_crime_raw.csv"))
    df["women_crime_share_pct"] = ((df["crimes_against_women"] / df["total_ipc_crimes"]) * 100).round(2)
    df["cyber_crime_rate_index"] = ((df["cyber_crimes"] / df["total_ipc_crimes"]) * 1000).round(2)
    df["judicial_clearance_composite"] = ((df["conviction_rate_pct"] * 0.5) + (df["chargesheet_rate_pct"] * 0.5)).round(1)
    df["crime_severity_tier"] = pd.qcut(df["crime_rate_per_lakh"], q=3, labels=["Moderate Incidence", "High Incidence", "Severe Reporting Incidence"])
    save_dataset(df, "d44_india_ncrb_crime")

def transform_d45_pmay_housing():
    df = pd.read_csv(os.path.join(RAW_DIR, "d45_india_pmay_housing_raw.csv"))
    df["grounding_rate_pct"] = ((df["houses_grounded_thousand"] / df["houses_sanctioned_thousand"]) * 100).round(2)
    df["avg_central_subsidy_per_house_inr"] = ((df["central_assistance_crore"] * 1e7) / (df["houses_completed_thousand"] * 1e3)).round(1)
    df["pipeline_houses_thousand"] = (df["houses_grounded_thousand"] - df["houses_completed_thousand"]).round(1)
    df["national_completion_share_pct"] = ((df["houses_completed_thousand"] / df["houses_completed_thousand"].sum()) * 100).round(2)
    save_dataset(df, "d45_india_pmay_housing")

def transform_d46_jal_jeevan_mission():
    df = pd.read_csv(os.path.join(RAW_DIR, "d46_india_jal_jeevan_mission_raw.csv"))
    df["coverage_expansion_percentage_points"] = (df["current_coverage_pct"] - df["baseline_2019_pct"]).round(1)
    df["unconnected_households_lakh"] = (df["total_rural_households_lakh"] - df["fhtc_provided_lakh"]).round(2)
    df["saturation_status"] = df["current_coverage_pct"].apply(lambda x: "Saturated (100%)" if x >= 100 else ("Near Saturation (>80%)" if x >= 80 else "In Progress"))
    df["growth_multiplier"] = (df["current_coverage_pct"] / (df["baseline_2019_pct"].replace(0, 0.1))).round(1)
    save_dataset(df, "d46_india_jal_jeevan_mission")

def transform_d47_udise_education():
    df = pd.read_csv(os.path.join(RAW_DIR, "d47_india_udise_education_raw.csv"))
    df["basic_amenities_composite_pct"] = ((df["electricity_avail_pct"] + df["drinking_water_avail_pct"] + df["girls_toilet_avail_pct"]) / 3.0).round(2)
    df["digital_readiness_composite_pct"] = ((df["computer_facility_pct"] + df["internet_facility_pct"]) / 2.0).round(2)
    df["ptr_gap"] = (df["ptr_primary"] - df["ptr_upper_primary"]).round(1)
    df["infrastructure_parity_tier"] = pd.qcut(df["digital_readiness_composite_pct"], q=3, labels=["Emerging Digital", "Progressive", "Advanced Digital"])
    save_dataset(df, "d47_india_udise_education")

def transform_d48_tourism_stats():
    df = pd.read_csv(os.path.join(RAW_DIR, "d48_india_tourism_stats_raw.csv"))
    df["fee_per_foreign_tourist_usd"] = ((df["foreign_exchange_earnings_usd_billion"] * 1e9) / (df["foreign_tourist_arrivals_million"] * 1e6)).round(1)
    df["domestic_to_foreign_ratio"] = (df["domestic_tourist_visits_million"] / df["foreign_tourist_arrivals_million"]).round(1)
    df["fta_yoy_growth_pct"] = df["foreign_tourist_arrivals_million"].pct_change().fillna(0).round(2) * 100
    df["domestic_visits_billion"] = (df["domestic_tourist_visits_million"] / 1000.0).round(3)
    save_dataset(df, "d48_india_tourism_stats")

def transform_d49_food_pds_nfsa():
    df = pd.read_csv(os.path.join(RAW_DIR, "d49_india_food_pds_nfsa_raw.csv"))
    df["rice_share_pct"] = ((df["rice_offtake_million_mt"] / df["total_offtake_million_mt"]) * 100).round(2)
    df["wheat_share_pct"] = ((df["wheat_offtake_million_mt"] / df["total_offtake_million_mt"]) * 100).round(2)
    df["subsidy_per_mt_inr"] = ((df["food_subsidy_thousand_crore"] * 1e11) / (df["total_offtake_million_mt"] * 1e6)).round(1)
    df["buffer_to_offtake_ratio"] = (df["central_buffer_stock_million_mt"] / df["total_offtake_million_mt"]).round(2)
    save_dataset(df, "d49_india_food_pds_nfsa")

def transform_d50_patents_ip():
    df = pd.read_csv(os.path.join(RAW_DIR, "d50_india_patents_ip_raw.csv"))
    df["grant_to_filing_ratio_pct"] = ((df["patents_granted"] / df["patents_filed"]) * 100).round(2)
    df["domestic_to_foreign_ratio"] = (df["domestic_filed"] / df["foreign_filed"]).round(2)
    df["patent_filings_yoy_growth_pct"] = df["patents_filed"].pct_change().fillna(0).round(2) * 100
    df["grants_yoy_growth_pct"] = df["patents_granted"].pct_change().fillna(0).round(2) * 100
    save_dataset(df, "d50_india_patents_ip")

def transform_d51_pm_kisan():
    df = pd.read_csv(os.path.join(RAW_DIR, "d51_india_pm_kisan_raw.csv"))
    df["avg_transfer_per_farmer_inr"] = ((df["cumulative_dbt_crore"] * 1e7) / (df["farmer_beneficiaries_lakh"] * 1e5)).round(1)
    df["digital_compliance_score"] = ((df["ekyc_authenticated_pct"] * 0.5) + (df["aadhaar_seeded_pct"] * 0.5)).round(2)
    df["national_farmer_share_pct"] = ((df["farmer_beneficiaries_lakh"] / df["farmer_beneficiaries_lakh"].sum()) * 100).round(2)
    df["beneficiary_scale_tier"] = pd.qcut(df["farmer_beneficiaries_lakh"], q=3, labels=["Tier 3 Scale", "Tier 2 Scale", "Mega Agrarian Base"])
    save_dataset(df, "d51_india_pm_kisan")

def transform_d52_automotive_siam():
    df = pd.read_csv(os.path.join(RAW_DIR, "d52_india_automotive_siam_raw.csv"))
    df["pv_share_of_production_pct"] = ((df["pv_production_million"] / df["total_production_million"]) * 100).round(2)
    df["two_wheeler_share_pct"] = ((df["two_wheeler_million"] / df["total_production_million"]) * 100).round(2)
    df["export_intensity_pct"] = ((df["total_exports_million"] / df["total_production_million"]) * 100).round(2)
    df["domestic_market_absorption_pct"] = ((df["domestic_sales_million"] / df["total_production_million"]) * 100).round(2)
    df["production_yoy_growth_pct"] = df["total_production_million"].pct_change().fillna(0).round(2) * 100
    save_dataset(df, "d52_india_automotive_siam")

def transform_d53_coal_production():
    df = pd.read_csv(os.path.join(RAW_DIR, "d53_india_coal_production_raw.csv"))
    df["non_cil_production_mt"] = (df["total_raw_coal_production_mt"] - df["cil_production_mt"]).round(1)
    df["cil_share_pct"] = ((df["cil_production_mt"] / df["total_raw_coal_production_mt"]) * 100).round(2)
    df["import_to_domestic_ratio"] = ((df["coal_imports_mt"] / df["total_raw_coal_production_mt"]) * 100).round(2)
    df["power_dispatch_yoy_growth_pct"] = df["power_sector_dispatch_mt"].pct_change().fillna(0).round(2) * 100
    save_dataset(df, "d53_india_coal_production")

def transform_d54_inland_waterways():
    df = pd.read_csv(os.path.join(RAW_DIR, "d54_india_inland_waterways_raw.csv"))
    df["nw1_ganga_share_pct"] = ((df["nw1_ganga_mmt"] / df["total_waterway_cargo_mmt"]) * 100).round(2)
    df["nw2_brahmaputra_share_pct"] = ((df["nw2_brahmaputra_mmt"] / df["total_waterway_cargo_mmt"]) * 100).round(2)
    df["tidal_coastal_cargo_mmt"] = (df["goa_waterways_mmt"] + df["maharashtra_waterways_mmt"]).round(1)
    df["cargo_yoy_growth_pct"] = df["total_waterway_cargo_mmt"].pct_change().fillna(0).round(2) * 100
    df["nw1_to_nw2_ratio"] = (df["nw1_ganga_mmt"] / df["nw2_brahmaputra_mmt"]).round(2)
    save_dataset(df, "d54_india_inland_waterways")

def run_all_part2_transforms():
    print("=== Executing Data Engineering Transformations (Part 2: D35 to D54) ===")
    transform_d35_gst_collections()
    transform_d36_pmjdy_inclusion()
    transform_d37_mgnregs_employment()
    transform_d38_civil_aviation()
    transform_d39_major_ports()
    transform_d40_telecom_trai()
    transform_d41_mining_minerals()
    transform_d42_forest_cover_isfr()
    transform_d43_petroleum_ppac()
    transform_d44_ncrb_crime()
    transform_d45_pmay_housing()
    transform_d46_jal_jeevan_mission()
    transform_d47_udise_education()
    transform_d48_tourism_stats()
    transform_d49_food_pds_nfsa()
    transform_d50_patents_ip()
    transform_d51_pm_kisan()
    transform_d52_automotive_siam()
    transform_d53_coal_production()
    transform_d54_inland_waterways()
    print("=== All 20 New Datasets Successfully Transformed & Stored ===")

if __name__ == "__main__":
    run_all_part2_transforms()
