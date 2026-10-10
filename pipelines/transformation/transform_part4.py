"""
Data Engineering Pipeline: Transform Part 4 Decision-Oriented Datasets (D75 to D94)
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

def transform_d75_who_amr_surveillance():
    df = pd.read_csv(os.path.join(RAW_DIR, "d75_who_amr_surveillance_raw.csv"))
    df["composite_amr_threat_score"] = ((df["mrsa_resistance_pct"] + df["ecoli_3gcr_resistance_pct"] + df["klebsiella_carbapenem_res_pct"]) / 3).round(1)
    df["stewardship_gap_pct"] = (100.0 - df["antimicrobial_stewardship_compliance_pct"]).round(1)
    df["resistance_severity_tier"] = pd.qcut(df["composite_amr_threat_score"], q=3, labels=["Controlled Resistance", "Moderate Resistance", "Critical Threat Level"])
    save_dataset(df, "d75_who_amr_surveillance")

def transform_d76_grid_india_frequency_stability():
    df = pd.read_csv(os.path.join(RAW_DIR, "d76_grid_india_frequency_stability_raw.csv"))
    df["total_frequency_excursions_pct"] = (df["frequency_excursion_high_pct"] + df["frequency_excursion_low_pct"]).round(1)
    df["renewable_share_of_capacity_pct"] = ((df["renewable_installed_capacity_gw"] / (df["peak_demand_met_gw"] * 1.6)) * 100).round(1)
    df["curtailment_volume_gw_est"] = ((df["renewable_installed_capacity_gw"] * df["estimated_renewable_curtailment_pct"]) / 100).round(2)
    df["yoy_peak_demand_growth_pct"] = (df["peak_demand_met_gw"].pct_change().fillna(0) * 100).round(1)
    save_dataset(df, "d76_grid_india_frequency_stability")

def transform_d77_cpcb_municipal_solid_waste():
    df = pd.read_csv(os.path.join(RAW_DIR, "d77_cpcb_municipal_solid_waste_raw.csv"))
    df["collection_efficiency_pct"] = ((df["waste_collected_tpd"] / df["waste_generated_tpd"]) * 100).round(1)
    df["processing_rate_pct"] = ((df["waste_processed_tpd"] / df["waste_generated_tpd"]) * 100).round(1)
    df["unprocessed_landfill_waste_tpd"] = (df["waste_collected_tpd"] - df["waste_processed_tpd"]).clip(lower=0)
    df["processing_performance_tier"] = pd.qcut(df["processing_rate_pct"], q=3, labels=["Lagging Processing (<50%)", "Moderate Processing", "High Circularity (>80%)"])
    save_dataset(df, "d77_cpcb_municipal_solid_waste")

def transform_d78_cgwb_groundwater_stress():
    df = pd.read_csv(os.path.join(RAW_DIR, "d78_cgwb_groundwater_stress_raw.csv"))
    df["net_groundwater_balance_bcm"] = (df["total_annual_extractable_bcm"] - df["current_annual_extraction_bcm"]).round(2)
    df["total_stressed_units"] = df["over_exploited_units_count"] + df["critical_units_count"]
    df["total_assessed_units"] = df["over_exploited_units_count"] + df["critical_units_count"] + df["safe_units_count"]
    df["stressed_units_share_pct"] = ((df["total_stressed_units"] / df["total_assessed_units"]) * 100).round(1)
    df["aquifer_stress_tier"] = pd.cut(df["stage_of_extraction_pct"], bins=[0, 70, 100, 300], labels=["Safe Extraction", "Semi-Critical / Critical", "Severe Over-Exploited (>100%)"])
    save_dataset(df, "d78_cgwb_groundwater_stress")

def transform_d79_iea_critical_minerals():
    df = pd.read_csv(os.path.join(RAW_DIR, "d79_iea_critical_minerals_raw.csv"))
    df["hhi_producer_concentration_index"] = ((df["top_producer_share_pct"] ** 2) / 100).round(0)
    df["hhi_refiner_concentration_index"] = ((df["top_refiner_share_pct"] ** 2) / 100).round(0)
    df["refining_to_mining_dominance_ratio"] = (df["top_refiner_share_pct"] / df["top_producer_share_pct"]).round(2)
    df["geopolitical_vulnerability_tier"] = pd.cut(df["top_refiner_share_pct"], bins=[0, 50, 75, 100], labels=["Diversified Refining", "Concentrated Hub", "Monopoly Bottleneck (>75%)"])
    save_dataset(df, "d79_iea_critical_minerals")

def transform_d80_nha_hospital_bed_capacity():
    df = pd.read_csv(os.path.join(RAW_DIR, "d80_nha_hospital_bed_capacity_raw.csv"))
    df["nurse_to_doctor_ratio"] = (df["nurses_per_1000"] / df["doctors_per_1000"]).round(2)
    df["who_bed_density_gap"] = (3.0 - df["beds_per_1000_population"]).round(2) # WHO benchmark 3 beds/1000
    df["total_staffing_density_per_1000"] = (df["doctors_per_1000"] + df["nurses_per_1000"]).round(2)
    df["healthcare_capacity_tier"] = pd.qcut(df["beds_per_1000_population"], q=3, labels=["Acute Deficit (<0.6/1k)", "Moderate Provision", "Adequate Bed Network"])
    save_dataset(df, "d80_nha_hospital_bed_capacity")

def transform_d81_fao_wfp_food_security():
    df = pd.read_csv(os.path.join(RAW_DIR, "d81_fao_wfp_food_security_raw.csv"))
    df["import_inflation_stress_index"] = ((df["cereal_import_dependency_ratio_pct"].clip(lower=0) * df["food_inflation_yoy_pct"]) / 100).round(1)
    df["caloric_gap_vs_benchmark_kcal"] = (df["per_capita_food_supply_kcal_day"] - 2500).round(0)
    df["food_security_vulnerability_tier"] = pd.cut(df["emergency_food_reserve_months"], bins=[0, 1.5, 3.0, 10], labels=["Critical Emergency (<1.5m)", "Fragile Reserve (1.5-3m)", "Secure Buffer (>3m)"])
    save_dataset(df, "d81_fao_wfp_food_security")

def transform_d82_morth_urban_traffic_congestion():
    df = pd.read_csv(os.path.join(RAW_DIR, "d82_morth_urban_traffic_congestion_raw.csv"))
    df["speed_reduction_penalty_pct"] = (((df["avg_off_peak_speed_kmh"] - df["avg_peak_speed_kmh"]) / df["avg_off_peak_speed_kmh"]) * 100).round(1)
    df["lost_economic_hours_per_day"] = (df["lost_hours_per_year_commute"] / 250.0).round(2)
    df["speed_ratio_offpeak_to_peak"] = (df["avg_off_peak_speed_kmh"] / df["avg_peak_speed_kmh"]).round(2)
    df["congestion_severity_tier"] = pd.qcut(df["congestion_level_pct"], q=3, labels=["Moderate Flow (<40%)", "Heavy Congestion", "Severe Choke-point (>55%)"])
    save_dataset(df, "d82_morth_urban_traffic_congestion")

def transform_d83_nbtc_blood_bank_reserves():
    df = pd.read_csv(os.path.join(RAW_DIR, "d83_nbtc_blood_bank_reserves_raw.csv"))
    df["rare_blood_group_average_reserve_days"] = ((df["o_negative_reserve_days"] + df["b_negative_reserve_days"]) / 2).round(1)
    df["annual_wastage_units_approx"] = ((df["annual_units_collected_lakh"] * 1e5 * df["annual_wastage_due_to_expiry_pct"]) / 100).round(0)
    df["blood_reserve_security_tier"] = pd.cut(df["rare_blood_group_average_reserve_days"], bins=[0, 2.0, 3.5, 10], labels=["Critical Stockout Risk (<2d)", "Fragile Reserve (2-3.5d)", "Secure Stock (>3.5d)"])
    save_dataset(df, "d83_nbtc_blood_bank_reserves")

def transform_d84_cpcb_cems_industrial_emissions():
    df = pd.read_csv(os.path.join(RAW_DIR, "d84_cpcb_cems_industrial_emissions_raw.csv"))
    df["combined_gaseous_compliance_rate_pct"] = ((df["so2_compliance_rate_pct"] + df["nox_compliance_rate_pct"]) / 2).round(1)
    df["stack_exceedance_stacks_estimate"] = ((df["cems_connected_stacks_count"] * df["stack_pm_exceedance_pct"]) / 100).round(0)
    df["pollution_severity_tier"] = pd.cut(df["cepi_pollution_index"], bins=[0, 70, 85, 100], labels=["Polluted Area", "Severely Polluted Cluster", "Critically Polluted (>85 CEPI)"])
    save_dataset(df, "d84_cpcb_cems_industrial_emissions")

def transform_d85_indian_railways_safety():
    df = pd.read_csv(os.path.join(RAW_DIR, "d85_indian_railways_safety_raw.csv"))
    df["usfd_fractures_per_1000_km"] = ((df["usfd_fractures_detected_count"] / df["track_route_km"]) * 1000).round(1)
    df["kavach_atp_coverage_pct"] = ((df["kavach_atp_deployed_km"] / df["track_route_km"]) * 100).round(1)
    df["derailment_rate_per_1000_km"] = ((df["derailments_count"] / df["track_route_km"]) * 1000).round(2)
    df["track_renewal_intensity_pct"] = ((df["track_renewal_executed_km"] / df["track_route_km"]) * 100).round(1)
    save_dataset(df, "d85_indian_railways_safety")

def transform_d86_bis_sovereign_debt_default_risk():
    df = pd.read_csv(os.path.join(RAW_DIR, "d86_bis_sovereign_debt_default_risk_raw.csv"))
    df["implied_1yr_default_prob_pct"] = ((df["cds_5yr_spread_bps"] / 10000.0) / (1 - 0.40) * 100).round(2) # Market standard 40% recovery assumption
    df["short_term_debt_vulnerability_index"] = ((df["external_debt_to_gni_pct"] * df["short_term_debt_share_pct"]) / 100).round(1)
    df["concessional_cushion_factor"] = (df["multilateral_concessional_share_pct"] / df["short_term_debt_share_pct"]).round(2)
    save_dataset(df, "d86_bis_sovereign_debt_default_risk")

def transform_d87_mnre_offgrid_solar_reliability():
    df = pd.read_csv(os.path.join(RAW_DIR, "d87_mnre_offgrid_solar_reliability_raw.csv"))
    df["capacity_per_hamlet_kwp"] = (df["minigrid_solar_capacity_kwp"] / df["beneficiary_hamlets_count"]).round(1)
    df["pumps_per_hamlet_density"] = (df["standalone_solar_pumps_installed"] / df["beneficiary_hamlets_count"]).round(1)
    df["daily_unserved_power_hours"] = (24.0 - df["avg_daily_power_supply_hours"]).round(1)
    df["dignified_energy_access_tier"] = pd.cut(df["avg_daily_power_supply_hours"], bins=[0, 16, 20, 24], labels=["Basic Energy Access (<16h)", "Intermediate Reliability", "Continuous Rural Power (>20h)"])
    save_dataset(df, "d87_mnre_offgrid_solar_reliability")

def transform_d88_njdg_court_case_pendency():
    df = pd.read_csv(os.path.join(RAW_DIR, "d88_njdg_court_case_pendency_raw.csv"))
    df["total_chronic_delay_cases_lakh"] = ((df["total_pending_cases_lakh"] * df["cases_older_than_5_years_pct"]) / 100).round(2)
    df["ultra_chronic_cases_over_10y_lakh"] = ((df["total_pending_cases_lakh"] * df["cases_older_than_10_years_pct"]) / 100).round(2)
    df["criminal_to_civil_ratio"] = (df["criminal_cases_share_pct"] / df["civil_cases_share_pct"]).round(2)
    df["pendency_distress_tier"] = pd.qcut(df["total_pending_cases_lakh"], q=3, labels=["Manageable Docket", "High Caseload", "Severe Pendency Gridlock"])
    save_dataset(df, "d88_njdg_court_case_pendency")

def transform_d89_certin_cyber_incidents():
    df = pd.read_csv(os.path.join(RAW_DIR, "d89_certin_cyber_incidents_raw.csv"))
    df["ransomware_share_of_incidents_pct"] = ((df["ransomware_attacks_reported"] / df["total_cyber_security_incidents"]) * 100).round(3)
    df["phishing_share_pct"] = ((df["phishing_incidents_count"] / df["total_cyber_security_incidents"]) * 100).round(2)
    df["yoy_incident_surge_pct"] = (df["total_cyber_security_incidents"].pct_change().fillna(0) * 100).round(1)
    df["containment_velocity_index"] = (142.0 / df["avg_incident_containment_hours"]).round(2) # Improvement over 2012 baseline
    save_dataset(df, "d89_certin_cyber_incidents")

def transform_d90_mofpi_cold_storage_logistics():
    df = pd.read_csv(os.path.join(RAW_DIR, "d90_mofpi_cold_storage_logistics_raw.csv"))
    df["avg_capacity_per_project_mt"] = ((df["cold_storage_capacity_lakh_mt"] * 1e5) / df["cold_storage_projects_count"]).round(0)
    df["multi_commodity_capacity_lakh_mt"] = ((df["cold_storage_capacity_lakh_mt"] * df["multi_commodity_storage_share_pct"]) / 100).round(2)
    df["cold_chain_deficit_risk_tier"] = pd.cut(df["estimated_horticultural_loss_pct"], bins=[0, 15, 20, 35], labels=["Controlled Post-Harvest Loss", "Moderate Loss (15-20%)", "Critical Wastage (>20%)"])
    save_dataset(df, "d90_mofpi_cold_storage_logistics")

def transform_d91_fsi_wildfire_early_warning():
    df = pd.read_csv(os.path.join(RAW_DIR, "d91_fsi_wildfire_early_warning_raw.csv"))
    df["fire_alerts_per_100_sqkm_forest"] = ((df["annual_fire_alerts_count"] / df["forest_cover_sqkm"]) * 100).round(1)
    df["affected_forest_share_pct"] = ((df["forest_area_affected_hectares"] / (df["forest_cover_sqkm"] * 100)) * 100).round(2)
    df["fire_watcher_density_per_1000_ha"] = ((df["fire_watchers_deployed"] / df["forest_area_affected_hectares"]) * 1000).round(1)
    df["fire_risk_priority_tier"] = pd.qcut(df["annual_fire_alerts_count"], q=3, labels=["Low Fire Alert Frequency", "Moderate Season", "Critical Flame Front"])
    save_dataset(df, "d91_fsi_wildfire_early_warning")

def transform_d92_mohua_urban_rental_housing():
    df = pd.read_csv(os.path.join(RAW_DIR, "d92_mohua_urban_rental_housing_raw.csv"))
    df["rental_affordability_stress_ratio"] = (df["rent_to_income_burden_pct"] / 30.0).round(2) # 30% international benchmark
    df["arhc_coverage_of_deficit_pct"] = ((df["arhc_sanctioned_rental_units"] / df["urban_housing_deficit_units"]) * 100).round(2)
    df["vacant_to_deficit_absorption_pct"] = ((df["vacant_formal_houses_count"] / df["urban_housing_deficit_units"]) * 100).round(1)
    df["rental_stress_tier"] = pd.cut(df["rent_to_income_burden_pct"], bins=[0, 30, 40, 60], labels=["Affordable Market (<30%)", "Moderate Cost Burden", "Severe Rent Distress (>40%)"])
    save_dataset(df, "d92_mohua_urban_rental_housing")

def transform_d93_cmfri_marine_fisheries():
    df = pd.read_csv(os.path.join(RAW_DIR, "d93_cmfri_marine_fisheries_raw.csv"))
    df["msy_exploitation_status"] = df["maximum_sustainable_yield_ratio"].apply(lambda x: "Biologically Sustainable" if x < 1.0 else ("At Capacity Limit" if x == 1.0 else "Over-Exploited Stock"))
    df["juvenile_bycatch_volume_lakh_t"] = ((df["annual_fish_landings_lakh_tonnes"] * df["juvenile_bycatch_share_pct"]) / 100).round(2)
    df["export_earning_per_tonne_inr"] = ((df["export_value_inr_crore"] * 1e7) / (df["annual_fish_landings_lakh_tonnes"] * 1e5)).round(0)
    save_dataset(df, "d93_cmfri_marine_fisheries")

def transform_d94_telemanas_mental_health():
    df = pd.read_csv(os.path.join(RAW_DIR, "d94_telemanas_mental_health_raw.csv"))
    df["psychiatrist_deficit_vs_who_target"] = (3.0 - df["psychiatrists_per_100k_population"]).round(2) # WHO target 3 psychiatrists/100k
    df["unresolved_distress_calls_pct"] = (100.0 - df["call_distress_resolution_pct"]).round(1)
    df["anxiety_depression_calls_volume"] = ((df["total_telemanas_calls_received"] * df["anxiety_depression_calls_pct"]) / 100).round(0)
    df["mental_health_infrastructure_tier"] = pd.cut(df["psychiatrists_per_100k_population"], bins=[0, 0.5, 1.0, 3.0], labels=["Extreme Specialist Deficit (<0.5/100k)", "Moderate Deficit", "Adequate Coverage (>1.0/100k)"])
    save_dataset(df, "d94_telemanas_mental_health")

def run_all_part4_transformations():
    print("=== Transforming Decision-Oriented Datasets D75 to D94 ===")
    transform_d75_who_amr_surveillance()
    transform_d76_grid_india_frequency_stability()
    transform_d77_cpcb_municipal_solid_waste()
    transform_d78_cgwb_groundwater_stress()
    transform_d79_iea_critical_minerals()
    transform_d80_nha_hospital_bed_capacity()
    transform_d81_fao_wfp_food_security()
    transform_d82_morth_urban_traffic_congestion()
    transform_d83_nbtc_blood_bank_reserves()
    transform_d84_cpcb_cems_industrial_emissions()
    transform_d85_indian_railways_safety()
    transform_d86_bis_sovereign_debt_default_risk()
    transform_d87_mnre_offgrid_solar_reliability()
    transform_d88_njdg_court_case_pendency()
    transform_d89_certin_cyber_incidents()
    transform_d90_mofpi_cold_storage_logistics()
    transform_d91_fsi_wildfire_early_warning()
    transform_d92_mohua_urban_rental_housing()
    transform_d93_cmfri_marine_fisheries()
    transform_d94_telemanas_mental_health()
    print("=== Successfully Transformed All 20 Analytical Datasets (D75 to D94) ===")

if __name__ == "__main__":
    run_all_part4_transformations()
