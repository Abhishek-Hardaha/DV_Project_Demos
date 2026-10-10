"""
Helper script to update scripts/build_dashboards.py with high-diversity visual recipes
and execute the build across all 34 dashboard modules.
"""

import os
import re

BUILD_DASHBOARDS_PATH = os.path.join(os.path.dirname(__file__), "build_dashboards.py")

NEW_CHARTS_BY_ID = {
    "D01": [
        ("line", "year", ["gdp_current_trillion_usd"], "India Nominal GDP Expansion Trajectory ($ Trillion)", "Year", "USD Trillions"),
        ("area", "year", ["agriculture_gva_pct", "industry_gva_pct", "services_gva_pct"], "Sectoral GVA Composition Over Time (%)", "Year", "GVA Share (%)"),
        ("scatter", "gross_capital_formation_pct", "gdp_growth_pct", "Capital Formation vs Real GDP Growth Correlation", "Gross Capital Formation (% of GDP)", "Real GDP Growth (%)"),
        ("horizontal_bar", "gdp_per_capita_usd", "year", "Per Capita GDP Trajectory Milestones ($)", "USD / Capita", "Year"),
        ("correlation_heatmap", ["gdp_growth_pct", "services_gva_pct", "gross_capital_formation_pct", "inflation_cpi_pct", "gdp_per_capita_usd"], None, "Macroeconomic Indicator Pearson Correlation Matrix"),
        ("histogram", "gdp_growth_pct", None, "Real GDP Growth Rate Frequency Distribution (%)", "Annual GDP Growth (%)", "Frequency Count"),
        ("radar", ["gdp_growth_pct", "services_gva_pct", "gross_capital_formation_pct", "inflation_cpi_pct"], None, "Latest Macroeconomic Profile Polar Radar Scan")
    ],
    "D02": [
        ("line", "date", ["headline_cpi_yoy", "rbi_repo_rate", "target_band_mid", "target_band_upper", "target_band_lower"], "Headline CPI vs RBI Policy Corridor & Tolerance Bands (%)", "Date", "Rate (%)"),
        ("bar", "date", "real_policy_rate", "Real Policy Rate Evolution (Repo minus CPI %)", "Date", "Real Rate (% pts)"),
        ("scatter", "headline_cpi_yoy", "rbi_repo_rate", "Monetary Reaction Function: CPI vs Repo Rate", "Headline CPI (%)", "RBI Repo Rate (%)"),
        ("violin", None, "food_inflation_yoy", "Food Inflation Volatility Dispersion & Jitter", "Spread", "YoY %"),
        ("correlation_heatmap", ["headline_cpi_yoy", "food_inflation_yoy", "fuel_inflation_yoy", "core_cpi_yoy", "rbi_repo_rate", "real_policy_rate"], None, "Inflation Dynamics & Policy Rate Correlation Matrix"),
        ("density_heatmap", "headline_cpi_yoy", "food_inflation_yoy", "Headline vs Food Inflation 2D Density Heatmap", "Headline CPI (%)", "Food Inflation (%)"),
        ("horizontal_bar", "food_fuel_spread", "year", "Food vs Fuel Inflation Spread by Annual Regime", "Spread (% pts)", "Year")
    ],
    "D03": [
        ("horizontal_bar", "pop_2011_millions", "state", "State & UT Population Scale (Millions)", "Population (M)", "State"),
        ("bar", "state", "literacy_pct", "State Literacy Rate Ranking (%)", "State", "Literacy Rate (%)"),
        ("treemap", ["urbanization_category", "state"], "pop_2011_millions", "Population Distribution by Urbanization Category", None, None),
        ("sunburst", ["urbanization_category", "state"], "pop_2011_millions", "Hierarchical Demographic Partitioning", None, None),
        ("scatter", "urban_pct", "literacy_pct", "Urbanization vs Literacy Rate Correlation", "Urban Population (%)", "Literacy Rate (%)"),
        ("violin", "urbanization_category", "sex_ratio", "Sex Ratio Distribution by Urbanization Tier", "Tier", "Sex Ratio"),
        ("histogram", "growth_pct", None, "Decadal Population Growth Rate Distribution (%)", "Decadal Growth (%)", "State Count")
    ],
    "D04": [
        ("bar", "state", "inst_births_pct", "Institutional Deliveries by State (%)", "State", "Institutional Births (%)"),
        ("horizontal_bar", "stunting_pct", "state", "Under-5 Child Stunting Prevalence Ranking (%)", "Stunting Rate (%)", "State"),
        ("treemap", ["health_performance_tier", "state"], "sanitation_pct", "Health Infrastructure Performance Tiers", None, None),
        ("scatter", "sanitation_pct", "stunting_pct", "Household Sanitation vs Child Stunting Reduction", "Sanitation (%)", "Child Stunting (%)"),
        ("correlation_heatmap", ["inst_births_pct", "immunization_pct", "stunting_pct", "anemia_women_pct", "sanitation_pct"], None, "Maternal & Child Health Metric Correlations"),
        ("violin", "health_performance_tier", "anemia_women_pct", "Female Anemia Distribution across Health Tiers", "Performance Tier", "Anemia (%)"),
        ("funnel", "inst_births_pct", "state", "State Maternal Care Transition Funnel Profile")
    ],
    "D05": [
        ("line", "crop_year", ["total_foodgrains_mt", "rolling_3yr_prod_mt"], "Total Foodgrain Production & 3-Year Rolling Trajectory (MT)", "Crop Year", "Production (MT)"),
        ("area", "crop_year", ["rice_mt", "wheat_mt", "pulses_mt", "coarse_cereals_mt"], "Cereal & Pulse Production Composition (Million Tonnes)", "Crop Year", "Million Tonnes"),
        ("bar", "crop_year", ["rice_yield_kg_ha", "wheat_yield_kg_ha"], "Staple Crop Yield Evolution (Kg/Hectare)", "Crop Year", "Yield (Kg/Ha)"),
        ("scatter", "foodgrains_area_mha", "total_foodgrains_mt", "Cultivated Land Area vs Harvest Output", "Area (Million Hectares)", "Production (MT)"),
        ("horizontal_bar", "foodgrains_yield_kg_ha", "crop_year", "Composite Foodgrain Yield Progression (Kg/Ha)", "Yield (Kg/Ha)", "Crop Year"),
        ("histogram", "foodgrain_growth_yoy_pct", None, "Annual Foodgrain Growth Volatility Distribution (%)", "YoY Growth (%)", "Frequency Count"),
        ("correlation_heatmap", ["total_foodgrains_mt", "foodgrains_yield_kg_ha", "rice_mt", "wheat_mt", "pulses_mt", "oilseeds_mt"], None, "Crop Harvest & Productivity Correlation Matrix")
    ],
    "D06": [
        ("area", "year", ["thermal_gw", "hydro_gw", "nuclear_gw", "solar_gw", "wind_gw"], "Installed Power Generation Capacity by Energy Source (GW)", "Year", "Capacity (GW)"),
        ("line", "year", ["clean_capacity_share_pct", "solar_wind_share_pct"], "Clean Energy Capacity Share Progression (%)", "Year", "Share (%)"),
        ("horizontal_bar", "total_clean_gw", "year", "Clean Capacity Expansion Milestones (GW)", "Clean Power (GW)", "Year"),
        ("scatter", "solar_gw", "total_generation_bu", "Solar Capacity Expansion vs National Gross Generation", "Solar Capacity (GW)", "Generation (Billion Units)"),
        ("radar", ["thermal_gw", "hydro_gw", "nuclear_gw", "solar_gw", "wind_gw"], None, "Current Power Generation Mix Profile (GW)"),
        ("violin", None, "solar_wind_growth_yoy_gw", "Annual Solar & Wind Capacity Addition Distribution (GW)", "Distribution", "GW Added"),
        ("correlation_heatmap", ["total_installed_gw", "solar_gw", "wind_gw", "clean_capacity_share_pct", "total_generation_bu"], None, "Energy Transition Matrix Correlations")
    ],
    "D07": [
        ("line", "fiscal_year", ["merchandise_exports_usd_b", "merchandise_imports_usd_b"], "Merchandise Exports vs Imports Trajectory ($ Billion)", "Fiscal Year", "USD Billions"),
        ("area", "fiscal_year", ["engineering_goods_usd_b", "petroleum_products_usd_b", "gems_jewellery_usd_b", "pharma_drugs_usd_b", "electronic_goods_usd_b"], "Export Basket Major Sector Composition ($ Billion)", "Fiscal Year", "USD Billions"),
        ("bar", "fiscal_year", "trade_balance_usd_b", "Annual Merchandise Trade Balance ($ Billion)", "Fiscal Year", "USD Billions"),
        ("scatter", "crude_oil_import_usd_b", "trade_balance_usd_b", "Crude Oil Import Bill vs Trade Balance Deficit", "Crude Oil Imports ($ B)", "Trade Balance ($ B)"),
        ("horizontal_bar", "total_trade_usd_b", "fiscal_year", "Total Merchandise Trade Turnover Progression ($ B)", "USD Billions", "Fiscal Year"),
        ("histogram", "export_growth_yoy_pct", None, "Export YoY Growth Rate Distribution (%)", "YoY Growth (%)", "Frequency Count"),
        ("radar", ["engineering_goods_usd_b", "petroleum_products_usd_b", "gems_jewellery_usd_b", "pharma_drugs_usd_b", "electronic_goods_usd_b"], None, "Major Export Commodity Value Profile ($ B)")
    ],
    "D08": [
        ("line", "fiscal_year", ["total_fdi_usd_b", "fdi_3yr_moving_avg_b"], "Annual Total FDI Inflow Trajectory ($ Billion)", "Fiscal Year", "USD Billions"),
        ("area", "fiscal_year", ["computer_software_hardware_m", "services_financial_banking_m", "telecommunications_m", "automobile_industry_m", "construction_infrastructure_m"], "Sectoral FDI Equity Inflows Breakdown ($ Million)", "Fiscal Year", "USD Millions"),
        ("horizontal_bar", "tech_services_fdi_usd_m", "fiscal_year", "Technology & Services FDI Inflows Progression ($ M)", "USD Millions", "Fiscal Year"),
        ("scatter", "computer_software_hardware_m", "total_fdi_usd_m", "Computer Software & Hardware vs Total FDI Inflows", "Software/Hardware ($ M)", "Total FDI ($ M)"),
        ("correlation_heatmap", ["total_fdi_usd_m", "computer_software_hardware_m", "services_financial_banking_m", "telecommunications_m", "tech_services_share_pct"], None, "Sectoral FDI Inflow Correlation Matrix"),
        ("violin", None, "fdi_yoy_growth_pct", "Annual FDI Growth Rate Dispersion (%)", "Dispersion", "YoY Growth (%)"),
        ("radar", ["computer_software_hardware_m", "services_financial_banking_m", "telecommunications_m", "automobile_industry_m", "pharma_drugs_m"], None, "Priority Sector FDI Capital Allocation Profile ($ M)")
    ],
    "D09": [
        ("line", "year", ["nh_total_length_km"], "Cumulative National Highway Network Length (KM)", "Year", "Total KM"),
        ("bar", "year", "construction_pace_km_day", "Daily Highway Construction Velocity (KM/Day)", "Year", "KM / Day"),
        ("area", "year", ["four_lane_plus_pct", "two_lane_pct", "single_intermediate_lane_pct"], "Highway Lane Configuration Composition (%)", "Year", "Lane Share (%)"),
        ("scatter", "capital_outlay_inr_cr", "construction_pace_km_day", "Budgetary Capital Outlay vs Construction Pace", "Capital Outlay (INR Cr)", "Pace (KM/Day)"),
        ("horizontal_bar", "capital_outlay_inr_cr", "year", "Annual Highway Ministry Capital Outlay (INR Crore)", "INR Crores", "Year"),
        ("histogram", "nh_added_in_year_km", None, "Annual Network Additions Distribution (KM)", "KM Added", "Frequency Count"),
        ("correlation_heatmap", ["nh_total_length_km", "nh_added_in_year_km", "construction_pace_km_day", "capital_outlay_inr_cr", "four_lane_plus_pct"], None, "Highway Infrastructure & Expenditure Correlations")
    ],
    "D10": [
        ("line", "year", ["total_freight_loading_mt"], "Total Railway Freight Loading Throughput (Million Tonnes)", "Year", "Million Tonnes"),
        ("area", "year", ["coal_freight_mt", "iron_ore_mt", "cement_mt", "steel_pig_iron_mt", "foodgrains_mt"], "Bulk Commodity Haulage Composition (MT)", "Year", "Million Tonnes"),
        ("bar", "year", "electrification_pct", "Broad Gauge Route Electrification Pace (%)", "Year", "Electrification (%)"),
        ("scatter", "total_freight_loading_mt", "operating_ratio_pct", "Freight Throughput Volume vs Financial Operating Ratio", "Freight Loading (MT)", "Operating Ratio (%)"),
        ("horizontal_bar", "coal_freight_mt", "year", "Coal Freight Haulage Progression (Million Tonnes)", "Million Tonnes", "Year"),
        ("violin", None, "operating_ratio_pct", "Railway Operating Ratio Dispersion (%)", "Dispersion", "Operating Ratio (%)"),
        ("radar", ["coal_freight_mt", "iron_ore_mt", "cement_mt", "steel_pig_iron_mt", "fertilizers_mt"], None, "Major Freight Commodity Throughput Profile (MT)")
    ],
    "D11": [
        ("geo_scatter", "latitude", "longitude", "National Continuous Ambient Air Quality Telemetry Stations", "cpcb_aqi", "cpcb_aqi", "city", "asia"),
        ("bar", "city", "cpcb_aqi", "Ambient Air Quality Index (CPCB AQI) by City", "City", "CPCB AQI"),
        ("horizontal_bar", "pm2_5", "city", "Fine Particulate Matter PM2.5 Concentrations (µg/m³)", "PM2.5 (µg/m³)", "City"),
        ("scatter", "pm2_5", "pm10", "PM2.5 vs PM10 Particulate Co-Movement Correlation", "PM2.5 (µg/m³)", "PM10 (µg/m³)"),
        ("correlation_heatmap", ["pm2_5", "pm10", "no2", "so2", "co", "ozone", "cpcb_aqi"], None, "Atmospheric Pollutants Pearson Correlation Matrix"),
        ("violin", "aqi_category", "cpcb_aqi", "AQI Severity Dispersion Across Air Quality Categories", "Category", "AQI"),
        ("treemap", ["state", "city"], "cpcb_aqi", "Air Quality Station Hierarchy by State and City", None, None)
    ],
    "D12": [
        ("line", "date", ["volume_billions"], "Monthly UPI Transaction Volume (Billions)", "Date", "Transactions (Billions)"),
        ("bar", "date", "value_inr_lakh_crore", "Gross Settlement Value (Lakh Crore INR)", "Date", "INR Lakh Crore"),
        ("area", "date", ["p2p_share_pct", "p2m_merchant_share_pct"], "UPI Channel Mix: P2P Person-to-Person vs P2M Merchant (%)", "Date", "Channel Share (%)"),
        ("scatter", "volume_billions", "avg_ticket_size_inr", "Transaction Volume Scale vs Average Ticket Size", "Volume (Billions)", "Ticket Size (INR)"),
        ("horizontal_bar", "value_inr_crore", "date", "Monthly Gross Value Progression (INR Crore)", "INR Crores", "Date"),
        ("histogram", "vol_mom_growth_pct", None, "Month-over-Month Transaction Volume Growth Distribution (%)", "MoM Growth (%)", "Frequency Count"),
        ("density_heatmap", "volume_billions", "value_inr_lakh_crore", "Transaction Volume vs Settlement Value 2D Density", "Volume (Billions)", "Value (Lakh Cr INR)")
    ],
    "D13": [
        ("horizontal_bar", "fiscal_deficit_gsdp_pct", "state", "Gross Fiscal Deficit to GSDP Ratio by State (%)", "Fiscal Deficit (% GSDP)", "State"),
        ("bar", "state", "debt_gsdp_pct", "Sub-National Debt-to-GSDP Burden Ranking (%)", "State", "Debt (% GSDP)"),
        ("scatter", "capital_outlay_pct_exp", "debt_gsdp_pct", "Capital Outlay Capex Share vs Debt-to-GSDP Burden", "Capital Outlay (% of Exp)", "Debt (% GSDP)"),
        ("correlation_heatmap", ["fiscal_deficit_gsdp_pct", "debt_gsdp_pct", "own_tax_revenue_share_pct", "capital_outlay_pct_exp", "fiscal_prudence_score"], None, "Subnational Fiscal Indicators Correlation Matrix"),
        ("violin", None, "fiscal_deficit_gsdp_pct", "State Fiscal Deficit Dispersion & Quartile Spread", "Dispersion", "Fiscal Deficit (% GSDP)"),
        ("histogram", "own_tax_revenue_share_pct", None, "Own Tax Revenue Share Distribution (%)", "Own Tax Share (%)", "State Count"),
        ("funnel", "fiscal_prudence_score", "state", "Fiscal Prudence Score Hierarchy Across States")
    ],
    "D14": [
        ("bar", "state", "ger_total", "Higher Education Gross Enrollment Ratio (GER) by State (%)", "State", "GER (%)"),
        ("horizontal_bar", "gpi", "state", "Gender Parity Index (GPI) in Higher Education", "Gender Parity Index", "State"),
        ("scatter", "colleges_per_lakh_pop", "ptr", "College Institutional Density vs Pupil-Teacher Ratio (PTR)", "Colleges per Lakh Pop", "Pupil-Teacher Ratio"),
        ("correlation_heatmap", ["ger_total", "ger_male", "ger_female", "gpi", "colleges_per_lakh_pop", "ptr"], None, "AISHE Educational Indicators Correlation Matrix"),
        ("violin", None, "ger_total", "State Gross Enrollment Ratio Distribution (%)", "Distribution", "GER (%)"),
        ("histogram", "ptr", None, "Pupil-Teacher Ratio (PTR) Frequency Distribution", "Pupil-Teacher Ratio", "State Count"),
        ("radar", ["ger_total", "ger_female", "gpi", "colleges_per_lakh_pop", "capacity_adequacy_ratio"], None, "National Higher Education Key Metrics Profile")
    ],
    "D15": [
        ("line", "survey_round", ["lfpr_total", "wpr_total"], "Labor Force Participation (LFPR) & Worker Pop Ratio (WPR) Trajectory (%)", "Survey Round", "Rate (%)"),
        ("area", "survey_round", ["agri_share", "industry_share", "services_share"], "Sectoral Workforce Employment Share Composition (%)", "Survey Round", "Share (%)"),
        ("bar", "survey_round", ["ur_urban_male", "ur_urban_female", "ur_rural_male", "ur_rural_female"], "Unemployment Rate Disaggregated by Gender & Sector (%)", "Survey Round", "Unemployment (%)"),
        ("scatter", "female_lfpr_gap", "ur_total", "Gender Participation Gap vs Overall Unemployment Rate", "Female LFPR Gap (% pts)", "Unemployment (%)"),
        ("horizontal_bar", "urban_rural_ur_gap", "survey_round", "Urban vs Rural Unemployment Gap Spread (% pts)", "Gap (% pts)", "Survey Round"),
        ("correlation_heatmap", ["lfpr_total", "lfpr_male", "lfpr_female", "wpr_total", "ur_total", "agri_share", "services_share"], None, "Employment & Labor Market Dynamics Correlation Matrix"),
        ("radar", ["lfpr_total", "wpr_total", "agri_share", "industry_share", "services_share"], None, "Latest Employment Structure Profile Scan")
    ],
    "D16": [
        ("area", "year", ["coal_twh", "gas_twh", "hydro_twh", "nuclear_twh", "solar_twh", "wind_twh"], "Global Power Generation Fuel Source Mix Evolution (TWh)", "Year", "Generation (TWh)"),
        ("line", "year", ["clean_share_pct", "solar_wind_share_pct"], "Clean & Renewable Generation Share Trajectory (%)", "Year", "Share (%)"),
        ("bar", "country", "renewable_power_twh", "Renewable Generation Volume Comparison by Country (TWh)", "Country", "TWh"),
        ("scatter", "solar_twh", "clean_share_pct", "Solar Power Generation vs Clean Share Expansion", "Solar Power (TWh)", "Clean Share (%)"),
        ("horizontal_bar", "clean_power_twh", "country", "Clean Power Generation Volume Ranking by Country (TWh)", "Clean Power (TWh)", "Country"),
        ("sunburst", ["country", "year"], "clean_power_twh", "Clean Generation Allocation by Country and Period", None, None),
        ("correlation_heatmap", ["coal_twh", "gas_twh", "solar_twh", "wind_twh", "clean_share_pct", "total_generation_twh"], None, "Power Generation Matrix Correlation Heatmap")
    ],
    "D17": [
        ("line", "year", ["co2_emissions_gt"], "Global Territorial Carbon Dioxide Emissions (Gigatonnes)", "Year", "Billion Tonnes CO2"),
        ("area", "year", ["coal_share_pct", "oil_share_pct", "gas_share_pct", "cement_flaring_share_pct"], "Fossil Fuel Source Share of Emissions (%)", "Year", "Share (%)"),
        ("horizontal_bar", "co2_per_capita_tonnes", "country", "Per Capita CO2 Emissions Intensity by Nation (Tonnes/Capita)", "Tonnes CO2 / Person", "Country"),
        ("scatter", "co2_per_capita_tonnes", "co2_emissions_mt", "Per Capita Emissions vs Total National Emissions", "Per Capita CO2 (Tonnes)", "Total CO2 (MT)"),
        ("violin", None, "co2_per_capita_tonnes", "Global Per Capita Carbon Emissions Dispersion", "Distribution", "Tonnes/Person"),
        ("histogram", "emissions_growth_yoy_pct", None, "Annual Emissions Growth Volatility Distribution (%)", "YoY Growth (%)", "Frequency Count"),
        ("correlation_heatmap", ["co2_emissions_mt", "co2_per_capita_tonnes", "coal_share_pct", "oil_share_pct", "gas_share_pct"], None, "Carbon Emissions & Energy Source Correlations")
    ],
    "D18": [
        ("line", "year", ["life_expectancy_years", "healthy_life_expectancy_years"], "Global Life Expectancy & Healthy Life Expectancy Progress (Years)", "Year", "Years"),
        ("bar", "country", "life_expectancy_years", "Life Expectancy Benchmark Ranking by Nation (Years)", "Country", "Years"),
        ("scatter", "life_expectancy_years", "under5_mortality_rate", "Life Expectancy vs Under-5 Child Mortality Rate Correlation", "Life Expectancy (Years)", "U5 Mortality (per 1k)"),
        ("treemap", ["region", "country"], "life_expectancy_years", "Life Expectancy Hierarchical Tree by World Region", None, None),
        ("violin", "income_group", "life_expectancy_years", "Life Expectancy Dispersion Across Income Classifications", "Income Tier", "Life Expectancy (Years)"),
        ("horizontal_bar", "maternal_mortality_ratio", "country", "Maternal Mortality Ratio by Country (per 100k births)", "Maternal Mortality Ratio", "Country"),
        ("correlation_heatmap", ["life_expectancy_years", "healthy_life_expectancy_years", "under5_mortality_rate", "maternal_mortality_ratio", "unhealthy_years_lived"], None, "Global Longevity & Mortality Indicators Correlation Matrix")
    ],
    "D19": [
        ("horizontal_bar", "u5_stunting_pct", "country", "Under-5 Child Stunting Prevalence Ranking (%)", "Stunting Rate (%)", "Country"),
        ("bar", "country", ["measles_immunization_pct", "dtp3_immunization_pct"], "Pediatric Immunization Coverage by Country (%)", "Country", "Coverage (%)"),
        ("scatter", "immunization_average_pct", "neonatal_mortality_rate", "Average Immunization Coverage vs Neonatal Mortality Rate", "Immunization (%)", "Neonatal Mortality"),
        ("correlation_heatmap", ["u5_stunting_pct", "measles_immunization_pct", "dtp3_immunization_pct", "exclusive_breastfeeding_pct", "neonatal_mortality_rate"], None, "Child Health & Nutrition Indicator Correlations"),
        ("violin", None, "exclusive_breastfeeding_pct", "Exclusive Breastfeeding Rate Dispersion Across Countries (%)", "Dispersion", "Breastfeeding (%)"),
        ("histogram", "child_survival_risk_index", None, "Child Survival Risk Index Frequency Distribution", "Risk Index", "Country Count"),
        ("funnel", "measles_immunization_pct", "country", "Child Health Immunization Coverage Funnel Hierarchy")
    ],
    "D20": [
        ("line", "year", ["poverty_headcount_2_15_pct", "poverty_headcount_3_65_pct"], "Poverty Headcount Trajectory ($2.15 & $3.65 Thresholds %)", "Year", "Headcount Share (%)"),
        ("bar", "region", "gini_index", "Gini Income Inequality Index by Geographic Region", "Region", "Gini Index"),
        ("horizontal_bar", "palma_ratio", "region", "Palma Ratio Comparison (Top 10% / Bottom 40% Income Share)", "Palma Ratio", "Region"),
        ("scatter", "poverty_headcount_2_15_pct", "gini_index", "Extreme Poverty Headcount vs Gini Inequality Index", "Poverty Headcount (%)", "Gini Index"),
        ("correlation_heatmap", ["poverty_headcount_2_15_pct", "poverty_headcount_3_65_pct", "gini_index", "income_share_richest_10_pct", "income_share_poorest_20_pct"], None, "Poverty & Wealth Concentration Correlations"),
        ("histogram", "gini_index", None, "Gini Inequality Index Spread Distribution", "Gini Index", "Frequency Count"),
        ("radar", ["poverty_headcount_2_15_pct", "poverty_headcount_3_65_pct", "gini_index", "income_share_richest_10_pct"], None, "Global Poverty & Inequality Multilateral Indicator Profile")
    ],
    "D21": [
        ("line", "year", ["fao_food_price_index"], "FAO Global Food Price Index Benchmark Trajectory", "Year", "Index (2014-2016=100)"),
        ("area", "year", ["wheat_production_mt", "rice_milled_mt", "maize_production_mt"], "Major Cereal Commodity Production Volumes (Million Tonnes)", "Year", "Production (MT)"),
        ("bar", "year", "global_undernourishment_pct", "Global Undernourishment Population Prevalence (%)", "Year", "Prevalence (%)"),
        ("scatter", "fao_food_price_index", "cereal_stocks_to_use_ratio_pct", "Food Price Index vs Cereal Stocks-to-Use Buffer Ratio", "Price Index", "Stocks-to-Use (%)"),
        ("horizontal_bar", "cereal_yield_kg_ha", "year", "Global Cereal Yield Productivity Gains (Kg/Ha)", "Yield (Kg/Ha)", "Year"),
        ("histogram", "food_price_yoy_pct", None, "Food Price Index Annual Volatility Distribution (%)", "YoY Change (%)", "Frequency Count"),
        ("correlation_heatmap", ["fao_food_price_index", "total_cereal_production_mt", "cereal_yield_kg_ha", "cereal_stocks_to_use_ratio_pct", "global_undernourishment_pct"], None, "Food Security, Production & Price Index Correlations")
    ],
    "D22": [
        ("line", "year", ["forest_area_sqkm"], "Global Forest Canopy Surface Area Trajectory (Sq Km)", "Year", "Sq Kilometers"),
        ("bar", "country", "forest_share_land_pct", "Forest Cover Share of Total Land Area by Country (%)", "Country", "Forest Share (%)"),
        ("horizontal_bar", "protected_areas_pct", "country", "Terrestrial Protected Nature Reserve Share (%)", "Protected Area (%)", "Country"),
        ("scatter", "forest_share_land_pct", "protected_areas_pct", "Forest Canopy Share vs Protected Area Coverage", "Forest Share (%)", "Protected Area (%)"),
        ("treemap", ["country"], "forest_area_sqkm", "Global Forest Area Distribution by Country", None, None),
        ("violin", None, "forest_share_land_pct", "National Forest Land Share Distribution Spread (%)", "Distribution", "Forest Share (%)"),
        ("correlation_heatmap", ["forest_share_land_pct", "forest_area_sqkm", "protected_areas_pct", "forest_change_since_base_pct"], None, "Canopy Cover & Conservation Correlation Matrix")
    ],
    "D23": [
        ("bar", "country", "water_stress_pct", "Freshwater Stress Level by Nation (% of Available Supply)", "Country", "Water Stress (%)"),
        ("horizontal_bar", "renewable_per_capita_m3", "country", "Renewable Freshwater Availability per Person (m³/year)", "Cubic Meters / Capita", "Country"),
        ("sunburst", ["country"], "water_stress_pct", "Water Stress Hierarchy Across Monitored Nations", None, None),
        ("scatter", "water_stress_pct", "renewable_per_capita_m3", "Freshwater Stress vs Per Capita Renewable Water Supply", "Water Stress (%)", "Per Capita Water (m³)"),
        ("correlation_heatmap", ["water_stress_pct", "renewable_per_capita_m3", "agri_withdrawal_pct", "industrial_pct", "municipal_pct"], None, "Hydrological Stress & Extraction Matrix Correlations"),
        ("violin", None, "water_stress_pct", "Global Freshwater Stress Distribution & Outliers", "Dispersion", "Stress (%)"),
        ("funnel", "renewable_per_capita_m3", "country", "Per Capita Freshwater Resource Abundance Funnel Profile")
    ],
    "D24": [
        ("line", "year", ["current_account_gdp_pct"], "Current Account Balance Trajectory (% of GDP)", "Year", "Balance (% GDP)"),
        ("bar", "country", "trade_openness_gdp_pct", "Trade Openness Ratio Share of GDP by Country (%)", "Country", "Trade Openness (% GDP)"),
        ("horizontal_bar", "current_account_gdp_pct", "country", "Current Account Balance Surpluses & Deficits (% GDP)", "Current Account (% GDP)", "Country"),
        ("scatter", "trade_openness_gdp_pct", "current_account_gdp_pct", "Trade Openness vs Current Account External Balance", "Trade Openness (% GDP)", "Current Account (% GDP)"),
        ("violin", "surplus_deficit", "current_account_gdp_pct", "Current Account Dispersion across Surplus & Deficit Groups", "Balance Group", "Current Account (% GDP)"),
        ("histogram", "current_account_gdp_pct", None, "Global Current Account Balance Distribution (%)", "Current Account (% GDP)", "Frequency Count"),
        ("density_heatmap", "trade_openness_gdp_pct", "current_account_gdp_pct", "Trade Openness vs Current Account 2D Density", "Trade Openness (%)", "Current Account (%)")
    ],
    "D25": [
        ("line", "year", ["internet_users_pct"], "Internet User Population Penetration Trajectory by Region (%)", "Year", "Penetration Rate (%)"),
        ("bar", "region", "mobile_cellular_per_100", "Mobile Cellular Subscriptions per 100 Inhabitants", "Region", "Subscriptions / 100"),
        ("horizontal_bar", "fixed_broadband_per_100", "region", "Fixed Broadband Infrastructure Subscriptions per 100", "Broadband / 100", "Region"),
        ("scatter", "fixed_broadband_per_100", "internet_users_pct", "Fixed Broadband vs Internet Penetration Correlation", "Broadband / 100", "Internet Users (%)"),
        ("correlation_heatmap", ["internet_users_pct", "fixed_broadband_per_100", "mobile_cellular_per_100", "offline_population_pct"], None, "Telecommunications Infrastructure Correlation Heatmap"),
        ("histogram", "offline_population_pct", None, "Offline Population Share Distribution across World Regions", "Offline Share (%)", "Frequency Count"),
        ("radar", ["internet_users_pct", "fixed_broadband_per_100", "mobile_cellular_per_100", "offline_population_pct"], None, "Regional Digital Infrastructure Capability Radar")
    ],
    "D26": [
        ("bar", "country", "rd_expenditure_pct_gdp", "Gross Domestic R&D Expenditure Share of GDP (%)", "Country", "R&D (% GDP)"),
        ("horizontal_bar", "researchers_per_million", "country", "Scientific Researcher Density per Million Inhabitants", "Researchers / Million", "Country"),
        ("scatter", "rd_expenditure_pct_gdp", "hightech_export_share_pct", "R&D Intensity vs High-Technology Export Share", "R&D (% GDP)", "High-Tech Exports (%)"),
        ("treemap", ["country"], "patents_resident", "Resident Patent Applications Volume by Country", None, None),
        ("correlation_heatmap", ["rd_expenditure_pct_gdp", "researchers_per_million", "patents_resident", "hightech_export_share_pct"], None, "R&D Inputs vs Intellectual Property Output Correlations"),
        ("violin", None, "rd_expenditure_pct_gdp", "Global R&D Expenditure Intensity Distribution", "Distribution", "R&D (% GDP)"),
        ("radar", ["rd_expenditure_pct_gdp", "researchers_per_million", "hightech_export_share_pct", "innovation_intensity_ratio"], None, "Multilateral National Innovation Capability Profile")
    ],
    "D27": [
        ("horizontal_bar", "external_debt_usd_b", "country", "Total External Sovereign Debt Stock ($ Billion)", "Debt Stock ($ B)", "Country"),
        ("bar", "country", "debt_to_gni_pct", "External Sovereign Debt-to-GNI Ratio Ranking (%)", "Country", "Debt to GNI (%)"),
        ("scatter", "debt_to_gni_pct", "debt_service_export_pct", "Debt-to-GNI Burden vs Debt Service to Exports", "Debt to GNI (%)", "Debt Service (% Exports)"),
        ("treemap", ["risk_category", "country"], "external_debt_usd_b", "External Debt Stock Distribution by Sovereign Risk Category", None, None),
        ("violin", "risk_category", "debt_to_gni_pct", "Debt-to-GNI Distribution Across Risk Tiers", "Risk Tier", "Debt (% GNI)"),
        ("histogram", "debt_vulnerability_score", None, "Debt Vulnerability Composite Score Distribution", "Vulnerability Score", "Country Count"),
        ("funnel", "external_debt_usd_b", "country", "Sovereign External Debt Exposure Volume Funnel Hierarchy")
    ],
    "D28": [
        ("geo_scatter", "latitude", "longitude", "Global Planetary Seismic Epicenter Telemetry Map", "magnitude", "depth_km", "place", "world"),
        ("histogram", "magnitude", None, "Earthquake Richter Magnitude Frequency Distribution", "Richter Magnitude", "Event Count"),
        ("scatter", "depth_km", "magnitude", "Focal Hypocenter Depth (KM) vs Richter Magnitude", "Depth (KM)", "Magnitude"),
        ("violin", "depth_category", "magnitude", "Richter Magnitude Dispersion across Depth Categories", "Depth Category", "Magnitude"),
        ("horizontal_bar", "significance", "place", "Earthquake Event Significance Index Top Occurrences", "Significance Score", "Location"),
        ("density_heatmap", "depth_km", "magnitude", "Focal Depth vs Earthquake Magnitude 2D Density Heatmap", "Depth (KM)", "Magnitude"),
        ("sunburst", ["depth_category", "high_magnitude"], "magnitude", "Seismic Events Partitioned by Depth and Severity", None, None)
    ],
    "D29": [
        ("line", "year", ["annual_mean_anomaly_c", "lowess_smoothing_c"], "Global Mean Surface Temperature Anomaly & LOWESS Trend (°C)", "Year", "Anomaly (°C)"),
        ("bar", "year", "annual_mean_anomaly_c", "Annual Surface Temperature Departure History (°C)", "Year", "Departure (°C)"),
        ("horizontal_bar", "warming_rate_per_decade", "decade", "Decadal Warming Rate Acceleration (°C / decade)", "Warming Rate (°C/decade)", "Decade"),
        ("scatter", "annual_mean_anomaly_c", "cumulative_warming_anomaly", "Annual Temperature Departure vs Cumulative Anomaly Metric", "Annual Departure (°C)", "Cumulative Metric"),
        ("violin", "decade", "annual_mean_anomaly_c", "Temperature Anomaly Distribution Shifts Across Decades", "Decade", "Anomaly (°C)"),
        ("histogram", "annual_mean_anomaly_c", None, "Surface Temperature Departure Frequency Histogram", "Anomaly (°C)", "Frequency Count"),
        ("correlation_heatmap", ["annual_mean_anomaly_c", "lowess_smoothing_c", "warming_rate_per_decade", "cumulative_warming_anomaly"], None, "Thermal Anomaly & Warming Momentum Correlation Matrix")
    ],
    "D30": [
        ("line", "year", ["population_millions"], "Megacity Population Growth Trajectory (Millions)", "Year", "Population (M)"),
        ("horizontal_bar", "population_millions", "city", "Megacity Population Scale Ranking Comparison (Millions)", "Population (M)", "City"),
        ("scatter", "population_millions", "growth_multiple_since_1980", "Metropolitan Scale vs Decadal Growth Multiple Since 1980", "Population (M)", "Growth Multiple"),
        ("treemap", ["country", "city"], "population_millions", "Global Urban Agglomeration Distribution by Country and City", None, None),
        ("violin", "country", "population_millions", "Megacity Scale Dispersion across Nations", "Country", "Population (M)"),
        ("histogram", "growth_multiple_since_1980", None, "Metropolitan Growth Multiple Frequency Distribution", "Growth Multiple", "City Count"),
        ("sunburst", ["country", "city"], "population_millions", "Hierarchical Metropolitan Population Allocation", None, None)
    ],
    "D31": [
        ("line", "year", ["tourist_arrivals_millions"], "International Tourist Arrivals Trajectory by Nation (Millions)", "Year", "Arrivals (M)"),
        ("bar", "country", "tourism_receipts_usd_billions", "International Travel Receipts by Destination Nation ($ Billion)", "Country", "Receipts ($ B)"),
        ("horizontal_bar", "receipt_per_arrival_usd", "country", "Average Spending Yield per Inbound Tourist Arrival ($ USD)", "Receipt / Visitor ($)", "Country"),
        ("scatter", "tourist_arrivals_millions", "tourism_receipts_usd_billions", "Tourist Arrival Volumes vs Gross Travel Receipts ($ B)", "Arrivals (M)", "Receipts ($ B)"),
        ("violin", "country", "tourist_arrivals_millions", "Arrival Volume Dispersion Across Destination Nations", "Country", "Arrivals (M)"),
        ("histogram", "tourism_receipts_usd_billions", None, "National Tourism Receipts Frequency Distribution ($ B)", "Receipts ($ B)", "Frequency Count"),
        ("correlation_heatmap", ["tourist_arrivals_millions", "tourism_receipts_usd_billions", "receipt_per_arrival_usd"], None, "International Tourism Volume & Yield Correlation Matrix")
    ],
    "D32": [
        ("line", "year", ["ev_market_share_pct"], "Electric Vehicle New Car Market Share Trajectory (%)", "Year", "Market Share (%)"),
        ("area", "year", ["powertrain_bev_pct", "powertrain_phev_pct"], "Clean Powertrain Mix: BEV Battery Electric vs PHEV Hybrid (%)", "Year", "Share (%)"),
        ("bar", "market", "ev_sales_thousands", "Electric Vehicle Annual Sales Volume by Market (Thousands)", "Market", "Sales (Thousands)"),
        ("scatter", "ev_sales_thousands", "ev_market_share_pct", "EV Sales Volume Scale vs Market Share Penetration (%)", "Sales (Thousands)", "Market Share (%)"),
        ("horizontal_bar", "ev_sales_millions", "market", "Electric Vehicle Cumulative Fleet Sales (Millions)", "Fleet Sales (M)", "Market"),
        ("histogram", "ev_market_share_pct", None, "Clean Mobility Market Share Growth Distribution (%)", "Market Share (%)", "Frequency Count"),
        ("radar", ["ev_market_share_pct", "powertrain_bev_pct", "ev_sales_millions"], None, "Global Clean Mobility Market Technology Profile")
    ],
    "D33": [
        ("line", "Date", ["SP500", "PE10"], "S&P 500 Price Benchmark & Shiller Cyclically Adjusted PE10", "Date", "Level / Ratio"),
        ("line", "Date", ["Gold_USD", "Brent_Oil_USD"], "Physical Gold (USD/oz) vs Brent Crude Oil Benchmark (USD/bbl)", "Date", "USD Price"),
        ("scatter", "Long Interest Rate", "PE10", "10-Year Long Interest Rate vs Shiller PE10 Valuation Multiple", "Long Interest Rate (%)", "Shiller PE10"),
        ("horizontal_bar", "SP500_Return_YoY", "Date", "S&P 500 Historical Annual Return Profile (%)", "Return YoY (%)", "Date"),
        ("correlation_heatmap", ["SP500", "Long Interest Rate", "PE10", "Gold_USD", "Brent_Oil_USD", "Gold_to_SP500_Ratio"], None, "Cross-Asset Financial Markets Correlation Matrix"),
        ("violin", None, "PE10", "Shiller CAPE PE10 Valuation Multiple Historical Dispersion", "Valuation Dispersion", "PE10 Ratio"),
        ("density_heatmap", "SP500_Return_YoY", "Gold_Return_YoY", "Equity Returns vs Gold Returns 2D Density Heatmap", "S&P 500 YoY (%)", "Gold YoY (%)")
    ],
    "D34": [
        ("line", "year", ["gross_debt_gdp_pct"], "General Government Gross Debt (% of GDP) across Major Economies", "Year", "Gross Debt (% GDP)"),
        ("bar", "country", "primary_balance_gdp_pct", "Primary Fiscal Balance Deficits / Surpluses (% of GDP)", "Country", "Balance (% GDP)"),
        ("horizontal_bar", "gross_debt_gdp_pct", "country", "Latest Sovereign Debt-to-GDP Ranking Comparison by Nation", "Debt (% GDP)", "Country"),
        ("scatter", "gross_debt_gdp_pct", "primary_balance_gdp_pct", "Gross Debt Burden vs Primary Fiscal Balance Stance", "Debt (% GDP)", "Fiscal Balance (%)"),
        ("treemap", ["economy_group", "country"], "gross_debt_gdp_pct", "Sovereign Debt Distribution by Economy Group and Country", None, None),
        ("violin", "economy_group", "gross_debt_gdp_pct", "Debt-to-GDP Divergence: Advanced vs Emerging Economies", "Group", "Debt (% GDP)"),
        ("histogram", "gross_debt_gdp_pct", None, "Sovereign Debt Global Distribution Spread (%)", "Debt (% GDP)", "Frequency Count")
    ]
}

def update_build_dashboards():
    with open(BUILD_DASHBOARDS_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Update DASHBOARD_SPECS by substituting the "charts" lists in content
    # Let's import the current DASHBOARD_SPECS
    import sys
    sys.path.insert(0, os.path.dirname(__file__))
    import build_dashboards

    # Update specs in memory
    for spec in build_dashboards.DASHBOARD_SPECS:
        did = spec["id"]
        if did in NEW_CHARTS_BY_ID:
            spec["charts"] = NEW_CHARTS_BY_ID[did]

    # 2. Update get_chart_subtitle in build_dashboards.py
    new_subtitle_func = '''def get_chart_subtitle(spec, chart_idx, c):
    ctype = c[0]
    if ctype == "geo_scatter":
        if "aqi" in c[3].lower() or "air" in c[3].lower():
            return "Geospatial air quality telemetry across major metropolitan environmental monitoring stations"
        elif "seismic" in c[3].lower() or "earthquake" in c[3].lower():
            return "Planetary seismic hypocenter distribution with Richter magnitude and focal depth mapping"
        return "Geospatial distribution and spatial clustering across monitored locations"
    if len(c) > 6 and c[6] and ctype not in ["geo_scatter", "scatter", "box", "bar", "treemap", "line", "area", "violin", "horizontal_bar", "histogram"]:
        return c[6]
    title = c[3].lower()
    
    if "gdp" in title and "growth" in title:
        return "Real annual economic output growth rate benchmarking cyclical volatility and structural momentum"
    elif "gdp" in title:
        return "Multi-decade national macroeconomic scale expansion derived from verified official accounts"
    elif "inflation" in title or "cpi" in title:
        return "Consumer price inflation dynamics tracked relative to monetary policy tolerance thresholds"
    elif "repo" in title or "policy rate" in title:
        return "Central bank policy stance and transmission across key interest rate corridors"
    elif "literacy" in title:
        return "Human capital foundation benchmarking educational attainment and gender literacy spreads"
    elif "stunting" in title or "malnutrition" in title:
        return "Under-5 pediatric nutritional distress indicators highlighting public health intervention priorities"
    elif "sanitation" in title or "immunization" in title:
        return "Preventative public healthcare infrastructure access and protective coverage rates"
    elif "foodgrain" in title or "cereal" in title or "yield" in title:
        return "Agricultural productivity, harvest volume output, and crop yield intensity trends"
    elif "clean" in title or "solar" in title or "renewable" in title:
        return "Decarbonization trajectory and variable renewable generation capacity additions"
    elif "trade" in title or "export" in title or "import" in title:
        return "Cross-border merchandise flow balances, foreign exchange earnings, and trade deficit exposures"
    elif "fdi" in title or "equity" in title:
        return "Inbound cross-border long-term capital flows, equity allocations, and priority sector routing"
    elif "highway" in title or "road" in title:
        return "National logistics infrastructure expansion pace and multi-lane modern corridor development"
    elif "railway" in title or "freight" in title:
        return "Bulk commodity haulage throughput, electrification velocity, and operational performance"
    elif "aqi" in title or "pm2.5" in title or "air quality" in title:
        return "Continuous ambient pollutant concentration measurements benchmarked against national standards"
    elif "upi" in title or "digital payment" in title:
        return "Real-time retail payment infrastructure adoption volume, ticket sizing, and financial velocity"
    elif "debt" in title or "fiscal" in title:
        return "Sovereign and subnational balance sheet prudence, debt-to-GDP ratios, and borrowing sustainability"
    elif "co2" in title or "emissions" in title or "carbon" in title:
        return "Territorial greenhouse gas output trajectory, per-capita intensity, and cumulative carbon budgets"
    elif "life expectancy" in title or "mortality" in title:
        return "Longitudinal longevity dividends, healthy life expectancy gains, and epidemiological transitions"
    elif "poverty" in title or "gini" in title or "inequality" in title:
        return "Poverty headcount eradication milestones and income distribution concentration dynamics"
    elif "forest" in title or "deforestation" in title:
        return "Terrestrial biome conservation, canopy density evolution, and protected reserve shares"
    elif "water" in title:
        return "Freshwater extraction pressures, renewable internal supplies, and hydrological vulnerability"
    elif "internet" in title or "broadband" in title or "connectivity" in title:
        return "Digital infrastructure accessibility, broadband penetration rates, and connectivity equity"
    elif "r&d" in title or "patent" in title or "innovation" in title:
        return "Gross domestic research expenditure intensity, human capital depth, and intellectual property output"
    elif "earthquake" in title or "seismic" in title:
        return "Real-time seismic hypocenter depth, Richter magnitude severity, and tectonic boundary distribution"
    elif "temperature" in title or "warming" in title or "anomaly" in title:
        return "Global mean surface temperature departures benchmarked against the 1951-1980 base period"
    elif "megacity" in title or "urban" in title:
        return "Metropolitan agglomeration demographic expansion, densification, and growth multiples"
    elif "tourism" in title or "arrival" in title:
        return "International tourist mobility volumes, pandemic shock contractions, and receipts recovery"
    elif "ev" in title or "electric vehicle" in title:
        return "Clean mobility penetration rates, battery-electric dominance, and fleet electrification curves"
    elif "stock" in title or "equity" in title or "s&p" in title or "nifty" in title or "gold" in title or "brent" in title:
        return "Global capital market valuation multiples, sovereign yield benchmarks, and asset class co-movements"
    elif ctype == "scatter":
        return "Bivariate cross-sectional correlation analysis with linear regression trajectory"
    elif ctype == "box":
        return "Statistical dispersion, interquartile distribution spread, and historical outlier density"
    elif ctype == "area":
        return "Component decomposition and proportional structural shifts over observed timeline"
    elif ctype == "bar":
        return "Comparative ranking distribution across key jurisdictional entities"
    elif ctype == "donut":
        return "Proportional compositional breakdown across classified segments"
    elif ctype == "horizontal_bar":
        return "Rank-ordered cross-sectional comparison across monitored categories"
    elif ctype == "histogram":
        return "Empirical frequency distribution with marginal density overlay"
    elif ctype == "violin":
        return "Continuous probability density profile with full observational scatter"
    elif ctype == "sunburst":
        return "Multi-tiered hierarchical structure and proportional value allocation"
    elif ctype == "funnel":
        return "Sequential progression and volume attrition across analytical stages"
    elif ctype == "correlation_heatmap":
        return "Pairwise Pearson correlation matrix across numerical indicators"
    elif ctype == "density_heatmap":
        return "Bivariate kernel density distribution with marginal frequency histograms"
    elif ctype == "radar":
        return "Multi-dimensional performance profile across normalized indicator dimensions"
    elif ctype == "waterfall":
        return "Incremental variance bridge and attribution progression"
    else:
        return "Longitudinal trend evolution across the observed analytical timeline"'''

    # 3. Update generate_chart_code in build_dashboards.py
    new_generate_chart_code = '''def generate_chart_code(fig_num, c, palette_slice, subtitle="", height=380, indent=8):
    ctype, x, y, title = c[0], c[1], c[2], c[3]
    var_name = f"fig{fig_num}"
    lines = []
    
    if ctype == "geo_scatter":
        size_val = f'"{c[4]}"' if len(c) > 4 and c[4] else "None"
        color_val = f'"{c[5]}"' if len(c) > 5 and c[5] else "None"
        hover_val = f'"{c[6]}"' if len(c) > 6 and c[6] else "None"
        scope_val = f'"{c[7]}"' if len(c) > 7 and c[7] else "None"
        lines.append(f"{var_name} = create_geo_scatter(df, lat=\\"{x}\\", lon=\\"{y}\\", size={size_val}, color={color_val}, hover_name={hover_val}, title=\\"{title}\\", subtitle=\\"{subtitle}\\", scope={scope_val}, height={height})")
    elif ctype == "area":
        lines.append(f"{var_name} = px.area(df, x=\\"{x}\\", y={y}, color_discrete_sequence={palette_slice})")
        lines.append(f"{var_name} = base_layout({var_name}, \\"{title}\\", \\"{c[4]}\\", \\"{c[5]}\\", height={height}, subtitle=\\"{subtitle}\\")")
    elif ctype == "line":
        lines.append(f"{var_name} = px.line(df, x=\\"{x}\\", y={y}, markers=True, color_discrete_sequence={palette_slice})")
        lines.append(f"{var_name} = base_layout({var_name}, \\"{title}\\", \\"{c[4]}\\", \\"{c[5]}\\", height={height}, subtitle=\\"{subtitle}\\")")
    elif ctype == "bar":
        y_expr = y if isinstance(y, list) else f'"{y}"'
        lines.append(f"{var_name} = px.bar(df, x=\\"{x}\\", y={y_expr}, color_discrete_sequence={palette_slice})")
        lines.append(f"{var_name} = base_layout({var_name}, \\"{title}\\", \\"{c[4]}\\", \\"{c[5]}\\", height={height}, subtitle=\\"{subtitle}\\")")
    elif ctype == "horizontal_bar":
        lines.append(f"{var_name} = create_horizontal_bar(df, x=\\"{x}\\", y=\\"{y}\\", title=\\"{title}\\", x_title=\\"{c[4]}\\", y_title=\\"{c[5]}\\", subtitle=\\"{subtitle}\\", height={height})")
    elif ctype == "donut":
        lines.append(f"df_donut{fig_num} = df[df[\\"{y}\\"] > 0] if \\"{y}\\" in df.columns else df")
        lines.append(f"{var_name} = create_donut_chart(df_donut{fig_num}, names=\\"{x}\\", values=\\"{y}\\", title=\\"{title}\\", subtitle=\\"{subtitle}\\", height={height})")
    elif ctype == "histogram":
        x_title = c[4] if len(c) > 4 and c[4] else ""
        y_title = c[5] if len(c) > 5 and c[5] else "Frequency"
        lines.append(f"{var_name} = create_histogram(df, x=\\"{x}\\", title=\\"{title}\\", x_title=\\"{x_title}\\", y_title=\\"{y_title}\\", subtitle=\\"{subtitle}\\", height={height})")
    elif ctype == "violin":
        x_expr = f'"{x}"' if x else "None"
        x_title = c[4] if len(c) > 4 and c[4] else ""
        y_title = c[5] if len(c) > 5 and c[5] else ""
        lines.append(f"{var_name} = create_violin_chart(df, x={x_expr}, y=\\"{y}\\", title=\\"{title}\\", x_title=\\"{x_title}\\", y_title=\\"{y_title}\\", subtitle=\\"{subtitle}\\", height={height})")
    elif ctype == "sunburst":
        lines.append(f"df_sun{fig_num} = df[df[\\"{y}\\"] > 0] if \\"{y}\\" in df.columns else df")
        lines.append(f"{var_name} = create_sunburst(df_sun{fig_num}, path={x}, values=\\"{y}\\", title=\\"{title}\\", subtitle=\\"{subtitle}\\", height={height})")
    elif ctype == "funnel":
        lines.append(f"{var_name} = create_funnel_chart(df, x=\\"{x}\\", y=\\"{y}\\", title=\\"{title}\\", subtitle=\\"{subtitle}\\", height={height})")
    elif ctype == "correlation_heatmap":
        cols_arg = f"{x}" if isinstance(x, list) else f"df.select_dtypes(include=['number']).columns.tolist()[:6]"
        lines.append(f"{var_name} = create_correlation_heatmap(df, cols={cols_arg}, title=\\"{title}\\", subtitle=\\"{subtitle}\\", height={height})")
    elif ctype == "density_heatmap":
        x_title = c[4] if len(c) > 4 and c[4] else ""
        y_title = c[5] if len(c) > 5 and c[5] else ""
        lines.append(f"{var_name} = create_density_heatmap(df, x=\\"{x}\\", y=\\"{y}\\", title=\\"{title}\\", x_title=\\"{x_title}\\", y_title=\\"{y_title}\\", subtitle=\\"{subtitle}\\", height={height})")
    elif ctype == "radar":
        lines.append(f"radar_cols_{fig_num} = [c for c in {x} if c in df.columns]")
        lines.append(f"radar_vals_{fig_num} = [float(df[c].dropna().iloc[-1]) if c in df.columns and len(df[c].dropna()) > 0 else 0.0 for c in radar_cols_{fig_num}]")
        lines.append(f"{var_name} = create_radar_chart(radar_cols_{fig_num}, radar_vals_{fig_num}, title=\\"{title}\\", subtitle=\\"{subtitle}\\", height={height})")
    elif ctype == "scatter":
        trend = ', trendline="ols"' if fig_num == 4 else ""
        lines.append(f"{var_name} = px.scatter(df, x=\\"{x}\\", y=\\"{y}\\"{trend}, color_discrete_sequence={palette_slice})")
        lines.append(f"{var_name} = base_layout({var_name}, \\"{title}\\", \\"{c[4]}\\", \\"{c[5]}\\", height={height}, subtitle=\\"{subtitle}\\")")
    elif ctype == "box":
        x_expr = f'"{x}"' if x else "None"
        lines.append(f"{var_name} = px.box(df, x={x_expr}, y=\\"{y}\\", color_discrete_sequence={palette_slice})")
        lines.append(f"{var_name} = base_layout({var_name}, \\"{title}\\", \\"{c[4]}\\", \\"{c[5]}\\", height={height}, subtitle=\\"{subtitle}\\")")
    elif ctype == "treemap":
        lines.append(f"df_tree{fig_num} = df[df[\\"{y}\\"] > 0] if \\"{y}\\" in df.columns else df")
        lines.append(f"{var_name} = px.treemap(df_tree{fig_num}, path={x}, values=\\"{y}\\", color_discrete_sequence={palette_slice})")
        lines.append(f"{var_name} = base_layout({var_name}, \\"{title}\\", height={height}, subtitle=\\"{subtitle}\\")")
    else:
        lines.append(f"{var_name} = px.line(df, x=\\"{x}\\", y={y}, color_discrete_sequence={palette_slice})")
        lines.append(f"{var_name} = base_layout({var_name}, \\"{title}\\", \\"{c[4]}\\", \\"{c[5]}\\", height={height}, subtitle=\\"{subtitle}\\")")
        
    pad = " " * indent
    return f"\\n{pad}".join(lines)'''

    # Now rewrite scripts/build_dashboards.py cleanly using the updated objects
    # 4. Imports in generate_dashboard_code
    old_imports_str = 'from app.components.charts import base_layout, COLOR_PALETTE, create_geo_scatter'
    new_imports_str = '''from app.components.charts import (
    base_layout, COLOR_PALETTE, create_geo_scatter, create_donut_chart,
    create_histogram, create_violin_chart, create_sunburst, create_funnel_chart,
    create_horizontal_bar, create_correlation_heatmap, create_density_heatmap,
    create_radar_chart, create_waterfall_chart, create_treemap, create_box_chart,
    create_line_chart, create_bar_chart, create_area_chart
)'''

    # Let's reconstruct the file by re-formatting DASHBOARD_SPECS
    # We can serialize DASHBOARD_SPECS as Python code:
    import pprint
    specs_str = "DASHBOARD_SPECS = " + pprint.pformat(build_dashboards.DASHBOARD_SPECS, indent=4, width=120)

    # Find boundaries in content
    specs_start = content.find("DASHBOARD_SPECS = [")
    specs_end = content.find("def get_chart_subtitle(")
    chart_code_end = content.find("def generate_dashboard_code(")

    part1 = content[:specs_start]
    part_briefings_and_rest = content[content.find("BRIEFING_CONTEXT = {"):specs_end] # wait, BRIEFING_CONTEXT is after get_chart_subtitle
    # Let's check order:
    # DASHBOARD_SPECS is first, then get_chart_subtitle, then BRIEFING_CONTEXT, then generate_chart_code, then generate_dashboard_code
    briefing_start = content.find("BRIEFING_CONTEXT = {")
    chart_code_start = content.find("def generate_chart_code(")
    dash_code_start = content.find("def generate_dashboard_code(")

    briefing_content = content[briefing_start:chart_code_start]
    dash_code_content = content[dash_code_start:].replace(old_imports_str, new_imports_str)

    new_full_content = (
        part1 +
        specs_str + "\n\n" +
        new_subtitle_func + "\n\n" +
        briefing_content +
        new_generate_chart_code + "\n\n" +
        dash_code_content
    )

    with open(BUILD_DASHBOARDS_PATH, "w", encoding="utf-8") as f:
        f.write(new_full_content)

    print("Updated scripts/build_dashboards.py successfully!")

    # Now execute build_all()
    # Re-import and run
    import importlib
    import build_dashboards as bd_updated
    importlib.reload(bd_updated)
    bd_updated.build_all()
    print("All 34 dashboard modules re-generated with rich visual typologies!")

if __name__ == "__main__":
    update_build_dashboards()
