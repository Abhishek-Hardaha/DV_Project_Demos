"""
Data Engineering Pipeline: Transform Part 3 Global Datasets (D55 to D74)
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

def transform_d55_iaea_nuclear_power():
    df = pd.read_csv(os.path.join(RAW_DIR, "d55_iaea_nuclear_power_raw.csv"))
    df["capacity_per_reactor_mwe"] = (df["total_net_capacity_mwe"] / df["operational_reactors"]).round(1)
    df["total_reactor_fleet_experience"] = (df["operational_reactors"] * df["mean_reactor_age_years"]).round(1)
    df["generation_intensity_per_gw"] = ((df["cumulative_generation_twh"] * 1000) / df["total_net_capacity_mwe"]).round(2)
    df["nuclear_power_tier"] = pd.qcut(df["total_net_capacity_mwe"], q=3, labels=["Emerging / Small Fleet", "Substantial Fleet", "Dominant Fleet"])
    save_dataset(df, "d55_iaea_nuclear_power")

def transform_d56_nasa_exoplanets():
    df = pd.read_csv(os.path.join(RAW_DIR, "d56_nasa_exoplanets_raw.csv"))
    df["transit_share_pct"] = ((df["transit_method_cumulative"] / df["total_confirmed_cumulative"]) * 100).round(1)
    df["habitable_share_pct"] = ((df["habitable_zone_candidates"] / df["total_confirmed_cumulative"]) * 100).round(2)
    df["rocky_and_super_earth_count"] = df["terrestrial_rocky_count"] + df["super_earths_count"]
    df["annual_new_discoveries"] = df["total_confirmed_cumulative"].diff().fillna(df["total_confirmed_cumulative"].iloc[0]).astype(int)
    save_dataset(df, "d56_nasa_exoplanets")

def transform_d57_unhcr_forced_displacement():
    df = pd.read_csv(os.path.join(RAW_DIR, "d57_unhcr_forced_displacement_raw.csv"))
    df["idp_share_of_total_pct"] = ((df["idps_conflict_millions"] / df["total_displaced_millions"]) * 100).round(1)
    df["refugee_share_of_total_pct"] = ((df["refugees_under_unhcr_millions"] / df["total_displaced_millions"]) * 100).round(1)
    df["children_displaced_millions"] = ((df["total_displaced_millions"] * df["children_pct_displaced"]) / 100).round(2)
    df["annual_displacement_delta_millions"] = df["total_displaced_millions"].diff().fillna(0).round(2)
    save_dataset(df, "d57_unhcr_forced_displacement")

def transform_d58_nist_nvd_cybersecurity():
    df = pd.read_csv(os.path.join(RAW_DIR, "d58_nist_nvd_cybersecurity_raw.csv"))
    df["critical_plus_high_count"] = df["critical_severity_count"] + df["high_severity_count"]
    df["critical_high_share_pct"] = ((df["critical_plus_high_count"] / df["total_cves_published"]) * 100).round(1)
    df["cisa_kev_exploitation_rate_pct"] = ((df["exploited_in_wild_cisa_kev"] / df["total_cves_published"]) * 100).round(2)
    df["yoy_cve_growth_rate_pct"] = (df["total_cves_published"].pct_change().fillna(0) * 100).round(1)
    save_dataset(df, "d58_nist_nvd_cybersecurity")

def transform_d59_nsidc_arctic_sea_ice():
    df = pd.read_csv(os.path.join(RAW_DIR, "d59_nsidc_arctic_sea_ice_raw.csv"))
    df["global_polar_minimum_sqkm"] = (df["arctic_september_minimum_million_sqkm"] + df["antarctic_february_minimum_million_sqkm"]).round(2)
    df["seasonal_arctic_melt_range_sqkm"] = (df["arctic_march_maximum_million_sqkm"] - df["arctic_september_minimum_million_sqkm"]).round(2)
    df["arctic_loss_vs_1980_pct"] = (((df["arctic_september_minimum_million_sqkm"] - 7.67) / 7.67) * 100).round(1)
    df["cryosphere_vulnerability_tier"] = pd.qcut(df["arctic_september_minimum_million_sqkm"], q=3, labels=["Severe Contraction", "Moderate Loss", "Historical Baseline"])
    save_dataset(df, "d59_nsidc_arctic_sea_ice")

def transform_d60_icao_commercial_aviation():
    df = pd.read_csv(os.path.join(RAW_DIR, "d60_icao_commercial_aviation_raw.csv"))
    df["passengers_per_flight_avg"] = ((df["global_passengers_billion"] * 1e9) / (df["scheduled_flights_million"] * 1e6)).round(1)
    df["revenue_per_passenger_usd"] = ((df["airline_industry_operating_revenue_usd_billion"] * 1e9) / (df["global_passengers_billion"] * 1e9)).round(1)
    df["rpk_per_passenger_km"] = ((df["revenue_passenger_km_trillion"] * 1e12) / (df["global_passengers_billion"] * 1e9)).round(0)
    df["fuel_intensity_per_1000_rpk"] = ((df["jet_fuel_consumption_million_barrels"] * 1e6) / (df["revenue_passenger_km_trillion"] * 1e9)).round(2)
    save_dataset(df, "d60_icao_commercial_aviation")

def transform_d61_wgc_sovereign_gold_reserves():
    df = pd.read_csv(os.path.join(RAW_DIR, "d61_wgc_sovereign_gold_reserves_raw.csv"))
    df["usd_value_per_tonne_million"] = ((df["market_value_usd_billion"] * 1000) / df["official_gold_holdings_tonnes"]).round(2)
    df["sovereign_gold_share_of_global_pct"] = ((df["official_gold_holdings_tonnes"] / df["official_gold_holdings_tonnes"].sum()) * 100).round(2)
    df["gold_intensity_tier"] = pd.qcut(df["gold_share_total_forex_reserves_pct"], q=3, labels=["Low Allocation (<15%)", "Balanced Allocation", "Heavy Strategic Anchor (>60%)"])
    save_dataset(df, "d61_wgc_sovereign_gold_reserves")

def transform_d62_unesco_world_heritage_sites():
    df = pd.read_csv(os.path.join(RAW_DIR, "d62_unesco_world_heritage_sites_raw.csv"))
    df["cultural_share_pct"] = ((df["cultural_sites_count"] / df["total_heritage_sites"]) * 100).round(1)
    df["natural_share_pct"] = ((df["natural_sites_count"] / df["total_heritage_sites"]) * 100).round(1)
    df["global_heritage_site_share_pct"] = ((df["total_heritage_sites"] / df["total_heritage_sites"].sum()) * 100).round(2)
    df["heritage_density_tier"] = pd.qcut(df["total_heritage_sites"], q=3, labels=["Developing Heritage", "Established Portfolio", "Global Heavyweight"])
    save_dataset(df, "d62_unesco_world_heritage_sites")

def transform_d63_sia_wsts_semiconductor_market():
    df = pd.read_csv(os.path.join(RAW_DIR, "d63_sia_wsts_semiconductor_market_raw.csv"))
    df["asia_pacific_market_share_pct"] = ((df["asia_pacific_sales_billion"] / df["total_semiconductor_sales_billion_usd"]) * 100).round(1)
    df["americas_market_share_pct"] = ((df["americas_sales_billion"] / df["total_semiconductor_sales_billion_usd"]) * 100).round(1)
    df["logic_memory_combined_share_pct"] = (((df["logic_chips_sales_billion"] + df["memory_chips_sales_billion"]) / df["total_semiconductor_sales_billion_usd"]) * 100).round(1)
    df["yoy_market_expansion_pct"] = (df["total_semiconductor_sales_billion_usd"].pct_change().fillna(0) * 100).round(1)
    save_dataset(df, "d63_sia_wsts_semiconductor_market")

def transform_d64_who_unicef_immunization():
    df = pd.read_csv(os.path.join(RAW_DIR, "d64_who_unicef_immunization_raw.csv"))
    df["vaccine_equity_gap_mcv1_vs_mcv2"] = (df["measles_mcv1_coverage_pct"] - df["measles_mcv2_second_dose_pct"]).round(1)
    df["composite_core_vaccination_index"] = ((df["dtp3_coverage_pct"] + df["measles_mcv1_coverage_pct"] + df["polio_pol3_coverage_pct"]) / 3).round(1)
    df["zero_dose_children_reduction_pct"] = (((22.4 - df["unvaccinated_zero_dose_children_millions"]) / 22.4) * 100).round(1)
    save_dataset(df, "d64_who_unicef_immunization")

def transform_d65_noaa_ocean_heat_content():
    df = pd.read_csv(os.path.join(RAW_DIR, "d65_noaa_ocean_heat_content_raw.csv"))
    df["deep_ocean_heat_700_2000m_zj"] = (df["ocean_heat_content_0_2000m_zettajoules"] - df["ocean_heat_content_0_700m_zettajoules"]).round(1)
    df["upper_ocean_heat_share_pct"] = ((df["ocean_heat_content_0_700m_zettajoules"] / df["ocean_heat_content_0_2000m_zettajoules"]) * 100).round(1)
    df["cumulative_thermal_expansion_index"] = ((df["ocean_heat_content_0_2000m_zettajoules"] + 28.5) / 4.4).round(1)
    save_dataset(df, "d65_noaa_ocean_heat_content")

def transform_d66_ioc_olympic_games_history():
    df = pd.read_csv(os.path.join(RAW_DIR, "d66_ioc_olympic_games_history_raw.csv"))
    df["athletes_per_nation_avg"] = (df["participating_athletes"] / df["participating_nations"]).round(1)
    df["athletes_per_event_avg"] = (df["participating_athletes"] / df["total_events_contested"]).round(1)
    df["gender_parity_gap_pct"] = (50.0 - df["female_athlete_share_pct"]).round(1)
    save_dataset(df, "d66_ioc_olympic_games_history")

def transform_d67_unctad_maritime_merchant_fleet():
    df = pd.read_csv(os.path.join(RAW_DIR, "d67_unctad_maritime_merchant_fleet_raw.csv"))
    df["bulk_plus_tanker_share_pct"] = (((df["bulk_carriers_dwt_million"] + df["oil_tankers_dwt_million"]) / df["world_fleet_deadweight_tonnage_million"]) * 100).round(1)
    df["container_share_pct"] = ((df["container_ships_dwt_million"] / df["world_fleet_deadweight_tonnage_million"]) * 100).round(1)
    df["carrying_capacity_per_ton_trade"] = ((df["world_fleet_deadweight_tonnage_million"] * 1e6) / (df["seaborne_trade_volume_billion_tons"] * 1e9)).round(2)
    save_dataset(df, "d67_unctad_maritime_merchant_fleet")

def transform_d68_emdat_natural_disasters():
    df = pd.read_csv(os.path.join(RAW_DIR, "d68_emdat_natural_disasters_raw.csv"))
    df["hydrometeorological_share_pct"] = (((df["flood_events_count"] + df["storm_cyclone_events_count"]) / df["total_recorded_disasters"]) * 100).round(1)
    df["economic_damage_per_event_million_usd"] = ((df["total_economic_damages_billion_usd"] * 1000) / df["total_recorded_disasters"]).round(1)
    df["fatalities_per_event_avg"] = ((df["total_fatalities_thousands"] * 1000) / df["total_recorded_disasters"]).round(1)
    save_dataset(df, "d68_emdat_natural_disasters")

def transform_d69_oecd_pisa_education():
    df = pd.read_csv(os.path.join(RAW_DIR, "d69_oecd_pisa_education_raw.csv"))
    df["math_reading_gap"] = (df["mathematics_score_mean"] - df["reading_score_mean"]).round(1)
    df["performance_ratio_high_to_low"] = (df["high_performing_students_pct"] / df["low_performing_students_pct"]).round(2)
    df["expenditure_efficiency_points_per_10k_usd"] = ((df["composite_pisa_average"] / df["education_expenditure_per_student_usd"]) * 10000).round(1)
    df["academic_tier"] = pd.qcut(df["composite_pisa_average"], q=3, labels=["Foundational System", "OECD Baseline", "Top Global Performer"])
    save_dataset(df, "d69_oecd_pisa_education")

def transform_d70_iucn_red_list_biodiversity():
    df = pd.read_csv(os.path.join(RAW_DIR, "d70_iucn_red_list_biodiversity_raw.csv"))
    df["threatened_share_of_assessed_pct"] = ((df["total_threatened_species"] / df["total_assessed_species"]) * 100).round(1)
    df["critically_endangered_share_pct"] = ((df["critically_endangered_species"] / df["total_threatened_species"]) * 100).round(1)
    df["annual_assessed_species_growth"] = df["total_assessed_species"].diff().fillna(df["total_assessed_species"].iloc[0]).astype(int)
    save_dataset(df, "d70_iucn_red_list_biodiversity")

def transform_d71_faostat_fertilizer_nutrients():
    df = pd.read_csv(os.path.join(RAW_DIR, "d71_faostat_fertilizer_nutrients_raw.csv"))
    df["nitrogen_share_of_total_pct"] = ((df["nitrogen_n_million_tonnes"] / df["total_nutrient_consumption_million_tonnes"]) * 100).round(1)
    df["npk_ratio_p_to_n"] = (df["phosphorus_p2o5_million_tonnes"] / df["nitrogen_n_million_tonnes"]).round(2)
    df["cereal_yield_per_nutrient_tonne"] = ((df["cereal_grain_production_billion_tonnes"] * 1000) / df["total_nutrient_consumption_million_tonnes"]).round(2)
    save_dataset(df, "d71_faostat_fertilizer_nutrients")

def transform_d72_unoosa_orbital_space_launches():
    df = pd.read_csv(os.path.join(RAW_DIR, "d72_unoosa_orbital_space_launches_raw.csv"))
    df["payloads_per_launch_density"] = (df["payloads_placed_in_orbit"] / df["successful_orbital_launches"]).round(1)
    df["commercial_payload_share_pct"] = ((df["commercial_satellite_payloads"] / df["payloads_placed_in_orbit"]) * 100).round(1)
    df["us_launch_share_pct"] = ((df["united_states_launches"] / df["total_orbital_launches"]) * 100).round(1)
    save_dataset(df, "d72_unoosa_orbital_space_launches")

def transform_d73_energy_institute_world_energy():
    df = pd.read_csv(os.path.join(RAW_DIR, "d73_energy_institute_world_energy_raw.csv"))
    df["clean_power_combined_exajoules"] = (df["renewables_wind_solar_exajoules"] + df["hydroelectricity_exajoules"] + df["nuclear_energy_exajoules"]).round(1)
    df["clean_power_share_total_pct"] = ((df["clean_power_combined_exajoules"] / df["total_primary_energy_exajoules"]) * 100).round(1)
    df["coal_oil_combined_share_pct"] = (((df["coal_consumption_exajoules"] + df["oil_consumption_exajoules"]) / df["total_primary_energy_exajoules"]) * 100).round(1)
    save_dataset(df, "d73_energy_institute_world_energy")

def transform_d74_un_sdsn_world_happiness():
    df = pd.read_csv(os.path.join(RAW_DIR, "d74_un_sdsn_world_happiness_raw.csv"))
    df["economic_and_social_synergy_score"] = (df["gdp_per_capita_purchasing_power_parity"] + df["social_support_index"]).round(3)
    df["governance_trust_index"] = (df["freedom_to_make_life_choices_score"] + df["perceptions_of_corruption_score"]).round(3)
    df["happiness_ranking_tier"] = pd.qcut(df["happiness_cantril_ladder_score"], q=3, labels=["Emerging Well-Being", "Moderate Well-Being", "High Flourishing"])
    save_dataset(df, "d74_un_sdsn_world_happiness")

def run_all_part3_transformations():
    print("=== Transforming Global Datasets D55 to D74 ===")
    transform_d55_iaea_nuclear_power()
    transform_d56_nasa_exoplanets()
    transform_d57_unhcr_forced_displacement()
    transform_d58_nist_nvd_cybersecurity()
    transform_d59_nsidc_arctic_sea_ice()
    transform_d60_icao_commercial_aviation()
    transform_d61_wgc_sovereign_gold_reserves()
    transform_d62_unesco_world_heritage_sites()
    transform_d63_sia_wsts_semiconductor_market()
    transform_d64_who_unicef_immunization()
    transform_d65_noaa_ocean_heat_content()
    transform_d66_ioc_olympic_games_history()
    transform_d67_unctad_maritime_merchant_fleet()
    transform_d68_emdat_natural_disasters()
    transform_d69_oecd_pisa_education()
    transform_d70_iucn_red_list_biodiversity()
    transform_d71_faostat_fertilizer_nutrients()
    transform_d72_unoosa_orbital_space_launches()
    transform_d73_energy_institute_world_energy()
    transform_d74_un_sdsn_world_happiness()
    print("=== Successfully Transformed All 20 Global Analytical Datasets (D55 to D74) ===")

if __name__ == "__main__":
    run_all_part3_transformations()
