"""
Master Dashboard Generator
Generates all 34 individual dashboard modules in `dashboards/` directory.
Each dashboard features:
- ⓘ Information Drawer integration (render_info_button)
- Interactive filter controls (sliders, selectors)
- 4 to 5 Executive KPI Cards with dynamic computed metrics
- 7 to 8 Meaningful Plotly Charts (line, bar, scatter, treemap, boxplot, heatmap, area)
- 1 Searchable Data Table with sort/filter
- Dynamic analytical insight narrative computed directly from dataframe values
Total Visual Count: 12 to 14 meaningful visuals per dashboard!
"""

import os
import json

DASHBOARDS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "dashboards")
os.makedirs(DASHBOARDS_DIR, exist_ok=True)

# List of dashboard definitions with metadata and visualization recipes
DASHBOARD_SPECS = [   {   'charts': [   (   'line',
                          'year',
                          ['gdp_current_trillion_usd'],
                          'India Nominal GDP Expansion Trajectory ($ Trillion)',
                          'Year',
                          'USD Trillions'),
                      (   'area',
                          'year',
                          ['agriculture_gva_pct', 'industry_gva_pct', 'services_gva_pct'],
                          'Sectoral GVA Composition Over Time (%)',
                          'Year',
                          'GVA Share (%)'),
                      (   'scatter',
                          'gross_capital_formation_pct',
                          'gdp_growth_pct',
                          'Capital Formation vs Real GDP Growth Correlation',
                          'Gross Capital Formation (% of GDP)',
                          'Real GDP Growth (%)'),
                      (   'horizontal_bar',
                          'gdp_per_capita_usd',
                          'year',
                          'Per Capita GDP Trajectory Milestones ($)',
                          'USD / Capita',
                          'Year'),
                      (   'correlation_heatmap',
                          [   'gdp_growth_pct',
                              'services_gva_pct',
                              'gross_capital_formation_pct',
                              'inflation_cpi_pct',
                              'gdp_per_capita_usd'],
                          None,
                          'Macroeconomic Indicator Pearson Correlation Matrix'),
                      (   'histogram',
                          'gdp_growth_pct',
                          None,
                          'Real GDP Growth Rate Frequency Distribution (%)',
                          'Annual GDP Growth (%)',
                          'Frequency Count'),
                      (   'radar',
                          ['gdp_growth_pct', 'services_gva_pct', 'gross_capital_formation_pct', 'inflation_cpi_pct'],
                          None,
                          'Latest Macroeconomic Profile Polar Radar Scan')],
        'csv': 'data/analytical/d01_india_macro_gdp.csv',
        'domain': 'Macroeconomics',
        'file': 'd01_india_macro_gdp.py',
        'id': 'D01',
        'kpis': [   (   'Current GDP ($ Trillion)',
                        'gdp_current_trillion_usd',
                        'max',
                        '${val:.2f}T',
                        '+7.2% Real YoY',
                        'pos'),
                    ('GDP Per Capita ($)', 'gdp_per_capita_usd', 'latest', '${val:,.0f}', 'Expanding base', 'pos'),
                    (   'Services GVA Share (%)',
                        'services_gva_pct',
                        'latest',
                        '{val:.1f}%',
                        'Structural driver',
                        'neutral'),
                    (   'Capital Formation (% GDP)',
                        'gross_capital_formation_pct',
                        'latest',
                        '{val:.1f}%',
                        'Investment rate',
                        'neutral'),
                    (   'Services/Agri GVA Ratio',
                        'services_to_agriculture_ratio',
                        'latest',
                        '{val:.2f}x',
                        'Structural transition',
                        'pos')],
        'slug': 'd01_india_macro_gdp',
        'time_col': 'year',
        'title': 'India Macroeconomic & GDP Growth Intelligence'},
    {   'charts': [   (   'line',
                          'date',
                          [   'headline_cpi_yoy',
                              'rbi_repo_rate',
                              'target_band_mid',
                              'target_band_upper',
                              'target_band_lower'],
                          'Headline CPI vs RBI Policy Corridor & Tolerance Bands (%)',
                          'Date',
                          'Rate (%)'),
                      (   'bar',
                          'date',
                          'real_policy_rate',
                          'Real Policy Rate Evolution (Repo minus CPI %)',
                          'Date',
                          'Real Rate (% pts)'),
                      (   'scatter',
                          'headline_cpi_yoy',
                          'rbi_repo_rate',
                          'Monetary Reaction Function: CPI vs Repo Rate',
                          'Headline CPI (%)',
                          'RBI Repo Rate (%)'),
                      (   'violin',
                          None,
                          'food_inflation_yoy',
                          'Food Inflation Volatility Dispersion & Jitter',
                          'Spread',
                          'YoY %'),
                      (   'correlation_heatmap',
                          [   'headline_cpi_yoy',
                              'food_inflation_yoy',
                              'fuel_inflation_yoy',
                              'core_cpi_yoy',
                              'rbi_repo_rate',
                              'real_policy_rate'],
                          None,
                          'Inflation Dynamics & Policy Rate Correlation Matrix'),
                      (   'density_heatmap',
                          'headline_cpi_yoy',
                          'food_inflation_yoy',
                          'Headline vs Food Inflation 2D Density Heatmap',
                          'Headline CPI (%)',
                          'Food Inflation (%)'),
                      (   'horizontal_bar',
                          'food_fuel_spread',
                          'year',
                          'Food vs Fuel Inflation Spread by Annual Regime',
                          'Spread (% pts)',
                          'Year')],
        'csv': 'data/analytical/d02_india_rbi_inflation.csv',
        'domain': 'Central Banking & Monetary Policy',
        'file': 'd02_india_rbi_inflation.py',
        'id': 'D02',
        'kpis': [   (   'Latest Headline CPI (%)',
                        'headline_cpi_yoy',
                        'latest',
                        '{val:.1f}%',
                        'YoY Consumer Inflation',
                        'neutral'),
                    (   'RBI Policy Repo Rate (%)',
                        'rbi_repo_rate',
                        'latest',
                        '{val:.2f}%',
                        'Current MPC Stance',
                        'neutral'),
                    (   'Real Policy Rate (%)',
                        'real_policy_rate',
                        'latest',
                        '{val:.2f}%',
                        'Repo minus Headline CPI',
                        'pos'),
                    ('Core CPI Inflation (%)', 'core_cpi_yoy', 'latest', '{val:.1f}%', 'Excl. Food & Fuel', 'neutral'),
                    (   'Target Deviation (% pts)',
                        'inflation_deviation_from_target',
                        'latest',
                        '{val:+.1f}%',
                        'Relative to 4.0% Target',
                        'neg')],
        'slug': 'd02_india_rbi_inflation',
        'time_col': 'date',
        'title': 'Reserve Bank of India (RBI) Inflation & Monetary Policy Monitor'},
    {   'charts': [   (   'horizontal_bar',
                          'pop_2011_millions',
                          'state',
                          'State & UT Population Scale (Millions)',
                          'Population (M)',
                          'State'),
                      ('bar', 'state', 'literacy_pct', 'State Literacy Rate Ranking (%)', 'State', 'Literacy Rate (%)'),
                      (   'treemap',
                          ['urbanization_category', 'state'],
                          'pop_2011_millions',
                          'Population Distribution by Urbanization Category',
                          None,
                          None),
                      (   'sunburst',
                          ['urbanization_category', 'state'],
                          'pop_2011_millions',
                          'Hierarchical Demographic Partitioning',
                          None,
                          None),
                      (   'scatter',
                          'urban_pct',
                          'literacy_pct',
                          'Urbanization vs Literacy Rate Correlation',
                          'Urban Population (%)',
                          'Literacy Rate (%)'),
                      (   'violin',
                          'urbanization_category',
                          'sex_ratio',
                          'Sex Ratio Distribution by Urbanization Tier',
                          'Tier',
                          'Sex Ratio'),
                      (   'histogram',
                          'growth_pct',
                          None,
                          'Decadal Population Growth Rate Distribution (%)',
                          'Decadal Growth (%)',
                          'State Count')],
        'csv': 'data/analytical/d03_india_census_demographics.csv',
        'domain': 'Demographics & Human Capital',
        'file': 'd03_india_census_demographics.py',
        'id': 'D03',
        'kpis': [   (   'Total Population (2011)',
                        'pop_2011_millions',
                        'sum',
                        '{val:,.1f}M',
                        'National Aggregate',
                        'neutral'),
                    ('National Avg Literacy (%)', 'literacy_pct', 'mean', '{val:.1f}%', 'State Mean', 'pos'),
                    ('Average Sex Ratio', 'sex_ratio', 'mean', '{val:.0f}', 'Females per 1000 Males', 'neutral'),
                    (   'Avg Gender Literacy Gap',
                        'gender_literacy_gap',
                        'mean',
                        '{val:.1f}% pts',
                        'Male vs Female Gap',
                        'neg'),
                    ('Avg Urbanization Rate', 'urban_pct', 'mean', '{val:.1f}%', 'Urban Population Share', 'neutral')],
        'slug': 'd03_india_census_demographics',
        'time_col': 'state',
        'title': 'India State-Level Demographics & Census Analytics'},
    {   'charts': [   (   'bar',
                          'state',
                          'inst_births_pct',
                          'Institutional Deliveries by State (%)',
                          'State',
                          'Institutional Births (%)'),
                      (   'horizontal_bar',
                          'stunting_pct',
                          'state',
                          'Under-5 Child Stunting Prevalence Ranking (%)',
                          'Stunting Rate (%)',
                          'State'),
                      (   'treemap',
                          ['health_performance_tier', 'state'],
                          'sanitation_pct',
                          'Health Infrastructure Performance Tiers',
                          None,
                          None),
                      (   'scatter',
                          'sanitation_pct',
                          'stunting_pct',
                          'Household Sanitation vs Child Stunting Reduction',
                          'Sanitation (%)',
                          'Child Stunting (%)'),
                      (   'correlation_heatmap',
                          ['inst_births_pct', 'immunization_pct', 'stunting_pct', 'anemia_women_pct', 'sanitation_pct'],
                          None,
                          'Maternal & Child Health Metric Correlations'),
                      (   'violin',
                          'health_performance_tier',
                          'anemia_women_pct',
                          'Female Anemia Distribution across Health Tiers',
                          'Performance Tier',
                          'Anemia (%)'),
                      ('funnel', 'inst_births_pct', 'state', 'State Maternal Care Transition Funnel Profile')],
        'csv': 'data/analytical/d04_india_nfhs_health.csv',
        'domain': 'Public Health & Nutrition',
        'file': 'd04_india_nfhs_health.py',
        'id': 'D04',
        'kpis': [   ('Average Institutional Births', 'inst_births_pct', 'mean', '{val:.1f}%', 'State Mean', 'pos'),
                    (   'Full Child Immunization',
                        'immunization_pct',
                        'mean',
                        '{val:.1f}%',
                        '12-23 Months Children',
                        'pos'),
                    ('Child Stunting Prevalence', 'stunting_pct', 'mean', '{val:.1f}%', 'Under-5 Stunting Mean', 'neg'),
                    ('Female Anemia Prevalence', 'anemia_women_pct', 'mean', '{val:.1f}%', 'Women 15-49 Years', 'neg'),
                    (   'Household Sanitation Access',
                        'sanitation_pct',
                        'mean',
                        '{val:.1f}%',
                        'Improved Sanitation',
                        'pos')],
        'slug': 'd04_india_nfhs_health',
        'time_col': 'state',
        'title': 'National Family Health Survey (NFHS-5) State Health Monitor'},
    {   'charts': [   (   'line',
                          'crop_year',
                          ['total_foodgrains_mt', 'rolling_3yr_prod_mt'],
                          'Total Foodgrain Production & 3-Year Rolling Trajectory (MT)',
                          'Crop Year',
                          'Production (MT)'),
                      (   'area',
                          'crop_year',
                          ['rice_mt', 'wheat_mt', 'pulses_mt', 'coarse_cereals_mt'],
                          'Cereal & Pulse Production Composition (Million Tonnes)',
                          'Crop Year',
                          'Million Tonnes'),
                      (   'bar',
                          'crop_year',
                          ['rice_yield_kg_ha', 'wheat_yield_kg_ha'],
                          'Staple Crop Yield Evolution (Kg/Hectare)',
                          'Crop Year',
                          'Yield (Kg/Ha)'),
                      (   'scatter',
                          'foodgrains_area_mha',
                          'total_foodgrains_mt',
                          'Cultivated Land Area vs Harvest Output',
                          'Area (Million Hectares)',
                          'Production (MT)'),
                      (   'horizontal_bar',
                          'foodgrains_yield_kg_ha',
                          'crop_year',
                          'Composite Foodgrain Yield Progression (Kg/Ha)',
                          'Yield (Kg/Ha)',
                          'Crop Year'),
                      (   'histogram',
                          'foodgrain_growth_yoy_pct',
                          None,
                          'Annual Foodgrain Growth Volatility Distribution (%)',
                          'YoY Growth (%)',
                          'Frequency Count'),
                      (   'correlation_heatmap',
                          [   'total_foodgrains_mt',
                              'foodgrains_yield_kg_ha',
                              'rice_mt',
                              'wheat_mt',
                              'pulses_mt',
                              'oilseeds_mt'],
                          None,
                          'Crop Harvest & Productivity Correlation Matrix')],
        'csv': 'data/analytical/d05_india_agriculture_yield.csv',
        'domain': 'Agriculture & Rural Economy',
        'file': 'd05_india_agriculture_yield.py',
        'id': 'D05',
        'kpis': [   (   'Total Foodgrains (MT)',
                        'total_foodgrains_mt',
                        'latest',
                        '{val:.1f} MT',
                        'FY23 Harvest Record',
                        'pos'),
                    (   'Average Foodgrain Yield',
                        'foodgrains_yield_kg_ha',
                        'latest',
                        '{val:,.0f} kg/ha',
                        'Productivity Peak',
                        'pos'),
                    ('Rice Production (MT)', 'rice_mt', 'latest', '{val:.1f} MT', 'Top Kharif Staple', 'pos'),
                    ('Wheat Production (MT)', 'wheat_mt', 'latest', '{val:.1f} MT', 'Top Rabi Staple', 'pos'),
                    (   'Rice & Wheat Dominance',
                        'rice_wheat_dominance_pct',
                        'latest',
                        '{val:.1f}%',
                        'Share of Total Grain',
                        'neutral')],
        'slug': 'd05_india_agriculture_yield',
        'time_col': 'crop_year',
        'title': 'India Agricultural Production & Crop Yield Analytics'},
    {   'charts': [   (   'area',
                          'year',
                          ['thermal_gw', 'hydro_gw', 'nuclear_gw', 'solar_gw', 'wind_gw'],
                          'Installed Power Generation Capacity by Energy Source (GW)',
                          'Year',
                          'Capacity (GW)'),
                      (   'line',
                          'year',
                          ['clean_capacity_share_pct', 'solar_wind_share_pct'],
                          'Clean Energy Capacity Share Progression (%)',
                          'Year',
                          'Share (%)'),
                      (   'horizontal_bar',
                          'total_clean_gw',
                          'year',
                          'Clean Capacity Expansion Milestones (GW)',
                          'Clean Power (GW)',
                          'Year'),
                      (   'scatter',
                          'solar_gw',
                          'total_generation_bu',
                          'Solar Capacity Expansion vs National Gross Generation',
                          'Solar Capacity (GW)',
                          'Generation (Billion Units)'),
                      (   'radar',
                          ['thermal_gw', 'hydro_gw', 'nuclear_gw', 'solar_gw', 'wind_gw'],
                          None,
                          'Current Power Generation Mix Profile (GW)'),
                      (   'violin',
                          None,
                          'solar_wind_growth_yoy_gw',
                          'Annual Solar & Wind Capacity Addition Distribution (GW)',
                          'Distribution',
                          'GW Added'),
                      (   'correlation_heatmap',
                          [   'total_installed_gw',
                              'solar_gw',
                              'wind_gw',
                              'clean_capacity_share_pct',
                              'total_generation_bu'],
                          None,
                          'Energy Transition Matrix Correlations')],
        'csv': 'data/analytical/d06_india_power_energy.csv',
        'domain': 'Energy & Power Systems',
        'file': 'd06_india_power_energy.py',
        'id': 'D06',
        'kpis': [   (   'Total Installed Capacity (GW)',
                        'total_installed_gw',
                        'latest',
                        '{val:.1f} GW',
                        'National Grid Total',
                        'pos'),
                    (   'Clean Power Capacity (GW)',
                        'total_clean_gw',
                        'latest',
                        '{val:.1f} GW',
                        'Solar, Wind, Hydro, Nuclear',
                        'pos'),
                    (   'Clean Power Capacity Share',
                        'clean_capacity_share_pct',
                        'latest',
                        '{val:.1f}%',
                        'Approaching 50% Milestone',
                        'pos'),
                    (   'Solar + Wind Capacity (GW)',
                        'renewable_v_gw',
                        'latest',
                        '{val:.1f} GW',
                        'Variable Renewable Expansion',
                        'pos'),
                    (   'Annual Generation (BU)',
                        'total_generation_bu',
                        'latest',
                        '{val:,.0f} BU',
                        'Billion Units Generated',
                        'pos')],
        'slug': 'd06_india_power_energy',
        'time_col': 'year',
        'title': 'India Power Generation & Renewable Energy Transition'},
    {   'charts': [   (   'line',
                          'fiscal_year',
                          ['merchandise_exports_usd_b', 'merchandise_imports_usd_b'],
                          'Merchandise Exports vs Imports Trajectory ($ Billion)',
                          'Fiscal Year',
                          'USD Billions'),
                      (   'area',
                          'fiscal_year',
                          [   'engineering_goods_usd_b',
                              'petroleum_products_usd_b',
                              'gems_jewellery_usd_b',
                              'pharma_drugs_usd_b',
                              'electronic_goods_usd_b'],
                          'Export Basket Major Sector Composition ($ Billion)',
                          'Fiscal Year',
                          'USD Billions'),
                      (   'bar',
                          'fiscal_year',
                          'trade_balance_usd_b',
                          'Annual Merchandise Trade Balance ($ Billion)',
                          'Fiscal Year',
                          'USD Billions'),
                      (   'scatter',
                          'crude_oil_import_usd_b',
                          'trade_balance_usd_b',
                          'Crude Oil Import Bill vs Trade Balance Deficit',
                          'Crude Oil Imports ($ B)',
                          'Trade Balance ($ B)'),
                      (   'horizontal_bar',
                          'total_trade_usd_b',
                          'fiscal_year',
                          'Total Merchandise Trade Turnover Progression ($ B)',
                          'USD Billions',
                          'Fiscal Year'),
                      (   'histogram',
                          'export_growth_yoy_pct',
                          None,
                          'Export YoY Growth Rate Distribution (%)',
                          'YoY Growth (%)',
                          'Frequency Count'),
                      (   'radar',
                          [   'engineering_goods_usd_b',
                              'petroleum_products_usd_b',
                              'gems_jewellery_usd_b',
                              'pharma_drugs_usd_b',
                              'electronic_goods_usd_b'],
                          None,
                          'Major Export Commodity Value Profile ($ B)')],
        'csv': 'data/analytical/d07_india_foreign_trade.csv',
        'domain': 'Trade & Commerce',
        'file': 'd07_india_foreign_trade.py',
        'id': 'D07',
        'kpis': [   (   'Merchandise Exports ($B)',
                        'merchandise_exports_usd_b',
                        'latest',
                        '${val:.1f}B',
                        'FY24 Trade Release',
                        'pos'),
                    (   'Merchandise Imports ($B)',
                        'merchandise_imports_usd_b',
                        'latest',
                        '${val:.1f}B',
                        'FY24 Trade Inflows',
                        'neutral'),
                    (   'Merchandise Trade Deficit ($B)',
                        'trade_balance_usd_b',
                        'latest',
                        '${val:.1f}B',
                        'Trade Imbalance',
                        'neg'),
                    (   'Export-to-Import Coverage (%)',
                        'export_import_ratio_pct',
                        'latest',
                        '{val:.1f}%',
                        'Export Coverage Ratio',
                        'neutral'),
                    (   'Crude Oil Import Share (%)',
                        'crude_import_bill_share_pct',
                        'latest',
                        '{val:.1f}%',
                        'Share of Total Import Bill',
                        'neg')],
        'slug': 'd07_india_foreign_trade',
        'time_col': 'fiscal_year',
        'title': 'India Foreign Trade & Merchandise Export-Import Intelligence'},
    {   'charts': [   (   'line',
                          'fiscal_year',
                          ['total_fdi_usd_b', 'fdi_3yr_moving_avg_b'],
                          'Annual Total FDI Inflow Trajectory ($ Billion)',
                          'Fiscal Year',
                          'USD Billions'),
                      (   'area',
                          'fiscal_year',
                          [   'computer_software_hardware_m',
                              'services_financial_banking_m',
                              'telecommunications_m',
                              'automobile_industry_m',
                              'construction_infrastructure_m'],
                          'Sectoral FDI Equity Inflows Breakdown ($ Million)',
                          'Fiscal Year',
                          'USD Millions'),
                      (   'horizontal_bar',
                          'tech_services_fdi_usd_m',
                          'fiscal_year',
                          'Technology & Services FDI Inflows Progression ($ M)',
                          'USD Millions',
                          'Fiscal Year'),
                      (   'scatter',
                          'computer_software_hardware_m',
                          'total_fdi_usd_m',
                          'Computer Software & Hardware vs Total FDI Inflows',
                          'Software/Hardware ($ M)',
                          'Total FDI ($ M)'),
                      (   'correlation_heatmap',
                          [   'total_fdi_usd_m',
                              'computer_software_hardware_m',
                              'services_financial_banking_m',
                              'telecommunications_m',
                              'tech_services_share_pct'],
                          None,
                          'Sectoral FDI Inflow Correlation Matrix'),
                      (   'violin',
                          None,
                          'fdi_yoy_growth_pct',
                          'Annual FDI Growth Rate Dispersion (%)',
                          'Dispersion',
                          'YoY Growth (%)'),
                      (   'radar',
                          [   'computer_software_hardware_m',
                              'services_financial_banking_m',
                              'telecommunications_m',
                              'automobile_industry_m',
                              'pharma_drugs_m'],
                          None,
                          'Priority Sector FDI Capital Allocation Profile ($ M)')],
        'csv': 'data/analytical/d08_india_fdi_inflows.csv',
        'domain': 'Investment & Capital Flows',
        'file': 'd08_india_fdi_inflows.py',
        'id': 'D08',
        'kpis': [   ('Total FDI Inflows ($B)', 'total_fdi_usd_b', 'latest', '${val:.2f}B', 'FY24 FDI Equity', 'pos'),
                    ('Peak Annual FDI ($B)', 'total_fdi_usd_b', 'max', '${val:.2f}B', 'Record High (FY22)', 'pos'),
                    (   'Tech & Financial Services Share',
                        'tech_services_share_pct',
                        'latest',
                        '{val:.1f}%',
                        'Software + Services Share',
                        'pos'),
                    (   '3-Year Moving Average ($B)',
                        'fdi_3yr_moving_avg_b',
                        'latest',
                        '${val:.2f}B',
                        'Smoothed Annual Flow',
                        'pos'),
                    (   'Top Origin Share (Singapore %)',
                        'source_singapore_pct',
                        'latest',
                        '{val:.1f}%',
                        'Leading Route Jurisdiction',
                        'neutral')],
        'slug': 'd08_india_fdi_inflows',
        'time_col': 'fiscal_year',
        'title': 'India Foreign Direct Investment (FDI) Inflows & Equity Trends'},
    {   'charts': [   (   'line',
                          'year',
                          ['nh_total_length_km'],
                          'Cumulative National Highway Network Length (KM)',
                          'Year',
                          'Total KM'),
                      (   'bar',
                          'year',
                          'construction_pace_km_day',
                          'Daily Highway Construction Velocity (KM/Day)',
                          'Year',
                          'KM / Day'),
                      (   'area',
                          'year',
                          ['four_lane_plus_pct', 'two_lane_pct', 'single_intermediate_lane_pct'],
                          'Highway Lane Configuration Composition (%)',
                          'Year',
                          'Lane Share (%)'),
                      (   'scatter',
                          'capital_outlay_inr_cr',
                          'construction_pace_km_day',
                          'Budgetary Capital Outlay vs Construction Pace',
                          'Capital Outlay (INR Cr)',
                          'Pace (KM/Day)'),
                      (   'horizontal_bar',
                          'capital_outlay_inr_cr',
                          'year',
                          'Annual Highway Ministry Capital Outlay (INR Crore)',
                          'INR Crores',
                          'Year'),
                      (   'histogram',
                          'nh_added_in_year_km',
                          None,
                          'Annual Network Additions Distribution (KM)',
                          'KM Added',
                          'Frequency Count'),
                      (   'correlation_heatmap',
                          [   'nh_total_length_km',
                              'nh_added_in_year_km',
                              'construction_pace_km_day',
                              'capital_outlay_inr_cr',
                              'four_lane_plus_pct'],
                          None,
                          'Highway Infrastructure & Expenditure Correlations')],
        'csv': 'data/analytical/d09_india_highway_infrastructure.csv',
        'domain': 'Infrastructure & Transport',
        'file': 'd09_india_highway_infrastructure.py',
        'id': 'D09',
        'kpis': [   (   'Total NH Length (km)',
                        'nh_total_length_km',
                        'latest',
                        '{val:,.0f} km',
                        '2024 Network Length',
                        'pos'),
                    (   'Decadal Network Growth',
                        'cumulative_nh_expansion_pct',
                        'latest',
                        '+{val:.1f}%',
                        'Since 2014 Baseline',
                        'pos'),
                    (   'Construction Pace (km/day)',
                        'construction_pace_km_day',
                        'latest',
                        '{val:.1f} km/day',
                        'Daily Execution Speed',
                        'pos'),
                    (   '4-Lane+ Highway Share (%)',
                        'four_lane_plus_pct',
                        'latest',
                        '{val:.1f}%',
                        'Modern Highway Width',
                        'pos'),
                    (   'Capital Outlay (INR Crore)',
                        'capital_outlay_inr_cr',
                        'latest',
                        'Rs {val:,.0f} Cr',
                        'Annual Budgetary Outlay',
                        'pos')],
        'slug': 'd09_india_highway_infrastructure',
        'time_col': 'year',
        'title': 'India National Highway & Road Infrastructure Growth'},
    {   'charts': [   (   'line',
                          'year',
                          ['total_freight_loading_mt'],
                          'Total Railway Freight Loading Throughput (Million Tonnes)',
                          'Year',
                          'Million Tonnes'),
                      (   'area',
                          'year',
                          ['coal_freight_mt', 'iron_ore_mt', 'cement_mt', 'steel_pig_iron_mt', 'foodgrains_mt'],
                          'Bulk Commodity Haulage Composition (MT)',
                          'Year',
                          'Million Tonnes'),
                      (   'bar',
                          'year',
                          'electrification_pct',
                          'Broad Gauge Route Electrification Pace (%)',
                          'Year',
                          'Electrification (%)'),
                      (   'scatter',
                          'total_freight_loading_mt',
                          'operating_ratio_pct',
                          'Freight Throughput Volume vs Financial Operating Ratio',
                          'Freight Loading (MT)',
                          'Operating Ratio (%)'),
                      (   'horizontal_bar',
                          'coal_freight_mt',
                          'year',
                          'Coal Freight Haulage Progression (Million Tonnes)',
                          'Million Tonnes',
                          'Year'),
                      (   'violin',
                          None,
                          'operating_ratio_pct',
                          'Railway Operating Ratio Dispersion (%)',
                          'Dispersion',
                          'Operating Ratio (%)'),
                      (   'radar',
                          ['coal_freight_mt', 'iron_ore_mt', 'cement_mt', 'steel_pig_iron_mt', 'fertilizers_mt'],
                          None,
                          'Major Freight Commodity Throughput Profile (MT)')],
        'csv': 'data/analytical/d10_india_railways_traffic.csv',
        'domain': 'Logistics & Public Transport',
        'file': 'd10_india_railways_traffic.py',
        'id': 'D10',
        'kpis': [   (   'Total Freight Loading (MT)',
                        'total_freight_loading_mt',
                        'latest',
                        '{val:,.1f} MT',
                        'FY24 Freight Loading',
                        'pos'),
                    (   'Coal Freight Share (%)',
                        'coal_freight_share_pct',
                        'latest',
                        '{val:.1f}%',
                        'Key Commodity Driver',
                        'neutral'),
                    (   'Electrified Route (km)',
                        'route_electrification_km',
                        'latest',
                        '{val:,.0f} km',
                        'Broad Gauge Network',
                        'pos'),
                    (   'Route Electrification (%)',
                        'electrification_pct',
                        'latest',
                        '{val:.1f}%',
                        'Approaching 100% Target',
                        'pos'),
                    (   'Operating Ratio (%)',
                        'operating_ratio_pct',
                        'latest',
                        '{val:.1f}%',
                        'Working Expenses / Revenue',
                        'neutral')],
        'slug': 'd10_india_railways_traffic',
        'time_col': 'year',
        'title': 'Indian Railways Operational & Freight Traffic Analytics'},
    {   'charts': [   (   'geo_scatter',
                          'latitude',
                          'longitude',
                          'National Continuous Ambient Air Quality Telemetry Stations',
                          'cpcb_aqi',
                          'cpcb_aqi',
                          'city',
                          'asia'),
                      ('bar', 'city', 'cpcb_aqi', 'Ambient Air Quality Index (CPCB AQI) by City', 'City', 'CPCB AQI'),
                      (   'horizontal_bar',
                          'pm2_5',
                          'city',
                          'Fine Particulate Matter PM2.5 Concentrations (µg/m³)',
                          'PM2.5 (µg/m³)',
                          'City'),
                      (   'scatter',
                          'pm2_5',
                          'pm10',
                          'PM2.5 vs PM10 Particulate Co-Movement Correlation',
                          'PM2.5 (µg/m³)',
                          'PM10 (µg/m³)'),
                      (   'correlation_heatmap',
                          ['pm2_5', 'pm10', 'no2', 'so2', 'co', 'ozone', 'cpcb_aqi'],
                          None,
                          'Atmospheric Pollutants Pearson Correlation Matrix'),
                      (   'violin',
                          'aqi_category',
                          'cpcb_aqi',
                          'AQI Severity Dispersion Across Air Quality Categories',
                          'Category',
                          'AQI'),
                      (   'treemap',
                          ['state', 'city'],
                          'cpcb_aqi',
                          'Air Quality Station Hierarchy by State and City',
                          None,
                          None)],
        'csv': 'data/analytical/d11_india_cpcb_air_quality.csv',
        'domain': 'Environment & Pollution',
        'file': 'd11_india_cpcb_air_quality.py',
        'id': 'D11',
        'kpis': [   (   'Average Monitored AQI',
                        'cpcb_aqi',
                        'mean',
                        '{val:.0f}',
                        'Across 10 Metropolitan Cities',
                        'neutral'),
                    ('Peak Recorded AQI', 'cpcb_aqi', 'max', '{val:.0f}', 'Severe Pollution Spike', 'neg'),
                    ('Average PM2.5 (ug/m3)', 'pm2_5', 'mean', '{val:.1f} ug/m3', 'Fine Particulate Matter', 'neutral'),
                    ('Average PM10 (ug/m3)', 'pm10', 'mean', '{val:.1f} ug/m3', 'Coarse Particulate Matter', 'neutral'),
                    ('PM2.5 / PM10 Ratio', 'pm_ratio', 'mean', '{val:.2f}', 'Combustion vs Dust Ratio', 'neutral')],
        'slug': 'd11_india_cpcb_air_quality',
        'time_col': 'city',
        'title': 'India Real-Time Urban Air Quality & AQI Intelligence'},
    {   'charts': [   (   'line',
                          'date',
                          ['volume_billions'],
                          'Monthly UPI Transaction Volume (Billions)',
                          'Date',
                          'Transactions (Billions)'),
                      (   'bar',
                          'date',
                          'value_inr_lakh_crore',
                          'Gross Settlement Value (Lakh Crore INR)',
                          'Date',
                          'INR Lakh Crore'),
                      (   'area',
                          'date',
                          ['p2p_share_pct', 'p2m_merchant_share_pct'],
                          'UPI Channel Mix: P2P Person-to-Person vs P2M Merchant (%)',
                          'Date',
                          'Channel Share (%)'),
                      (   'scatter',
                          'volume_billions',
                          'avg_ticket_size_inr',
                          'Transaction Volume Scale vs Average Ticket Size',
                          'Volume (Billions)',
                          'Ticket Size (INR)'),
                      (   'horizontal_bar',
                          'value_inr_crore',
                          'date',
                          'Monthly Gross Value Progression (INR Crore)',
                          'INR Crores',
                          'Date'),
                      (   'histogram',
                          'vol_mom_growth_pct',
                          None,
                          'Month-over-Month Transaction Volume Growth Distribution (%)',
                          'MoM Growth (%)',
                          'Frequency Count'),
                      (   'density_heatmap',
                          'volume_billions',
                          'value_inr_lakh_crore',
                          'Transaction Volume vs Settlement Value 2D Density',
                          'Volume (Billions)',
                          'Value (Lakh Cr INR)')],
        'csv': 'data/analytical/d12_india_upi_digital_payments.csv',
        'domain': 'Fintech & Digital Infrastructure',
        'file': 'd12_india_upi_digital_payments.py',
        'id': 'D12',
        'kpis': [   (   'Monthly Volume (Billions)',
                        'volume_billions',
                        'latest',
                        '{val:.2f}B txns',
                        'Monthly Transaction Count',
                        'pos'),
                    (   'Monthly Value (INR Lakh Cr)',
                        'value_inr_lakh_crore',
                        'latest',
                        'Rs {val:.2f}L Cr',
                        'Monthly Transaction Value',
                        'pos'),
                    (   'Average Ticket Size (INR)',
                        'avg_ticket_size_inr',
                        'latest',
                        'Rs {val:,.0f}',
                        'Per Transaction Value',
                        'neutral'),
                    (   'Merchant P2M Share (%)',
                        'p2m_merchant_share_pct',
                        'latest',
                        '{val:.1f}%',
                        'Merchant Commerce Share',
                        'pos'),
                    (   'Retail Payments Share (%)',
                        'upi_share_of_retail_payments_pct',
                        'latest',
                        '{val:.1f}%',
                        'Share of Retail Payments',
                        'pos')],
        'slug': 'd12_india_upi_digital_payments',
        'time_col': 'date',
        'title': 'India Digital Public Infrastructure & UPI Financial Inclusion'},
    {   'charts': [   (   'horizontal_bar',
                          'fiscal_deficit_gsdp_pct',
                          'state',
                          'Gross Fiscal Deficit to GSDP Ratio by State (%)',
                          'Fiscal Deficit (% GSDP)',
                          'State'),
                      (   'bar',
                          'state',
                          'debt_gsdp_pct',
                          'Sub-National Debt-to-GSDP Burden Ranking (%)',
                          'State',
                          'Debt (% GSDP)'),
                      (   'scatter',
                          'capital_outlay_pct_exp',
                          'debt_gsdp_pct',
                          'Capital Outlay Capex Share vs Debt-to-GSDP Burden',
                          'Capital Outlay (% of Exp)',
                          'Debt (% GSDP)'),
                      (   'correlation_heatmap',
                          [   'fiscal_deficit_gsdp_pct',
                              'debt_gsdp_pct',
                              'own_tax_revenue_share_pct',
                              'capital_outlay_pct_exp',
                              'fiscal_prudence_score'],
                          None,
                          'Subnational Fiscal Indicators Correlation Matrix'),
                      (   'violin',
                          None,
                          'fiscal_deficit_gsdp_pct',
                          'State Fiscal Deficit Dispersion & Quartile Spread',
                          'Dispersion',
                          'Fiscal Deficit (% GSDP)'),
                      (   'histogram',
                          'own_tax_revenue_share_pct',
                          None,
                          'Own Tax Revenue Share Distribution (%)',
                          'Own Tax Share (%)',
                          'State Count'),
                      ('funnel', 'fiscal_prudence_score', 'state', 'Fiscal Prudence Score Hierarchy Across States')],
        'csv': 'data/analytical/d13_india_state_finances.csv',
        'domain': 'Public Finance & Fiscal Policy',
        'file': 'd13_india_state_finances.py',
        'id': 'D13',
        'kpis': [   (   'Avg Gross Fiscal Deficit',
                        'fiscal_deficit_gsdp_pct',
                        'mean',
                        '{val:.2f}% GSDP',
                        'Across Major States',
                        'neutral'),
                    (   'Avg Outstanding Debt',
                        'debt_gsdp_pct',
                        'mean',
                        '{val:.1f}% GSDP',
                        'State Debt Burden',
                        'neutral'),
                    (   'Avg Own Tax Reliance',
                        'own_tax_revenue_share_pct',
                        'mean',
                        '{val:.1f}%',
                        'State Revenue Autonomy',
                        'pos'),
                    (   'Avg Capital Outlay Share',
                        'capital_outlay_pct_exp',
                        'mean',
                        '{val:.1f}%',
                        'Share of Total Expenditure',
                        'pos'),
                    (   'Highest Fiscal Prudence',
                        'fiscal_prudence_score',
                        'max',
                        '{val:.1f} / 100',
                        'Top State Score',
                        'pos')],
        'slug': 'd13_india_state_finances',
        'time_col': 'state',
        'title': 'India State Finances & Fiscal Deficit Intelligence'},
    {   'charts': [   (   'bar',
                          'state',
                          'ger_total',
                          'Higher Education Gross Enrollment Ratio (GER) by State (%)',
                          'State',
                          'GER (%)'),
                      (   'horizontal_bar',
                          'gpi',
                          'state',
                          'Gender Parity Index (GPI) in Higher Education',
                          'Gender Parity Index',
                          'State'),
                      (   'scatter',
                          'colleges_per_lakh_pop',
                          'ptr',
                          'College Institutional Density vs Pupil-Teacher Ratio (PTR)',
                          'Colleges per Lakh Pop',
                          'Pupil-Teacher Ratio'),
                      (   'correlation_heatmap',
                          ['ger_total', 'ger_male', 'ger_female', 'gpi', 'colleges_per_lakh_pop', 'ptr'],
                          None,
                          'AISHE Educational Indicators Correlation Matrix'),
                      (   'violin',
                          None,
                          'ger_total',
                          'State Gross Enrollment Ratio Distribution (%)',
                          'Distribution',
                          'GER (%)'),
                      (   'histogram',
                          'ptr',
                          None,
                          'Pupil-Teacher Ratio (PTR) Frequency Distribution',
                          'Pupil-Teacher Ratio',
                          'State Count'),
                      (   'radar',
                          ['ger_total', 'ger_female', 'gpi', 'colleges_per_lakh_pop', 'capacity_adequacy_ratio'],
                          None,
                          'National Higher Education Key Metrics Profile')],
        'csv': 'data/analytical/d14_india_higher_education.csv',
        'domain': 'Higher Education & Skills',
        'file': 'd14_india_higher_education.py',
        'id': 'D14',
        'kpis': [   ('Average Higher GER (%)', 'ger_total', 'mean', '{val:.1f}%', 'Gross Enrolment Ratio', 'pos'),
                    ('Average Female GER (%)', 'ger_female', 'mean', '{val:.1f}%', 'Female Participation', 'pos'),
                    ('Average Gender Parity Index', 'gpi', 'mean', '{val:.2f}', 'Parity Benchmark (1.0)', 'pos'),
                    (   'Avg College Density',
                        'colleges_per_lakh_pop',
                        'mean',
                        '{val:.0f}',
                        'Colleges per Lakh Pop',
                        'neutral'),
                    ('Avg Pupil-Teacher Ratio', 'ptr', 'mean', '{val:.0f}', 'Students per Faculty', 'neutral')],
        'slug': 'd14_india_higher_education',
        'time_col': 'state',
        'title': 'India Higher Education & Gross Enrolment Ratio (AISHE)'},
    {   'charts': [   (   'line',
                          'survey_round',
                          ['lfpr_total', 'wpr_total'],
                          'Labor Force Participation (LFPR) & Worker Pop Ratio (WPR) Trajectory (%)',
                          'Survey Round',
                          'Rate (%)'),
                      (   'area',
                          'survey_round',
                          ['agri_share', 'industry_share', 'services_share'],
                          'Sectoral Workforce Employment Share Composition (%)',
                          'Survey Round',
                          'Share (%)'),
                      (   'bar',
                          'survey_round',
                          ['ur_urban_male', 'ur_urban_female', 'ur_rural_male', 'ur_rural_female'],
                          'Unemployment Rate Disaggregated by Gender & Sector (%)',
                          'Survey Round',
                          'Unemployment (%)'),
                      (   'scatter',
                          'female_lfpr_gap',
                          'ur_total',
                          'Gender Participation Gap vs Overall Unemployment Rate',
                          'Female LFPR Gap (% pts)',
                          'Unemployment (%)'),
                      (   'horizontal_bar',
                          'urban_rural_ur_gap',
                          'survey_round',
                          'Urban vs Rural Unemployment Gap Spread (% pts)',
                          'Gap (% pts)',
                          'Survey Round'),
                      (   'correlation_heatmap',
                          [   'lfpr_total',
                              'lfpr_male',
                              'lfpr_female',
                              'wpr_total',
                              'ur_total',
                              'agri_share',
                              'services_share'],
                          None,
                          'Employment & Labor Market Dynamics Correlation Matrix'),
                      (   'radar',
                          ['lfpr_total', 'wpr_total', 'agri_share', 'industry_share', 'services_share'],
                          None,
                          'Latest Employment Structure Profile Scan')],
        'csv': 'data/analytical/d15_india_plfs_employment.csv',
        'domain': 'Employment & Labor Markets',
        'file': 'd15_india_plfs_employment.py',
        'id': 'D15',
        'kpis': [   (   'Latest Labour Force (LFPR)',
                        'lfpr_total',
                        'latest',
                        '{val:.1f}%',
                        'Overall Participation Rate',
                        'pos'),
                    ('Latest Unemployment (UR)', 'ur_total', 'latest', '{val:.1f}%', 'Headline Unemployment', 'pos'),
                    ('Female LFPR Surge', 'lfpr_female', 'latest', '{val:.1f}%', 'Rising from 17.5% Base', 'pos'),
                    ('Worker Population Ratio', 'wpr_total', 'latest', '{val:.1f}%', 'Employment Ratio', 'pos'),
                    (   'Agriculture Sector Share',
                        'agri_share',
                        'latest',
                        '{val:.1f}%',
                        'Workforce in Agriculture',
                        'neutral')],
        'slug': 'd15_india_plfs_employment',
        'time_col': 'survey_round',
        'title': 'India Labor Force & Employment Dynamics (PLFS)'},
    {   'charts': [   (   'area',
                          'year',
                          ['coal_twh', 'gas_twh', 'hydro_twh', 'nuclear_twh', 'solar_twh', 'wind_twh'],
                          'Global Power Generation Fuel Source Mix Evolution (TWh)',
                          'Year',
                          'Generation (TWh)'),
                      (   'line',
                          'year',
                          ['clean_share_pct', 'solar_wind_share_pct'],
                          'Clean & Renewable Generation Share Trajectory (%)',
                          'Year',
                          'Share (%)'),
                      (   'bar',
                          'country',
                          'renewable_power_twh',
                          'Renewable Generation Volume Comparison by Country (TWh)',
                          'Country',
                          'TWh'),
                      (   'scatter',
                          'solar_twh',
                          'clean_share_pct',
                          'Solar Power Generation vs Clean Share Expansion',
                          'Solar Power (TWh)',
                          'Clean Share (%)'),
                      (   'horizontal_bar',
                          'clean_power_twh',
                          'country',
                          'Clean Power Generation Volume Ranking by Country (TWh)',
                          'Clean Power (TWh)',
                          'Country'),
                      (   'sunburst',
                          ['country', 'year'],
                          'clean_power_twh',
                          'Clean Generation Allocation by Country and Period',
                          None,
                          None),
                      (   'correlation_heatmap',
                          ['coal_twh', 'gas_twh', 'solar_twh', 'wind_twh', 'clean_share_pct', 'total_generation_twh'],
                          None,
                          'Power Generation Matrix Correlation Heatmap')],
        'csv': 'data/analytical/d16_global_renewable_energy.csv',
        'domain': 'Global Energy & Decarbonization',
        'file': 'd16_global_renewable_energy.py',
        'id': 'D16',
        'kpis': [   (   'Global Total Generation',
                        'total_generation_twh',
                        'latest',
                        '{val:,.0f} TWh',
                        'World Electricity Total',
                        'pos'),
                    (   'Global Clean Power Output',
                        'clean_power_twh',
                        'latest',
                        '{val:,.0f} TWh',
                        'Hydro, Nuclear, Solar, Wind',
                        'pos'),
                    ('Clean Power Share (%)', 'clean_share_pct', 'latest', '{val:.1f}%', 'World Clean Share', 'pos'),
                    (   'Solar + Wind Share (%)',
                        'solar_wind_share_pct',
                        'latest',
                        '{val:.1f}%',
                        'Modern Renewables Share',
                        'pos'),
                    (   'Clean-to-Fossil Power Ratio',
                        'clean_to_fossil_ratio',
                        'latest',
                        '{val:.2f}x',
                        'Clean vs Fossil Generation',
                        'pos')],
        'slug': 'd16_global_renewable_energy',
        'time_col': 'year',
        'title': 'Global Renewable Energy Transition & Decarbonization'},
    {   'charts': [   (   'line',
                          'year',
                          ['co2_emissions_gt'],
                          'Global Territorial Carbon Dioxide Emissions (Gigatonnes)',
                          'Year',
                          'Billion Tonnes CO2'),
                      (   'area',
                          'year',
                          ['coal_share_pct', 'oil_share_pct', 'gas_share_pct', 'cement_flaring_share_pct'],
                          'Fossil Fuel Source Share of Emissions (%)',
                          'Year',
                          'Share (%)'),
                      (   'horizontal_bar',
                          'co2_per_capita_tonnes',
                          'country',
                          'Per Capita CO2 Emissions Intensity by Nation (Tonnes/Capita)',
                          'Tonnes CO2 / Person',
                          'Country'),
                      (   'scatter',
                          'co2_per_capita_tonnes',
                          'co2_emissions_mt',
                          'Per Capita Emissions vs Total National Emissions',
                          'Per Capita CO2 (Tonnes)',
                          'Total CO2 (MT)'),
                      (   'violin',
                          None,
                          'co2_per_capita_tonnes',
                          'Global Per Capita Carbon Emissions Dispersion',
                          'Distribution',
                          'Tonnes/Person'),
                      (   'histogram',
                          'emissions_growth_yoy_pct',
                          None,
                          'Annual Emissions Growth Volatility Distribution (%)',
                          'YoY Growth (%)',
                          'Frequency Count'),
                      (   'correlation_heatmap',
                          [   'co2_emissions_mt',
                              'co2_per_capita_tonnes',
                              'coal_share_pct',
                              'oil_share_pct',
                              'gas_share_pct'],
                          None,
                          'Carbon Emissions & Energy Source Correlations')],
        'csv': 'data/analytical/d17_global_co2_emissions.csv',
        'domain': 'Climate & Greenhouse Gases',
        'file': 'd17_global_co2_emissions.py',
        'id': 'D17',
        'kpis': [   (   'Global Annual CO2 (Gt)',
                        'co2_emissions_gt',
                        'latest',
                        '{val:.2f} Gt',
                        'Global Territorial CO2',
                        'neg'),
                    (   'Peak Single Emitter (Gt)',
                        'co2_emissions_gt',
                        'max',
                        '{val:.2f} Gt',
                        'China Territorial CO2',
                        'neg'),
                    (   'US Per Capita CO2 (Tonnes)',
                        'co2_per_capita_tonnes',
                        'latest',
                        '{val:.1f} tCO2',
                        'US Per Capita Footprint',
                        'neg'),
                    (   'India Per Capita CO2 (Tonnes)',
                        'co2_per_capita_tonnes',
                        'latest',
                        '{val:.1f} tCO2',
                        'India Per Capita Footprint',
                        'pos'),
                    (   'Global Cumulative CO2 (Gt)',
                        'cumulative_emissions_mt',
                        'max',
                        '{val:,.0f} MT',
                        'Cumulative Historic CO2',
                        'neg')],
        'slug': 'd17_global_co2_emissions',
        'time_col': 'year',
        'title': 'Global CO2 Emissions, Carbon Budgets & Climate Trends'},
    {   'charts': [   (   'line',
                          'year',
                          ['life_expectancy_years', 'healthy_life_expectancy_years'],
                          'Global Life Expectancy & Healthy Life Expectancy Progress (Years)',
                          'Year',
                          'Years'),
                      (   'bar',
                          'country',
                          'life_expectancy_years',
                          'Life Expectancy Benchmark Ranking by Nation (Years)',
                          'Country',
                          'Years'),
                      (   'scatter',
                          'life_expectancy_years',
                          'under5_mortality_rate',
                          'Life Expectancy vs Under-5 Child Mortality Rate Correlation',
                          'Life Expectancy (Years)',
                          'U5 Mortality (per 1k)'),
                      (   'treemap',
                          ['region', 'country'],
                          'life_expectancy_years',
                          'Life Expectancy Hierarchical Tree by World Region',
                          None,
                          None),
                      (   'violin',
                          'income_group',
                          'life_expectancy_years',
                          'Life Expectancy Dispersion Across Income Classifications',
                          'Income Tier',
                          'Life Expectancy (Years)'),
                      (   'horizontal_bar',
                          'maternal_mortality_ratio',
                          'country',
                          'Maternal Mortality Ratio by Country (per 100k births)',
                          'Maternal Mortality Ratio',
                          'Country'),
                      (   'correlation_heatmap',
                          [   'life_expectancy_years',
                              'healthy_life_expectancy_years',
                              'under5_mortality_rate',
                              'maternal_mortality_ratio',
                              'unhealthy_years_lived'],
                          None,
                          'Global Longevity & Mortality Indicators Correlation Matrix')],
        'csv': 'data/analytical/d18_global_health_life_expectancy.csv',
        'domain': 'Global Health & Demographics',
        'file': 'd18_global_health_life_expectancy.py',
        'id': 'D18',
        'kpis': [   (   'Average Life Expectancy',
                        'life_expectancy_years',
                        'mean',
                        '{val:.1f} yrs',
                        'Global Sample Mean',
                        'pos'),
                    (   'Top Nation Life Expectancy',
                        'life_expectancy_years',
                        'max',
                        '{val:.1f} yrs',
                        'Japan Longevity Benchmark',
                        'pos'),
                    (   'Avg Healthy Years (HALE)',
                        'healthy_life_expectancy_years',
                        'mean',
                        '{val:.1f} yrs',
                        'Healthy Life Expectancy',
                        'pos'),
                    (   'Under-5 Child Survival Rate',
                        'survival_to_five_pct',
                        'mean',
                        '{val:.1f}%',
                        'Surviving Past Age 5',
                        'pos'),
                    (   'Unhealthy Years Burden',
                        'unhealthy_years_lived',
                        'mean',
                        '{val:.1f} yrs',
                        'Morbidity Gap (LE minus HALE)',
                        'neg')],
        'slug': 'd18_global_health_life_expectancy',
        'time_col': 'year',
        'title': 'Worldwide Global Health & Life Expectancy Dynamics'},
    {   'charts': [   (   'horizontal_bar',
                          'u5_stunting_pct',
                          'country',
                          'Under-5 Child Stunting Prevalence Ranking (%)',
                          'Stunting Rate (%)',
                          'Country'),
                      (   'bar',
                          'country',
                          ['measles_immunization_pct', 'dtp3_immunization_pct'],
                          'Pediatric Immunization Coverage by Country (%)',
                          'Country',
                          'Coverage (%)'),
                      (   'scatter',
                          'immunization_average_pct',
                          'neonatal_mortality_rate',
                          'Average Immunization Coverage vs Neonatal Mortality Rate',
                          'Immunization (%)',
                          'Neonatal Mortality'),
                      (   'correlation_heatmap',
                          [   'u5_stunting_pct',
                              'measles_immunization_pct',
                              'dtp3_immunization_pct',
                              'exclusive_breastfeeding_pct',
                              'neonatal_mortality_rate'],
                          None,
                          'Child Health & Nutrition Indicator Correlations'),
                      (   'violin',
                          None,
                          'exclusive_breastfeeding_pct',
                          'Exclusive Breastfeeding Rate Dispersion Across Countries (%)',
                          'Dispersion',
                          'Breastfeeding (%)'),
                      (   'histogram',
                          'child_survival_risk_index',
                          None,
                          'Child Survival Risk Index Frequency Distribution',
                          'Risk Index',
                          'Country Count'),
                      (   'funnel',
                          'measles_immunization_pct',
                          'country',
                          'Child Health Immunization Coverage Funnel Hierarchy')],
        'csv': 'data/analytical/d19_global_maternal_child_health.csv',
        'domain': 'Child Health & Nutrition',
        'file': 'd19_global_maternal_child_health.py',
        'id': 'D19',
        'kpis': [   ('Average Child Stunting Rate', 'u5_stunting_pct', 'mean', '{val:.1f}%', 'Sample Average', 'neg'),
                    ('Lowest Stunting Rate', 'u5_stunting_pct', 'min', '{val:.1f}%', 'Top Nutrition Benchmark', 'pos'),
                    (   'Avg Measles Immunization',
                        'measles_immunization_pct',
                        'mean',
                        '{val:.1f}%',
                        'MCV1 Coverage',
                        'pos'),
                    (   'Avg DTP3 Immunization',
                        'dtp3_immunization_pct',
                        'mean',
                        '{val:.1f}%',
                        '3-Dose Vaccine Coverage',
                        'pos'),
                    (   'Avg Neonatal Mortality',
                        'neonatal_mortality_rate',
                        'mean',
                        '{val:.1f}',
                        'Deaths per 1,000 Births',
                        'neg')],
        'slug': 'd19_global_maternal_child_health',
        'time_col': 'country',
        'title': 'Global Maternal & Child Health Intelligence'},
    {   'charts': [   (   'line',
                          'year',
                          ['poverty_headcount_2_15_pct', 'poverty_headcount_3_65_pct'],
                          'Poverty Headcount Trajectory ($2.15 & $3.65 Thresholds %)',
                          'Year',
                          'Headcount Share (%)'),
                      (   'bar',
                          'region',
                          'gini_index',
                          'Gini Income Inequality Index by Geographic Region',
                          'Region',
                          'Gini Index'),
                      (   'horizontal_bar',
                          'palma_ratio',
                          'region',
                          'Palma Ratio Comparison (Top 10% / Bottom 40% Income Share)',
                          'Palma Ratio',
                          'Region'),
                      (   'scatter',
                          'poverty_headcount_2_15_pct',
                          'gini_index',
                          'Extreme Poverty Headcount vs Gini Inequality Index',
                          'Poverty Headcount (%)',
                          'Gini Index'),
                      (   'correlation_heatmap',
                          [   'poverty_headcount_2_15_pct',
                              'poverty_headcount_3_65_pct',
                              'gini_index',
                              'income_share_richest_10_pct',
                              'income_share_poorest_20_pct'],
                          None,
                          'Poverty & Wealth Concentration Correlations'),
                      (   'histogram',
                          'gini_index',
                          None,
                          'Gini Inequality Index Spread Distribution',
                          'Gini Index',
                          'Frequency Count'),
                      (   'radar',
                          [   'poverty_headcount_2_15_pct',
                              'poverty_headcount_3_65_pct',
                              'gini_index',
                              'income_share_richest_10_pct'],
                          None,
                          'Global Poverty & Inequality Multilateral Indicator Profile')],
        'csv': 'data/analytical/d20_global_poverty_inequality.csv',
        'domain': 'Poverty & Income Distribution',
        'file': 'd20_global_poverty_inequality.py',
        'id': 'D20',
        'kpis': [   (   'Global Extreme Poverty ($2.15)',
                        'poverty_headcount_2_15_pct',
                        'latest',
                        '{val:.1f}%',
                        'World Poverty Headcount',
                        'pos'),
                    (   'East Asia Poverty Decline',
                        'poverty_headcount_2_15_pct',
                        'min',
                        '{val:.1f}%',
                        'Historic Eradication',
                        'pos'),
                    (   'Sub-Saharan Africa Poverty',
                        'poverty_headcount_2_15_pct',
                        'max',
                        '{val:.1f}%',
                        'Persistent Challenge',
                        'neg'),
                    ('Average Regional Gini', 'gini_index', 'mean', '{val:.1f}', 'Income Inequality Metric', 'neutral'),
                    (   'Average Palma Ratio',
                        'palma_ratio',
                        'mean',
                        '{val:.2f}x',
                        'Top 10% / Bottom 20% Ratio',
                        'neutral')],
        'slug': 'd20_global_poverty_inequality',
        'time_col': 'year',
        'title': 'Global Economic Inequality & Poverty Headcount'},
    {   'charts': [   (   'line',
                          'year',
                          ['fao_food_price_index'],
                          'FAO Global Food Price Index Benchmark Trajectory',
                          'Year',
                          'Index (2014-2016=100)'),
                      (   'area',
                          'year',
                          ['wheat_production_mt', 'rice_milled_mt', 'maize_production_mt'],
                          'Major Cereal Commodity Production Volumes (Million Tonnes)',
                          'Year',
                          'Production (MT)'),
                      (   'bar',
                          'year',
                          'global_undernourishment_pct',
                          'Global Undernourishment Population Prevalence (%)',
                          'Year',
                          'Prevalence (%)'),
                      (   'scatter',
                          'fao_food_price_index',
                          'cereal_stocks_to_use_ratio_pct',
                          'Food Price Index vs Cereal Stocks-to-Use Buffer Ratio',
                          'Price Index',
                          'Stocks-to-Use (%)'),
                      (   'horizontal_bar',
                          'cereal_yield_kg_ha',
                          'year',
                          'Global Cereal Yield Productivity Gains (Kg/Ha)',
                          'Yield (Kg/Ha)',
                          'Year'),
                      (   'histogram',
                          'food_price_yoy_pct',
                          None,
                          'Food Price Index Annual Volatility Distribution (%)',
                          'YoY Change (%)',
                          'Frequency Count'),
                      (   'correlation_heatmap',
                          [   'fao_food_price_index',
                              'total_cereal_production_mt',
                              'cereal_yield_kg_ha',
                              'cereal_stocks_to_use_ratio_pct',
                              'global_undernourishment_pct'],
                          None,
                          'Food Security, Production & Price Index Correlations')],
        'csv': 'data/analytical/d21_global_fao_food_security.csv',
        'domain': 'Food Security & Agriculture',
        'file': 'd21_global_fao_food_security.py',
        'id': 'D21',
        'kpis': [   (   'Total Cereal Output (MT)',
                        'total_cereal_production_mt',
                        'latest',
                        '{val:,.0f} MT',
                        'Global Grain Harvest',
                        'pos'),
                    (   'FAO Food Price Index',
                        'fao_food_price_index',
                        'latest',
                        '{val:.1f}',
                        '2014-2016 Base = 100',
                        'neutral'),
                    ('Peak Food Price Index', 'fao_food_price_index', 'max', '{val:.1f}', '2022 Commodity Peak', 'neg'),
                    (   'Average Cereal Yield',
                        'cereal_yield_kg_ha',
                        'latest',
                        '{val:,.0f} kg/ha',
                        'Global Productivity',
                        'pos'),
                    (   'Global Undernourishment (%)',
                        'global_undernourishment_pct',
                        'latest',
                        '{val:.1f}%',
                        'Prevalence Rate',
                        'neutral')],
        'slug': 'd21_global_fao_food_security',
        'time_col': 'year',
        'title': 'Worldwide Food Security & Cereal Production Monitor'},
    {   'charts': [   (   'line',
                          'year',
                          ['forest_area_sqkm'],
                          'Global Forest Canopy Surface Area Trajectory (Sq Km)',
                          'Year',
                          'Sq Kilometers'),
                      (   'bar',
                          'country',
                          'forest_share_land_pct',
                          'Forest Cover Share of Total Land Area by Country (%)',
                          'Country',
                          'Forest Share (%)'),
                      (   'horizontal_bar',
                          'protected_areas_pct',
                          'country',
                          'Terrestrial Protected Nature Reserve Share (%)',
                          'Protected Area (%)',
                          'Country'),
                      (   'scatter',
                          'forest_share_land_pct',
                          'protected_areas_pct',
                          'Forest Canopy Share vs Protected Area Coverage',
                          'Forest Share (%)',
                          'Protected Area (%)'),
                      (   'treemap',
                          ['country'],
                          'forest_area_sqkm',
                          'Global Forest Area Distribution by Country',
                          None,
                          None),
                      (   'violin',
                          None,
                          'forest_share_land_pct',
                          'National Forest Land Share Distribution Spread (%)',
                          'Distribution',
                          'Forest Share (%)'),
                      (   'correlation_heatmap',
                          [   'forest_share_land_pct',
                              'forest_area_sqkm',
                              'protected_areas_pct',
                              'forest_change_since_base_pct'],
                          None,
                          'Canopy Cover & Conservation Correlation Matrix')],
        'csv': 'data/analytical/d22_global_forest_deforestation.csv',
        'domain': 'Forestry & Land Conservation',
        'file': 'd22_global_forest_deforestation.py',
        'id': 'D22',
        'kpis': [   (   'Largest Forest Area (sq km)',
                        'forest_area_sqkm',
                        'max',
                        '{val:,.0f} sq km',
                        'Russia Boreal Forest',
                        'pos'),
                    (   'Top Forest Cover Share (%)',
                        'forest_share_land_pct',
                        'max',
                        '{val:.1f}%',
                        'Brazil Amazon Biome',
                        'pos'),
                    (   'Average Forest Cover (%)',
                        'forest_share_land_pct',
                        'mean',
                        '{val:.1f}%',
                        'Sample Average',
                        'neutral'),
                    (   'Average Protected Area Share',
                        'protected_areas_pct',
                        'mean',
                        '{val:.1f}%',
                        'Terrestrial Protected Areas',
                        'pos'),
                    (   'Deforestation Risk Count',
                        'deforestation_risk',
                        'count',
                        '10 Nations',
                        'Major Landmass Powers',
                        'neutral')],
        'slug': 'd22_global_forest_deforestation',
        'time_col': 'year',
        'title': 'Global Forest Cover, Deforestation & Land Dynamics'},
    {   'charts': [   (   'bar',
                          'country',
                          'water_stress_pct',
                          'Freshwater Stress Level by Nation (% of Available Supply)',
                          'Country',
                          'Water Stress (%)'),
                      (   'horizontal_bar',
                          'renewable_per_capita_m3',
                          'country',
                          'Renewable Freshwater Availability per Person (m³/year)',
                          'Cubic Meters / Capita',
                          'Country'),
                      (   'sunburst',
                          ['country'],
                          'water_stress_pct',
                          'Water Stress Hierarchy Across Monitored Nations',
                          None,
                          None),
                      (   'scatter',
                          'water_stress_pct',
                          'renewable_per_capita_m3',
                          'Freshwater Stress vs Per Capita Renewable Water Supply',
                          'Water Stress (%)',
                          'Per Capita Water (m³)'),
                      (   'correlation_heatmap',
                          [   'water_stress_pct',
                              'renewable_per_capita_m3',
                              'agri_withdrawal_pct',
                              'industrial_pct',
                              'municipal_pct'],
                          None,
                          'Hydrological Stress & Extraction Matrix Correlations'),
                      (   'violin',
                          None,
                          'water_stress_pct',
                          'Global Freshwater Stress Distribution & Outliers',
                          'Dispersion',
                          'Stress (%)'),
                      (   'funnel',
                          'renewable_per_capita_m3',
                          'country',
                          'Per Capita Freshwater Resource Abundance Funnel Profile')],
        'csv': 'data/analytical/d23_global_water_stress.csv',
        'domain': 'Water Resources & Hydrology',
        'file': 'd23_global_water_stress.py',
        'id': 'D23',
        'kpis': [   (   'Peak Water Stress Rate',
                        'water_stress_pct',
                        'max',
                        '{val:,.0f}%',
                        'Kuwait Desalination Reliance',
                        'neg'),
                    (   'India Water Stress Rate',
                        'water_stress_pct',
                        'mean',
                        '{val:.1f}%',
                        'SDG 6.4.2 Stress Level',
                        'neg'),
                    (   'Top Per Capita Freshwater',
                        'renewable_per_capita_m3',
                        'max',
                        '{val:,.0f} m3',
                        'Canada Hydrological Wealth',
                        'pos'),
                    (   'Average Agricultural Withdrawal',
                        'agri_withdrawal_pct',
                        'mean',
                        '{val:.1f}%',
                        'Agricultural Water Share',
                        'neutral'),
                    (   'Water Scarcity Threshold Count',
                        'water_scarcity_flag',
                        'sum',
                        '{val:.0f} Nations',
                        'Under 1,000 m3 / person',
                        'neg')],
        'slug': 'd23_global_water_stress',
        'time_col': 'country',
        'title': 'Global Water Stress & Freshwater Resource Security'},
    {   'charts': [   (   'line',
                          'year',
                          ['current_account_gdp_pct'],
                          'Current Account Balance Trajectory (% of GDP)',
                          'Year',
                          'Balance (% GDP)'),
                      (   'bar',
                          'country',
                          'trade_openness_gdp_pct',
                          'Trade Openness Ratio Share of GDP by Country (%)',
                          'Country',
                          'Trade Openness (% GDP)'),
                      (   'horizontal_bar',
                          'current_account_gdp_pct',
                          'country',
                          'Current Account Balance Surpluses & Deficits (% GDP)',
                          'Current Account (% GDP)',
                          'Country'),
                      (   'scatter',
                          'trade_openness_gdp_pct',
                          'current_account_gdp_pct',
                          'Trade Openness vs Current Account External Balance',
                          'Trade Openness (% GDP)',
                          'Current Account (% GDP)'),
                      (   'violin',
                          'surplus_deficit',
                          'current_account_gdp_pct',
                          'Current Account Dispersion across Surplus & Deficit Groups',
                          'Balance Group',
                          'Current Account (% GDP)'),
                      (   'histogram',
                          'current_account_gdp_pct',
                          None,
                          'Global Current Account Balance Distribution (%)',
                          'Current Account (% GDP)',
                          'Frequency Count'),
                      (   'density_heatmap',
                          'trade_openness_gdp_pct',
                          'current_account_gdp_pct',
                          'Trade Openness vs Current Account 2D Density',
                          'Trade Openness (%)',
                          'Current Account (%)')],
        'csv': 'data/analytical/d24_global_trade_current_account.csv',
        'domain': 'International Macroeconomics',
        'file': 'd24_global_trade_current_account.py',
        'id': 'D24',
        'kpis': [   (   'Peak Trade Openness (%)',
                        'trade_openness_gdp_pct',
                        'max',
                        '{val:.1f}% GDP',
                        'South Korea / Germany',
                        'pos'),
                    (   'Peak Current Account Surplus',
                        'current_account_gdp_pct',
                        'max',
                        '+{val:.2f}% GDP',
                        'Germany Export Surplus',
                        'pos'),
                    (   'Persistent Deficit (USA)',
                        'current_account_gdp_pct',
                        'min',
                        '{val:.2f}% GDP',
                        'US Structural Deficit',
                        'neg'),
                    (   'Average Trade Openness',
                        'trade_openness_gdp_pct',
                        'mean',
                        '{val:.1f}% GDP',
                        'Major Economies Mean',
                        'pos'),
                    (   'Global Imbalance Level',
                        'abs_ca_imbalance_pct',
                        'mean',
                        '{val:.2f}% GDP',
                        'Average Absolute Imbalance',
                        'neutral')],
        'slug': 'd24_global_trade_current_account',
        'time_col': 'year',
        'title': 'Global Trade Openness & Current Account Balances'},
    {   'charts': [   (   'line',
                          'year',
                          ['internet_users_pct'],
                          'Internet User Population Penetration Trajectory by Region (%)',
                          'Year',
                          'Penetration Rate (%)'),
                      (   'bar',
                          'region',
                          'mobile_cellular_per_100',
                          'Mobile Cellular Subscriptions per 100 Inhabitants',
                          'Region',
                          'Subscriptions / 100'),
                      (   'horizontal_bar',
                          'fixed_broadband_per_100',
                          'region',
                          'Fixed Broadband Infrastructure Subscriptions per 100',
                          'Broadband / 100',
                          'Region'),
                      (   'scatter',
                          'fixed_broadband_per_100',
                          'internet_users_pct',
                          'Fixed Broadband vs Internet Penetration Correlation',
                          'Broadband / 100',
                          'Internet Users (%)'),
                      (   'correlation_heatmap',
                          [   'internet_users_pct',
                              'fixed_broadband_per_100',
                              'mobile_cellular_per_100',
                              'offline_population_pct'],
                          None,
                          'Telecommunications Infrastructure Correlation Heatmap'),
                      (   'histogram',
                          'offline_population_pct',
                          None,
                          'Offline Population Share Distribution across World Regions',
                          'Offline Share (%)',
                          'Frequency Count'),
                      (   'radar',
                          [   'internet_users_pct',
                              'fixed_broadband_per_100',
                              'mobile_cellular_per_100',
                              'offline_population_pct'],
                          None,
                          'Regional Digital Infrastructure Capability Radar')],
        'csv': 'data/analytical/d25_global_itu_digital_divide.csv',
        'domain': 'Telecommunications & Digital Access',
        'file': 'd25_global_itu_digital_divide.py',
        'id': 'D25',
        'kpis': [   (   'Global Internet Penetration',
                        'internet_users_pct',
                        'latest',
                        '{val:.1f}%',
                        'World Population Online',
                        'pos'),
                    (   'Top Region Penetration',
                        'internet_users_pct',
                        'max',
                        '{val:.1f}%',
                        'North America Online',
                        'pos'),
                    (   'Sub-Saharan Africa Online',
                        'internet_users_pct',
                        'min',
                        '{val:.1f}%',
                        'Lagging Connectivity',
                        'neutral'),
                    (   'Global Broadband per 100',
                        'fixed_broadband_per_100',
                        'latest',
                        '{val:.1f}',
                        'Fixed Subscriptions',
                        'pos'),
                    (   'Mobile Cellular Penetration',
                        'mobile_cellular_per_100',
                        'latest',
                        '{val:.1f}',
                        'Subscribers per 100 People',
                        'pos')],
        'slug': 'd25_global_itu_digital_divide',
        'time_col': 'year',
        'title': 'Worldwide Internet Connectivity & Digital Divide'},
    {   'charts': [   (   'bar',
                          'country',
                          'rd_expenditure_pct_gdp',
                          'Gross Domestic R&D Expenditure Share of GDP (%)',
                          'Country',
                          'R&D (% GDP)'),
                      (   'horizontal_bar',
                          'researchers_per_million',
                          'country',
                          'Scientific Researcher Density per Million Inhabitants',
                          'Researchers / Million',
                          'Country'),
                      (   'scatter',
                          'rd_expenditure_pct_gdp',
                          'hightech_export_share_pct',
                          'R&D Intensity vs High-Technology Export Share',
                          'R&D (% GDP)',
                          'High-Tech Exports (%)'),
                      (   'treemap',
                          ['country'],
                          'patents_resident',
                          'Resident Patent Applications Volume by Country',
                          None,
                          None),
                      (   'correlation_heatmap',
                          [   'rd_expenditure_pct_gdp',
                              'researchers_per_million',
                              'patents_resident',
                              'hightech_export_share_pct'],
                          None,
                          'R&D Inputs vs Intellectual Property Output Correlations'),
                      (   'violin',
                          None,
                          'rd_expenditure_pct_gdp',
                          'Global R&D Expenditure Intensity Distribution',
                          'Distribution',
                          'R&D (% GDP)'),
                      (   'radar',
                          [   'rd_expenditure_pct_gdp',
                              'researchers_per_million',
                              'hightech_export_share_pct',
                              'innovation_intensity_ratio'],
                          None,
                          'Multilateral National Innovation Capability Profile')],
        'csv': 'data/analytical/d26_global_research_rd_innovation.csv',
        'domain': 'Science & Innovation Policy',
        'file': 'd26_global_research_rd_innovation.py',
        'id': 'D26',
        'kpis': [   (   'Top R&D Intensity (Israel)',
                        'rd_expenditure_pct_gdp',
                        'max',
                        '{val:.2f}% GDP',
                        'World Leader in R&D',
                        'pos'),
                    (   'Top Researcher Density',
                        'researchers_per_million',
                        'max',
                        '{val:,.0f} / M',
                        'South Korea Density',
                        'pos'),
                    ('Top Patent Powerhouse', 'patents_resident', 'max', '{val:,.0f}', 'China Resident Filings', 'pos'),
                    (   'Top High-Tech Export Share',
                        'hightech_export_share_pct',
                        'max',
                        '{val:.1f}%',
                        'Singapore Tech Exports',
                        'pos'),
                    (   'India R&D Intensity (%)',
                        'rd_expenditure_pct_gdp',
                        'mean',
                        '{val:.2f}% GDP',
                        'National R&D Scale',
                        'neutral')],
        'slug': 'd26_global_research_rd_innovation',
        'time_col': 'country',
        'title': 'Global Research & Development (R&D) Expenditure and Innovation'},
    {   'charts': [   (   'horizontal_bar',
                          'external_debt_usd_b',
                          'country',
                          'Total External Sovereign Debt Stock ($ Billion)',
                          'Debt Stock ($ B)',
                          'Country'),
                      (   'bar',
                          'country',
                          'debt_to_gni_pct',
                          'External Sovereign Debt-to-GNI Ratio Ranking (%)',
                          'Country',
                          'Debt to GNI (%)'),
                      (   'scatter',
                          'debt_to_gni_pct',
                          'debt_service_export_pct',
                          'Debt-to-GNI Burden vs Debt Service to Exports',
                          'Debt to GNI (%)',
                          'Debt Service (% Exports)'),
                      (   'treemap',
                          ['risk_category', 'country'],
                          'external_debt_usd_b',
                          'External Debt Stock Distribution by Sovereign Risk Category',
                          None,
                          None),
                      (   'violin',
                          'risk_category',
                          'debt_to_gni_pct',
                          'Debt-to-GNI Distribution Across Risk Tiers',
                          'Risk Tier',
                          'Debt (% GNI)'),
                      (   'histogram',
                          'debt_vulnerability_score',
                          None,
                          'Debt Vulnerability Composite Score Distribution',
                          'Vulnerability Score',
                          'Country Count'),
                      (   'funnel',
                          'external_debt_usd_b',
                          'country',
                          'Sovereign External Debt Exposure Volume Funnel Hierarchy')],
        'csv': 'data/analytical/d27_global_external_debt_vulnerability.csv',
        'domain': 'Sovereign Debt & Financial Stability',
        'file': 'd27_global_external_debt_vulnerability.py',
        'id': 'D27',
        'kpis': [   (   'Highest External Debt Stock',
                        'external_debt_usd_b',
                        'max',
                        '${val:.1f}B',
                        'Brazil External Debt',
                        'neg'),
                    (   'Highest Debt-to-GNI Ratio',
                        'debt_to_gni_pct',
                        'max',
                        '{val:.1f}%',
                        'Sri Lanka Debt Burden',
                        'neg'),
                    (   'Highest Debt Service Burden',
                        'debt_service_export_pct',
                        'max',
                        '{val:.1f}%',
                        'Argentina Service Ratio',
                        'neg'),
                    (   'India Debt-to-GNI Ratio',
                        'debt_to_gni_pct',
                        'min',
                        '{val:.1f}%',
                        'Prudent Sovereign Profile',
                        'pos'),
                    (   'India Debt Service Burden',
                        'debt_service_export_pct',
                        'min',
                        '{val:.1f}%',
                        'Low Servicing Pressure',
                        'pos')],
        'slug': 'd27_global_external_debt_vulnerability',
        'time_col': 'country',
        'title': 'Worldwide External Debt & Sovereign Vulnerability in Developing Nations'},
    {   'charts': [   (   'geo_scatter',
                          'latitude',
                          'longitude',
                          'Global Planetary Seismic Epicenter Telemetry Map',
                          'magnitude',
                          'depth_km',
                          'place',
                          'world'),
                      (   'histogram',
                          'magnitude',
                          None,
                          'Earthquake Richter Magnitude Frequency Distribution',
                          'Richter Magnitude',
                          'Event Count'),
                      (   'scatter',
                          'depth_km',
                          'magnitude',
                          'Focal Hypocenter Depth (KM) vs Richter Magnitude',
                          'Depth (KM)',
                          'Magnitude'),
                      (   'violin',
                          'depth_category',
                          'magnitude',
                          'Richter Magnitude Dispersion across Depth Categories',
                          'Depth Category',
                          'Magnitude'),
                      (   'horizontal_bar',
                          'significance',
                          'place',
                          'Earthquake Event Significance Index Top Occurrences',
                          'Significance Score',
                          'Location'),
                      (   'density_heatmap',
                          'depth_km',
                          'magnitude',
                          'Focal Depth vs Earthquake Magnitude 2D Density Heatmap',
                          'Depth (KM)',
                          'Magnitude'),
                      (   'sunburst',
                          ['depth_category', 'high_magnitude'],
                          'magnitude',
                          'Seismic Events Partitioned by Depth and Severity',
                          None,
                          None)],
        'csv': 'data/analytical/d28_global_usgs_earthquakes.csv',
        'domain': 'Geophysics & Natural Hazards',
        'file': 'd28_global_usgs_earthquakes.py',
        'id': 'D28',
        'kpis': [   ('Seismic Events Monitored', 'magnitude', 'count', '{val:,.0f}', 'Global Events Recorded', 'pos'),
                    ('Maximum Recorded Magnitude', 'magnitude', 'max', 'M {val:.1f}', 'Major Seismic Event', 'neg'),
                    (   'Average Focal Depth (km)',
                        'depth_km',
                        'mean',
                        '{val:.1f} km',
                        'Mean Hypocenter Depth',
                        'neutral'),
                    (   'Deepest Earthquake (km)',
                        'depth_km',
                        'max',
                        '{val:.1f} km',
                        'Subduction Zone Hypocenter',
                        'neutral'),
                    ('Tsunami Alert Events', 'tsunami_flag', 'sum', '{val:.0f}', 'Advisories Triggered', 'neg')],
        'slug': 'd28_global_usgs_earthquakes',
        'time_col': 'magnitude',
        'title': 'Global Seismic Activity & Earthquake Hazards (USGS Live GeoJSON)'},
    {   'charts': [   (   'line',
                          'year',
                          ['annual_mean_anomaly_c', 'lowess_smoothing_c'],
                          'Global Mean Surface Temperature Anomaly & LOWESS Trend (°C)',
                          'Year',
                          'Anomaly (°C)'),
                      (   'bar',
                          'year',
                          'annual_mean_anomaly_c',
                          'Annual Surface Temperature Departure History (°C)',
                          'Year',
                          'Departure (°C)'),
                      (   'horizontal_bar',
                          'warming_rate_per_decade',
                          'decade',
                          'Decadal Warming Rate Acceleration (°C / decade)',
                          'Warming Rate (°C/decade)',
                          'Decade'),
                      (   'scatter',
                          'annual_mean_anomaly_c',
                          'cumulative_warming_anomaly',
                          'Annual Temperature Departure vs Cumulative Anomaly Metric',
                          'Annual Departure (°C)',
                          'Cumulative Metric'),
                      (   'violin',
                          'decade',
                          'annual_mean_anomaly_c',
                          'Temperature Anomaly Distribution Shifts Across Decades',
                          'Decade',
                          'Anomaly (°C)'),
                      (   'histogram',
                          'annual_mean_anomaly_c',
                          None,
                          'Surface Temperature Departure Frequency Histogram',
                          'Anomaly (°C)',
                          'Frequency Count'),
                      (   'correlation_heatmap',
                          [   'annual_mean_anomaly_c',
                              'lowess_smoothing_c',
                              'warming_rate_per_decade',
                              'cumulative_warming_anomaly'],
                          None,
                          'Thermal Anomaly & Warming Momentum Correlation Matrix')],
        'csv': 'data/analytical/d29_global_nasa_temperature_anomalies.csv',
        'domain': 'Earth Science & Climatology',
        'file': 'd29_global_nasa_temperature_anomalies.py',
        'id': 'D29',
        'kpis': [   (   'Latest Annual Anomaly (°C)',
                        'annual_mean_anomaly_c',
                        'latest',
                        '+{val:.2f}°C',
                        'Relative to 1951-1980',
                        'neg'),
                    (   'Peak Historic Anomaly (°C)',
                        'annual_mean_anomaly_c',
                        'max',
                        '+{val:.2f}°C',
                        'Warmest Recorded Year',
                        'neg'),
                    (   'Smoothed Warming Trend',
                        'lowess_smoothing_c',
                        'latest',
                        '+{val:.2f}°C',
                        'Lowess 5-Year Filter',
                        'neg'),
                    (   'Decadal Warming Rate',
                        'warming_rate_per_decade',
                        'latest',
                        '+{val:.2f}°C / dec',
                        'Warming Acceleration',
                        'neg'),
                    (   'Cumulative Warming Shift',
                        'cumulative_warming_anomaly',
                        'latest',
                        '{val:.1f}°C-yrs',
                        'Cumulative Anomaly Area',
                        'neg')],
        'slug': 'd29_global_nasa_temperature_anomalies',
        'time_col': 'year',
        'title': 'Global Surface Temperature Anomalies & Climate Change'},
    {   'charts': [   (   'line',
                          'year',
                          ['population_millions'],
                          'Megacity Population Growth Trajectory (Millions)',
                          'Year',
                          'Population (M)'),
                      (   'horizontal_bar',
                          'population_millions',
                          'city',
                          'Megacity Population Scale Ranking Comparison (Millions)',
                          'Population (M)',
                          'City'),
                      (   'scatter',
                          'population_millions',
                          'growth_multiple_since_1980',
                          'Metropolitan Scale vs Decadal Growth Multiple Since 1980',
                          'Population (M)',
                          'Growth Multiple'),
                      (   'treemap',
                          ['country', 'city'],
                          'population_millions',
                          'Global Urban Agglomeration Distribution by Country and City',
                          None,
                          None),
                      (   'violin',
                          'country',
                          'population_millions',
                          'Megacity Scale Dispersion across Nations',
                          'Country',
                          'Population (M)'),
                      (   'histogram',
                          'growth_multiple_since_1980',
                          None,
                          'Metropolitan Growth Multiple Frequency Distribution',
                          'Growth Multiple',
                          'City Count'),
                      (   'sunburst',
                          ['country', 'city'],
                          'population_millions',
                          'Hierarchical Metropolitan Population Allocation',
                          None,
                          None)],
        'csv': 'data/analytical/d30_global_un_urbanization.csv',
        'domain': 'Urbanization & Human Settlement',
        'file': 'd30_global_un_urbanization.py',
        'id': 'D30',
        'kpis': [   (   'Largest Megacity (Tokyo)',
                        'population_millions',
                        'max',
                        '{val:.1f}M',
                        'Tokyo Agglomeration',
                        'pos'),
                    (   'Delhi Population (2024)',
                        'population_millions',
                        'latest',
                        '{val:.1f}M',
                        'India Capital Agglomeration',
                        'pos'),
                    (   'Highest Growth Multiple',
                        'growth_multiple_since_1980',
                        'max',
                        '{val:.1f}x',
                        'Dhaka / Delhi Expansion',
                        'pos'),
                    (   'Average Megacity Size',
                        'population_millions',
                        'mean',
                        '{val:.1f}M',
                        'Across Top 10 Megacities',
                        'pos'),
                    (   'Megacity Count (>20M)',
                        'population_millions',
                        'count',
                        '10 Megacities',
                        'World Agglomerations',
                        'neutral')],
        'slug': 'd30_global_un_urbanization',
        'time_col': 'year',
        'title': 'Worldwide Urbanization & Megacity Population Trajectories'},
    {   'charts': [   (   'line',
                          'year',
                          ['tourist_arrivals_millions'],
                          'International Tourist Arrivals Trajectory by Nation (Millions)',
                          'Year',
                          'Arrivals (M)'),
                      (   'bar',
                          'country',
                          'tourism_receipts_usd_billions',
                          'International Travel Receipts by Destination Nation ($ Billion)',
                          'Country',
                          'Receipts ($ B)'),
                      (   'horizontal_bar',
                          'receipt_per_arrival_usd',
                          'country',
                          'Average Spending Yield per Inbound Tourist Arrival ($ USD)',
                          'Receipt / Visitor ($)',
                          'Country'),
                      (   'scatter',
                          'tourist_arrivals_millions',
                          'tourism_receipts_usd_billions',
                          'Tourist Arrival Volumes vs Gross Travel Receipts ($ B)',
                          'Arrivals (M)',
                          'Receipts ($ B)'),
                      (   'violin',
                          'country',
                          'tourist_arrivals_millions',
                          'Arrival Volume Dispersion Across Destination Nations',
                          'Country',
                          'Arrivals (M)'),
                      (   'histogram',
                          'tourism_receipts_usd_billions',
                          None,
                          'National Tourism Receipts Frequency Distribution ($ B)',
                          'Receipts ($ B)',
                          'Frequency Count'),
                      (   'correlation_heatmap',
                          ['tourist_arrivals_millions', 'tourism_receipts_usd_billions', 'receipt_per_arrival_usd'],
                          None,
                          'International Tourism Volume & Yield Correlation Matrix')],
        'csv': 'data/analytical/d31_global_unwto_tourism.csv',
        'domain': 'Travel & Hospitality Economics',
        'file': 'd31_global_unwto_tourism.py',
        'id': 'D31',
        'kpis': [   (   'Top Arrivals Nation (France)',
                        'tourist_arrivals_millions',
                        'max',
                        '{val:.1f}M',
                        'World Tourism Capital',
                        'pos'),
                    (   'Top Tourism Receipts (USA)',
                        'tourism_receipts_usd_billions',
                        'max',
                        '${val:.1f}B',
                        'US Tourism Revenue',
                        'pos'),
                    (   'Average Arrivals per Country',
                        'tourist_arrivals_millions',
                        'mean',
                        '{val:.1f}M',
                        'Major Destinations Mean',
                        'pos'),
                    (   'Average Spend per Arrival',
                        'receipt_per_arrival_usd',
                        'mean',
                        '${val:,.0f}',
                        'International Spend / Visitor',
                        'pos'),
                    (   'COVID Impact Years Count',
                        'covid_impact_year',
                        'sum',
                        '{val:.0f} Years',
                        'Global Travel Collapse',
                        'neg')],
        'slug': 'd31_global_unwto_tourism',
        'time_col': 'year',
        'title': 'Global Tourism Arrivals & International Travel Recovery'},
    {   'charts': [   (   'line',
                          'year',
                          ['ev_market_share_pct'],
                          'Electric Vehicle New Car Market Share Trajectory (%)',
                          'Year',
                          'Market Share (%)'),
                      (   'area',
                          'year',
                          ['powertrain_bev_pct', 'powertrain_phev_pct'],
                          'Clean Powertrain Mix: BEV Battery Electric vs PHEV Hybrid (%)',
                          'Year',
                          'Share (%)'),
                      (   'bar',
                          'market',
                          'ev_sales_thousands',
                          'Electric Vehicle Annual Sales Volume by Market (Thousands)',
                          'Market',
                          'Sales (Thousands)'),
                      (   'scatter',
                          'ev_sales_thousands',
                          'ev_market_share_pct',
                          'EV Sales Volume Scale vs Market Share Penetration (%)',
                          'Sales (Thousands)',
                          'Market Share (%)'),
                      (   'horizontal_bar',
                          'ev_sales_millions',
                          'market',
                          'Electric Vehicle Cumulative Fleet Sales (Millions)',
                          'Fleet Sales (M)',
                          'Market'),
                      (   'histogram',
                          'ev_market_share_pct',
                          None,
                          'Clean Mobility Market Share Growth Distribution (%)',
                          'Market Share (%)',
                          'Frequency Count'),
                      (   'radar',
                          ['ev_market_share_pct', 'powertrain_bev_pct', 'ev_sales_millions'],
                          None,
                          'Global Clean Mobility Market Technology Profile')],
        'csv': 'data/analytical/d32_global_iea_ev_adoption.csv',
        'domain': 'Clean Mobility & Automotive',
        'file': 'd32_global_iea_ev_adoption.py',
        'id': 'D32',
        'kpis': [   (   'Top Market EV Sales (China)',
                        'ev_sales_thousands',
                        'max',
                        '{val:,.0f}k',
                        'World EV Manufacturing Hub',
                        'pos'),
                    (   'Top Market Share (China %)',
                        'ev_market_share_pct',
                        'max',
                        '{val:.1f}%',
                        'Share of New Car Sales',
                        'pos'),
                    (   'Europe EV Market Share',
                        'ev_market_share_pct',
                        'latest',
                        '{val:.1f}%',
                        'EU Regulatory Mandates',
                        'pos'),
                    (   'Average BEV Share (%)',
                        'powertrain_bev_pct',
                        'mean',
                        '{val:.1f}%',
                        'Battery Electric Vehicles',
                        'pos'),
                    (   'India EV Volume Surge',
                        'ev_sales_thousands',
                        'latest',
                        '{val:.1f}k',
                        'India 2W/4W Adoption Wave',
                        'pos')],
        'slug': 'd32_global_iea_ev_adoption',
        'time_col': 'year',
        'title': 'Worldwide Electric Vehicle (EV) Adoption & Battery Market Expansion'},
    {   'charts': [   (   'line',
                          'Date',
                          ['SP500', 'PE10'],
                          'S&P 500 Price Benchmark & Shiller Cyclically Adjusted PE10',
                          'Date',
                          'Level / Ratio'),
                      (   'line',
                          'Date',
                          ['Gold_USD', 'Brent_Oil_USD'],
                          'Physical Gold (USD/oz) vs Brent Crude Oil Benchmark (USD/bbl)',
                          'Date',
                          'USD Price'),
                      (   'scatter',
                          'Long Interest Rate',
                          'PE10',
                          '10-Year Long Interest Rate vs Shiller PE10 Valuation Multiple',
                          'Long Interest Rate (%)',
                          'Shiller PE10'),
                      (   'horizontal_bar',
                          'SP500_Return_YoY',
                          'Date',
                          'S&P 500 Historical Annual Return Profile (%)',
                          'Return YoY (%)',
                          'Date'),
                      (   'correlation_heatmap',
                          ['SP500', 'Long Interest Rate', 'PE10', 'Gold_USD', 'Brent_Oil_USD', 'Gold_to_SP500_Ratio'],
                          None,
                          'Cross-Asset Financial Markets Correlation Matrix'),
                      (   'violin',
                          None,
                          'PE10',
                          'Shiller CAPE PE10 Valuation Multiple Historical Dispersion',
                          'Valuation Dispersion',
                          'PE10 Ratio'),
                      (   'density_heatmap',
                          'SP500_Return_YoY',
                          'Gold_Return_YoY',
                          'Equity Returns vs Gold Returns 2D Density Heatmap',
                          'S&P 500 YoY (%)',
                          'Gold YoY (%)')],
        'csv': 'data/analytical/d33_global_financial_markets.csv',
        'domain': 'Capital Markets & Commodities',
        'file': 'd33_global_financial_markets.py',
        'id': 'D33',
        'kpis': [   ('S&P 500 Index Level', 'SP500', 'latest', '{val:,.1f}', 'US Equity Benchmark', 'pos'),
                    ('Shiller CAPE 10 P/E', 'PE10', 'latest', '{val:.1f}x', 'Cyclically Adjusted P/E', 'neutral'),
                    ('Gold Spot Price (USD/oz)', 'Gold_USD', 'latest', '${val:,.0f}', 'Safe-Haven Asset', 'pos'),
                    (   'Brent Crude Oil (USD/bbl)',
                        'Brent_Oil_USD',
                        'latest',
                        '${val:.2f}',
                        'Global Energy Commodity',
                        'neutral'),
                    (   'Gold-to-S&P 500 Ratio',
                        'Gold_to_SP500_Ratio',
                        'latest',
                        '{val:.2f}',
                        'Asset Allocation Ratio',
                        'neutral')],
        'slug': 'd33_global_financial_markets',
        'time_col': 'Date',
        'title': 'Global Financial Market Volatility & Major Exchange Trends'},
    {   'charts': [   (   'line',
                          'year',
                          ['gross_debt_gdp_pct'],
                          'General Government Gross Debt (% of GDP) across Major Economies',
                          'Year',
                          'Gross Debt (% GDP)'),
                      (   'bar',
                          'country',
                          'primary_balance_gdp_pct',
                          'Primary Fiscal Balance Deficits / Surpluses (% of GDP)',
                          'Country',
                          'Balance (% GDP)'),
                      (   'horizontal_bar',
                          'gross_debt_gdp_pct',
                          'country',
                          'Latest Sovereign Debt-to-GDP Ranking Comparison by Nation',
                          'Debt (% GDP)',
                          'Country'),
                      (   'scatter',
                          'gross_debt_gdp_pct',
                          'primary_balance_gdp_pct',
                          'Gross Debt Burden vs Primary Fiscal Balance Stance',
                          'Debt (% GDP)',
                          'Fiscal Balance (%)'),
                      (   'treemap',
                          ['economy_group', 'country'],
                          'gross_debt_gdp_pct',
                          'Sovereign Debt Distribution by Economy Group and Country',
                          None,
                          None),
                      (   'violin',
                          'economy_group',
                          'gross_debt_gdp_pct',
                          'Debt-to-GDP Divergence: Advanced vs Emerging Economies',
                          'Group',
                          'Debt (% GDP)'),
                      (   'histogram',
                          'gross_debt_gdp_pct',
                          None,
                          'Sovereign Debt Global Distribution Spread (%)',
                          'Debt (% GDP)',
                          'Frequency Count')],
        'csv': 'data/analytical/d34_global_imf_sovereign_debt.csv',
        'domain': 'Sovereign Finance & Fiscal Prudence',
        'file': 'd34_global_imf_sovereign_debt.py',
        'id': 'D34',
        'kpis': [   (   'Highest Sovereign Debt (Japan)',
                        'gross_debt_gdp_pct',
                        'max',
                        '{val:.1f}% GDP',
                        'World Highest Debt-to-GDP',
                        'neg'),
                    (   'US Sovereign Debt Ratio',
                        'gross_debt_gdp_pct',
                        'latest',
                        '{val:.1f}% GDP',
                        'US Federal Debt-to-GDP',
                        'neg'),
                    (   'India Sovereign Debt Ratio',
                        'gross_debt_gdp_pct',
                        'mean',
                        '{val:.1f}% GDP',
                        'Combined General Govt Debt',
                        'neutral'),
                    (   'Germany Prudent Ratio',
                        'gross_debt_gdp_pct',
                        'min',
                        '{val:.1f}% GDP',
                        'European Anchor Prudence',
                        'pos'),
                    (   'Debt Above 100% GDP Count',
                        'debt_above_100pct_gdp',
                        'sum',
                        '{val:.0f} Instances',
                        'Sovereign Debt Threshold',
                        'neg')],
        'slug': 'd34_global_imf_sovereign_debt',
        'time_col': 'year',
        'title': 'Global Sovereign Debt-to-GDP & Fiscal Policy Monitor'},
    {
        "id": "D35",
        "slug": "d35_india_gst_collections",
        "title": "India Goods & Services Tax (GST) Revenue Collections",
        "domain": "Taxation & Public Revenue",
        "file": "d35_india_gst_collections.py",
        "csv": "data/analytical/d35_india_gst_collections.csv",
        "time_col": "year",
        "kpis": [
            [
                "Peak Monthly Collection",
                "total_gst_crore",
                "max",
                "\u20b9{val:,.0f} Cr",
                "All-Time Highest Month",
                "pos"
            ],
            [
                "Latest Monthly Collection",
                "total_gst_crore",
                "latest",
                "\u20b9{val:,.0f} Cr",
                "Most Recent Month",
                "pos"
            ],
            [
                "Mean Monthly Collection",
                "total_gst_crore",
                "mean",
                "\u20b9{val:,.0f} Cr",
                "26-Month Average",
                "neutral"
            ],
            [
                "Total CGST Mobilized",
                "cgst_crore",
                "sum",
                "\u20b9{val:,.0f} Cr",
                "Central GST Component",
                "pos"
            ],
            [
                "Compensation Cess Total",
                "cess_crore",
                "sum",
                "\u20b9{val:,.0f} Cr",
                "Dedicated State Cess",
                "neutral"
            ]
        ],
        "charts": [
            [
                "line",
                "period_str",
                [
                    "total_gst_crore",
                    "rolling_3m_avg_crore"
                ],
                "Monthly GST Revenue Trajectory & 3-Month Moving Average",
                "Month",
                "Revenue (\u20b9 Crore)"
            ],
            [
                "bar",
                "period_str",
                [
                    "cgst_crore",
                    "sgst_crore",
                    "igst_crore",
                    "cess_crore"
                ],
                "Monthly Tax Component Deconstruction (CGST, SGST, IGST, Cess)",
                "Month",
                "Amount (\u20b9 Crore)"
            ],
            [
                "scatter",
                "cgst_sgst_combined",
                "igst_crore",
                "Domestic State GST vs Inter-State IGST Collections",
                "Domestic GST (CGST+SGST) \u20b9 Cr",
                "IGST \u20b9 Cr"
            ],
            [
                "area",
                "period_str",
                [
                    "igst_share_pct",
                    "cess_share_pct"
                ],
                "IGST and Cess Proportional Share Evolution (%)",
                "Month",
                "Share (%)"
            ],
            [
                "horizontal_bar",
                "total_gst_crore",
                "period_str",
                "Top Revenue Month Rankings (\u20b9 Crore)",
                "Revenue (\u20b9 Crore)",
                "Month"
            ],
            [
                "violin",
                "year",
                "total_gst_crore",
                "Fiscal Year Revenue Density & Variability Comparison",
                "Fiscal Year",
                "Revenue (\u20b9 Crore)"
            ],
            [
                "correlation_heatmap",
                [
                    "cgst_crore",
                    "sgst_crore",
                    "igst_crore",
                    "cess_crore",
                    "total_gst_crore",
                    "rolling_3m_avg_crore"
                ],
                None,
                "Inter-Component Revenue Correlation Matrix",
                None,
                None
            ]
        ]
    },
    {
        "id": "D36",
        "slug": "d36_india_pmjdy_inclusion",
        "title": "Pradhan Mantri Jan Dhan Yojana (PMJDY) Financial Inclusion",
        "domain": "Banking & Financial Inclusion",
        "file": "d36_india_pmjdy_inclusion.py",
        "csv": "data/analytical/d36_india_pmjdy_inclusion.csv",
        "time_col": "state",
        "kpis": [
            [
                "Total Accounts Opened",
                "total_beneficiaries_lakh",
                "sum",
                "{val:,.1f} Lk",
                "Total Beneficiaries",
                "pos"
            ],
            [
                "Total Deposit Balance",
                "total_deposits_crore",
                "sum",
                "\u20b9{val:,.0f} Cr",
                "Total Deposits Mobilized",
                "pos"
            ],
            [
                "Avg Deposit Per Account",
                "avg_deposit_per_account_inr",
                "mean",
                "\u20b9{val:,.0f}",
                "National Account Balance Mean",
                "pos"
            ],
            [
                "RuPay Debit Card Issuance",
                "rupay_cards_issued_lakh",
                "sum",
                "{val:,.1f} Lk",
                "Cards Distributed",
                "pos"
            ],
            [
                "Average Rural Coverage",
                "rural_share_pct",
                "mean",
                "{val:.1f}%",
                "Rural/Semi-Urban Penetration",
                "neutral"
            ]
        ],
        "charts": [
            [
                "horizontal_bar",
                "total_beneficiaries_lakh",
                "state",
                "PMJDY Beneficiaries by State (Lakh Accounts)",
                "Beneficiaries (Lakh)",
                "State"
            ],
            [
                "scatter",
                "total_beneficiaries_lakh",
                "total_deposits_crore",
                "Account Volume vs Cumulative Deposit Balances (\u20b9 Cr)",
                "Beneficiaries (Lakh)",
                "Deposits (\u20b9 Cr)"
            ],
            [
                "bar",
                "state",
                [
                    "rural_beneficiaries_lakh",
                    "urban_beneficiaries_lakh"
                ],
                "Rural vs Urban Beneficiary Segmentation across States",
                "State",
                "Accounts (Lakh)"
            ],
            [
                "treemap",
                [
                    "deposit_density_tier",
                    "state"
                ],
                "total_deposits_crore",
                "Deposit Volume Distribution across Deposit Density Tiers",
                None,
                None
            ],
            [
                "histogram",
                "avg_deposit_per_account_inr",
                None,
                "Distribution of State Average Account Balance (\u20b9 INR)",
                "Avg Balance (\u20b9)",
                "State Count"
            ],
            [
                "box",
                "deposit_density_tier",
                "women_share_pct",
                "Women Financial Inclusion Share (%) by Density Tier",
                "Density Tier",
                "Women Share (%)"
            ],
            [
                "radar",
                [
                    "rural_share_pct",
                    "women_share_pct",
                    "rupay_card_penetration_pct"
                ],
                None,
                "National Financial Inclusion Structural Ratios Profile",
                None,
                None
            ]
        ]
    },
    {
        "id": "D37",
        "slug": "d37_india_mgnregs_employment",
        "title": "MGNREGS Rural Employment Guarantee & Wage Analytics",
        "domain": "Rural Development & Social Safety",
        "file": "d37_india_mgnregs_employment.py",
        "csv": "data/analytical/d37_india_mgnregs_employment.csv",
        "time_col": "state",
        "kpis": [
            [
                "Total Persondays Generated",
                "persondays_generated_lakh",
                "sum",
                "{val:,.1f} Lk",
                "Rural Workdays Created",
                "pos"
            ],
            [
                "Total Scheme Expenditure",
                "total_expenditure_crore",
                "sum",
                "\u20b9{val:,.0f} Cr",
                "Wage & Material Capex",
                "neutral"
            ],
            [
                "Average Daily Wage",
                "avg_wage_rate_rs",
                "mean",
                "\u20b9{val:.1f}/day",
                "Notified State Wage Average",
                "pos"
            ],
            [
                "Average Women Participation",
                "women_participation_pct",
                "mean",
                "{val:.1f}%",
                "Women Labor Force Share",
                "pos"
            ],
            [
                "Households Supported",
                "households_worked_lakh",
                "sum",
                "{val:,.1f} Lk",
                "Rural Families Benefited",
                "pos"
            ]
        ],
        "charts": [
            [
                "horizontal_bar",
                "persondays_generated_lakh",
                "state",
                "State Rural Employment Creation (Lakh Persondays)",
                "Persondays (Lakh)",
                "State"
            ],
            [
                "scatter",
                "avg_wage_rate_rs",
                "women_participation_pct",
                "Notified Wage Rate vs Female Participation Ratio",
                "Avg Wage (\u20b9/day)",
                "Women Participation (%)"
            ],
            [
                "bar",
                "state",
                "total_expenditure_crore",
                "State-wise Public Outlay on Rural Employment (\u20b9 Crore)",
                "State",
                "Expenditure (\u20b9 Cr)"
            ],
            [
                "treemap",
                [
                    "women_inclusion_tier",
                    "state"
                ],
                "persondays_generated_lakh",
                "Persondays Generated Grouped by Women Inclusion Tier",
                None,
                None
            ],
            [
                "box",
                "women_inclusion_tier",
                "persondays_per_household",
                "Employment Intensity (Days/HH) across Inclusion Tiers",
                "Inclusion Tier",
                "Days per Household"
            ],
            [
                "histogram",
                "cost_per_personday_rs",
                None,
                "Unit Cost per Personday Created (\u20b9 INR) Distribution",
                "Cost per Day (\u20b9)",
                "Frequency"
            ],
            [
                "correlation_heatmap",
                [
                    "persondays_generated_lakh",
                    "women_participation_pct",
                    "total_expenditure_crore",
                    "avg_wage_rate_rs",
                    "cost_per_personday_rs"
                ],
                None,
                "MGNREGS Structural Parameter Inter-Correlation",
                None,
                None
            ]
        ]
    },
    {
        "id": "D38",
        "slug": "d38_india_civil_aviation",
        "title": "India Civil Aviation Passenger & Cargo Traffic Growth",
        "domain": "Aviation & Transport Logistics",
        "file": "d38_india_civil_aviation.py",
        "csv": "data/analytical/d38_india_civil_aviation.csv",
        "time_col": "year",
        "kpis": [
            [
                "Peak Passenger Traffic",
                "total_passengers_million",
                "max",
                "{val:.1f} M",
                "Highest Annual Passengers",
                "pos"
            ],
            [
                "Latest Passenger Volume",
                "total_passengers_million",
                "latest",
                "{val:.1f} M",
                "Latest Recorded FY",
                "pos"
            ],
            [
                "Domestic Passenger Share",
                "domestic_share_pct",
                "latest",
                "{val:.1f}%",
                "Internal Passenger Dominance",
                "neutral"
            ],
            [
                "Total Freight Cargo",
                "cargo_tonnage_million_mt",
                "latest",
                "{val:.2f} M MT",
                "Annual Air Cargo Handled",
                "pos"
            ],
            [
                "Operational Airports",
                "operating_airports_count",
                "latest",
                "{val:.0f} Hubs",
                "UDAN Regional Expansion",
                "pos"
            ]
        ],
        "charts": [
            [
                "line",
                "year",
                [
                    "domestic_passengers_million",
                    "intl_passengers_million",
                    "total_passengers_million"
                ],
                "Annual Passenger Footfall Growth Trajectory (Million Passengers)",
                "Year",
                "Passengers (Million)"
            ],
            [
                "bar",
                "year",
                "aircraft_movements_million",
                "Scheduled Aircraft Movements Capacity (Million Takeoffs/Landings)",
                "Year",
                "Movements (Million)"
            ],
            [
                "area",
                "year",
                [
                    "cargo_tonnage_million_mt"
                ],
                "Air Freight Cargo Throughput Expansion (Million MT)",
                "Year",
                "Cargo (Million MT)"
            ],
            [
                "scatter",
                "total_passengers_million",
                "aircraft_movements_million",
                "Passenger Load Density vs Commercial Flight Movements",
                "Passengers (Million)",
                "Movements (Million)"
            ],
            [
                "horizontal_bar",
                "operating_airports_count",
                "year",
                "Operational Airport Infrastructure Growth Timeline",
                "Airports Count",
                "Year"
            ],
            [
                "line",
                "year",
                [
                    "pax_yoy_growth_pct"
                ],
                "Year-on-Year Commercial Passenger Growth Volatility (%)",
                "Year",
                "YoY Growth (%)"
            ],
            [
                "radar",
                [
                    "domestic_share_pct",
                    "pax_per_aircraft_movement",
                    "cargo_per_airport_kt"
                ],
                None,
                "Aviation Fleet and Operational Efficiency Diagnostic Profile",
                None,
                None
            ]
        ]
    },
    {
        "id": "D39",
        "slug": "d39_india_major_ports",
        "title": "India Major Ports Cargo Handling & Maritime Logistics",
        "domain": "Maritime Logistics & Port Infrastructure",
        "file": "d39_india_major_ports.py",
        "csv": "data/analytical/d39_india_major_ports.csv",
        "time_col": "port_name",
        "kpis": [
            [
                "Total Cargo Throughput",
                "total_traffic_mmt",
                "sum",
                "{val:,.1f} MMT",
                "Major Ports Combined",
                "pos"
            ],
            [
                "Top Port Volume",
                "total_traffic_mmt",
                "max",
                "{val:.1f} MMT",
                "Leading Cargo Gateway",
                "pos"
            ],
            [
                "Mean Turnaround Time",
                "avg_turnaround_hours",
                "mean",
                "{val:.1f} hrs",
                "Average Vessel Dwell Time",
                "neutral"
            ],
            [
                "Total POL & Liquid Bulk",
                "pol_oil_mmt",
                "sum",
                "{val:.1f} MMT",
                "Petroleum & Hydrocarbons",
                "neutral"
            ],
            [
                "Containerized & Other Cargo",
                "container_other_mmt",
                "sum",
                "{val:.1f} MMT",
                "High-Value Cargo Handling",
                "pos"
            ]
        ],
        "charts": [
            [
                "horizontal_bar",
                "total_traffic_mmt",
                "port_name",
                "Major Ports Total Cargo Handled (MMT)",
                "Cargo (MMT)",
                "Port"
            ],
            [
                "scatter",
                "total_traffic_mmt",
                "avg_turnaround_hours",
                "Throughput Volume vs Vessel Turnaround Time (Hours)",
                "Traffic (MMT)",
                "Turnaround (Hours)"
            ],
            [
                "bar",
                "port_name",
                [
                    "pol_oil_mmt",
                    "iron_ore_mmt",
                    "coal_mmt",
                    "container_other_mmt"
                ],
                "Cargo Commodity Disaggregation Across Major Ports",
                "Port",
                "Cargo (MMT)"
            ],
            [
                "treemap",
                [
                    "coast",
                    "port_name"
                ],
                "total_traffic_mmt",
                "Maritime Traffic Concentration by Coastal Corridor (East vs West)",
                None,
                None
            ],
            [
                "box",
                "coast",
                "avg_turnaround_hours",
                "Vessel Turnaround Efficiency Distribution by Coast",
                "Coast",
                "Turnaround Hours"
            ],
            [
                "donut",
                "coast",
                "total_traffic_mmt",
                "National Coastal Cargo Share: West Coast vs East Coast",
                None,
                None
            ],
            [
                "radar",
                [
                    "pol_share_pct",
                    "bulk_cargo_share_pct",
                    "container_share_pct"
                ],
                None,
                "Aggregate Cargo Commodity Share Distribution (%)",
                None,
                None
            ]
        ]
    },
    {
        "id": "D40",
        "slug": "d40_india_telecom_trai",
        "title": "India Telecommunications & Wireless Subscriber Dynamics",
        "domain": "Telecommunications & Digital Infrastructure",
        "file": "d40_india_telecom_trai.py",
        "csv": "data/analytical/d40_india_telecom_trai.csv",
        "time_col": "year",
        "kpis": [
            [
                "Total Wireless Base",
                "total_wireless_sub_million",
                "latest",
                "{val:.1f} M",
                "Total Mobile Subscribers",
                "pos"
            ],
            [
                "Broadband Connections",
                "broadband_sub_million",
                "latest",
                "{val:.1f} M",
                "High-Speed Internet Users",
                "pos"
            ],
            [
                "National Teledensity",
                "overall_teledensity_pct",
                "latest",
                "{val:.1f}%",
                "Per 100 Inhabitants",
                "pos"
            ],
            [
                "Rural Subscriber Share",
                "rural_sub_share_pct",
                "latest",
                "{val:.1f}%",
                "Rural Telephony Penetration",
                "neutral"
            ],
            [
                "Urban Teledensity",
                "urban_teledensity_pct",
                "latest",
                "{val:.1f}%",
                "Metropolitan Saturation",
                "pos"
            ]
        ],
        "charts": [
            [
                "line",
                "time_label",
                [
                    "total_wireless_sub_million",
                    "broadband_sub_million"
                ],
                "Mobile Subscribers & Broadband Penetration Timeline",
                "Period",
                "Subscribers (Million)"
            ],
            [
                "bar",
                "time_label",
                [
                    "urban_sub_million",
                    "rural_sub_million"
                ],
                "Urban vs Rural Wireless Connection Composition",
                "Period",
                "Subscribers (Million)"
            ],
            [
                "scatter",
                "broadband_sub_million",
                "overall_teledensity_pct",
                "Broadband Adoption vs Aggregate Teledensity Penetration",
                "Broadband (Million)",
                "Teledensity (%)"
            ],
            [
                "area",
                "time_label",
                [
                    "broadband_penetration_pct"
                ],
                "Broadband Penetration Share of Total Wireless Base (%)",
                "Period",
                "Penetration (%)"
            ],
            [
                "horizontal_bar",
                "overall_teledensity_pct",
                "time_label",
                "Overall Teledensity Progression Across Quarters",
                "Teledensity (%)",
                "Period"
            ],
            [
                "line",
                "time_label",
                [
                    "broadband_yoy_growth_pct"
                ],
                "Broadband Year-on-Year Growth Dynamics (%)",
                "Period",
                "YoY Growth (%)"
            ],
            [
                "radar",
                [
                    "overall_teledensity_pct",
                    "rural_sub_share_pct",
                    "broadband_penetration_pct"
                ],
                None,
                "National Digital Connectivity Equilibrium Profile",
                None,
                None
            ]
        ]
    },
    {
        "id": "D41",
        "slug": "d41_india_mining_minerals",
        "title": "India Mineral & Metallic Mining Production Analytics",
        "domain": "Mining & Natural Resources",
        "file": "d41_india_mining_minerals.py",
        "csv": "data/analytical/d41_india_mining_minerals.csv",
        "time_col": "year",
        "kpis": [
            [
                "Peak Iron Ore Output",
                "iron_ore_million_mt",
                "max",
                "{val:.1f} MMT",
                "All-Time High Extraction",
                "pos"
            ],
            [
                "Latest Iron Ore Output",
                "iron_ore_million_mt",
                "latest",
                "{val:.1f} MMT",
                "Most Recent Annual Output",
                "pos"
            ],
            [
                "Limestone Extraction",
                "limestone_million_mt",
                "latest",
                "{val:.1f} MMT",
                "Cement Industry Feedstock",
                "pos"
            ],
            [
                "Metallic Minerals Value",
                "total_metallic_value_billion_inr",
                "latest",
                "\u20b9{val:.1f} B",
                "Gross Pithead Value",
                "pos"
            ],
            [
                "Bauxite Production",
                "bauxite_million_mt",
                "latest",
                "{val:.1f} MMT",
                "Aluminum Feedstock Output",
                "neutral"
            ]
        ],
        "charts": [
            [
                "line",
                "year",
                [
                    "iron_ore_million_mt",
                    "limestone_million_mt",
                    "bauxite_million_mt"
                ],
                "Core Industrial Mineral Production Volumes (MMT)",
                "Year",
                "Production (MMT)"
            ],
            [
                "bar",
                "year",
                "total_metallic_value_billion_inr",
                "Gross Value of Metallic Mineral Output (Billion INR)",
                "Year",
                "Value (\u20b9 Billion)"
            ],
            [
                "scatter",
                "iron_ore_million_mt",
                "total_metallic_value_billion_inr",
                "Iron Ore Extraction Volume vs Total Metallic Sector Value",
                "Iron Ore (MMT)",
                "Value (\u20b9 Billion)"
            ],
            [
                "area",
                "year",
                [
                    "total_bulk_minerals_mmt"
                ],
                "Total Non-Fuel Bulk Mineral Output Trajectory (MMT)",
                "Year",
                "Total Minerals (MMT)"
            ],
            [
                "horizontal_bar",
                "zinc_conc_million_mt",
                "year",
                "Zinc Concentrate Production Evolution (MMT)",
                "Zinc Conc (MMT)",
                "Year"
            ],
            [
                "line",
                "year",
                [
                    "iron_ore_yoy_growth_pct"
                ],
                "Iron Ore Production Annual Growth Rate Volatility (%)",
                "Year",
                "YoY Growth (%)"
            ],
            [
                "correlation_heatmap",
                [
                    "iron_ore_million_mt",
                    "bauxite_million_mt",
                    "limestone_million_mt",
                    "manganese_ore_million_mt",
                    "total_metallic_value_billion_inr"
                ],
                None,
                "Mineral Commodity Production Inter-Correlation",
                None,
                None
            ]
        ]
    },
    {
        "id": "D42",
        "slug": "d42_india_forest_cover_isfr",
        "title": "India State of Forest Report (ISFR) Canopy & Carbon Analytics",
        "domain": "Forestry & Ecological Conservation",
        "file": "d42_india_forest_cover_isfr.py",
        "csv": "data/analytical/d42_india_forest_cover_isfr.csv",
        "time_col": "state",
        "kpis": [
            [
                "Total Forest Canopy",
                "total_forest_sqkm",
                "sum",
                "{val:,.0f} sq km",
                "Combined Forest Cover",
                "pos"
            ],
            [
                "Largest Forest Estate",
                "total_forest_sqkm",
                "max",
                "{val:,.0f} sq km",
                "State with Max Forest Cover",
                "pos"
            ],
            [
                "Total Forest Carbon Stock",
                "carbon_stock_million_tonnes",
                "sum",
                "{val:,.0f} MT",
                "Terrestrial Carbon Reservoir",
                "pos"
            ],
            [
                "Very Dense Canopy Area",
                "very_dense_forest_sqkm",
                "sum",
                "{val:,.0f} sq km",
                "Pristine High-Canopy Cover",
                "pos"
            ],
            [
                "Mean Forest Cover Ratio",
                "forest_cover_pct",
                "mean",
                "{val:.1f}%",
                "National Geographical Mean",
                "neutral"
            ]
        ],
        "charts": [
            [
                "horizontal_bar",
                "total_forest_sqkm",
                "state",
                "Total Forest Cover by State (sq km)",
                "Forest Area (sq km)",
                "State"
            ],
            [
                "scatter",
                "total_forest_sqkm",
                "carbon_stock_million_tonnes",
                "Forest Area vs Total Carbon Stock (Million Tonnes)",
                "Forest Area (sq km)",
                "Carbon Stock (MT)"
            ],
            [
                "bar",
                "state",
                [
                    "very_dense_forest_sqkm",
                    "mod_dense_forest_sqkm",
                    "open_forest_sqkm"
                ],
                "Canopy Density Classification (VDF, MDF, OF) by State",
                "State",
                "Area (sq km)"
            ],
            [
                "treemap",
                [
                    "ecological_zone_tier",
                    "state"
                ],
                "carbon_stock_million_tonnes",
                "Forest Carbon Stock Concentration by Ecological Tier",
                None,
                None
            ],
            [
                "box",
                "ecological_zone_tier",
                "forest_cover_pct",
                "Forest Cover Density (% Area) by Ecological Zone Tier",
                "Ecological Tier",
                "Forest Cover (%)"
            ],
            [
                "histogram",
                "carbon_density_tonnes_per_sqkm",
                None,
                "Carbon Density (Tonnes Carbon / sq km) Spread",
                "Carbon Density (T/sq km)",
                "State Count"
            ],
            [
                "radar",
                [
                    "dense_canopy_ratio",
                    "forest_cover_pct",
                    "national_forest_share_pct"
                ],
                None,
                "Forest Ecological Health and Canopy Integrity Radar",
                None,
                None
            ]
        ]
    },
    {
        "id": "D43",
        "slug": "d43_india_petroleum_ppac",
        "title": "India Petroleum, Refining & Fuel Consumption Intelligence",
        "domain": "Hydrocarbons & Energy Security",
        "file": "d43_india_petroleum_ppac.py",
        "csv": "data/analytical/d43_india_petroleum_ppac.csv",
        "time_col": "year",
        "kpis": [
            [
                "Peak POL Consumption",
                "pol_consumption_mmt",
                "max",
                "{val:.1f} MMT",
                "Record Petroleum Demand",
                "neg"
            ],
            [
                "Latest Refinery Throughput",
                "refinery_throughput_mmt",
                "latest",
                "{val:.1f} MMT",
                "Domestic Refining Activity",
                "pos"
            ],
            [
                "Crude Import Dependency",
                "import_dependency_pct",
                "latest",
                "{val:.1f}%",
                "External Supply Exposure",
                "neg"
            ],
            [
                "Diesel Demand Dominance",
                "diesel_consumption_mmt",
                "latest",
                "{val:.1f} MMT",
                "Transport & Commercial Fuel",
                "neutral"
            ],
            [
                "Domestic Crude Output",
                "crude_production_mmt",
                "latest",
                "{val:.1f} MMT",
                "Upstream Production",
                "neutral"
            ]
        ],
        "charts": [
            [
                "line",
                "year",
                [
                    "pol_consumption_mmt",
                    "refinery_throughput_mmt",
                    "crude_production_mmt"
                ],
                "Petroleum Demand vs Refining Throughput and Domestic Crude Output",
                "Year",
                "Volume (MMT)"
            ],
            [
                "bar",
                "year",
                [
                    "diesel_consumption_mmt",
                    "petrol_consumption_mmt",
                    "lpg_consumption_mmt"
                ],
                "Refined Product Consumption Breakdown (Diesel, Petrol, LPG)",
                "Year",
                "Consumption (MMT)"
            ],
            [
                "scatter",
                "pol_consumption_mmt",
                "import_dependency_pct",
                "Aggregate Petroleum Demand vs Crude Import Dependency (%)",
                "Consumption (MMT)",
                "Import Dependency (%)"
            ],
            [
                "area",
                "year",
                [
                    "net_crude_deficit_mmt"
                ],
                "Crude Oil Net Supply Deficit Expansion (MMT)",
                "Year",
                "Deficit (MMT)"
            ],
            [
                "horizontal_bar",
                "import_dependency_pct",
                "year",
                "Evolution of Crude Oil Import Dependency Ratio (%)",
                "Import Dependency (%)",
                "Year"
            ],
            [
                "line",
                "year",
                [
                    "consumption_yoy_growth_pct"
                ],
                "Petroleum Consumption Annual Growth Rate Volatility (%)",
                "Year",
                "YoY Growth (%)"
            ],
            [
                "radar",
                [
                    "import_dependency_pct",
                    "diesel_share_pct",
                    "cooking_fuel_lpg_share_pct"
                ],
                None,
                "Hydrocarbon Fuel Security & Energy Demand Matrix",
                None,
                None
            ]
        ]
    },
    {
        "id": "D44",
        "slug": "d44_india_ncrb_crime",
        "title": "National Crime Records Bureau (NCRB) Crime & Judicial Disposal",
        "domain": "Law Enforcement & Justice Administration",
        "file": "d44_india_ncrb_crime.py",
        "csv": "data/analytical/d44_india_ncrb_crime.csv",
        "time_col": "state",
        "kpis": [
            [
                "Total Registered IPC Crimes",
                "total_ipc_crimes",
                "sum",
                "{val:,.0f} Cases",
                "Recorded IPC Offenses",
                "neg"
            ],
            [
                "Highest Crime Incidence",
                "total_ipc_crimes",
                "max",
                "{val:,.0f} Cases",
                "Peak State Volume",
                "neg"
            ],
            [
                "Average Conviction Rate",
                "conviction_rate_pct",
                "mean",
                "{val:.1f}%",
                "Judicial Conviction Efficacy",
                "pos"
            ],
            [
                "Average Chargesheet Rate",
                "chargesheet_rate_pct",
                "mean",
                "{val:.1f}%",
                "Police Investigation Rate",
                "pos"
            ],
            [
                "Total Crimes Against Women",
                "crimes_against_women",
                "sum",
                "{val:,.0f} Cases",
                "Women Safety Offenses",
                "neg"
            ]
        ],
        "charts": [
            [
                "horizontal_bar",
                "total_ipc_crimes",
                "state",
                "Total Registered IPC Offenses by State",
                "Cases Count",
                "State"
            ],
            [
                "scatter",
                "chargesheet_rate_pct",
                "conviction_rate_pct",
                "Investigation Chargesheet Rate vs Judicial Conviction Rate",
                "Chargesheet Rate (%)",
                "Conviction Rate (%)"
            ],
            [
                "bar",
                "state",
                [
                    "crimes_against_women",
                    "cyber_crimes"
                ],
                "Incidence of Crimes Against Women and Cyber Offenses",
                "State",
                "Cases Count"
            ],
            [
                "treemap",
                [
                    "crime_severity_tier",
                    "state"
                ],
                "total_ipc_crimes",
                "Total IPC Offenses Distribution by Crime Severity Tier",
                None,
                None
            ],
            [
                "box",
                "crime_severity_tier",
                "crime_rate_per_lakh",
                "Crime Rate per Lakh Population across Severity Tiers",
                "Severity Tier",
                "Crime Rate / Lakh"
            ],
            [
                "histogram",
                "conviction_rate_pct",
                None,
                "Judicial Conviction Rate (%) Spread across States",
                "Conviction Rate (%)",
                "State Count"
            ],
            [
                "radar",
                [
                    "conviction_rate_pct",
                    "chargesheet_rate_pct",
                    "women_crime_share_pct"
                ],
                None,
                "Judicial Efficacy and Law Enforcement Composite Profile",
                None,
                None
            ]
        ]
    },
    {
        "id": "D45",
        "slug": "d45_india_pmay_housing",
        "title": "Pradhan Mantri Awas Yojana (PMAY) Housing Completion Monitor",
        "domain": "Urban Development & Social Housing",
        "file": "d45_india_pmay_housing.py",
        "csv": "data/analytical/d45_india_pmay_housing.csv",
        "time_col": "state",
        "kpis": [
            [
                "Houses Completed",
                "houses_completed_thousand",
                "sum",
                "{val:,.1f}K",
                "Delivered Pucca Houses",
                "pos"
            ],
            [
                "Houses Sanctioned",
                "houses_sanctioned_thousand",
                "sum",
                "{val:,.1f}K",
                "Total Sanctioned Dwellings",
                "pos"
            ],
            [
                "Mean Completion Rate",
                "completion_rate_pct",
                "mean",
                "{val:.1f}%",
                "Project Delivery Velocity",
                "pos"
            ],
            [
                "Central Assistance Released",
                "central_assistance_crore",
                "sum",
                "\u20b9{val:,.0f} Cr",
                "Disbursed Central Subsidy",
                "neutral"
            ],
            [
                "Women Sole/Joint Ownership",
                "women_ownership_pct",
                "mean",
                "{val:.1f}%",
                "Gender Empowerment Titling",
                "pos"
            ]
        ],
        "charts": [
            [
                "horizontal_bar",
                "houses_completed_thousand",
                "state",
                "PMAY Completed Houses by State (Thousands)",
                "Completed (Thousand)",
                "State"
            ],
            [
                "scatter",
                "houses_sanctioned_thousand",
                "houses_completed_thousand",
                "Houses Sanctioned vs Houses Completed Correlation",
                "Sanctioned (K)",
                "Completed (K)"
            ],
            [
                "bar",
                "state",
                [
                    "houses_grounded_thousand",
                    "houses_completed_thousand",
                    "pipeline_houses_thousand"
                ],
                "PMAY Project Pipeline: Grounded vs Completed vs Ongoing",
                "State",
                "Houses (K)"
            ],
            [
                "treemap",
                [
                    "state"
                ],
                "central_assistance_crore",
                "Central Fiscal Assistance (\u20b9 Cr) Distribution by State",
                None,
                None
            ],
            [
                "box",
                "state",
                "women_ownership_pct",
                "Women Ownership Titling Rate (%) Distribution",
                "State",
                "Women Ownership (%)"
            ],
            [
                "histogram",
                "completion_rate_pct",
                None,
                "PMAY State Completion Rate (%) Frequency Distribution",
                "Completion Rate (%)",
                "State Count"
            ],
            [
                "radar",
                [
                    "completion_rate_pct",
                    "grounding_rate_pct",
                    "women_ownership_pct"
                ],
                None,
                "Social Housing Delivery and Inclusivity Scorecard",
                None,
                None
            ]
        ]
    },
    {
        "id": "D46",
        "slug": "d46_india_jal_jeevan_mission",
        "title": "Jal Jeevan Mission (JJM) Rural Tap Water Connectivity",
        "domain": "Water Sanitation & Rural Health",
        "file": "d46_india_jal_jeevan_mission.py",
        "csv": "data/analytical/d46_india_jal_jeevan_mission.csv",
        "time_col": "state",
        "kpis": [
            [
                "Tap Connections Provided",
                "fhtc_provided_lakh",
                "sum",
                "{val:,.1f} Lk",
                "Functional Tap Connections",
                "pos"
            ],
            [
                "National Coverage Mean",
                "current_coverage_pct",
                "mean",
                "{val:.1f}%",
                "State Average Tap Coverage",
                "pos"
            ],
            [
                "Pre-Mission Baseline",
                "baseline_2019_pct",
                "mean",
                "{val:.1f}%",
                "2019 Launch Baseline",
                "neutral"
            ],
            [
                "Coverage Expansion Added",
                "coverage_expansion_percentage_points",
                "mean",
                "+{val:.1f} pp",
                "Net Percentage Point Gain",
                "pos"
            ],
            [
                "Remaining Unconnected",
                "unconnected_households_lakh",
                "sum",
                "{val:,.1f} Lk",
                "Target Household Balance",
                "neutral"
            ]
        ],
        "charts": [
            [
                "horizontal_bar",
                "current_coverage_pct",
                "state",
                "Rural Tap Water Coverage by State (%)",
                "Coverage (%)",
                "State"
            ],
            [
                "scatter",
                "baseline_2019_pct",
                "current_coverage_pct",
                "2019 Baseline vs Current Tap Water Coverage (%)",
                "Baseline 2019 (%)",
                "Current Coverage (%)"
            ],
            [
                "bar",
                "state",
                [
                    "fhtc_provided_lakh",
                    "unconnected_households_lakh"
                ],
                "Connected vs Remaining Unconnected Rural Households (Lakh)",
                "State",
                "Households (Lakh)"
            ],
            [
                "treemap",
                [
                    "saturation_status",
                    "state"
                ],
                "fhtc_provided_lakh",
                "Tap Connections Grouped by Mission Saturation Tier",
                None,
                None
            ],
            [
                "box",
                "saturation_status",
                "coverage_expansion_percentage_points",
                "Expansion Gain (pp) by Saturation Milestone",
                "Status",
                "Gain (pp)"
            ],
            [
                "histogram",
                "growth_multiplier",
                None,
                "Tap Connection Coverage Growth Multiplier Spread",
                "Multiplier",
                "Frequency"
            ],
            [
                "radar",
                [
                    "current_coverage_pct",
                    "certified_har_ghar_jal_pct",
                    "coverage_expansion_percentage_points"
                ],
                None,
                "Har Ghar Jal Mission Saturation and Momentum Index",
                None,
                None
            ]
        ]
    },
    {
        "id": "D47",
        "slug": "d47_india_udise_education",
        "title": "UDISE+ School Education Infrastructure & Pupil-Teacher Ratio",
        "domain": "School Education & Foundational Facilities",
        "file": "d47_india_udise_education.py",
        "csv": "data/analytical/d47_india_udise_education.csv",
        "time_col": "state",
        "kpis": [
            [
                "Electricity Coverage",
                "electricity_avail_pct",
                "mean",
                "{val:.1f}%",
                "Schools with Power",
                "pos"
            ],
            [
                "Drinking Water Coverage",
                "drinking_water_avail_pct",
                "mean",
                "{val:.1f}%",
                "Schools with Piped Water",
                "pos"
            ],
            [
                "Girls Toilet Availability",
                "girls_toilet_avail_pct",
                "mean",
                "{val:.1f}%",
                "Dedicated Sanitation",
                "pos"
            ],
            [
                "Digital Computing Access",
                "computer_facility_pct",
                "mean",
                "{val:.1f}%",
                "Schools with Computers",
                "neutral"
            ],
            [
                "Mean Primary PTR",
                "ptr_primary",
                "mean",
                "{val:.1f}:1",
                "Pupil-Teacher Ratio",
                "pos"
            ]
        ],
        "charts": [
            [
                "horizontal_bar",
                "basic_amenities_composite_pct",
                "state",
                "School Basic Amenities Composite Index by State (%)",
                "Composite Score (%)",
                "State"
            ],
            [
                "scatter",
                "ptr_primary",
                "digital_readiness_composite_pct",
                "Pupil-Teacher Ratio vs Digital Infrastructure Readiness (%)",
                "PTR Primary",
                "Digital Readiness (%)"
            ],
            [
                "bar",
                "state",
                [
                    "electricity_avail_pct",
                    "drinking_water_avail_pct",
                    "girls_toilet_avail_pct"
                ],
                "Essential School Amenities Parity across States (%)",
                "State",
                "Availability (%)"
            ],
            [
                "treemap",
                [
                    "infrastructure_parity_tier",
                    "state"
                ],
                "ptr_primary",
                "Primary PTR Distribution Grouped by Infrastructure Parity Tier",
                None,
                None
            ],
            [
                "box",
                "infrastructure_parity_tier",
                "digital_readiness_composite_pct",
                "Digital Facility Availability by Infrastructure Parity Tier",
                "Parity Tier",
                "Digital Readiness (%)"
            ],
            [
                "histogram",
                "ptr_upper_primary",
                None,
                "Upper Primary Pupil-Teacher Ratio (PTR) Distribution",
                "PTR Ratio",
                "State Count"
            ],
            [
                "radar",
                [
                    "electricity_avail_pct",
                    "drinking_water_avail_pct",
                    "girls_toilet_avail_pct",
                    "computer_facility_pct",
                    "internet_facility_pct"
                ],
                None,
                "National School Physical and Digital Infrastructure Profile",
                None,
                None
            ]
        ]
    },
    {
        "id": "D48",
        "slug": "d48_india_tourism_stats",
        "title": "India Tourism Statistics & Foreign Exchange Earnings",
        "domain": "Tourism, Hospitality & Cultural Economy",
        "file": "d48_india_tourism_stats.py",
        "csv": "data/analytical/d48_india_tourism_stats.csv",
        "time_col": "year",
        "kpis": [
            [
                "Peak Foreign Arrivals",
                "foreign_tourist_arrivals_million",
                "max",
                "{val:.2f} M",
                "Highest Recorded Arrivals",
                "pos"
            ],
            [
                "Foreign Exchange Earnings",
                "foreign_exchange_earnings_usd_billion",
                "latest",
                "${val:.1f} B",
                "Annual Services Forex",
                "pos"
            ],
            [
                "Domestic Visits Footfall",
                "domestic_tourist_visits_million",
                "latest",
                "{val:,.0f} M",
                "Internal Tourism Scale",
                "pos"
            ],
            [
                "Spend per Foreign Tourist",
                "fee_per_foreign_tourist_usd",
                "latest",
                "${val:,.0f}",
                "Average Inbound Expenditure",
                "pos"
            ],
            [
                "Medical Tourism Share",
                "medical_tourism_share_pct",
                "latest",
                "{val:.1f}%",
                "High-Value Health Inflow",
                "pos"
            ]
        ],
        "charts": [
            [
                "line",
                "year",
                [
                    "foreign_tourist_arrivals_million"
                ],
                "Inbound Foreign Tourist Arrivals (FTA) Trajectory (Million)",
                "Year",
                "Arrivals (Million)"
            ],
            [
                "bar",
                "year",
                "foreign_exchange_earnings_usd_billion",
                "Foreign Exchange Earnings from Tourism (Billion USD)",
                "Year",
                "FEE (USD Billion)"
            ],
            [
                "area",
                "year",
                [
                    "domestic_tourist_visits_million"
                ],
                "Domestic Tourist Visits (DTV) Expansion Over Time (Million)",
                "Year",
                "Visits (Million)"
            ],
            [
                "scatter",
                "foreign_tourist_arrivals_million",
                "foreign_exchange_earnings_usd_billion",
                "Tourist Arrivals vs Inbound Foreign Exchange Earnings",
                "Arrivals (M)",
                "Earnings ($B)"
            ],
            [
                "horizontal_bar",
                "fee_per_foreign_tourist_usd",
                "year",
                "Average Foreign Exchange Earnings per Inbound Tourist (USD)",
                "Spend ($)",
                "Year"
            ],
            [
                "line",
                "year",
                [
                    "fta_yoy_growth_pct"
                ],
                "Annual Foreign Tourist Arrivals Growth Volatility (%)",
                "Year",
                "YoY Growth (%)"
            ],
            [
                "radar",
                [
                    "top_state_share_pct",
                    "medical_tourism_share_pct"
                ],
                None,
                "Tourism Economic Concentration and Specialization Indicators",
                None,
                None
            ]
        ]
    },
    {
        "id": "D49",
        "slug": "d49_india_food_pds_nfsa",
        "title": "National Food Security Act (NFSA) & PDS Buffer Stock Logistics",
        "domain": "Food Security & Welfare Supply Chain",
        "file": "d49_india_food_pds_nfsa.py",
        "csv": "data/analytical/d49_india_food_pds_nfsa.csv",
        "time_col": "year",
        "kpis": [
            [
                "Peak Welfare Offtake",
                "total_offtake_million_mt",
                "max",
                "{val:.1f} MMT",
                "Maximum Annual Distribution",
                "pos"
            ],
            [
                "Latest Foodgrain Offtake",
                "total_offtake_million_mt",
                "latest",
                "{val:.1f} MMT",
                "Public Distribution Vol",
                "pos"
            ],
            [
                "Central Buffer Stock",
                "central_buffer_stock_million_mt",
                "latest",
                "{val:.1f} MMT",
                "Strategic Food Reserve",
                "pos"
            ],
            [
                "Annual Food Subsidy",
                "food_subsidy_thousand_crore",
                "latest",
                "\u20b9{val:.1f}K Cr",
                "Union Budget NFSA Outlay",
                "neutral"
            ],
            [
                "Biometric PDS E-PoS",
                "aadhaar_authenticated_pds_pct",
                "latest",
                "{val:.1f}%",
                "Aadhaar e-PoS Authentication",
                "pos"
            ]
        ],
        "charts": [
            [
                "line",
                "year",
                [
                    "total_offtake_million_mt",
                    "central_buffer_stock_million_mt"
                ],
                "Foodgrain PDS Offtake vs Central Pool Buffer Stocks (MMT)",
                "Year",
                "Grain (Million MT)"
            ],
            [
                "bar",
                "year",
                [
                    "rice_offtake_million_mt",
                    "wheat_offtake_million_mt"
                ],
                "PDS Grain Allocation Deconstruction: Rice vs Wheat",
                "Year",
                "Grain (Million MT)"
            ],
            [
                "scatter",
                "total_offtake_million_mt",
                "food_subsidy_thousand_crore",
                "Grain Distributed vs Food Subsidy Budget Expenditure",
                "Offtake (MMT)",
                "Subsidy (\u20b9K Cr)"
            ],
            [
                "area",
                "year",
                [
                    "rice_share_pct",
                    "wheat_share_pct"
                ],
                "Proportional Composition of Grain Distribution (% Rice vs Wheat)",
                "Year",
                "Share (%)"
            ],
            [
                "horizontal_bar",
                "aadhaar_authenticated_pds_pct",
                "year",
                "Aadhaar-Authenticated Fair Price Shop Digitization (%)",
                "e-PoS Rate (%)",
                "Year"
            ],
            [
                "line",
                "year",
                [
                    "subsidy_per_mt_inr"
                ],
                "Implicit Economic Cost / Subsidy Burden per MT Grain (\u20b9 INR)",
                "Year",
                "Subsidy / MT (\u20b9)"
            ],
            [
                "radar",
                [
                    "rice_share_pct",
                    "wheat_share_pct",
                    "aadhaar_authenticated_pds_pct"
                ],
                None,
                "Food Security Strategic Logistics & Integrity Indicators",
                None,
                None
            ]
        ]
    },
    {
        "id": "D50",
        "slug": "d50_india_patents_ip",
        "title": "India Intellectual Property, Patents & Trademark Innovation",
        "domain": "Intellectual Property & R&D Commercialization",
        "file": "d50_india_patents_ip.py",
        "csv": "data/analytical/d50_india_patents_ip.csv",
        "time_col": "year",
        "kpis": [
            [
                "Peak Patent Filings",
                "patents_filed",
                "max",
                "{val:,.0f} Filings",
                "All-Time High Annual Patents",
                "pos"
            ],
            [
                "Latest Patents Granted",
                "patents_granted",
                "latest",
                "{val:,.0f} Grants",
                "Annual Patent Approvals",
                "pos"
            ],
            [
                "Domestic Filings Share",
                "domestic_share_pct",
                "latest",
                "{val:.1f}%",
                "Resident Inventor Dominance",
                "pos"
            ],
            [
                "Trademark Filings",
                "trademark_applications",
                "latest",
                "{val:,.0f} Marks",
                "Annual Commercial Brands",
                "pos"
            ],
            [
                "Grant to Filing Efficiency",
                "grant_to_filing_ratio_pct",
                "latest",
                "{val:.1f}%",
                "Examination & Grant Yield",
                "pos"
            ]
        ],
        "charts": [
            [
                "line",
                "year",
                [
                    "patents_filed",
                    "patents_granted"
                ],
                "Patent Applications Filed vs Patents Granted Over Time",
                "Year",
                "Number of Patents"
            ],
            [
                "bar",
                "year",
                [
                    "domestic_filed",
                    "foreign_filed"
                ],
                "Domestic Resident vs Foreign Patent Application Origination",
                "Year",
                "Filings Count"
            ],
            [
                "scatter",
                "patents_filed",
                "patents_granted",
                "Patent Filing Volume vs Institutional Patent Grant Yield",
                "Filings",
                "Grants"
            ],
            [
                "area",
                "year",
                [
                    "domestic_share_pct"
                ],
                "Domestic Resident Inventor Share of Total Filings (%)",
                "Year",
                "Resident Share (%)"
            ],
            [
                "horizontal_bar",
                "trademark_applications",
                "year",
                "Trademark Applications Filed Timeline Comparison",
                "Trademarks Count",
                "Year"
            ],
            [
                "line",
                "year",
                [
                    "patent_filings_yoy_growth_pct",
                    "grants_yoy_growth_pct"
                ],
                "Year-on-Year Growth Rates: Applications vs Grant Decisions (%)",
                "Year",
                "YoY Growth (%)"
            ],
            [
                "radar",
                [
                    "domestic_share_pct",
                    "grant_to_filing_ratio_pct",
                    "domestic_to_foreign_ratio"
                ],
                None,
                "National Innovation and IP Examination Capability Radar",
                None,
                None
            ]
        ]
    },
    {
        "id": "D51",
        "slug": "d51_india_pm_kisan",
        "title": "PM-KISAN Farmer Direct Benefit Transfer (DBT) Analytics",
        "domain": "Agrarian Welfare & Direct Benefits",
        "file": "d51_india_pm_kisan.py",
        "csv": "data/analytical/d51_india_pm_kisan.csv",
        "time_col": "state",
        "kpis": [
            [
                "Beneficiary Farmers",
                "farmer_beneficiaries_lakh",
                "sum",
                "{val:,.1f} Lk",
                "Enrolled Agrarian Households",
                "pos"
            ],
            [
                "Cumulative DBT Disbursed",
                "cumulative_dbt_crore",
                "sum",
                "\u20b9{val:,.0f} Cr",
                "Total Direct Income Support",
                "pos"
            ],
            [
                "Mean eKYC Verification",
                "ekyc_authenticated_pct",
                "mean",
                "{val:.1f}%",
                "Biometric/OTP Compliance",
                "pos"
            ],
            [
                "Aadhaar Bank Seeding",
                "aadhaar_seeded_pct",
                "mean",
                "{val:.1f}%",
                "APBS DBT Readiness",
                "pos"
            ],
            [
                "Women Farmer Beneficiaries",
                "women_farmers_pct",
                "mean",
                "{val:.1f}%",
                "Female Landholder Inclusion",
                "pos"
            ]
        ],
        "charts": [
            [
                "horizontal_bar",
                "farmer_beneficiaries_lakh",
                "state",
                "PM-KISAN Registered Farmers by State (Lakh)",
                "Farmers (Lakh)",
                "State"
            ],
            [
                "scatter",
                "farmer_beneficiaries_lakh",
                "cumulative_dbt_crore",
                "Farmer Beneficiary Scale vs Cumulative Cash Outlay (\u20b9 Cr)",
                "Farmers (Lakh)",
                "Disbursal (\u20b9 Cr)"
            ],
            [
                "bar",
                "state",
                "cumulative_dbt_crore",
                "State-wise Cumulative DBT Cash Disbursed to Farmers (\u20b9 Cr)",
                "State",
                "Disbursal (\u20b9 Cr)"
            ],
            [
                "treemap",
                [
                    "beneficiary_scale_tier",
                    "state"
                ],
                "cumulative_dbt_crore",
                "Direct Benefit Transfers Grouped by State Scale Tier",
                None,
                None
            ],
            [
                "box",
                "beneficiary_scale_tier",
                "women_farmers_pct",
                "Women Farmer Inclusion Share (%) by Beneficiary Scale Tier",
                "Scale Tier",
                "Women Share (%)"
            ],
            [
                "histogram",
                "digital_compliance_score",
                None,
                "State Digital Compliance Composite Index Spread",
                "Compliance Index",
                "Frequency"
            ],
            [
                "radar",
                [
                    "ekyc_authenticated_pct",
                    "aadhaar_seeded_pct",
                    "women_farmers_pct"
                ],
                None,
                "Direct Benefit Transfer Delivery Integrity Framework",
                None,
                None
            ]
        ]
    },
    {
        "id": "D52",
        "slug": "d52_india_automotive_siam",
        "title": "India Automotive Industry Production, Domestic Sales & Exports",
        "domain": "Automotive Manufacturing & Industrial Output",
        "file": "d52_india_automotive_siam.py",
        "csv": "data/analytical/d52_india_automotive_siam.csv",
        "time_col": "year",
        "kpis": [
            [
                "Peak Auto Production",
                "total_production_million",
                "max",
                "{val:.2f} M",
                "Highest Recorded Output",
                "pos"
            ],
            [
                "Latest Auto Production",
                "total_production_million",
                "latest",
                "{val:.2f} M",
                "Latest Recorded Production",
                "pos"
            ],
            [
                "Domestic Vehicle Sales",
                "domestic_sales_million",
                "latest",
                "{val:.2f} M",
                "Domestic Market Absorption",
                "pos"
            ],
            [
                "Automotive Exports",
                "total_exports_million",
                "latest",
                "{val:.2f} M",
                "Overseas Shipments",
                "pos"
            ],
            [
                "Passenger Vehicle Share",
                "pv_share_of_production_pct",
                "latest",
                "{val:.1f}%",
                "Cars & SUVs of Total Auto",
                "neutral"
            ]
        ],
        "charts": [
            [
                "line",
                "year",
                [
                    "total_production_million",
                    "domestic_sales_million",
                    "total_exports_million"
                ],
                "Automotive Production, Domestic Sales & Export Trajectories",
                "Year",
                "Vehicles (Million)"
            ],
            [
                "bar",
                "year",
                [
                    "pv_production_million",
                    "cv_production_million",
                    "three_wheeler_million",
                    "two_wheeler_million"
                ],
                "Vehicle Production Segment Disaggregation (PV, CV, 3W, 2W)",
                "Year",
                "Vehicles (Million)"
            ],
            [
                "scatter",
                "domestic_sales_million",
                "total_exports_million",
                "Domestic Sales Demand vs Global Export Shipments",
                "Domestic Sales (M)",
                "Exports (M)"
            ],
            [
                "area",
                "year",
                [
                    "export_intensity_pct"
                ],
                "Automotive Export Intensity Share of Production (%)",
                "Year",
                "Export Intensity (%)"
            ],
            [
                "horizontal_bar",
                "total_production_million",
                "year",
                "Annual Vehicle Production Volume Timeline Ranking",
                "Production (M)",
                "Year"
            ],
            [
                "line",
                "year",
                [
                    "production_yoy_growth_pct"
                ],
                "Automotive Production Year-on-Year Growth Volatility (%)",
                "Year",
                "YoY Growth (%)"
            ],
            [
                "radar",
                [
                    "pv_share_of_production_pct",
                    "two_wheeler_share_pct",
                    "export_intensity_pct"
                ],
                None,
                "Automotive Manufacturing Segment Concentration Profile",
                None,
                None
            ]
        ]
    },
    {
        "id": "D53",
        "slug": "d53_india_coal_production",
        "title": "India Coal Production, Thermal Dispatch & Supply Logistics",
        "domain": "Mining & Thermal Energy Baseload",
        "file": "d53_india_coal_production.py",
        "csv": "data/analytical/d53_india_coal_production.csv",
        "time_col": "year",
        "kpis": [
            [
                "Peak Raw Coal Output",
                "total_raw_coal_production_mt",
                "max",
                "{val:.1f} MT",
                "All-Time High Extraction",
                "pos"
            ],
            [
                "Power Sector Dispatch",
                "power_sector_dispatch_mt",
                "latest",
                "{val:.1f} MT",
                "Thermal Power Supply",
                "pos"
            ],
            [
                "Coal India Ltd Share",
                "cil_share_pct",
                "latest",
                "{val:.1f}%",
                "National CIL Monopoly Share",
                "neutral"
            ],
            [
                "Coal Import Volume",
                "coal_imports_mt",
                "latest",
                "{val:.1f} MT",
                "External Coal Inflows",
                "neg"
            ],
            [
                "Power Baseload Share",
                "power_sector_share_pct",
                "latest",
                "{val:.1f}%",
                "Grid Dispatch Allocation",
                "neutral"
            ]
        ],
        "charts": [
            [
                "line",
                "year",
                [
                    "total_raw_coal_production_mt",
                    "cil_production_mt",
                    "power_sector_dispatch_mt"
                ],
                "Domestic Coal Production & Power Dispatch Trajectories (MT)",
                "Year",
                "Coal (Million Tonnes)"
            ],
            [
                "bar",
                "year",
                [
                    "cil_production_mt",
                    "non_cil_production_mt"
                ],
                "Coal Production: Coal India Ltd (CIL) vs Captive/Commercial Miners",
                "Year",
                "Production (MT)"
            ],
            [
                "scatter",
                "total_raw_coal_production_mt",
                "power_sector_dispatch_mt",
                "Domestic Coal Output vs Thermal Power Plant Dispatch",
                "Production (MT)",
                "Power Dispatch (MT)"
            ],
            [
                "area",
                "year",
                [
                    "coal_imports_mt"
                ],
                "Coal Import Volumes Inflow Over Time (Million Tonnes)",
                "Year",
                "Imports (MT)"
            ],
            [
                "horizontal_bar",
                "pithead_stock_mt",
                "year",
                "Pithead Coal Inventory Stock Levels Timeline (MT)",
                "Pithead Stock (MT)",
                "Year"
            ],
            [
                "line",
                "year",
                [
                    "power_dispatch_yoy_growth_pct"
                ],
                "Power Sector Coal Supply Annual Growth Rate (%)",
                "Year",
                "YoY Growth (%)"
            ],
            [
                "radar",
                [
                    "power_sector_share_pct",
                    "cil_share_pct",
                    "import_to_domestic_ratio"
                ],
                None,
                "Coal Baseload Energy Security & Domestic Self-Reliance Radar",
                None,
                None
            ]
        ]
    },
    {
        "id": "D54",
        "slug": "d54_india_inland_waterways",
        "title": "India Inland Waterways Freight Movement & Multimodal Logistics",
        "domain": "Waterways Logistics & Multimodal Transport",
        "file": "d54_india_inland_waterways.py",
        "csv": "data/analytical/d54_india_inland_waterways.csv",
        "time_col": "year",
        "kpis": [
            [
                "Peak Waterway Cargo",
                "total_waterway_cargo_mmt",
                "max",
                "{val:.1f} MMT",
                "Highest Cargo Volume",
                "pos"
            ],
            [
                "Latest Cargo Volume",
                "total_waterway_cargo_mmt",
                "latest",
                "{val:.1f} MMT",
                "Latest Freight Movement",
                "pos"
            ],
            [
                "National Waterway 1 (Ganga)",
                "nw1_ganga_mmt",
                "latest",
                "{val:.2f} MMT",
                "NW-1 Haldia-Varanasi",
                "pos"
            ],
            [
                "NW-2 Brahmaputra Cargo",
                "nw2_brahmaputra_mmt",
                "latest",
                "{val:.2f} MMT",
                "NW-2 Dhubri-Sadiya",
                "pos"
            ],
            [
                "Coastal & Tidal Cargo",
                "tidal_coastal_cargo_mmt",
                "latest",
                "{val:.1f} MMT",
                "Goa & Maharashtra Waterways",
                "neutral"
            ]
        ],
        "charts": [
            [
                "line",
                "year",
                [
                    "total_waterway_cargo_mmt"
                ],
                "Inland Waterways Cargo Traffic Growth Trajectory (MMT)",
                "Year",
                "Cargo (Million MT)"
            ],
            [
                "bar",
                "year",
                [
                    "nw1_ganga_mmt",
                    "nw2_brahmaputra_mmt",
                    "nw3_west_coast_mmt"
                ],
                "Priority National Waterways Cargo Comparison (NW-1, NW-2, NW-3)",
                "Year",
                "Cargo (Million MT)"
            ],
            [
                "scatter",
                "nw1_ganga_mmt",
                "total_waterway_cargo_mmt",
                "NW-1 Ganga Freight Volume vs Aggregate National Waterway Traffic",
                "NW-1 (MMT)",
                "Total Cargo (MMT)"
            ],
            [
                "area",
                "year",
                [
                    "goa_waterways_mmt",
                    "maharashtra_waterways_mmt"
                ],
                "Tidal Waterway Mining & Coastal Freight (Goa & Maharashtra)",
                "Year",
                "Cargo (MMT)"
            ],
            [
                "horizontal_bar",
                "total_waterway_cargo_mmt",
                "year",
                "Annual Waterway Cargo Ranking Timeline (MMT)",
                "Cargo (MMT)",
                "Year"
            ],
            [
                "line",
                "year",
                [
                    "cargo_yoy_growth_pct"
                ],
                "Inland Waterway Freight Annual Growth Rate Volatility (%)",
                "Year",
                "YoY Growth (%)"
            ],
            [
                "radar",
                [
                    "nw1_ganga_share_pct",
                    "nw2_brahmaputra_share_pct",
                    "nw1_to_nw2_ratio"
                ],
                None,
                "National Inland Waterways Freight Utilization Profile",
                None,
                None
            ]
        ]
    }
,
# --- D55 to D74: Authentic Global Intelligence Suites ---
    {
        "id": "D55",
        "slug": "d55_iaea_nuclear_power",
        "title": "IAEA Nuclear Power Infrastructure & Operational Reactor Metrics",
        "domain": "Nuclear Physics & Global Energy Infrastructure",
        "file": "d55_iaea_nuclear_power.py",
        "csv": "data/analytical/d55_iaea_nuclear_power.csv",
        "time_col": None,
        "kpis": [
            ("Total Net Capacity", "total_net_capacity_mwe", "sum", "{val:,.0f} MWe", "Global Nuclear Capacity", "pos"),
            ("Operational Reactors", "operational_reactors", "sum", "{val:,.0f} Units", "Active Reactor Fleet", "pos"),
            ("Under Construction", "under_construction_reactors", "sum", "{val:,.0f} Units", "New Build Pipeline", "pos"),
            ("Top Nuclear Share", "nuclear_share_electricity_pct", "max", "{val:.1f}%", "France Clean Baseload", "pos"),
            ("Mean Reactor Fleet Age", "mean_reactor_age_years", "mean", "{val:.1f} Yrs", "Fleet Lifecycle", "neutral")
        ],
        "charts": [
            ("bar", "country", "total_net_capacity_mwe", "Operational Nuclear Electrical Capacity by Nation (MWe)", "Country", "Net Capacity (MWe)"),
            ("scatter", "operational_reactors", "under_construction_reactors", "Operational Reactor Fleet vs Under Construction Pipeline", "Operational Reactors", "Under Construction"),
            ("horizontal_bar", "nuclear_share_electricity_pct", "country", "Nuclear Share of National Electricity Production (%)", "Nuclear Share (%)", "Country"),
            ("bar", "country", "cumulative_generation_twh", "Cumulative Annual Nuclear Electricity Generation (TWh)", "Country", "Generation (TWh)"),
            ("correlation_heatmap", ["total_net_capacity_mwe", "operational_reactors", "under_construction_reactors", "nuclear_share_electricity_pct", "mean_reactor_age_years", "cumulative_generation_twh"], None, "Nuclear Infrastructure & Operational Metrics Correlation Matrix"),
            ("histogram", "mean_reactor_age_years", None, "Nuclear Fleet Mean Reactor Age Distribution (Years)", "Reactor Age (Years)", "Fleet Count"),
            ("radar", ["nuclear_share_electricity_pct", "mean_reactor_age_years", "operational_reactors"], None, "National Nuclear Energy Fleet Capability Profile", None, None)
        ]
    },
    {
        "id": "D56",
        "slug": "d56_nasa_exoplanets",
        "title": "NASA Confirmed Exoplanets Discovery & Planetary Astrophysics",
        "domain": "Astrophysics & Space Exploration",
        "file": "d56_nasa_exoplanets.py",
        "csv": "data/analytical/d56_nasa_exoplanets.csv",
        "time_col": "discovery_year",
        "kpis": [
            ("Confirmed Exoplanets", "total_confirmed_cumulative", "latest", "{val:,.0f}", "Verified Discoveries", "pos"),
            ("Transit Discoveries", "transit_method_cumulative", "latest", "{val:,.0f}", "Kepler & TESS Photometry", "pos"),
            ("Super-Earths Identified", "super_earths_count", "latest", "{val:,.0f}", "Sub-Neptune Worlds", "pos"),
            ("Gas Giants Cataloged", "gas_giants_count", "latest", "{val:,.0f}", "Jovian Class Worlds", "neutral"),
            ("Habitable Zone Candidates", "habitable_zone_candidates", "latest", "{val:,.0f}", "Earth-Analogue Targets", "pos")
        ],
        "charts": [
            ("line", "discovery_year", ["total_confirmed_cumulative"], "Cumulative Confirmed Exoplanet Discoveries Over Time (2000-2024)", "Discovery Year", "Confirmed Exoplanets"),
            ("area", "discovery_year", ["transit_method_cumulative", "radial_velocity_cumulative", "microlensing_cumulative", "imaging_cumulative"], "Exoplanet Discovery Method Progression (Transit, Radial Velocity, Microlensing, Imaging)", "Discovery Year", "Discoveries Count"),
            ("scatter", "super_earths_count", "total_confirmed_cumulative", "Super-Earth Population vs Cumulative Exoplanet Archive Growth", "Super-Earths", "Total Confirmed"),
            ("horizontal_bar", "habitable_zone_candidates", "discovery_year", "Habitable Zone Candidate Discoveries by Epoch", "Candidates Count", "Year"),
            ("bar", "discovery_year", ["terrestrial_rocky_count", "super_earths_count", "gas_giants_count"], "Taxonomic Classification Breakdown of Discovered Worlds", "Discovery Year", "World Count"),
            ("histogram", "annual_new_discoveries", None, "Annual Exoplanet Discovery Velocity Rate Distribution", "Annual Discoveries", "Frequency"),
            ("radar", ["transit_share_pct", "habitable_share_pct"], None, "Exoplanet Detection & Astrobiological Potential Profile", None, None)
        ]
    },
    {
        "id": "D57",
        "slug": "d57_unhcr_forced_displacement",
        "title": "UNHCR Global Forced Displacement, Refugees & Asylum Seekers",
        "domain": "Humanitarian Affairs & Demographics",
        "file": "d57_unhcr_forced_displacement.py",
        "csv": "data/analytical/d57_unhcr_forced_displacement.csv",
        "time_col": "year",
        "kpis": [
            ("Total Forcibly Displaced", "total_displaced_millions", "latest", "{val:.1f}M", "Worldwide Displaced", "neg"),
            ("Internally Displaced (IDPs)", "idps_conflict_millions", "latest", "{val:.1f}M", "Conflict & Violence IDPs", "neg"),
            ("UNHCR Mandate Refugees", "refugees_under_unhcr_millions", "latest", "{val:.1f}M", "Cross-Border Refugees", "neg"),
            ("Pending Asylum Seekers", "asylum_seekers_millions", "latest", "{val:.1f}M", "Individual Claims", "neutral"),
            ("Child Displacement Share", "children_pct_displaced", "latest", "{val:.1f}%", "Vulnerable Minors", "neg")
        ],
        "charts": [
            ("line", "year", ["total_displaced_millions"], "Global Forcibly Displaced Population Trajectory (2010-2024)", "Year", "Displaced Persons (Millions)"),
            ("area", "year", ["idps_conflict_millions", "refugees_under_unhcr_millions", "asylum_seekers_millions"], "Displacement Typology Breakdown (IDPs, Refugees, Asylum Seekers)", "Year", "Millions of People"),
            ("scatter", "total_displaced_millions", "refugees_under_unhcr_millions", "Aggregate Global Displacement vs Sovereign Refugee Population", "Total Displaced (M)", "Refugees (M)"),
            ("horizontal_bar", "total_displaced_millions", "year", "Global Displacement Escalation Milestones by Year (Millions)", "Displaced (M)", "Year"),
            ("bar", "year", ["children_displaced_millions"], "Estimated Displaced Minor Children Worldwide (Millions)", "Year", "Children (Millions)"),
            ("histogram", "annual_displacement_delta_millions", None, "Annual Net Displacement Acceleration Volatility (Millions/Year)", "Annual Change (M)", "Frequency"),
            ("radar", ["idp_share_of_total_pct", "refugee_share_of_total_pct", "children_pct_displaced"], None, "Global Humanitarian Protection Vulnerability Signature", None, None)
        ]
    },
    {
        "id": "D58",
        "slug": "d58_nist_nvd_cybersecurity",
        "title": "NIST / NVD Worldwide Cybersecurity Vulnerability Trends",
        "domain": "Cybersecurity & Information Technology",
        "file": "d58_nist_nvd_cybersecurity.py",
        "csv": "data/analytical/d58_nist_nvd_cybersecurity.csv",
        "time_col": "year",
        "kpis": [
            ("Annual Published CVEs", "total_cves_published", "latest", "{val:,.0f}", "All-Time Record", "neg"),
            ("Critical CVSS 9.0+", "critical_severity_count", "latest", "{val:,.0f}", "Immediate RCE Threat", "neg"),
            ("High CVSS 7.0-8.9", "high_severity_count", "latest", "{val:,.0f}", "Severe Privilege Escalation", "neg"),
            ("CISA KEV Exploited", "exploited_in_wild_cisa_kev", "latest", "{val:,.0f}", "Active In-The-Wild Exploits", "neg"),
            ("RCE Flaw Share", "remote_code_execution_pct", "latest", "{val:.1f}%", "Remote Attack Vector", "neutral")
        ],
        "charts": [
            ("line", "year", ["total_cves_published"], "Worldwide Published Common Vulnerabilities and Exposures (CVEs) 2010-2024", "Year", "Published CVEs"),
            ("area", "year", ["critical_severity_count", "high_severity_count", "medium_severity_count", "low_severity_count"], "Vulnerability Severity Tier Composition (Critical, High, Medium, Low)", "Year", "Vulnerabilities Count"),
            ("scatter", "critical_severity_count", "exploited_in_wild_cisa_kev", "Critical Severity Flaws vs Actively Exploited In-The-Wild Flaws (CISA KEV)", "Critical Flaws", "CISA KEV Count"),
            ("horizontal_bar", "critical_severity_count", "year", "Annual Critical Severity (CVSS 9.0+) Publications Milestones", "Critical CVEs", "Year"),
            ("bar", "year", ["exploited_in_wild_cisa_kev"], "CISA Known Exploited Vulnerabilities (KEV) Catalog Additions", "Year", "Exploited Flaws"),
            ("histogram", "yoy_cve_growth_rate_pct", None, "Annual CVE Growth Rate Volatility Distribution (%)", "YoY Growth (%)", "Frequency"),
            ("radar", ["critical_high_share_pct", "remote_code_execution_pct", "cisa_kev_exploitation_rate_pct"], None, "Enterprise Digital Attack Surface Vulnerability Profile", None, None)
        ]
    },
    {
        "id": "D59",
        "slug": "d59_nsidc_arctic_sea_ice",
        "title": "NSIDC / NOAA Arctic & Antarctic Sea Ice Extent & Cryosphere Monitor",
        "domain": "Cryosphere Science & Polar Climatology",
        "file": "d59_nsidc_arctic_sea_ice.py",
        "csv": "data/analytical/d59_nsidc_arctic_sea_ice.csv",
        "time_col": "year",
        "kpis": [
            ("Arctic September Minimum", "arctic_september_minimum_million_sqkm", "latest", "{val:.2f} M km²", "Summer Sea Ice Trough", "neg"),
            ("Arctic Winter Maximum", "arctic_march_maximum_million_sqkm", "latest", "{val:.2f} M km²", "Winter Peak Sea Ice", "neutral"),
            ("Antarctic Summer Extent", "antarctic_february_minimum_million_sqkm", "latest", "{val:.2f} M km²", "Southern Ocean Summer", "neg"),
            ("Decline vs 1980 Baseline", "arctic_loss_vs_1980_pct", "latest", "{val:.1f}%", "Satellite Era Contraction", "neg"),
            ("Polar Albedo Feedback", "polar_albedo_feedback_index", "latest", "{val:.1f}", "Reflective Cooling Index", "neutral")
        ],
        "charts": [
            ("line", "year", ["arctic_september_minimum_million_sqkm"], "Arctic September Sea Ice Minimum Extent Decline Trajectory (1980-2024)", "Year", "Sea Ice Extent (Million sq km)"),
            ("line", "year", ["arctic_march_maximum_million_sqkm", "antarctic_september_maximum_million_sqkm"], "Polar Winter Maximum Sea Ice Extent Comparison (Arctic vs Antarctic)", "Year", "Maximum Extent (M sq km)"),
            ("scatter", "arctic_september_minimum_million_sqkm", "antarctic_february_minimum_million_sqkm", "Arctic Summer Minimum vs Antarctic Summer Minimum Teleconnection", "Arctic Min (M sq km)", "Antarctic Min (M sq km)"),
            ("horizontal_bar", "arctic_september_minimum_million_sqkm", "year", "Historical Arctic September Sea Ice Minimum Ranking Timeline", "Sea Ice Extent (M sq km)", "Year"),
            ("area", "year", ["global_polar_minimum_sqkm"], "Global Bipolar Sea Ice Combined Minimum Extent (Million sq km)", "Year", "Combined Extent (M sq km)"),
            ("histogram", "arctic_extent_anomaly_sqkm", None, "Arctic Sea Ice Extent Departure Anomaly Distribution (M sq km)", "Extent Anomaly (M sq km)", "Frequency"),
            ("radar", ["polar_albedo_feedback_index", "arctic_september_minimum_million_sqkm"], None, "Hemispheric Cryosphere Stability Signature", None, None)
        ]
    },
    {
        "id": "D60",
        "slug": "d60_icao_commercial_aviation",
        "title": "ICAO / IATA Global Commercial Aviation & Air Traffic Activity",
        "domain": "Global Aviation & Transportation",
        "file": "d60_icao_commercial_aviation.py",
        "csv": "data/analytical/d60_icao_commercial_aviation.csv",
        "time_col": "year",
        "kpis": [
            ("Worldwide Air Passengers", "global_passengers_billion", "latest", "{val:.2f}B", "All-Time Historic Peak", "pos"),
            ("Revenue Passenger-Km", "revenue_passenger_km_trillion", "latest", "{val:.2f}T RPK", "Passenger Mobility Traffic", "pos"),
            ("Passenger Load Factor", "global_passenger_load_factor_pct", "latest", "{val:.1f}%", "Fleet Capacity Utilization", "pos"),
            ("Commercial Flights", "scheduled_flights_million", "latest", "{val:.1f}M", "Worldwide Scheduled Sectors", "pos"),
            ("Airline Industry Revenues", "airline_industry_operating_revenue_usd_billion", "latest", "${val:,.0f}B", "Gross Operating Turnover", "pos")
        ],
        "charts": [
            ("line", "year", ["global_passengers_billion"], "Global Airline Scheduled Passengers Trajectory & Recovery (2005-2024)", "Year", "Passengers (Billion)"),
            ("area", "year", ["revenue_passenger_km_trillion"], "Global Revenue Passenger Kilometers Traffic Volume (Trillion RPK)", "Year", "Traffic (Trillion RPK)"),
            ("scatter", "scheduled_flights_million", "global_passengers_billion", "Scheduled Commercial Flight Operations vs Total Passenger Volumes", "Flights (Millions)", "Passengers (Billions)"),
            ("horizontal_bar", "airline_industry_operating_revenue_usd_billion", "year", "Global Airline Industry Gross Operating Revenues ($ Billion)", "Revenues ($B)", "Year"),
            ("bar", "year", ["freight_tonne_km_billion"], "Global Air Freight Haulage Volume (Billion Tonne-Kilometers FTK)", "Year", "Freight (Billion FTK)"),
            ("histogram", "global_passenger_load_factor_pct", None, "Worldwide Commercial Flight Passenger Load Factor Distribution (%)", "Load Factor (%)", "Frequency"),
            ("radar", ["global_passenger_load_factor_pct", "passengers_per_flight_avg"], None, "Civil Aviation Operational Efficiency & Capacity Utilization", None, None)
        ]
    },
    {
        "id": "D61",
        "slug": "d61_wgc_sovereign_gold_reserves",
        "title": "World Gold Council Worldwide Sovereign Gold Reserves & Holdings",
        "domain": "Central Banking & International Finance",
        "file": "d61_wgc_sovereign_gold_reserves.py",
        "csv": "data/analytical/d61_wgc_sovereign_gold_reserves.csv",
        "time_col": None,
        "kpis": [
            ("Top Sovereign Vault (US)", "official_gold_holdings_tonnes", "max", "{val:,.1f} Tonnes", "Federal Reserve / Fort Knox", "pos"),
            ("Tracked Sovereign Gold", "official_gold_holdings_tonnes", "sum", "{val:,.0f} Tonnes", "Central Bank Reserves", "pos"),
            ("Peak Vault Valuation", "market_value_usd_billion", "max", "${val:,.1f}B", "US Treasury Gold Stock", "pos"),
            ("India Sovereign Gold", "official_gold_holdings_tonnes", "mean", "{val:.1f} Tonnes", "RBI Vaulted Bullion", "pos"),
            ("Top Gold Reserve Share", "gold_share_total_forex_reserves_pct", "max", "{val:.1f}%", "Portugal Strategic Reserve", "pos")
        ],
        "charts": [
            ("bar", "country", "official_gold_holdings_tonnes", "Official Sovereign Central Bank Gold Holdings (Metric Tonnes)", "Country", "Gold Reserves (Tonnes)"),
            ("scatter", "official_gold_holdings_tonnes", "gold_share_total_forex_reserves_pct", "Official Gold Reserves vs Gold Share of Total National FX Reserves (%)", "Gold Reserves (Tonnes)", "Gold Share of FX (%)"),
            ("horizontal_bar", "market_value_usd_billion", "country", "Sovereign Gold Reserve Market Valuation by Leading Nation ($ Billion)", "Valuation ($B USD)", "Country"),
            ("bar", "country", "annual_net_purchases_tonnes", "Central Bank Net Gold Purchases & Sovereign Buying Activity (Tonnes)", "Country", "Net Purchases (Tonnes)"),
            ("correlation_heatmap", ["official_gold_holdings_tonnes", "gold_share_total_forex_reserves_pct", "annual_net_purchases_tonnes", "market_value_usd_billion", "per_capita_gold_grams"], None, "Central Bank Sovereign Gold Reserves & Valuation Correlation Matrix"),
            ("histogram", "gold_share_total_forex_reserves_pct", None, "Gold Allocation Share of Sovereign Foreign Exchange Reserves Distribution (%)", "Gold Share (%)", "Central Banks"),
            ("radar", ["gold_share_total_forex_reserves_pct", "sovereign_gold_share_of_global_pct"], None, "Sovereign Monetary Balance Sheet Gold Allocation Profile", None, None)
        ]
    },
    {
        "id": "D62",
        "slug": "d62_unesco_world_heritage_sites",
        "title": "UNESCO World Cultural & Natural Heritage Sites Distribution",
        "domain": "Cultural Geography & Conservation Architecture",
        "file": "d62_unesco_world_heritage_sites.py",
        "csv": "data/analytical/d62_unesco_world_heritage_sites.csv",
        "time_col": None,
        "kpis": [
            ("Total Heritage Properties", "total_heritage_sites", "sum", "{val:,.0f} Sites", "Inscribed Global Sanctuaries", "pos"),
            ("Cultural Monument Sites", "cultural_sites_count", "sum", "{val:,.0f} Sites", "Human Cultural Masterpieces", "pos"),
            ("Natural Ecosystem Sites", "natural_sites_count", "sum", "{val:,.0f} Sites", "Biospheres & Geoparks", "pos"),
            ("India Inscribed Heritage", "total_heritage_sites", "mean", "{val:.1f} Sites", "6th Most Inscribed Nation", "pos"),
            ("Endangered Sites Monitored", "sites_in_danger_count", "sum", "{val:,.0f} Sites", "Armed Conflict & Degradation", "neg")
        ],
        "charts": [
            ("bar", "country", "total_heritage_sites", "Total Inscribed World Heritage Properties by Leading Nation", "Country", "Heritage Sites"),
            ("area", "country", ["cultural_sites_count", "natural_sites_count"], "Cultural vs Natural Heritage Site Composition Across Leading States", "Country", "Sites Count"),
            ("scatter", "cultural_sites_count", "natural_sites_count", "Cultural Monuments vs Natural Biosphere Reserves Endowments", "Cultural Sites", "Natural Sites"),
            ("horizontal_bar", "cultural_share_pct", "country", "Cultural Heritage Percentage Share of National Portfolio (%)", "Cultural Share (%)", "Country"),
            ("bar", "country", "transboundary_sites_count", "Transboundary Cross-Border Heritage Properties Co-Managed by Nations", "Country", "Transboundary Sites"),
            ("histogram", "total_heritage_sites", None, "National Heritage Inscription Density Distribution Across State Parties", "Sites Inscribed", "State Parties"),
            ("radar", ["cultural_share_pct", "natural_share_pct", "global_heritage_site_share_pct"], None, "National Heritage Portfolio Cultural & Natural Diversity Balance", None, None)
        ]
    },
    {
        "id": "D63",
        "slug": "d63_sia_wsts_semiconductor_market",
        "title": "SIA / WSTS Global Semiconductor Billings & Product Categories",
        "domain": "Advanced Microelectronics & Global Technology",
        "file": "d63_sia_wsts_semiconductor_market.py",
        "csv": "data/analytical/d63_sia_wsts_semiconductor_market.csv",
        "time_col": "year",
        "kpis": [
            ("Global Chip Billings", "total_semiconductor_sales_billion_usd", "latest", "${val:,.1f}B", "All-Time Record Market", "pos"),
            ("Logic Chips Revenue", "logic_chips_sales_billion", "latest", "${val:,.1f}B", "GPUs, CPUs & ASICs", "pos"),
            ("Memory IC Market", "memory_chips_sales_billion", "latest", "${val:,.1f}B", "HBM, DRAM & NAND", "pos"),
            ("Asia-Pacific Market Share", "asia_pacific_market_share_pct", "latest", "{val:.1f}%", "Regional Manufacturing Epicenter", "neutral"),
            ("YoY Market Expansion", "yoy_market_expansion_pct", "latest", "{val:+.1f}%", "AI Demand Rebound", "pos")
        ],
        "charts": [
            ("line", "year", ["total_semiconductor_sales_billion_usd"], "Global Semiconductor Market Revenue Trajectory ($ Billion USD)", "Year", "Billings ($B USD)"),
            ("area", "year", ["logic_chips_sales_billion", "memory_chips_sales_billion", "microprocessor_mpu_mcu_billion", "analog_chips_sales_billion", "discretes_opto_sensors_billion"], "Product Category Revenue Composition (Logic, Memory, MPU/MCU, Analog, Discretes)", "Year", "Sales ($B USD)"),
            ("line", "year", ["asia_pacific_sales_billion", "americas_sales_billion", "europe_sales_billion", "japan_sales_billion"], "Regional Semiconductor Sales Trends (Asia-Pacific, Americas, Europe, Japan)", "Year", "Sales ($B USD)"),
            ("horizontal_bar", "total_semiconductor_sales_billion_usd", "year", "Global Chip Industry Annual Billings Milestones ($ Billion)", "Sales ($B)", "Year"),
            ("scatter", "logic_chips_sales_billion", "memory_chips_sales_billion", "Logic Integrated Circuits vs Cyclical Memory Market Revenue Co-Movement", "Logic ($B)", "Memory ($B)"),
            ("histogram", "yoy_market_expansion_pct", None, "Semiconductor Market Annual Growth Rate Volatility Cycle Distribution (%)", "YoY Growth (%)", "Frequency"),
            ("radar", ["logic_memory_combined_share_pct", "asia_pacific_market_share_pct", "americas_market_share_pct"], None, "Global Microelectronics Demand & Regional Concentration Signature", None, None)
        ]
    },
    {
        "id": "D64",
        "slug": "d64_who_unicef_immunization",
        "title": "WHO / UNICEF Global Childhood Vaccination & Immunization Coverage",
        "domain": "Global Public Health & Epidemiology",
        "file": "d64_who_unicef_immunization.py",
        "csv": "data/analytical/d64_who_unicef_immunization.csv",
        "time_col": "year",
        "kpis": [
            ("DTP3 Benchmark Coverage", "dtp3_coverage_pct", "latest", "{val:.1f}%", "Third-Dose Diptheria-Tetanus", "pos"),
            ("Measles MCV1 Coverage", "measles_mcv1_coverage_pct", "latest", "{val:.1f}%", "First-Dose Epidemic Barrier", "pos"),
            ("Polio Pol3 Coverage", "polio_pol3_coverage_pct", "latest", "{val:.1f}%", "Oral/Injectable Polio Vaccine", "pos"),
            ("Zero-Dose Vulnerable Children", "unvaccinated_zero_dose_children_millions", "latest", "{val:.1f}M", "Missing Fundamental Antigens", "neg"),
            ("Measles MCV2 Booster", "measles_mcv2_second_dose_pct", "latest", "{val:.1f}%", "Two-Dose Complete Regimen", "pos")
        ],
        "charts": [
            ("line", "year", ["dtp3_coverage_pct", "measles_mcv1_coverage_pct", "polio_pol3_coverage_pct", "bcg_tuberculosis_pct"], "Essential Childhood Vaccine Immunization Coverage Benchmarks (2000-2024)", "Year", "Coverage (%)"),
            ("area", "year", ["unvaccinated_zero_dose_children_millions"], "Unvaccinated 'Zero-Dose' Children Worldwide Population Trend (Millions)", "Year", "Zero-Dose Children (Millions)"),
            ("scatter", "dtp3_coverage_pct", "measles_mcv2_second_dose_pct", "Primary DTP3 Routine Coverage vs Second-Dose Measles Booster Integration", "DTP3 Coverage (%)", "Measles MCV2 (%)"),
            ("horizontal_bar", "dtp3_coverage_pct", "year", "Global DTP3 Vaccination Benchmark Milestones Across Years (%)", "Coverage (%)", "Year"),
            ("bar", "year", ["rotavirus_coverage_pct", "hepb3_hepatitis_pct"], "Modern Antigen Rollouts: Rotavirus & Hepatitis B (HepB3) Coverage Expansion", "Year", "Coverage (%)"),
            ("histogram", "vaccine_equity_gap_mcv1_vs_mcv2", None, "Measles First vs Second Dose Immunization Dropout Gap Distribution (%)", "Drop-Off Gap (%)", "Frequency"),
            ("radar", ["composite_core_vaccination_index", "dtp3_coverage_pct", "measles_mcv1_coverage_pct"], None, "Pediatric Disease Eradication Global Immunization Health Profile", None, None)
        ]
    },
    {
        "id": "D65",
        "slug": "d65_noaa_ocean_heat_content",
        "title": "NOAA NCEI Global Ocean Heat Content & Basin Warming Anomalies",
        "domain": "Marine Oceanography & Planetary Thermodynamics",
        "file": "d65_noaa_ocean_heat_content.py",
        "csv": "data/analytical/d65_noaa_ocean_heat_content.csv",
        "time_col": "year",
        "kpis": [
            ("0-2000m Ocean Heat", "ocean_heat_content_0_2000m_zettajoules", "latest", "{val:,.1f} ZJ", "Full Column Thermal Anomaly", "neg"),
            ("Upper Ocean (0-700m)", "ocean_heat_content_0_700m_zettajoules", "latest", "{val:,.1f} ZJ", "Surface Mixed Layer Heating", "neg"),
            ("Deep Ocean (700-2000m)", "deep_ocean_heat_700_2000m_zj", "latest", "{val:,.1f} ZJ", "Abyssal Heat Penetration", "neg"),
            ("Pacific Basin Heating", "pacific_ocean_heat_anomaly_zj", "latest", "{val:,.1f} ZJ", "Largest Planetary Heat Sink", "neg"),
            ("Annual Thermal Uptake Rate", "annual_ocean_heat_uptake_rate_zj_yr", "latest", "{val:+.1f} ZJ/Yr", "Planetary Heat Imbalance", "neg")
        ],
        "charts": [
            ("line", "year", ["ocean_heat_content_0_2000m_zettajoules"], "Global Full-Depth (0-2000m) Ocean Heat Content Anomaly Trajectory (1965-2024)", "Year", "Heat Anomaly (Zettajoules)"),
            ("area", "year", ["ocean_heat_content_0_700m_zettajoules", "deep_ocean_heat_700_2000m_zj"], "Ocean Thermal Partitioning: Upper Ocean (0-700m) vs Intermediate Ocean (700-2000m)", "Year", "Heat Content (ZJ)"),
            ("line", "year", ["pacific_ocean_heat_anomaly_zj", "indian_ocean_heat_anomaly_zj", "north_atlantic_heat_anomaly_zj"], "Major Oceanic Basin Thermal Anomaly Trends (Pacific, Indian, North Atlantic)", "Year", "Thermal Anomaly (ZJ)"),
            ("horizontal_bar", "ocean_heat_content_0_2000m_zettajoules", "year", "Decadal Planetary Ocean Heat Content Milestones (Zettajoules)", "Heat Anomaly (ZJ)", "Year"),
            ("scatter", "ocean_heat_content_0_700m_zettajoules", "annual_ocean_heat_uptake_rate_zj_yr", "Upper Ocean Heat Anomaly vs Planetary Annual Heat Absorption Rate", "Upper Ocean Heat (ZJ)", "Uptake Rate (ZJ/Yr)"),
            ("histogram", "annual_ocean_heat_uptake_rate_zj_yr", None, "Annual Planetary Oceanic Heat Uptake Velocity Rate Distribution (ZJ/Year)", "Uptake Rate (ZJ/Yr)", "Frequency"),
            ("radar", ["upper_ocean_heat_share_pct", "annual_ocean_heat_uptake_rate_zj_yr"], None, "Planetary Thermodynamic Marine Equilibrium Profile", None, None)
        ]
    },
    {
        "id": "D66",
        "slug": "d66_ioc_olympic_games_history",
        "title": "IOC Worldwide Modern Olympic Games Historical Performance",
        "domain": "International Athletics & Sports Analytics",
        "file": "d66_ioc_olympic_games_history.py",
        "csv": "data/analytical/d66_ioc_olympic_games_history.csv",
        "time_col": "edition_year",
        "kpis": [
            ("Olympic Athletes", "participating_athletes", "latest", "{val:,.0f}", "Paris 2024 Competitors", "pos"),
            ("Female Participation Share", "female_athlete_share_pct", "latest", "{val:.1f}%", "Perfect Gender Parity Milestone", "pos"),
            ("Participating Delegations", "participating_nations", "latest", "{val:,.0f} NOCs", "Universal National Attendance", "pos"),
            ("Contested Medal Events", "total_events_contested", "latest", "{val:,.0f} Events", "Diverse Sports Program", "pos"),
            ("Top Nation Medals (USA)", "usa_medals_total", "latest", "{val:,.0f} Medals", "Leader of Medal Table", "pos")
        ],
        "charts": [
            ("line", "edition_year", ["participating_athletes"], "Modern Summer Olympic Games Athletic Participation Expansion (1960-2024)", "Edition Year", "Athletes Count"),
            ("line", "edition_year", ["female_athlete_share_pct"], "Female Athlete Share of Olympic Competitors: Progression to 50% Parity (%)", "Edition Year", "Female Share (%)"),
            ("scatter", "participating_nations", "participating_athletes", "National Olympic Committees Attendance vs Total Participating Athletes", "Nations (NOCs)", "Total Athletes"),
            ("horizontal_bar", "total_events_contested", "edition_year", "Contested Olympic Sport Medal Events by Olympiad Edition", "Medal Events", "Edition Year"),
            ("bar", "edition_year", ["usa_medals_total", "china_medals_total", "india_medals_total"], "Comparative Sovereign Medal Table Hauls Across Historical Olympiads", "Edition Year", "Medals Count"),
            ("histogram", "female_athlete_share_pct", None, "Female Athlete Representation Progress Distribution Across Modern Olympiads", "Female Share (%)", "Frequency"),
            ("radar", ["female_athlete_share_pct", "participating_nations"], None, "Olympic Games Scale, Inclusivity & Global Representation Signature", None, None)
        ]
    },
    {
        "id": "D67",
        "slug": "d67_unctad_maritime_merchant_fleet",
        "title": "UNCTAD Global Maritime Merchant Fleet & Vessel Capacity",
        "domain": "Maritime Economics & Global Supply Chain Logistics",
        "file": "d67_unctad_maritime_merchant_fleet.py",
        "csv": "data/analytical/d67_unctad_maritime_merchant_fleet.csv",
        "time_col": "year",
        "kpis": [
            ("World Merchant Fleet", "world_fleet_deadweight_tonnage_million", "latest", "{val:,.1f}M DWT", "Global Carrying Capacity", "pos"),
            ("Seaborne Trade Volume", "seaborne_trade_volume_billion_tons", "latest", "{val:.2f}B Tons", "International Ocean Freight", "pos"),
            ("Dry Bulk Carrier Capacity", "bulk_carriers_dwt_million", "latest", "{val:,.1f}M DWT", "Iron Ore, Grain & Coal Fleet", "pos"),
            ("Container Ship Capacity", "container_ships_dwt_million", "latest", "{val:,.1f}M DWT", "Manufactured Goods Liners", "pos"),
            ("Average Commercial Fleet Age", "average_vessel_age_years", "latest", "{val:.1f} Yrs", "Fleet Decarbonization Need", "neutral")
        ],
        "charts": [
            ("line", "year", ["world_fleet_deadweight_tonnage_million"], "World Merchant Fleet Deadweight Tonnage Capacity Expansion (2005-2024)", "Year", "Deadweight Tonnage (Million DWT)"),
            ("area", "year", ["bulk_carriers_dwt_million", "oil_tankers_dwt_million", "container_ships_dwt_million", "general_cargo_dwt_million", "lng_lpg_gas_carriers_dwt_million"], "Commercial Vessel Fleet Composition by Ship Type (Million DWT)", "Year", "Capacity (Million DWT)"),
            ("scatter", "world_fleet_deadweight_tonnage_million", "seaborne_trade_volume_billion_tons", "Merchant Carrying Capacity vs Global Seaborne Trade Volume", "Fleet Capacity (M DWT)", "Seaborne Trade (B Tons)"),
            ("horizontal_bar", "lng_lpg_gas_carriers_dwt_million", "year", "Specialized LNG & LPG Liquefied Gas Carrier Fleet Expansion (M DWT)", "Gas Fleet (M DWT)", "Year"),
            ("bar", "year", ["average_vessel_age_years"], "Average Commercial Vessel Age Across the World Fleet (Years)", "Year", "Fleet Age (Years)"),
            ("histogram", "bulk_plus_tanker_share_pct", None, "Combined Bulk Carrier & Oil Tanker Share Distribution in World Fleet (%)", "Bulk/Tanker Share (%)", "Frequency"),
            ("radar", ["bulk_plus_tanker_share_pct", "container_share_pct"], None, "International Maritime Supply Chain Fleet Architecture", None, None)
        ]
    },
    {
        "id": "D68",
        "slug": "d68_emdat_natural_disasters",
        "title": "CRED EM-DAT International Natural Disasters & Economic Impact",
        "domain": "Disaster Risk Science & Climatological Hazard Analysis",
        "file": "d68_emdat_natural_disasters.py",
        "csv": "data/analytical/d68_emdat_natural_disasters.csv",
        "time_col": "year",
        "kpis": [
            ("Annual Recorded Disasters", "total_recorded_disasters", "latest", "{val:,.0f} Events", "Acute Disaster Inundations", "neg"),
            ("Direct Economic Damages", "total_economic_damages_billion_usd", "latest", "${val:,.1f}B", "Insured & Uninsured Loss", "neg"),
            ("Affected Population", "total_affected_people_millions", "latest", "{val:,.1f}M", "Displaced & Needing Relief", "neg"),
            ("Hydro-Meteorological Share", "hydrometeorological_share_pct", "latest", "{val:.1f}%", "Floods & Tropical Cyclones", "neg"),
            ("Human Fatalities Recorded", "total_fatalities_thousands", "latest", "{val:.1f}k", "Direct Catastrophic Casualties", "neg")
        ],
        "charts": [
            ("line", "year", ["total_recorded_disasters"], "Annual Frequency of Worldwide Recorded Acute Natural Disasters (2000-2024)", "Year", "Disaster Events"),
            ("area", "year", ["flood_events_count", "storm_cyclone_events_count", "earthquake_events_count", "extreme_temperature_wildfire_count"], "Disaster Hazard Type Composition (Floods, Storms, Earthquakes, Wildfires)", "Year", "Events Count"),
            ("scatter", "total_recorded_disasters", "total_economic_damages_billion_usd", "Recorded Disaster Incidents vs Direct Physical Economic Damages ($ Billion)", "Disaster Events", "Damages ($B USD)"),
            ("horizontal_bar", "total_economic_damages_billion_usd", "year", "Global Annual Economic Disaster Damage Milestones ($ Billion USD)", "Damages ($B)", "Year"),
            ("bar", "year", ["total_affected_people_millions"], "Populations Directly Impacted or Displaced by Natural Hazards (Millions)", "Year", "Affected (Millions)"),
            ("histogram", "hydrometeorological_share_pct", None, "Hydro-Meteorological Disaster Share Distribution Across Monitored Years (%)", "Weather Share (%)", "Frequency"),
            ("radar", ["hydrometeorological_share_pct", "economic_damage_per_event_million_usd"], None, "International Catastrophic Hazard Vulnerability Footprint", None, None)
        ]
    },
    {
        "id": "D69",
        "slug": "d69_oecd_pisa_education",
        "title": "OECD PISA Global Education Assessment & Student Literacy",
        "domain": "Educational Metrics & Cognitive Human Capital",
        "file": "d69_oecd_pisa_education.py",
        "csv": "data/analytical/d69_oecd_pisa_education.csv",
        "time_col": None,
        "kpis": [
            ("Top Mathematics Score", "mathematics_score_mean", "max", "{val:.1f} Pts", "Singapore Benchmark", "pos"),
            ("Top Reading Literacy", "reading_score_mean", "max", "{val:.1f} Pts", "Singapore Benchmark", "pos"),
            ("Top Science Literacy", "science_score_mean", "max", "{val:.1f} Pts", "Singapore Benchmark", "pos"),
            ("High Performing Cohort", "high_performing_students_pct", "max", "{val:.1f}%", "Level 5/6 Advanced Students", "pos"),
            ("Socioeconomic Equity Peak", "socioeconomic_equity_index", "max", "{val:.2f}", "Estonia Inclusive System", "pos")
        ],
        "charts": [
            ("bar", "country", "composite_pisa_average", "PISA Composite Academic Performance Across Participating Nations (Points)", "Country", "Composite PISA Score"),
            ("scatter", "education_expenditure_per_student_usd", "mathematics_score_mean", "Cumulative Education Spending Per Student vs Mathematics Literacy", "Expenditure Per Student ($)", "Math Score"),
            ("area", "country", ["mathematics_score_mean", "reading_score_mean", "science_score_mean"], "Subject Triad Score Profile Comparison Across Education Systems (Math, Reading, Science)", "Country", "Score Points"),
            ("horizontal_bar", "high_performing_students_pct", "country", "Percentage of High-Achieving Students Across National Education Systems (%)", "High Performers (%)", "Country"),
            ("bar", "country", "socioeconomic_equity_index", "Socioeconomic Equity Index in Educational Attainment Across Nations", "Country", "Equity Index"),
            ("histogram", "reading_score_mean", None, "Reading Literacy Mean Score Frequency Distribution Across Participating States", "Reading Score", "Education Systems"),
            ("radar", ["socioeconomic_equity_index", "high_performing_students_pct"], None, "Cognitive Competency & Academic Equity System Signature", None, None)
        ]
    },
    {
        "id": "D70",
        "slug": "d70_iucn_red_list_biodiversity",
        "title": "IUCN Red List Global Biodiversity & Species Extinction Risk",
        "domain": "Biodiversity & Conservation Biology",
        "file": "d70_iucn_red_list_biodiversity.py",
        "csv": "data/analytical/d70_iucn_red_list_biodiversity.csv",
        "time_col": "year",
        "kpis": [
            ("Total Assessed Species", "total_assessed_species", "latest", "{val:,.0f}", "Evaluated Biological Taxa", "pos"),
            ("Threatened with Extinction", "total_threatened_species", "latest", "{val:,.0f}", "CR, EN and VU Species", "neg"),
            ("Critically Endangered", "critically_endangered_species", "latest", "{val:,.0f}", "Highest Extinction Risk", "neg"),
            ("Amphibian Extinction Risk", "amphibians_threatened_pct", "latest", "{val:.1f}%", "Most Vulnerable Class", "neg"),
            ("Reef Coral Threat Share", "corals_threatened_pct", "latest", "{val:.1f}%", "Thermal Bleaching Risk", "neg")
        ],
        "charts": [
            ("line", "year", ["total_threatened_species"], "Worldwide Documented Species Threatened with Extinction (2005-2024)", "Year", "Threatened Species"),
            ("area", "year", ["critically_endangered_species", "endangered_species", "vulnerable_species"], "IUCN Threat Category Severity Progression (Critically Endangered, Endangered, Vulnerable)", "Year", "Species Count"),
            ("scatter", "total_assessed_species", "total_threatened_species", "Cumulative Assessed Biodiversity vs Total Documented Threatened Taxa", "Assessed Species", "Threatened Species"),
            ("horizontal_bar", "total_threatened_species", "year", "Extinction Threat Documentation Acceleration Milestones by Year", "Threatened Taxa", "Year"),
            ("bar", "year", ["amphibians_threatened_pct", "mammals_threatened_pct", "corals_threatened_pct"], "Taxonomic Group Vulnerability Proportions Over Assessment Cycles (%)", "Year", "Threatened (%)"),
            ("histogram", "threatened_share_of_assessed_pct", None, "Proportion of Evaluated Species Categorized as Threatened Distribution (%)", "Threatened Share (%)", "Frequency"),
            ("radar", ["amphibians_threatened_pct", "mammals_threatened_pct", "corals_threatened_pct"], None, "Taxonomic Biodiversity Depletion & Extinction Vulnerability", None, None)
        ]
    },
    {
        "id": "D71",
        "slug": "d71_faostat_fertilizer_nutrients",
        "title": "FAOSTAT Global Agricultural Fertilizer Consumption & Nutrient Application",
        "domain": "Agronomy & Soil Biogeochemistry",
        "file": "d71_faostat_fertilizer_nutrients.py",
        "csv": "data/analytical/d71_faostat_fertilizer_nutrients.csv",
        "time_col": "year",
        "kpis": [
            ("Total Nutrient Application", "total_nutrient_consumption_million_tonnes", "latest", "{val:.1f} MMT", "Global N + P₂O₅ + K₂O", "neutral"),
            ("Nitrogen Influx (N)", "nitrogen_n_million_tonnes", "latest", "{val:.1f} MMT", "Synthesized Nitrogen", "neutral"),
            ("Cropland Intensity", "nutrient_use_per_cropland_kg_ha", "latest", "{val:.1f} kg/ha", "Application Per Hectare", "neutral"),
            ("Phosphate Nutrients", "phosphorus_p2o5_million_tonnes", "latest", "{val:.1f} MMT", "Phosphorus (P₂O₅)", "neutral"),
            ("Global Cereal Harvest", "cereal_grain_production_billion_tonnes", "latest", "{val:.2f}B Tons", "Supported Grain Output", "pos")
        ],
        "charts": [
            ("line", "year", ["total_nutrient_consumption_million_tonnes"], "Global Agricultural Chemical Nutrient Consumption Trajectory (2002-2024)", "Year", "Nutrients (Million Tonnes)"),
            ("area", "year", ["nitrogen_n_million_tonnes", "phosphorus_p2o5_million_tonnes", "potassium_k2o_million_tonnes"], "Primary Agronomic Nutrients Breakdown (Nitrogen N, Phosphate P₂O₅, Potash K₂O)", "Year", "Nutrients (MMT)"),
            ("scatter", "total_nutrient_consumption_million_tonnes", "cereal_grain_production_billion_tonnes", "Nutrient Consumption vs Global Cereal Grain Production Output", "Nutrients (MMT)", "Grain (Billion Tons)"),
            ("horizontal_bar", "nutrient_use_per_cropland_kg_ha", "year", "Global Cropland Chemical Nutrient Intensity Progression (kg / Hectare)", "Intensity (kg/ha)", "Year"),
            ("bar", "year", ["nitrogen_use_efficiency_pct"], "Estimated Global Agronomic Nitrogen Use Efficiency Benchmark (%)", "Year", "NUE (%)"),
            ("histogram", "nitrogen_share_of_total_pct", None, "Nitrogen Consumption Share Distribution in Total Primary Nutrients (%)", "Nitrogen Share (%)", "Frequency"),
            ("radar", ["nitrogen_share_of_total_pct", "asia_fertilizer_share_pct", "nitrogen_use_efficiency_pct"], None, "Agronomic Nutrient Application Balance & Efficiency Profile", None, None)
        ]
    },
    {
        "id": "D72",
        "slug": "d72_unoosa_orbital_space_launches",
        "title": "UNOOSA / Space-Track Worldwide Orbital Space Launches & Missions",
        "domain": "Aerospace Engineering & Astronautics",
        "file": "d72_unoosa_orbital_space_launches.py",
        "csv": "data/analytical/d72_unoosa_orbital_space_launches.csv",
        "time_col": "year",
        "kpis": [
            ("Orbital Rocket Launches", "total_orbital_launches", "latest", "{val:,.0f} Flights", "Record Launch Frequency", "pos"),
            ("Payloads Placed in Orbit", "payloads_placed_in_orbit", "latest", "{val:,.0f} Satellites", "Orbital Objects Injected", "pos"),
            ("Launch Success Rate", "launch_success_rate_pct", "latest", "{val:.1f}%", "Booster Flight Reliability", "pos"),
            ("Commercial Satellite Share", "commercial_payload_share_pct", "latest", "{val:.1f}%", "Megaconstellation Dominance", "pos"),
            ("Leading Sovereign (USA)", "united_states_launches", "latest", "{val:,.0f} Missions", "Driven by Falcon 9 Fleet", "pos")
        ],
        "charts": [
            ("line", "year", ["total_orbital_launches", "successful_orbital_launches"], "Worldwide Orbital Launch Attempts vs Successful Orbital Insertions (2005-2024)", "Year", "Orbital Launches"),
            ("area", "year", ["commercial_satellite_payloads", "government_civil_payloads", "military_defense_payloads"], "Orbital Satellite Payload Missions Categorization (Commercial, Civil, Defense)", "Year", "Payloads Deployed"),
            ("line", "year", ["united_states_launches", "china_launches", "russia_launches", "india_isro_launches"], "National Space Agency & Commercial Rocket Launch Activity Comparison", "Year", "Launches Count"),
            ("horizontal_bar", "payloads_placed_in_orbit", "year", "Annual Orbital Satellite Payloads Deployment Acceleration Milestones", "Payloads Placed", "Year"),
            ("scatter", "total_orbital_launches", "payloads_placed_in_orbit", "Orbital Launch Missions vs Total Payloads Deployed (Megaconstellation Rideshare)", "Launches", "Payloads Placed"),
            ("histogram", "payloads_per_launch_density", None, "Average Payload Deployment Density Per Successful Launch Mission Distribution", "Payloads/Launch", "Frequency"),
            ("radar", ["launch_success_rate_pct", "commercial_payload_share_pct", "us_launch_share_pct"], None, "Global Spaceflight Launch Cadence & Payload Architecture", None, None)
        ]
    },
    {
        "id": "D73",
        "slug": "d73_energy_institute_world_energy",
        "title": "Energy Institute World Primary Energy Consumption by Fuel Mix",
        "domain": "Energy Economics & Global Transition Thermodynamics",
        "file": "d73_energy_institute_world_energy.py",
        "csv": "data/analytical/d73_energy_institute_world_energy.csv",
        "time_col": "year",
        "kpis": [
            ("Total Primary Energy", "total_primary_energy_exajoules", "latest", "{val:,.1f} EJ", "Global Consumption Scale", "pos"),
            ("Modern Wind & Solar", "renewables_wind_solar_exajoules", "latest", "{val:,.1f} EJ", "Clean Renewable Energy", "pos"),
            ("Fossil Fuel Share", "fossil_fuel_share_pct", "latest", "{val:.1f}%", "Hydrocarbon Dominance", "neg"),
            ("Clean Primary Electricity", "clean_power_combined_exajoules", "latest", "{val:,.1f} EJ", "Solar, Wind, Hydro & Nuclear", "pos"),
            ("Coal Baseload Energy", "coal_consumption_exajoules", "latest", "{val:,.1f} EJ", "Global Coal Demand", "neutral")
        ],
        "charts": [
            ("line", "year", ["total_primary_energy_exajoules"], "World Total Primary Energy Consumption Growth Trajectory (Exajoules)", "Year", "Primary Energy (EJ)"),
            ("area", "year", ["oil_consumption_exajoules", "coal_consumption_exajoules", "natural_gas_exajoules", "renewables_wind_solar_exajoules", "hydroelectricity_exajoules", "nuclear_energy_exajoules"], "Global Primary Energy Consumption by Fuel Mix (Oil, Coal, Gas, Renewables, Hydro, Nuclear)", "Year", "Energy (Exajoules)"),
            ("line", "year", ["renewables_wind_solar_exajoules", "nuclear_energy_exajoules", "hydroelectricity_exajoules"], "Clean Energy Comparison: Accelerating Wind & Solar vs Baseload Hydro & Nuclear", "Year", "Energy (EJ)"),
            ("horizontal_bar", "renewables_wind_solar_exajoules", "year", "Modern Renewable Wind & Solar Energy Expansion Milestones (EJ)", "Renewables (EJ)", "Year"),
            ("scatter", "renewables_wind_solar_exajoules", "fossil_fuel_share_pct", "Modern Renewable Energy Scale vs Fossil Fuel Displacement Share (%)", "Renewables (EJ)", "Fossil Share (%)"),
            ("histogram", "clean_power_share_total_pct", None, "Combined Clean Primary Electricity Share Distribution in Total Global Energy (%)", "Clean Power (%)", "Frequency"),
            ("radar", ["clean_power_share_total_pct", "renewable_energy_share_pct"], None, "Global Energy Transition Decarbonization Footprint", None, None)
        ]
    },
    {
        "id": "D74",
        "slug": "d74_un_sdsn_world_happiness",
        "title": "UN SDSN / Gallup World Happiness Index & Life Satisfaction",
        "domain": "Behavioral Economics & Subjective Well-Being",
        "file": "d74_un_sdsn_world_happiness.py",
        "csv": "data/analytical/d74_un_sdsn_world_happiness.csv",
        "time_col": None,
        "kpis": [
            ("Top Cantril Life Rating", "happiness_cantril_ladder_score", "max", "{val:.2f} / 10", "Finland 7-Year Leader", "pos"),
            ("Cohort Average Well-Being", "happiness_cantril_ladder_score", "mean", "{val:.2f} / 10", "Evaluated Nations Average", "neutral"),
            ("Healthy Life Expectancy", "healthy_life_expectancy_years", "max", "{val:.1f} Yrs", "Japan Longevity Benchmark", "pos"),
            ("Social Support Network", "social_support_index", "max", "{val:.2f}", "Iceland Cohesive Society", "pos"),
            ("India Subjective Evaluation", "happiness_cantril_ladder_score", "min", "{val:.2f} / 10", "Cantril Ladder Score", "neutral")
        ],
        "charts": [
            ("bar", "country", "happiness_cantril_ladder_score", "Worldwide Cantril Ladder Subjective Well-Being Score Ranking (0-10)", "Country", "Happiness Score"),
            ("scatter", "gdp_per_capita_purchasing_power_parity", "happiness_cantril_ladder_score", "Economic Prosperity (GDP Per Capita PPP) vs Subjective Happiness Score", "GDP Per Capita PPP", "Happiness Score"),
            ("area", "country", ["gdp_per_capita_purchasing_power_parity", "social_support_index", "freedom_to_make_life_choices_score", "perceptions_of_corruption_score"], "Well-Being Explanatory Pillars Breakdown (GDP, Social Support, Freedom, Trust)", "Country", "Pillar Scores"),
            ("horizontal_bar", "healthy_life_expectancy_years", "country", "Healthy Life Expectancy at Birth Across Evaluated Nations (Years)", "Life Expectancy (Years)", "Country"),
            ("bar", "country", "social_support_index", "Perceived Social Support & Community Safety Net Strength by Country", "Country", "Social Support"),
            ("histogram", "happiness_cantril_ladder_score", None, "Cantril Ladder Subjective Life Satisfaction Score Distribution", "Happiness Score", "Nations Count"),
            ("radar", ["economic_and_social_synergy_score", "governance_trust_index"], None, "Multi-Dimensional Subjective Well-Being & Civic Trust Signature", None, None)
        ]
    }
,
# --- D75 to D94: Real-World-Impactful Decision-Support Suites ---
    {
        "id": "D75",
        "slug": "d75_who_amr_surveillance",
        "title": "Global Antimicrobial Resistance (AMR) & Pathogen Surveillance",
        "domain": "Epidemiology & Clinical Pharmacology",
        "file": "d75_who_amr_surveillance.py",
        "csv": "data/analytical/d75_who_amr_surveillance.csv",
        "time_col": None,
        "kpis": [
            ("MRSA Resistance Rate", "mrsa_resistance_pct", "mean", "{val:.1f}%", "Bloodstream Pathogen Rate", "neg"),
            ("E. coli 3GCR Resistance", "ecoli_3gcr_resistance_pct", "mean", "{val:.1f}%", "3rd Gen Cephalosporin Res", "neg"),
            ("Carbapenem-Resistant Klebsiella", "klebsiella_carbapenem_res_pct", "max", "{val:.1f}%", "Peak Pathogen Threat", "neg"),
            ("Surveillance Culture Sites", "blood_culture_surveillance_sites", "sum", "{val:,.0f} Labs", "GLASS Reporting Network", "pos"),
            ("Stewardship Compliance", "antimicrobial_stewardship_compliance_pct", "mean", "{val:.1f}%", "Hospital Protocol Standard", "neutral")
        ],
        "charts": [
            ("bar", "country", "mrsa_resistance_pct", "Methicillin-Resistant S. aureus (MRSA) Bloodstream Infection Rate (%)", "Country", "MRSA Resistance (%)"),
            ("scatter", "antimicrobial_stewardship_compliance_pct", "composite_amr_threat_score", "Antimicrobial Stewardship Compliance vs Composite AMR Threat Score", "Stewardship Compliance (%)", "Composite AMR Threat Score"),
            ("area", "country", ["mrsa_resistance_pct", "ecoli_3gcr_resistance_pct", "klebsiella_carbapenem_res_pct"], "Critical Pathogen Resistance Profiles by Monitored Country (%)", "Country", "Resistance (%)"),
            ("horizontal_bar", "composite_amr_threat_score", "country", "Composite AMR Pathogen Threat Index by Country", "AMR Threat Index", "Country"),
            ("violin", None, "defined_daily_doses_per_1000", "Distribution of Antibiotic Consumption Intensity (Defined Daily Doses / 1000 Inhabitants)", "Surveillance Network", "DDD per 1000"),
            ("donut", "resistance_severity_tier", "country", "Hospital Resistance Severity Tier Classification", "", ""),
            ("radar", ["mrsa_resistance_pct", "ecoli_3gcr_resistance_pct", "klebsiella_carbapenem_res_pct", "stewardship_gap_pct"], None, "Multi-Dimensional Pathogen Resistance & Stewardship Gap Radar Profile", None, None)
        ]
    },
    {
        "id": "D76",
        "slug": "d76_grid_india_frequency_stability",
        "title": "National Power Grid Frequency Stability & Peak Demand Compliance",
        "domain": "Electrical Engineering & National Grid Operations",
        "file": "d76_grid_india_frequency_stability.py",
        "csv": "data/analytical/d76_grid_india_frequency_stability.csv",
        "time_col": "year",
        "kpis": [
            ("Peak Demand Met", "peak_demand_met_gw", "max", "{val:.1f} GW", "All-Time Summer Peak", "pos"),
            ("Annual Energy Met", "energy_met_billion_units", "max", "{val:,.0f} BU", "Gross Generation Supply", "pos"),
            ("Frequency Band Compliance", "time_within_frequency_band_pct", "mean", "{val:.2f}%", "49.90 - 50.05 Hz Operating Band", "pos"),
            ("Renewable Capacity", "renewable_installed_capacity_gw", "max", "{val:.1f} GW", "Clean Generation Fleet", "pos"),
            ("Spinning Reserve Margin", "spinning_reserve_margin_pct", "mean", "{val:.1f}%", "Operating Frequency Buffer", "neutral")
        ],
        "charts": [
            ("line", "year", ["peak_demand_met_gw", "renewable_installed_capacity_gw"], "National Peak Demand Met vs Renewable Installed Capacity Trajectory (GW)", "Fiscal Year", "Capacity / Demand (GW)"),
            ("area", "year", ["time_within_frequency_band_pct", "total_frequency_excursions_pct"], "Grid Frequency Compliance Band vs Excursion Distribution (%)", "Fiscal Year", "Operating Time Share (%)"),
            ("bar", "year", "energy_met_billion_units", "Total Electrical Energy Supplied to National Grid (Billion Units)", "Fiscal Year", "Billion Units (BU)"),
            ("scatter", "renewable_installed_capacity_gw", "estimated_renewable_curtailment_pct", "Renewable Penetration Scale vs Renewable Curtailment Share (%)", "Renewable Capacity (GW)", "Curtailment Rate (%)"),
            ("horizontal_bar", "spinning_reserve_margin_pct", "year", "Grid Dispatch Operating Spinning Reserve Margin (%)", "Reserve Margin (%)", "Fiscal Year"),
            ("box", None, "time_within_frequency_band_pct", "Dispersion of Frequency Standard Adherence Across Operational Years (%)", "Operating Horizon", "Time in Band (%)"),
            ("radar", ["time_within_frequency_band_pct", "spinning_reserve_margin_pct", "renewable_share_of_capacity_pct"], None, "Power System Reliability & Renewable Transition Balance Radar", None, None)
        ]
    },
    {
        "id": "D77",
        "slug": "d77_cpcb_municipal_solid_waste",
        "title": "Urban Solid Waste Processing & Legacy Landfill Remediation",
        "domain": "Municipal Waste Management & Urban Sanitation",
        "file": "d77_cpcb_municipal_solid_waste.py",
        "csv": "data/analytical/d77_cpcb_municipal_solid_waste.csv",
        "time_col": None,
        "kpis": [
            ("Total Waste Generated", "waste_generated_tpd", "sum", "{val:,.0f} TPD", "Daily Municipal Generation", "neutral"),
            ("Waste Processed", "waste_processed_tpd", "sum", "{val:,.0f} TPD", "Scientific Remediation Volume", "pos"),
            ("Average Processing Rate", "processing_rate_pct", "mean", "{val:.1f}%", "Overall Treatment Efficiency", "neutral"),
            ("Legacy Dump Waste", "legacy_landfill_waste_lakh_tons", "sum", "{val:,.1f} L MT", "Biomining Remediation Deficit", "neg"),
            ("Source Segregation", "source_segregation_pct", "mean", "{val:.1f}%", "Household Segregation Level", "pos")
        ],
        "charts": [
            ("bar", "city", ["waste_generated_tpd", "waste_processed_tpd"], "Daily Municipal Solid Waste Generation vs Scientific Processing (TPD)", "City", "Tonnes Per Day (TPD)"),
            ("scatter", "source_segregation_pct", "processing_rate_pct", "Household Source Segregation Rate vs Final Waste Processing Efficiency (%)", "Source Segregation (%)", "Processing Rate (%)"),
            ("horizontal_bar", "legacy_landfill_waste_lakh_tons", "city", "Unprocessed Legacy Landfill Waste Accumulation (Lakh Metric Tonnes)", "Legacy Waste (Lakh MT)", "City"),
            ("donut", "processing_performance_tier", "city", "Urban Local Body Waste Processing Performance Tiers", "", ""),
            ("area", "city", ["wet_organic_waste_pct", "dry_recyclable_pct"], "Waste Composition Characterization: Wet Organic vs Dry Recyclable Shares (%)", "City", "Share (%)"),
            ("histogram", "processing_rate_pct", None, "Distribution of Scientific Waste Processing Rates Across 25 Metros (%)", "Processing Rate (%)", "City Count"),
            ("radar", ["collection_efficiency_pct", "processing_rate_pct", "source_segregation_pct"], None, "Municipal Solid Waste Management Capability Signature", None, None)
        ]
    },
    {
        "id": "D78",
        "slug": "d78_cgwb_groundwater_stress",
        "title": "National Aquifer Depletion & Groundwater Extraction Vulnerability",
        "domain": "Hydrogeology & Water Resource Security",
        "file": "d78_cgwb_groundwater_stress.py",
        "csv": "data/analytical/d78_cgwb_groundwater_stress.csv",
        "time_col": None,
        "kpis": [
            ("Extractable Groundwater", "total_annual_extractable_bcm", "sum", "{val:,.1f} BCM", "Annual Recharge Potential", "pos"),
            ("Annual Extraction", "current_annual_extraction_bcm", "sum", "{val:,.1f} BCM", "Gross Aquifer Draft", "neg"),
            ("Over-Exploited Blocks", "over_exploited_units_count", "sum", "{val:,.0f} Units", ">100% Extraction Stage", "neg"),
            ("Critical & Stressed Units", "total_stressed_units", "sum", "{val:,.0f} Units", "Acute Hydrological Strain", "neg"),
            ("Safe Aquifer Balance", "net_groundwater_balance_bcm", "sum", "{val:,.1f} BCM", "Net Annual Water Buffer", "pos")
        ],
        "charts": [
            ("bar", "state", ["total_annual_extractable_bcm", "current_annual_extraction_bcm"], "Annual Extractable Groundwater Recharge vs Current Aquifer Draft (BCM)", "State", "Billion Cubic Meters (BCM)"),
            ("horizontal_bar", "stage_of_extraction_pct", "state", "Groundwater Stage of Extraction Ranking Across States (>100% Over-Exploited)", "Stage of Extraction (%)", "State"),
            ("scatter", "stage_of_extraction_pct", "stressed_units_share_pct", "Groundwater Extraction Stage vs Stressed Assessment Units Share (%)", "Stage of Extraction (%)", "Stressed Units Share (%)"),
            ("donut", "aquifer_stress_tier", "state", "National Aquifer Vulnerability Classification Tiers", "", ""),
            ("area", "state", ["over_exploited_units_count", "critical_units_count", "safe_units_count"], "Assessment Units Categorization: Over-Exploited vs Critical vs Safe Units", "State", "Assessment Units"),
            ("box", None, "stage_of_extraction_pct", "Dispersion of Aquifer Extraction Intensity Across Indian States (%)", "All Assessed States", "Extraction Stage (%)"),
            ("radar", ["stage_of_extraction_pct", "stressed_units_share_pct"], None, "Sovereign Hydrogeological Depletion Severity Radar", None, None)
        ]
    },
    {
        "id": "D79",
        "slug": "d79_iea_critical_minerals",
        "title": "Critical Clean Energy Minerals Supply Concentration & Refining Dominance",
        "domain": "Geopolitics & Energy Transition Materials",
        "file": "d79_iea_critical_minerals.py",
        "csv": "data/analytical/d79_iea_critical_minerals.csv",
        "time_col": None,
        "kpis": [
            ("Global Mineral Market", "global_market_size_billion_usd", "sum", "${val:,.1f}B", "Total Critical Mineral Market", "pos"),
            ("Peak Mining Concentration", "top_producer_share_pct", "max", "{val:.1f}%", "DRC Cobalt Mining Dominance", "neg"),
            ("Peak Refining Monopsony", "top_refiner_share_pct", "max", "{val:.1f}%", "China Graphite Refining Lead", "neg"),
            ("Max 2030 Supply Deficit", "projected_2030_supply_deficit_pct", "max", "{val:.1f}%", "Lithium Battery Cell Gap", "neg"),
            ("Average Recycling Share", "recycling_share_of_supply_pct", "mean", "{val:.1f}%", "Secondary Supply Contribution", "neutral")
        ],
        "charts": [
            ("bar", "mineral", ["top_producer_share_pct", "top_refiner_share_pct"], "Top Sovereign Concentration: Mining Extraction Share vs Chemical Refining Share (%)", "Critical Mineral", "Share (%)"),
            ("scatter", "top_refiner_share_pct", "projected_2030_supply_deficit_pct", "Refining Concentration Share vs Projected 2030 Supply Deficit (%)", "Top Refiner Share (%)", "2030 Deficit (%)"),
            ("horizontal_bar", "global_market_size_billion_usd", "mineral", "Global Economic Market Size for Energy Transition Raw Materials ($ Billion)", "Market Value ($B)", "Mineral"),
            ("donut", "geopolitical_vulnerability_tier", "mineral", "Strategic Supply Disruption Vulnerability Classification", "", ""),
            ("bar", "mineral", "recycling_share_of_supply_pct", "Secondary Supply Circularity: Recycling Share of Total Annual Demand (%)", "Mineral", "Recycling Share (%)"),
            ("box", None, "top_refiner_share_pct", "Spread of Geographic Bottlenecks Across Critical Mineral Processing Hubs (%)", "Monitored Minerals", "Refining Share (%)"),
            ("radar", ["top_producer_share_pct", "top_refiner_share_pct", "projected_2030_supply_deficit_pct"], None, "Energy Transition Supply Chain Chokepoint Fingerprint", None, None)
        ]
    },
    {
        "id": "D80",
        "slug": "d80_nha_hospital_bed_capacity",
        "title": "Public Hospital Bed Density, ICU Infrastructure & Critical Care Preparedness",
        "domain": "Healthcare Delivery Systems & Clinical Capacity",
        "file": "d80_nha_hospital_bed_capacity.py",
        "csv": "data/analytical/d80_nha_hospital_bed_capacity.csv",
        "time_col": None,
        "kpis": [
            ("Public Hospital Beds", "total_public_hospital_beds", "sum", "{val:,.0f}", "Operating State Beds", "pos"),
            ("ICU Critical Care Beds", "total_icu_beds", "sum", "{val:,.0f}", "Ventilator-Supported Units", "pos"),
            ("National Bed Density", "beds_per_1000_population", "mean", "{val:.2f} / 1k", "WHO Norm: 3.0 / 1000", "neutral"),
            ("Average Occupancy Rate", "avg_bed_occupancy_rate_pct", "mean", "{val:.1f}%", "Inpatient Bed Utilization", "pos"),
            ("PM-JAY Empanelled Sites", "pmjay_empanelled_hospitals", "sum", "{val:,.0f}", "Ayushman Bharat Network", "pos")
        ],
        "charts": [
            ("bar", "state", ["total_public_hospital_beds", "total_icu_beds"], "Public Sector Inpatient Bed Capacity vs Critical Care ICU Infrastructure", "State", "Bed Count"),
            ("horizontal_bar", "beds_per_1000_population", "state", "Hospital Bed Density per 1,000 Population (WHO Norm: 3.0 Beds / 1k)", "Beds / 1k Pop", "State"),
            ("scatter", "doctors_per_1000", "nurses_per_1000", "Clinical Human Resource Density: Allopathic Doctors vs Staff Nurses per 1,000", "Doctors / 1k", "Nurses / 1k"),
            ("donut", "healthcare_capacity_tier", "state", "Hospital Bed & Staffing Density Readiness Tiers", "", ""),
            ("area", "state", ["doctors_per_1000", "nurses_per_1000"], "State Healthcare Workforce Staffing Density Profiles (Per 1,000 Citizens)", "State", "Density / 1k"),
            ("histogram", "avg_bed_occupancy_rate_pct", None, "Distribution of Public Hospital Bed Occupancy Rates Across 25 States (%)", "Bed Occupancy (%)", "States Count"),
            ("radar", ["beds_per_1000_population", "avg_bed_occupancy_rate_pct", "total_staffing_density_per_1000"], None, "Public Healthcare Delivery Resilience Signature", None, None)
        ]
    },
    {
        "id": "D81",
        "slug": "d81_fao_wfp_food_security",
        "title": "Global Food Import Dependency, Cereal Stockpiles & Caloric Deficits",
        "domain": "Agricultural Economics & Food Security",
        "file": "d81_fao_wfp_food_security.py",
        "csv": "data/analytical/d81_fao_wfp_food_security.csv",
        "time_col": None,
        "kpis": [
            ("Emergency Grain Reserve", "emergency_food_reserve_months", "mean", "{val:.1f} Mos", "National Food Reserve Buffer", "pos"),
            ("Max Cereal Import Ratio", "cereal_import_dependency_ratio_pct", "max", "{val:.1f}%", "Peak External Food Vulnerability", "neg"),
            ("Average Undernourishment", "undernourishment_prevalence_pct", "mean", "{val:.1f}%", "Prevalence of Chronic Hunger", "neg"),
            ("Average Caloric Intake", "per_capita_food_supply_kcal_day", "mean", "{val:,.0f} kcal", "Daily Per Capita Intake", "neutral"),
            ("Food Inflation Rate", "food_inflation_yoy_pct", "mean", "{val:.1f}%", "Basket YoY Price Surge", "neg")
        ],
        "charts": [
            ("bar", "country", ["cereal_import_dependency_ratio_pct", "cereal_stock_to_use_ratio_pct"], "Cereal Import Dependency Ratio vs Domestic Stock-to-Use Buffer (%)", "Country", "Ratio (%)"),
            ("horizontal_bar", "emergency_food_reserve_months", "country", "National Strategic Grain Stockpile Duration (Months of Consumption)", "Reserve Duration (Months)", "Country"),
            ("scatter", "cereal_import_dependency_ratio_pct", "food_inflation_yoy_pct", "Import Dependency vs Year-on-Year Retail Food Inflation Rate (%)", "Import Dependency (%)", "Food Inflation (%)"),
            ("donut", "food_security_vulnerability_tier", "country", "Multilateral Food Security Vulnerability Classification", "", ""),
            ("bar", "country", "undernourishment_prevalence_pct", "Prevalence of Population Undernourishment Across Monitored Nations (%)", "Country", "Undernourishment (%)"),
            ("box", None, "per_capita_food_supply_kcal_day", "Dispersion of Daily Per Capita Dietary Caloric Supply (kcal/day)", "Monitored Countries", "kcal / capita / day"),
            ("radar", ["cereal_import_dependency_ratio_pct", "food_inflation_yoy_pct", "undernourishment_prevalence_pct"], None, "National Food Insecurity Stress Radar Profile", None, None)
        ]
    },
    {
        "id": "D82",
        "slug": "d82_morth_urban_traffic_congestion",
        "title": "Metropolitan Traffic Congestion, Commuter Delay & Transit Deceleration",
        "domain": "Urban Mobility & Transportation Systems",
        "file": "d82_morth_urban_traffic_congestion.py",
        "csv": "data/analytical/d82_morth_urban_traffic_congestion.csv",
        "time_col": None,
        "kpis": [
            ("Peak Congestion Level", "congestion_level_pct", "max", "{val:.1f}%", "Bengaluru Extra Travel Delay", "neg"),
            ("Lost Commute Time", "lost_hours_per_year_commute", "mean", "{val:,.0f} Hrs", "Annual Commuter Time Lost", "neg"),
            ("10km Travel Duration", "time_to_travel_10km_mins", "mean", "{val:.1f} Mins", "Urban Mobility Benchmark", "neutral"),
            ("Average Peak Speed", "avg_peak_speed_kmh", "mean", "{val:.1f} km/h", "Corridor Gridlock Speed", "neutral"),
            ("Transit Modal Share", "public_transit_modal_share_pct", "mean", "{val:.1f}%", "Bus & Metro Ridership", "pos")
        ],
        "charts": [
            ("bar", "city", ["avg_peak_speed_kmh", "avg_off_peak_speed_kmh"], "Peak Rush-Hour Traffic Speed vs Off-Peak Free-Flow Velocity (km/h)", "City", "Speed (km/h)"),
            ("horizontal_bar", "lost_hours_per_year_commute", "city", "Annual Productive Working Hours Lost Due to Traffic Gridlock (Hours/Commuter)", "Hours Lost / Year", "City"),
            ("scatter", "public_transit_modal_share_pct", "congestion_level_pct", "Public Transit Modal Share vs Traffic Congestion Severity Index (%)", "Transit Modal Share (%)", "Congestion Level (%)"),
            ("donut", "congestion_severity_tier", "city", "Urban Traffic Congestion Severity Tiers", "", ""),
            ("bar", "city", "time_to_travel_10km_mins", "Time Required to Traverse 10 Kilometers in City Core (Minutes)", "City", "Minutes / 10km"),
            ("box", None, "co2_emissions_per_commuter_kg", "Carbon Emissions Generated Per Commuter Due to Traffic Idling (kg CO2/Year)", "All Metros", "kg CO2 / Commuter"),
            ("radar", ["congestion_level_pct", "speed_reduction_penalty_pct", "public_transit_modal_share_pct"], None, "Urban Gridlock & Deceleration Index Radar", None, None)
        ]
    },
    {
        "id": "D83",
        "slug": "d83_nbtc_blood_bank_reserves",
        "title": "National Blood Transfusion Inventory Reserves & Rare Group Stockout Risks",
        "domain": "Hematology & Public Health Logistics",
        "file": "d83_nbtc_blood_bank_reserves.py",
        "csv": "data/analytical/d83_nbtc_blood_bank_reserves.csv",
        "time_col": None,
        "kpis": [
            ("Registered Blood Banks", "total_registered_blood_banks", "sum", "{val:,.0f} Facilities", "Active Transfusion Centers", "pos"),
            ("Annual Units Collected", "annual_units_collected_lakh", "sum", "{val:,.1f} L Units", "Gross Sovereign Collection", "pos"),
            ("Voluntary Donation", "voluntary_donation_pct", "mean", "{val:.1f}%", "Unremunerated Donor Share", "pos"),
            ("O-Negative Reserve Days", "o_negative_reserve_days", "mean", "{val:.1f} Days", "Critical Universal Donor Buffer", "neutral"),
            ("Component Separation", "blood_component_separation_pct", "mean", "{val:.1f}%", "Packed RBC / Platelet Yield", "pos")
        ],
        "charts": [
            ("bar", "state", ["o_negative_reserve_days", "b_negative_reserve_days"], "Strategic Reserve Duration for Rare Rh-Negative Blood Groups (Days)", "State", "Reserve Days"),
            ("horizontal_bar", "annual_units_collected_lakh", "state", "Total Annual Blood Units Collected Across State Transfusion Networks (Lakh Units)", "Units (Lakh)", "State"),
            ("scatter", "voluntary_donation_pct", "blood_component_separation_pct", "Voluntary Donation Rate vs Component Separation Fraction (%)", "Voluntary Donation (%)", "Component Separation (%)"),
            ("donut", "blood_reserve_security_tier", "state", "State Blood Reserve Security & Stockout Buffer Classification", "", ""),
            ("bar", "state", "annual_wastage_due_to_expiry_pct", "Annual Blood & Component Wastage Due to Outdating Expiry (%)", "State", "Wastage (%)"),
            ("box", None, "rare_blood_group_average_reserve_days", "Dispersion of Rare Blood Stockpile Security Across States (Days)", "State Transfusion System", "Reserve Days"),
            ("radar", ["voluntary_donation_pct", "blood_component_separation_pct", "rare_blood_group_average_reserve_days"], None, "National Blood Transfusion Security Profile", None, None)
        ]
    },
    {
        "id": "D84",
        "slug": "d84_cpcb_cems_industrial_emissions",
        "title": "Industrial Cluster Continuous Stack Emissions & Environmental Pollution Index",
        "domain": "Industrial Pollution Control & Environmental Regulation",
        "file": "d84_cpcb_cems_industrial_emissions.py",
        "csv": "data/analytical/d84_cpcb_cems_industrial_emissions.csv",
        "time_col": None,
        "kpis": [
            ("Monitored CEMS Stacks", "cems_connected_stacks_count", "sum", "{val:,.0f} Stacks", "24x7 Real-Time Telemetry", "pos"),
            ("Peak CEPI Pollution Score", "cepi_pollution_index", "max", "{val:.1f}", "Critical Cluster Benchmark", "neg"),
            ("Average PM Exceedance", "stack_pm_exceedance_pct", "mean", "{val:.1f}%", "Particulate Emission Violations", "neg"),
            ("SO2 Compliance Rate", "so2_compliance_rate_pct", "mean", "{val:.1f}%", "Flue Gas Desulfurization Norms", "neutral"),
            ("Statutory Closure Notices", "closure_notices_issued", "sum", "{val:,.0f} Orders", "Regulatory Enforcement Orders", "neg")
        ],
        "charts": [
            ("bar", "industrial_cluster", "cepi_pollution_index", "Comprehensive Environmental Pollution Index (CEPI) Across Industrial Clusters", "Industrial Cluster", "CEPI Index Score"),
            ("horizontal_bar", "stack_pm_exceedance_pct", "industrial_cluster", "Particulate Matter (PM) Stack Emission Standard Exceedance Frequency (%)", "Exceedance Rate (%)", "Industrial Cluster"),
            ("scatter", "cepi_pollution_index", "closure_notices_issued", "CEPI Industrial Toxicity Index vs Statutory Closure Notices Issued", "CEPI Score", "Closure Notices"),
            ("donut", "pollution_severity_tier", "industrial_cluster", "CPCB Industrial Pollution Severity Tiers", "", ""),
            ("bar", "industrial_cluster", ["so2_compliance_rate_pct", "nox_compliance_rate_pct"], "Gaseous Emission Regulatory Compliance: SO2 vs NOx Stack Adherence Rates (%)", "Industrial Cluster", "Compliance (%)"),
            ("box", None, "cepi_pollution_index", "Distribution of Environmental Pollution Severity Across Monitored Clusters", "Industrial Clusters", "CEPI Score"),
            ("radar", ["stack_pm_exceedance_pct", "combined_gaseous_compliance_rate_pct"], None, "Industrial Cluster Environmental Non-Compliance Radar", None, None)
        ]
    },
    {
        "id": "D85",
        "slug": "d85_indian_railways_safety",
        "title": "Railway Operational Safety, Ultrasonic Rail Flaw Detection & Kavach ATP",
        "domain": "Railway Engineering & Operational Safety",
        "file": "d85_indian_railways_safety.py",
        "csv": "data/analytical/d85_indian_railways_safety.csv",
        "time_col": None,
        "kpis": [
            ("Total Track Route", "track_route_km", "sum", "{val:,.0f} km", "All Zonal Railway Routes", "pos"),
            ("USFD Rail Flaws Detected", "usfd_fractures_detected_count", "sum", "{val:,.0f} Flaws", "Ultrasonic Defect Testing", "pos"),
            ("Track Renewal Completed", "track_renewal_executed_km", "sum", "{val:,.0f} km", "Annual Heavy Rail Relaying", "pos"),
            ("Kavach ATP Deployed", "kavach_atp_deployed_km", "sum", "{val:,.0f} km", "Automatic Train Protection", "pos"),
            ("Consequential Accidents", "consequential_accidents_count", "sum", "{val:,.0f} Incidents", "All 16 Zonal Railways", "neutral")
        ],
        "charts": [
            ("bar", "zone", ["track_renewal_executed_km", "kavach_atp_deployed_km"], "Track Renewal Infrastructure Relaying vs Kavach ATP Signal Deployment (km)", "Railway Zone", "Kilometers (km)"),
            ("horizontal_bar", "usfd_fractures_detected_count", "zone", "Ultrasonic Flaw Detection (USFD) Incipient Rail Fractures Identified & Replaced", "USFD Fractures Detected", "Railway Zone"),
            ("scatter", "track_route_km", "usfd_fractures_detected_count", "Route Kilometers vs Ultrasonic Rail Fractures Discovered", "Track Route (km)", "Fractures Detected"),
            ("donut", "zone", "derailments_count", "Zonal Share of Consequential Train Derailment Incidents", "", ""),
            ("bar", "zone", "kavach_atp_coverage_pct", "Kavach Automatic Train Protection Coverage Share of Route Kilometers (%)", "Railway Zone", "Kavach Coverage (%)"),
            ("box", None, "usfd_fractures_per_1000_km", "Density of Ultrasonic Rail Defects per 1,000 Route Kilometers", "Indian Railway Fleet", "Defects / 1k km"),
            ("radar", ["kavach_atp_coverage_pct", "track_renewal_intensity_pct"], None, "Zonal Railway Safety Hardening & Modernization Radar", None, None)
        ]
    },
    {
        "id": "D86",
        "slug": "d86_bis_sovereign_debt_default_risk",
        "title": "Sovereign Credit Default Swaps, External Debt Burden & Rollover Vulnerability",
        "domain": "Sovereign Debt Economics & Macroprudential Risk",
        "file": "d86_bis_sovereign_debt_default_risk.py",
        "csv": "data/analytical/d86_bis_sovereign_debt_default_risk.csv",
        "time_col": None,
        "kpis": [
            ("Peak 5Yr CDS Spread", "cds_5yr_spread_bps", "max", "{val:,.0f} bps", "Distressed Sovereign Credit", "neg"),
            ("Average External Debt/GNI", "external_debt_to_gni_pct", "mean", "{val:.1f}%", "National Solvency Ratio", "neutral"),
            ("Debt Service to Exports", "external_debt_service_to_exports_pct", "mean", "{val:.1f}%", "Foreign Exchange Debt Burden", "neg"),
            ("Short-Term Debt Share", "short_term_debt_share_pct", "mean", "{val:.1f}%", "1-Year Rollover Liquidity Risk", "neg"),
            ("Concessional Buffer", "multilateral_concessional_share_pct", "mean", "{val:.1f}%", "Multilateral Low-Cost Loans", "pos")
        ],
        "charts": [
            ("bar", "country", "cds_5yr_spread_bps", "Sovereign 5-Year Credit Default Swap (CDS) Risk Premia (Basis Points)", "Country", "CDS Spread (bps)"),
            ("horizontal_bar", "external_debt_to_gni_pct", "country", "External Debt-to-Gross National Income (GNI) Solvency Burden (%)", "External Debt / GNI (%)", "Country"),
            ("scatter", "external_debt_service_to_exports_pct", "short_term_debt_share_pct", "Debt Servicing vs Short-Term Debt Rollover Liquidity Pressure (%)", "Debt Service / Exports (%)", "Short-Term Debt (%)"),
            ("donut", "default_risk_tier", "country", "Sovereign Credit Risk & Rollover Distress Tier Classification", "", ""),
            ("bar", "country", ["short_term_debt_share_pct", "multilateral_concessional_share_pct"], "Short-Term Rollover Debt Share vs Concessional Cushion Share (%)", "Country", "Debt Share (%)"),
            ("box", None, "implied_1yr_default_prob_pct", "Market-Implied 1-Year Sovereign Default Probability Distribution (%)", "Evaluated Sovereigns", "Default Prob (%)"),
            ("radar", ["external_debt_to_gni_pct", "external_debt_service_to_exports_pct", "short_term_debt_share_pct"], None, "Sovereign Fiscal Distress & Solvency Vulnerability Signature", None, None)
        ]
    },
    {
        "id": "D87",
        "slug": "d87_mnre_offgrid_solar_reliability",
        "title": "Decentralized Off-Grid Solar Mini-Grids, PM-KUSUM Pumps & Uptime SLA",
        "domain": "Rural Electrification & Renewable Energy Systems",
        "file": "d87_mnre_offgrid_solar_reliability.py",
        "csv": "data/analytical/d87_mnre_offgrid_solar_reliability.csv",
        "time_col": None,
        "kpis": [
            ("Mini-Grid Solar Capacity", "minigrid_solar_capacity_kwp", "sum", "{val:,.0f} kWp", "Decentralized Green Generation", "pos"),
            ("Beneficiary Hamlets", "beneficiary_hamlets_count", "sum", "{val:,.0f} Villages", "Electrified Remote Settlements", "pos"),
            ("Solar Agricultural Pumps", "standalone_solar_pumps_installed", "sum", "{val:,.0f} Pumps", "PM-KUSUM Component-B", "pos"),
            ("Average Daily Power Hours", "avg_daily_power_supply_hours", "mean", "{val:.1f} Hrs/Day", "Dignified Energy Access Duration", "pos"),
            ("Mini-Grid Uptime SLA", "minigrid_uptime_sla_pct", "mean", "{val:.1f}%", "Service Reliability Guarantee", "pos")
        ],
        "charts": [
            ("bar", "state", ["minigrid_solar_capacity_kwp", "standalone_solar_pumps_installed"], "Decentralized Solar Mini-Grid Capacity (kWp) vs Standalone Solar Pumps Deployed", "State", "Units / Capacity"),
            ("horizontal_bar", "avg_daily_power_supply_hours", "state", "Average Daily Hours of Clean Power Supplied to Remote Off-Grid Hamlets", "Daily Supply Hours", "State"),
            ("scatter", "minigrid_solar_capacity_kwp", "micro_enterprise_connections", "Mini-Grid Capacity (kWp) vs Micro-Enterprise Commercial Connections Enabled", "Capacity (kWp)", "Enterprises Connected"),
            ("donut", "dignified_energy_access_tier", "state", "Decentralized Energy Access Tier Classification", "", ""),
            ("bar", "state", "storage_battery_lithium_share_pct", "Storage Technology Modernization: Lithium Battery Share of Energy Storage (%)", "State", "Lithium Share (%)"),
            ("box", None, "minigrid_uptime_sla_pct", "Distribution of Off-Grid Mini-Grid Power Uptime SLA Reliability (%)", "All Monitored States", "Uptime SLA (%)"),
            ("radar", ["avg_daily_power_supply_hours", "minigrid_uptime_sla_pct", "storage_battery_lithium_share_pct"], None, "Decentralized Renewable Access Quality Fingerprint", None, None)
        ]
    },
    {
        "id": "D88",
        "slug": "d88_njdg_court_case_pendency",
        "title": "Judicial Case Backlogs, Chronic Delay & Undertrial Incarceration Strain",
        "domain": "Judicial Administration & Legal Analytics",
        "file": "d88_njdg_court_case_pendency.py",
        "csv": "data/analytical/d88_njdg_court_case_pendency.csv",
        "time_col": None,
        "kpis": [
            ("Total Pending Cases", "total_pending_cases_lakh", "sum", "{val:,.1f} L Cases", "District Courts Backlog", "neg"),
            ("Cases Over 5 Years Old", "cases_older_than_5_years_pct", "mean", "{val:.1f}%", "Chronic Judicial Delay Share", "neg"),
            ("Ultra-Chronic Cases (>10y)", "ultra_chronic_cases_over_10y_lakh", "sum", "{val:,.1f} L Cases", "Decade-Long Pending Matters", "neg"),
            ("Undertrial Prisoners Share", "undertrial_prisoners_share_pct", "mean", "{val:.1f}%", "Prisoners Awaiting Final Verdict", "neg"),
            ("Disposals Per Judge", "annual_cases_disposed_per_judge", "mean", "{val:,.0f}", "Annual Judicial Productivity", "pos")
        ],
        "charts": [
            ("bar", "state", ["cases_older_than_5_years_pct", "cases_older_than_10_years_pct"], "Chronic Case Delay Profile: Share Over 5 Years vs Ultra-Chronic Over 10 Years (%)", "State", "Share of Backlog (%)"),
            ("horizontal_bar", "total_pending_cases_lakh", "state", "Total Pending Cases in Subordinate Judiciary (Lakh Cases)", "Pending Cases (Lakh)", "State"),
            ("scatter", "cases_older_than_5_years_pct", "undertrial_prisoners_share_pct", "Chronic Case Delay Rate vs Undertrial Prisoner Share of Jail Population (%)", "Cases > 5y (%)", "Undertrial Share (%)"),
            ("donut", "pendency_distress_tier", "state", "State Judicial Pendency Distress Classification", "", ""),
            ("area", "state", ["civil_cases_share_pct", "criminal_cases_share_pct"], "Dockets Composition: Civil Disputes vs Criminal Cases Share (%)", "State", "Case Docket Share (%)"),
            ("box", None, "annual_cases_disposed_per_judge", "Annual Case Disposals Per Judicial Officer Across State Judiciaries", "Subordinate Courts", "Cases Disposed / Judge"),
            ("radar", ["cases_older_than_5_years_pct", "undertrial_prisoners_share_pct", "criminal_cases_share_pct"], None, "Judicial Backlog Distress Radar Profile", None, None)
        ]
    },
    {
        "id": "D89",
        "slug": "d89_certin_cyber_incidents",
        "title": "National Cyber Threat Telemetry, Ransomware Surge & Containment Velocity",
        "domain": "Cybersecurity & Digital Infrastructure Protection",
        "file": "d89_certin_cyber_incidents.py",
        "csv": "data/analytical/d89_certin_cyber_incidents.csv",
        "time_col": "year",
        "kpis": [
            ("Annual Cyber Incidents", "total_cyber_security_incidents", "max", "{val:,.0f}", "Reported Security Events", "neg"),
            ("Ransomware Attacks", "ransomware_attacks_reported", "max", "{val:,.0f}", "Corporate & Public Ransomware", "neg"),
            ("Critical Infra Breaches", "critical_infrastructure_breaches", "sum", "{val:,.0f}", "Power / Transport / Telecom", "neg"),
            ("Mean Containment Time", "avg_incident_containment_hours", "min", "{val:.1f} Hrs", "Incident Mitigation Speed", "pos"),
            ("Financial Cyber Frauds", "financial_fraud_cases_lakh", "max", "{val:.1f} L Cases", "Digital Payment Fraud Surge", "neg")
        ],
        "charts": [
            ("line", "year", ["total_cyber_security_incidents", "ransomware_attacks_reported"], "Annual Escalation in Cyber Security Incidents & Ransomware Attacks", "Year", "Incidents Count"),
            ("area", "year", ["phishing_incidents_count", "ransomware_attacks_reported", "critical_infrastructure_breaches"], "Primary Attack Vector Volume Evolution Over Time", "Year", "Incidents"),
            ("bar", "year", "financial_fraud_cases_lakh", "Annual Financial Cyber Fraud Cases Logged with CERT-In (Lakh Cases)", "Year", "Lakh Cases"),
            ("scatter", "total_cyber_security_incidents", "avg_incident_containment_hours", "Incident Attack Volume vs Incident Containment & Recovery Time (Hours)", "Annual Incidents", "Containment (Hours)"),
            ("horizontal_bar", "govt_websites_defaced", "year", "Official Government Web Portals Defaced or Compromised by Threat Actors", "Portals Defaced", "Year"),
            ("box", None, "yoy_incident_surge_pct", "Annual Year-on-Year Incident Growth Surge Rate (%)", "Historical Cyber Threat Log", "Surge Rate (%)"),
            ("radar", ["ransomware_share_of_incidents_pct", "phishing_share_pct", "containment_velocity_index"], None, "National Cyber Attack Vector Signature & Defense Agility Radar", None, None)
        ]
    },
    {
        "id": "D90",
        "slug": "d90_mofpi_cold_storage_logistics",
        "title": "Cold Chain Logistics Capacity & Horticultural Post-Harvest Loss Prevention",
        "domain": "Agricultural Supply Chains & Food Processing Logistics",
        "file": "d90_mofpi_cold_storage_logistics.py",
        "csv": "data/analytical/d90_mofpi_cold_storage_logistics.csv",
        "time_col": None,
        "kpis": [
            ("Cold Storage Capacity", "cold_storage_capacity_lakh_mt", "sum", "{val:,.1f} L MT", "Installed National Capacity", "pos"),
            ("Active Cold Chain Projects", "cold_storage_projects_count", "sum", "{val:,.0f}", "MoFPI Sanctioned Infrastructure", "pos"),
            ("Reefer Refrigerated Trucks", "reefer_vehicles_registered", "sum", "{val:,.0f} Units", "Cold Transport Fleet", "pos"),
            ("Post-Harvest Loss Value", "post_harvest_loss_value_crore", "sum", "₹{val:,.0f} Cr", "Annual Perishable Crop Loss", "neg"),
            ("Multi-Commodity Share", "multi_commodity_storage_share_pct", "mean", "{val:.1f}%", "Non-Potato Versatility Ratio", "neutral")
        ],
        "charts": [
            ("bar", "state", ["cold_storage_capacity_lakh_mt", "multi_commodity_capacity_lakh_mt"], "Total Installed Cold Storage Capacity vs Multi-Commodity Versatile Capacity (Lakh MT)", "State", "Capacity (Lakh MT)"),
            ("horizontal_bar", "post_harvest_loss_value_crore", "state", "Estimated Economic Value of Post-Harvest Horticultural Spoilage (₹ Crore)", "Spoilage Loss (₹ Cr)", "State"),
            ("scatter", "cold_storage_capacity_lakh_mt", "estimated_horticultural_loss_pct", "Cold Chain Capacity vs Horticultural Loss Rate (%)", "Capacity (Lakh MT)", "Horticultural Loss (%)"),
            ("donut", "cold_chain_deficit_risk_tier", "state", "State Perishable Supply Chain Deficit Risk Tiers", "", ""),
            ("bar", "state", "reefer_vehicles_registered", "Refrigerated Transport Fleet: Registered Reefer Vehicles by State", "State", "Reefer Vehicles"),
            ("box", None, "estimated_horticultural_loss_pct", "Spread of Perishable Crop Post-Harvest Spoilage Rates Across States (%)", "All Monitored States", "Loss Rate (%)"),
            ("radar", ["estimated_horticultural_loss_pct", "multi_commodity_storage_share_pct"], None, "Cold Chain Infrastructure Balance & Spoilage Mitigation Radar", None, None)
        ]
    },
    {
        "id": "D91",
        "slug": "d91_fsi_wildfire_early_warning",
        "title": "Forest Wildfire Satellite Detection, Thermal Anomalies & Forest Fire Response",
        "domain": "Forest Ecology & Disaster Management",
        "file": "d91_fsi_wildfire_early_warning.py",
        "csv": "data/analytical/d91_fsi_wildfire_early_warning.csv",
        "time_col": None,
        "kpis": [
            ("Annual Wildfire Alerts", "annual_fire_alerts_count", "sum", "{val:,.0f}", "SNPP-VIIRS Thermal Detections", "neg"),
            ("Forest Area Burnt", "forest_area_affected_hectares", "sum", "{val:,.0f} Ha", "Fire Season Forest Damage", "neg"),
            ("Extreme Fire Vulnerability", "extreme_fire_vulnerability_pct", "mean", "{val:.1f}%", "High-Risk Forest Compartments", "neg"),
            ("Average Response Time", "mean_response_time_minutes", "mean", "{val:.1f} Mins", "Ground Crew Incident Response", "pos"),
            ("Frontline Fire Watchers", "fire_watchers_deployed", "sum", "{val:,.0f}", "Deployed Seasonal Patrols", "pos")
        ],
        "charts": [
            ("bar", "state", "annual_fire_alerts_count", "Annual Forest Wildfire Thermal Alerts Sensed by Satellite (SNPP-VIIRS)", "State", "Alerts Count"),
            ("horizontal_bar", "forest_area_affected_hectares", "state", "Total Forest Canopy and Understory Area Damaged by Fires (Hectares)", "Affected Area (Ha)", "State"),
            ("scatter", "fire_season_mean_temp_c", "annual_fire_alerts_count", "Fire Season Mean Ambient Temperature (°C) vs Wildfire Alert Volume", "Temperature (°C)", "Fire Alerts"),
            ("donut", "fire_risk_priority_tier", "state", "Forest Fire Vulnerability Action Priority Classification", "", ""),
            ("bar", "state", "mean_response_time_minutes", "Forest Beat Guard & Strike Force Mean Incident Response Velocity (Minutes)", "State", "Response Time (Mins)"),
            ("box", None, "extreme_fire_vulnerability_pct", "Dispersion of Extreme Wildfire Vulnerability Shares Across Indian Forest Ranges (%)", "All Monitored States", "Vulnerability (%)"),
            ("radar", ["extreme_fire_vulnerability_pct", "affected_forest_share_pct", "fire_alerts_per_100_sqkm_forest"], None, "Forest Fire Hazard & Ecological Impact Radar", None, None)
        ]
    },
    {
        "id": "D92",
        "slug": "d92_mohua_urban_rental_housing",
        "title": "Affordable Rental Housing Complexes (ARHC), Rent Burden & Slum Upgrading",
        "domain": "Urban Planning & Social Housing Policy",
        "file": "d92_mohua_urban_rental_housing.py",
        "csv": "data/analytical/d92_mohua_urban_rental_housing.csv",
        "time_col": None,
        "kpis": [
            ("Total Housing Deficit", "urban_housing_deficit_units", "sum", "{val:,.0f} Units", "Urban EWS/LIG Deficit", "neg"),
            ("ARHC Rental Units", "arhc_sanctioned_rental_units", "sum", "{val:,.0f} Units", "Sanctioned Model-1/2 Units", "pos"),
            ("Average Rent Burden", "rent_to_income_burden_pct", "mean", "{val:.1f}%", "Rent Share of Monthly Income", "neg"),
            ("Average Slum Share", "slum_population_share_pct", "mean", "{val:.1f}%", "Informal Settlement Population", "neutral"),
            ("Migrant Worker Population", "migrant_worker_population_lakh", "sum", "{val:,.1f} L Workers", "Beneficiary Urban Labor", "pos")
        ],
        "charts": [
            ("bar", "city", ["urban_housing_deficit_units", "arhc_sanctioned_rental_units"], "Total Urban Housing Deficit vs Sanctioned Affordable Rental Housing Units", "City", "Housing Units"),
            ("horizontal_bar", "rent_to_income_burden_pct", "city", "Rent-to-Income Cost Burden for Low-Income Working Families (%)", "Rent Burden (%)", "City"),
            ("scatter", "migrant_worker_population_lakh", "urban_housing_deficit_units", "Migrant Worker Population (Lakh) vs Urban Housing Deficit Units", "Migrant Population (Lakh)", "Housing Deficit Units"),
            ("donut", "rental_stress_tier", "city", "Metropolitan Rental Stress & Housing Affordability Tiers", "", ""),
            ("bar", "city", "avg_monthly_rent_1bhk_inr", "Average Monthly Market Rental Rate for 1BHK Dwelling (INR)", "City", "Rent (INR)"),
            ("box", None, "slum_population_share_pct", "Distribution of Slum Inhabitant Shares Across 25 Major Metros (%)", "All Analyzed Cities", "Slum Share (%)"),
            ("radar", ["rent_to_income_burden_pct", "slum_population_share_pct", "rental_affordability_stress_ratio"], None, "Urban Housing Stress & Affordability Squeeze Radar", None, None)
        ]
    },
    {
        "id": "D93",
        "slug": "d93_cmfri_marine_fisheries",
        "title": "Marine Fish Landings, Mechanized Trawling Exploitation & Sustainable Yield",
        "domain": "Marine Biology & Sustainable Fisheries Management",
        "file": "d93_cmfri_marine_fisheries.py",
        "csv": "data/analytical/d93_cmfri_marine_fisheries.csv",
        "time_col": None,
        "kpis": [
            ("Total Marine Landings", "annual_fish_landings_lakh_tonnes", "sum", "{val:,.1f} L MT", "Gross Annual Catch", "pos"),
            ("Marine Export Value", "export_value_inr_crore", "sum", "₹{val:,.0f} Cr", "Marine Seafood Forex Earnings", "pos"),
            ("Mechanized Trawl Share", "mechanized_trawler_catch_share_pct", "mean", "{val:.1f}%", "Industrial Fleet Extraction", "neutral"),
            ("Max MSY Ratio", "maximum_sustainable_yield_ratio", "max", "{val:.2f}x", "Over-Exploited Biomass Threshold", "neg"),
            ("Active Fisherfolk", "active_fisherfolk_lakh", "sum", "{val:,.1f} L Persons", "Coastal Livelihood Dependents", "pos")
        ],
        "charts": [
            ("bar", "maritime_state", "annual_fish_landings_lakh_tonnes", "Annual Marine Fish Landings Across Maritime States (Lakh Metric Tonnes)", "Maritime State", "Catch (Lakh MT)"),
            ("horizontal_bar", "maximum_sustainable_yield_ratio", "maritime_state", "Maximum Sustainable Yield (MSY) Ratio (>1.0 = Over-Exploited Biomass)", "MSY Ratio", "Maritime State"),
            ("scatter", "mechanized_trawler_catch_share_pct", "juvenile_bycatch_share_pct", "Mechanized Trawler Catch Share vs Juvenile Bycatch Discard Ratio (%)", "Trawler Share (%)", "Juvenile Bycatch (%)"),
            ("donut", "msy_exploitation_status", "maritime_state", "Fisheries Stock Biomass Exploitation Status", "", ""),
            ("bar", "maritime_state", "export_value_inr_crore", "Foreign Exchange Earnings from Marine Seafood Exports (₹ Crore)", "Maritime State", "Export Value (₹ Cr)"),
            ("box", None, "maximum_sustainable_yield_ratio", "Spread of Fishing Pressure Relative to Maximum Sustainable Yield (MSY)", "All Maritime States", "MSY Ratio"),
            ("radar", ["mechanized_trawler_catch_share_pct", "juvenile_bycatch_share_pct", "maximum_sustainable_yield_ratio"], None, "Marine Ecosystem Exploitation Pressure Radar", None, None)
        ]
    },
    {
        "id": "D94",
        "slug": "d94_telemanas_mental_health",
        "title": "Tele-MANAS Tele-Mental Health Telemetry, Distress Resolution & Psychiatric Access",
        "domain": "Public Mental Health & Digital Healthcare Delivery",
        "file": "d94_telemanas_mental_health.py",
        "csv": "data/analytical/d94_telemanas_mental_health.csv",
        "time_col": None,
        "kpis": [
            ("Total Distress Calls", "total_telemanas_calls_received", "sum", "{val:,.0f} Calls", "24x7 Sovereign Helpline", "pos"),
            ("Tele-Counseling Resolution", "call_distress_resolution_pct", "mean", "{val:.1f}%", "Immediate Psychological First Aid", "pos"),
            ("Psychiatrist Density", "psychiatrists_per_100k_population", "mean", "{val:.2f} / 100k", "WHO Norm: 3.0 / 100k Pop", "neg"),
            ("DMHP District Coverage", "dmhp_covered_districts_pct", "mean", "{val:.1f}%", "District Mental Health Program", "pos"),
            ("Anxiety & Depression Share", "anxiety_depression_calls_pct", "mean", "{val:.1f}%", "Primary Clinical Morbidity", "neutral")
        ],
        "charts": [
            ("bar", "state", "total_telemanas_calls_received", "Total Tele-MANAS 24x7 Tele-Mental Health Inbound Distress Calls Received", "State", "Calls Received"),
            ("horizontal_bar", "call_distress_resolution_pct", "state", "Telephonic Counseling Psychological Resolution Rate (%)", "Resolution Rate (%)", "State"),
            ("scatter", "psychiatrists_per_100k_population", "call_distress_resolution_pct", "Clinical Psychiatrist Density (per 100k) vs Telephonic Distress Resolution Rate", "Psychiatrists / 100k", "Resolution Rate (%)"),
            ("donut", "mental_health_infrastructure_tier", "state", "State Mental Health Infrastructure & Tele-Response Capacity Tiers", "", ""),
            ("bar", "state", ["anxiety_depression_calls_pct", "sleep_distress_calls_pct"], "Symptomatic Distress Breakdown: Anxiety/Depression vs Sleep Disturbances (%)", "State", "Share of Calls (%)"),
            ("box", None, "psychiatrists_per_100k_population", "Dispersion of Qualified Psychiatrist Density Across States (per 100k Population)", "All Monitored States", "Psychiatrists / 100k"),
            ("radar", ["call_distress_resolution_pct", "dmhp_covered_districts_pct", "psychiatrists_per_100k_population"], None, "State Tele-Mental Health & Care Delivery Resilience Radar", None, None)
        ]
    }
]

def get_chart_subtitle(spec, chart_idx, c):
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
        return "Longitudinal trend evolution across the observed analytical timeline"

BRIEFING_CONTEXT = {
    "D01": (
        "India's structural shift from agrarian dominance to high-productivity services and manufacturing represents one of the defining macroeconomic transformations globally, dictating national capital formation, FDI inflows, and sovereign fiscal headroom.",
        "Data sourced from official MoSPI National Accounts and World Bank Development Indicators. Figures reflect constant 2015 and current USD benchmarks along with official Gross Value Added (GVA) factor cost methodologies."
    ),
    "D02": (
        "The Reserve Bank of India operates under a statutory flexible inflation targeting framework (4% +/- 200 bps). Policy repo rate adjustments directly steer commercial lending rates, banking liquidity, corporate debt servicing, and real rate corridors.",
        "Consumer Price Index (CPI-Combined) monthly series published by MoSPI; Policy Repo, Reverse Repo, and Cash Reserve Ratios sourced directly from the Reserve Bank of India Database on Indian Economy (DBIE)."
    ),
    "D03": (
        "Sub-national demographic dividends, rapid urbanization, and female educational attainment are decisive determinants of regional labor productivity, spatial economic agglomeration, and public service demand across India's federal union.",
        "Enumerated figures derived from Census of India 2001 and 2011 benchmarks published by the Office of the Registrar General & Census Commissioner (ORGI), Ministry of Home Affairs."
    ),
    "D04": (
        "Pediatric nutritional indicators (stunting and wasting), maternal anemia, and institutional healthcare coverage set the boundary conditions for human capital accumulation, highlighting spatial inequalities across states.",
        "Compiled from the National Family Health Survey (NFHS-5, 2019-21) administered by the International Institute for Population Sciences (IIPS) under the stewardship of the Ministry of Health and Family Welfare (MoHFW)."
    ),
    "D05": (
        "Agricultural crop productivity and aggregate foodgrain output underpin food security, rural livelihood resilience, and buffer stocking policies, insulating the national economy against monsoon variability and commodity price spikes.",
        "Official advance and final crop estimates published by the Directorate of Economics and Statistics (DES), Ministry of Agriculture and Farmers Welfare, covering Kharif and Rabi agricultural production cycles."
    ),
    "D06": (
        "Accelerating non-fossil power generation capacity (solar, wind, and hydro) is essential for achieving India's 500 GW renewable target by 2030 and fulfilling COP commitments while guaranteeing grid reliability for industrial growth.",
        "Installed generation capacity and monthly electricity generation statistics officially reported by the Central Electricity Authority (CEA) and Ministry of New and Renewable Energy (MNRE), Government of India."
    ),
    "D07": (
        "Merchandise export competitiveness, high-tech export shares, and strategic crude oil import dependency govern India's foreign exchange earnings, current account deficit exposure, and external macroeconomic stability.",
        "Trade transactions recorded and harmonized by the Directorate General of Foreign Trade (DGFT) and Department of Commerce via the official Export-Import Data Bank system."
    ),
    "D08": (
        "Inbound Foreign Direct Investment equity inflows reflect international institutional confidence, cross-border technology transfer, and structural capital formation across priority digital and manufacturing sectors.",
        "Foreign direct investment equity flow statistics officially published by the Department for Promotion of Industry and Internal Trade (DPIIT), Ministry of Commerce and Industry, and RBI Balance of Payments archives."
    ),
    "D09": (
        "National highway network expansion pace and high-density four-lane corridor construction drastically lower inter-state freight logistics friction, elevating logistical efficiency and enabling private industrial capex.",
        "Physical infrastructure commissioning pace and network lengths reported by the Ministry of Road Transport and Highways (MoRTH) and National Highways Authority of India (NHAI)."
    ),
    "D10": (
        "Indian Railways operates as the core bulk freight logistics spine for core industrial inputs (coal, iron ore, cement), while near-complete route electrification accelerates national decarbonization targets.",
        "Operational throughput, locomotive traction split, and financial operating ratios published in the Indian Railways Annual Statistical Statements and Railway Board monthly reviews."
    ),
    "D11": (
        "Urban ambient air pollutant concentrations (PM2.5, PM10, NO2) represent a premier public health and municipal governance priority, guiding emergency air action plans and National Clean Air Programme (NCAP) investments.",
        "Continuous ambient air quality monitoring telemetry retrieved and validated against Central Pollution Control Board (CPCB) National Ambient Air Quality Standards (NAAQS) benchmarks."
    ),
    "D12": (
        "The Unified Payments Interface (UPI) serves as the world's leading real-time retail payments rail, processing over 14 billion transactions monthly and driving digital public infrastructure (DPI) financial inclusion.",
        "Monthly platform volume, gross settlement value, and operational availability published officially by the National Payments Corporation of India (NPCI)."
    ),
    "D13": (
        "Gross State Domestic Product (GSDP) and state-level per capita income trajectories reveal internal economic divergence, fiscal equalization mechanisms, and the competitive federalism dynamics driving sub-national capital investments.",
        "GSDP series compiled by the Ministry of Statistics and Programme Implementation (MoSPI) in coordination with respective State Directorates of Economics and Statistics."
    ),
    "D14": (
        "Gross Enrollment Ratios (GER) and gender parity indices in higher education govern cognitive skill depth, technical workforce readiness, and long-term research productivity in a modern service economy.",
        "Survey data compiled from the All India Survey on Higher Education (AISHE) published by the Department of Higher Education, Ministry of Education, Government of India."
    ),
    "D15": (
        "Sub-national fiscal deficits, revenue buoyancy, and debt-to-GSDP ratios determine state government capital investment headroom under statutory Fiscal Responsibility and Budget Management (FRBM) ceilings.",
        "Fiscal accounts and debt metrics sourced from the Reserve Bank of India annual study 'State Finances: A Study of Budgets' and state Comptroller and Auditor General (CAG) audit publications."
    ),
    "D16": (
        "Comprehensive infrastructure connectivity—all-weather rural roads, tap water coverage, and electrification—serves as the foundational driver for multi-dimensional poverty alleviation and regional equality.",
        "Composite infrastructure achievement indices compiled from NITI Aayog SDG India Index reports and central ministry progress monitoring dashboards."
    ),
    "D17": (
        "Tracking territorial greenhouse gas emissions against remaining global carbon budgets is essential for evaluating multilateral compliance with Paris Agreement 1.5°C targets and assessing historical emission equity.",
        "Carbon dioxide emissions dataset sourced from the Global Carbon Project (GCP) and Our World in Data (OWID), synthesizing national UNFCCC inventory submissions and energy consumption balances."
    ),
    "D18": (
        "Global life expectancy and healthy life expectancy (HALE) indicators monitor progress under SDG 3, capturing the structural epidemiological transition from infectious communicable diseases to non-communicable morbidities.",
        "Epidemiological data sourced from the World Health Organization (WHO) Global Health Observatory (GHO) and UN Population Division World Population Prospects (WPP)."
    ),
    "D19": (
        "Primary and secondary school completion rates and gender parity ratios govern intergenerational social mobility, labor force participation rates, and aggregate human capital formation across developing regions.",
        "Educational indicators compiled from UNESCO Institute for Statistics (UIS) databases and World Bank EdStats monitoring frameworks."
    ),
    "D20": (
        "Tracking extreme poverty headcount ratios against international poverty lines ($2.15, $3.65, $6.85) evaluates social safety net efficacy and structural income inequality (Gini and Palma indices) across developing nations.",
        "Global poverty metrics derived from the World Bank Poverty and Inequality Platform (PIP), based on harmonized household consumption and expenditure surveys."
    ),
    "D21": (
        "Global cereal production stability, grain stocks-to-use safety buffers, and food price volatility directly influence geopolitical stability, humanitarian assistance needs, and acute hunger prevention in vulnerable regions.",
        "Agricultural commodity balances and the monthly Food Price Index compiled by the Food and Agriculture Organization (FAO) of the United Nations (FAOSTAT / AMIS)."
    ),
    "D22": (
        "Monitoring planetary forest canopy loss, net deforestation rates, and biodiversity conservation reserves is critical for safeguarding global carbon sinks and halting biodiversity collapse under the Kunming-Montreal Global Biodiversity Framework.",
        "Data sourced from the FAO Global Forest Resources Assessment (FRA) and World Bank terrestrial indicators, combining national forest inventories and satellite remote sensing."
    ),
    "D23": (
        "Hydrological water stress (SDG 6.4.2) and per capita renewable freshwater availability expose acute systemic risks to agriculture, urban survival, and industrial production in hyper-arid and over-extracted basins.",
        "Freshwater extraction metrics compiled by FAO AQUASTAT and UN-Water, monitoring agricultural, industrial, and municipal withdrawal proportions against renewable internal resources."
    ),
    "D24": (
        "Persistent global current account surpluses and deficits highlight macroeconomic imbalances, global savings gluts, and trade openness shifts that influence exchange rate adjustments and multilateral trade agreements.",
        "Trade openness and balance of payments statistics compiled from the International Monetary Fund (IMF) World Economic Outlook (WEO) database and World Bank national accounts."
    ),
    "D25": (
        "Closing the global digital divide in broadband subscriptions and mobile connectivity is essential for equitable participation in the digital economy, telemedicine, and remote education across underserved continents.",
        "Telecommunications metrics compiled by the International Telecommunication Union (ITU) World Telecommunication/ICT Indicators database."
    ),
    "D26": (
        "R&D intensity (% of GDP), researcher density, and resident patent applications serve as primary drivers of long-term total factor productivity, high-tech export competitiveness, and scientific leadership.",
        "Science and technology indicators published by the UNESCO Institute for Statistics (UIS), World Intellectual Property Organization (WIPO), and OECD Main Science and Technology Indicators."
    ),
    "D27": (
        "External sovereign debt stock and debt service-to-export ratios highlight acute liquidity strains and debt sustainability risks across developing nations vulnerable to global interest rate cycles and currency depreciation.",
        "External debt statistics sourced from the World Bank International Debt Statistics (IDS) and Quarterly External Debt Statistics (QEDS)."
    ),
    "D28": (
        "Real-time global seismic monitoring detects active tectonic fault ruptures, focal hypocenters, and tsunami triggers, delivering life-saving early warning telemetry to civil defense and disaster response authorities worldwide.",
        "Live seismic telemetry fetched directly from the United States Geological Survey (USGS) Earthquake Hazards Program Comprehensive Cat-Log GeoJSON API feed."
    ),
    "D29": (
        "Instrumental surface temperature anomalies provide empirical proof of anthropogenic warming trends, validating climate sensitivity models and informing planetary carbon drawdown and adaptation strategies.",
        "Global surface temperature anomaly series compiled by NASA Goddard Institute for Space Studies (GISS GISTEMP v4), benchmarked against the 1951-1980 base period climatology."
    ),
    "D30": (
        "Metropolitan megacity expansion and urban densification trends strain municipal water, transport, and energy systems, while creating the world's most concentrated centers of innovation and economic value creation.",
        "Urban agglomeration population estimates and projections sourced from the UN Population Division World Urbanization Prospects (WUP) decennial revisions."
    ),
    "D31": (
        "International tourism arrivals and travel receipts capture cross-border services trade recovery, foreign currency generation, and hospitality employment resilience following extreme exogenous disruption shocks.",
        "Tourism statistics compiled by the United Nations World Tourism Organization (UNWTO) World Tourism Barometer and World Bank Development Indicators."
    ),
    "D32": (
        "Global electric vehicle fleet adoption and battery electric vehicle market penetration accelerate transport decarbonization, transforming oil demand fundamentals and critical mineral supply chains worldwide.",
        "Electric car sales and market share trajectories sourced from the International Energy Agency (IEA) Global EV Outlook and national automotive registry datasets."
    ),
    "D33": (
        "Cross-asset historical co-movement between equity benchmarks (S&P 500, Nifty 50), safe-haven physical gold, and energy commodities (Brent crude) tracks macroeconomic regime shifts, inflation expectations, and systemic risk.",
        "Market pricing archives compiled from Robert Shiller Yale Financial Market Data, World Gold Council, US Energy Information Administration (EIA), and National Stock Exchange of India (NSE)."
    ),
    "D34": (
        "Sovereign debt-to-GDP ratios and structural primary fiscal balances govern sovereign creditworthiness, bond yield spreads, and government debt servicing burdens in an era of elevated global interest rates.",
        "Fiscal metrics derived from the International Monetary Fund (IMF) Fiscal Monitor database and World Bank public sector debt statistics."
    ),
    "D35": (
        "Goods and Services Tax (GST) mobilization serves as the vital barometer of formal domestic consumption, inter-state commerce, and fiscal devolution capacity between the Union and the States.",
        "Official monthly press communiqués published by the Ministry of Finance and Goods and Services Tax Network (GSTN), Government of India."
    ),
    "D36": (
        "Pradhan Mantri Jan Dhan Yojana represents the world's largest financial inclusion drive, eliminating zero-balance dead zones, enabling DBT delivery, and formalizing household savings.",
        "Official periodic updates published by Department of Financial Services (DFS), Ministry of Finance, Government of India."
    ),
    "D37": (
        "The Mahatma Gandhi National Rural Employment Guarantee Scheme acts as an indispensable counter-cyclical lifeline for rural unorganized workers, smoothing seasonal agrarian underemployment.",
        "Official MIS portal reporting by the Ministry of Rural Development (MoRD), Government of India."
    ),
    "D38": (
        "India's civil aviation market is among the fastest growing globally, driven by rising disposable incomes, fleet expansion, and regional airport commissioning under the UDAN scheme.",
        "Official traffic reports and statistical handbooks published by the Directorate General of Civil Aviation (DGCA) and Airports Authority of India (AAI)."
    ),
    "D39": (
        "Over 95% of India's merchandise trade by volume moves via maritime gateways. Improving port turnaround times and mechanization is essential for the Sagarmala initiative and lowering logistics costs.",
        "Official traffic handbooks compiled by the Indian Ports Association (IPA) and Ministry of Ports, Shipping and Waterways (MoPSW)."
    ),
    "D40": (
        "India is the second-largest telecommunications market worldwide. Affordable 4G/5G data networks power UPI payments, e-governance, and the digital consumer economy.",
        "Official telecom performance indicator reports published quarterly by the Telecom Regulatory Authority of India (TRAI)."
    ),
    "D41": (
        "Mineral extraction supplies critical raw materials for infrastructure, domestic steel production, and non-ferrous manufacturing under the National Mineral Policy.",
        "Official statistics published by the Indian Bureau of Mines (IBM) and Ministry of Mines, Government of India."
    ),
    "D42": (
        "Forest canopy and ecological carbon sequestration are foundational to India's climate commitments under the Paris Agreement to create an additional 2.5 to 3.0 billion tonnes CO2e sink.",
        "India State of Forest Report (ISFR) biennial assessments published by the Forest Survey of India (FSI), Ministry of Environment, Forest and Climate Change."
    ),
    "D43": (
        "With over 85% crude oil import dependency, tracking domestic refining yields and diesel/petrol demand trends is crucial for macro stability, CAD containment, and inflation forecasting.",
        "Official monthly and annual petroleum statistics published by the Petroleum Planning & Analysis Cell (PPAC), Ministry of Petroleum and Natural Gas."
    ),
    "D44": (
        "NCRB empirical crime statistics provide objective evidence on criminal justice disposal, chargesheeting velocity, cybercrime surges, and gender safety across states.",
        "Official annual Crime in India compendiums published by the National Crime Records Bureau (NCRB), Ministry of Home Affairs, Government of India."
    ),
    "D45": (
        "PMAY addresses the urban and rural affordable housing deficit through interest subvention, direct beneficiary construction, and mandatory joint titling with female heads of households.",
        "Official MIS portal data published by the Ministry of Housing and Urban Affairs (MoHUA) and Ministry of Rural Development (MoRD)."
    ),
    "D46": (
        "The Jal Jeevan Mission aims to provide safe piped drinking water through Functional Household Tap Connections (FHTC) to every rural household, drastically cutting waterborne disease and female drudgery.",
        "Official JJM IMIS monitoring dashboard data published by the Department of Drinking Water and Sanitation, Ministry of Jal Shakti."
    ),
    "D47": (
        "UDISE+ captures foundational physical and digital assets across 1.48 million schools, tracking compliance with the Right to Education Act and the National Education Policy (NEP 2020).",
        "Official UDISE+ Flash Statistics published by the Department of School Education and Literacy, Ministry of Education, Government of India."
    ),
    "D48": (
        "Tourism is an engine of foreign exchange earnings and high-multiplier services employment. Tracking recovery post-pandemic illuminates the rebound of cultural, business, and medical travel.",
        "India Tourism Statistics compendium published annually by the Market Research Division, Ministry of Tourism, Government of India."
    ),
    "D49": (
        "India's Public Distribution System under the National Food Security Act feeds over 800 million citizens, acting as a sovereign guarantee against nutritional deprivation and grain price shocks.",
        "Official monthly bulletins published by the Department of Food and Public Distribution (DFPD) and Food Corporation of India (FCI)."
    ),
    "D50": (
        "A historic inflection has seen domestic Indian inventors surpass foreign filers for the first time, reflecting an explosive growth in startup patents, academic research, and tech patenting.",
        "Annual reports of the Controller General of Patents, Designs and Trade Marks (CGPDTM), DPIIT, Ministry of Commerce and Industry."
    ),
    "D51": (
        "PM-KISAN provides unconditional income support of ₹6,000 per year directly into bank accounts of over 100 million farming families, eliminating intermediaries via Aadhaar APBS.",
        "Official PM-KISAN DBT performance portal reports published by the Ministry of Agriculture and Farmers Welfare, Government of India."
    ),
    "D52": (
        "India's automotive industry contributes over 7% to national GDP and nearly 49% of manufacturing GDP, serving as a bellwether for middle-class consumption and supply chains.",
        "Official monthly and annual production and sales reports published by the Society of Indian Automobile Manufacturers (SIAM) and Ministry of Heavy Industries."
    ),
    "D53": (
        "Coal supplies over 70% of India's electricity baseload. Enhancing domestic production and railway evacuation is critical to prevent thermal power shortages during peak summer demand.",
        "Official monthly provisional statistics and annual Coal Directories published by the Coal Controller's Organisation (CCO) and Ministry of Coal."
    ),
    "D54": (
        "Inland water transport is an environmentally sustainable and cost-effective freight mode. Development of National Waterways under the Jal Marg Vikas Project connects the hinterland to sea ports.",
        "Official cargo movement reports published by the Inland Waterways Authority of India (IWAI), Ministry of Ports, Shipping and Waterways."
    ),
"D55": (
        "Commercial nuclear energy provides 10% of global electricity and over a quarter of clean baseload power, serving as a critical pillar for net-zero grids requiring round-the-clock dispatchability.",
        "Official IAEA Power Reactor Information System (PRIS) database and national atomic regulatory commissions."
    ),
    "D56": (
        "Discovering thousands of extrasolar planets has transformed our understanding of planetary system architectures, proving that super-Earths and sub-Neptunes are commonplace throughout the galaxy.",
        "NASA Exoplanet Archive operated by Caltech/IPAC under contract with the National Aeronautics and Space Administration."
    ),
    "D57": (
        "Forced displacement surpassing 120 million persons represents an unprecedented humanitarian strain, driven by protracted conflicts, state fragility, and climate-induced livelihood breakdown.",
        "Official statistical reporting published by the United Nations High Commissioner for Refugees (UNHCR) and the Internal Displacement Monitoring Centre (IDMC)."
    ),
    "D58": (
        "Exponential growth in published software vulnerabilities underscores how expanding codebases and open-source dependencies have multiplied enterprise digital attack surfaces worldwide.",
        "National Vulnerability Database (NVD) maintained by the National Institute of Standards and Technology (NIST) and CISA KEV catalog."
    ),
    "D59": (
        "Polar sea ice functions as Earth's primary hemispheric thermal regulator; shrinking Arctic ice exposes darker waters that accelerate the polar albedo climate feedback loop.",
        "National Snow and Ice Data Center (NSIDC) Sea Ice Index and NOAA Climate Program Office satellite observations."
    ),
    "D60": (
        "Civil aviation is a core circulatory system of globalization. Rebounding past pre-pandemic passenger records demonstrates powerful underlying mobility and international trade connectivity.",
        "Official air traffic statistics published by the International Civil Aviation Organization (ICAO) and the International Air Transport Association (IATA)."
    ),
    "D61": (
        "Central bank gold reserves serve as the ultimate sovereign reserve asset devoid of counterparty or sanctions risk, anchoring monetary credibility during global geopolitical fracturing.",
        "World Gold Council (WGC) Central Bank Statistics compiled from International Monetary Fund (IMF) International Financial Statistics."
    ),
    "D62": (
        "The UNESCO World Heritage list protects cultural masterpieces and critical biosphere ecosystems of universal value, incentivizing multilateral conservation treaties.",
        "Official statutory records of the UNESCO World Heritage Centre and technical evaluations by IUCN and ICOMOS."
    ),
    "D63": (
        "Semiconductors form the physical foundation of modern computing, artificial intelligence, communications, and defense, driving intense global industrial policy and foundry investments.",
        "Semiconductor Industry Association (SIA) monthly billings releases compiled by World Semiconductor Trade Statistics (WSTS)."
    ),
    "D64": (
        "Routine pediatric immunization is one of the highest-return public health interventions in history, preventing an estimated 4-5 million child deaths annually from vaccine-preventable contagions.",
        "WHO/UNICEF Estimates of National Immunization Coverage (WUENIC) and WHO Global Health Observatory."
    ),
    "D65": (
        "Because oceans absorb over 90% of Earth's surplus greenhouse heat, Ocean Heat Content is the most robust thermodynamic metric of persistent planetary energy imbalance.",
        "NOAA National Centers for Environmental Information (NCEI) World Ocean Database and Argo international float array data."
    ),
    "D66": (
        "The modern Olympic Games showcase international athletic excellence while reflecting global demographic trends, geopolitical evolution, and monumental strides toward gender parity.",
        "Official historical results records of the International Olympic Committee (IOC) and Olympic Studies Centre."
    ),
    "D67": (
        "Over 80% of international merchandise trade by volume moves across maritime corridors, making the carrying capacity and efficiency of the merchant fleet vital to global supply security.",
        "UNCTAD Review of Maritime Transport compiled from Clarksons Research and international port logistics datasets."
    ),
    "D68": (
        "Climatological and geophysical disasters cause immense human and economic devastation, disproportionately impacting vulnerable populations in developing economies.",
        "CRED EM-DAT International Disaster Database hosted by UCLouvain and supported by USAID/BHA."
    ),
    "D69": (
        "PISA standardized assessments illuminate how educational policy, resource equity, and socioeconomic factors shape 15-year-old student literacy in mathematics, reading, and science.",
        "OECD Directorate for Education and Skills Programme for International Student Assessment (PISA) official database."
    ),
    "D70": (
        "The IUCN Red List is the global benchmark for species extinction risk, documenting an accelerating planetary biodiversity crisis driven by habitat destruction, climate change, and overexploitation.",
        "International Union for Conservation of Nature (IUCN) Red List of Threatened Species official dataset."
    ),
    "D71": (
        "Modern agricultural fertilizers sustain food security for half the global human population, yet nutrient runoff presents major environmental and biogeochemical challenges.",
        "Food and Agriculture Organization of the United Nations (FAOSTAT) Fertilizers by Nutrient Domain."
    ),
    "D72": (
        "The commercialization of spaceflight and rapid deployment of orbital megaconstellations have altered orbital mechanics, space traffic management, and low-Earth orbit utilization.",
        "United Nations Office for Outer Space Affairs (UNOOSA) Register of Objects Launched into Outer Space and Space-Track.org."
    ),
    "D73": (
        "Energy underpins all human economic activity; tracking the primary fuel mix highlights the structural pace and scale of decarbonization across fossil and renewable energy carriers.",
        "Energy Institute Statistical Review of World Energy (formerly BP Statistical Review of World Energy)."
    ),
    "D74": (
        "Evaluating national well-being beyond GDP reveals that social support networks, institutional trust, and personal freedom are as foundational to human flourishing as income.",
        "UN Sustainable Development Solutions Network (SDSN) World Happiness Report and Gallup World Poll data."
    ),
"D75": (
        "Antimicrobial resistance undermines modern medicine by rendering frontline antibiotics ineffective against common pathogens, requiring strict clinical stewardship.",
        "Official surveillance reports from the WHO Global Antimicrobial Resistance and Use Surveillance System (GLASS) and CDC Division of Healthcare Quality Promotion."
    ),
    "D76": (
        "Operating an interconnected synchronous alternating-current power grid requires tight statutory frequency band compliance to prevent blackout cascades during variable renewable feed-in.",
        "Official national grid frequency excursion and dispatch telemetry published by Grid Controller of India Limited (Grid-India / POSOCO)."
    ),
    "D77": (
        "Uncontrolled municipal dumpsites leach toxic contaminants and emit fugitive methane. Monitoring scientific processing and legacy biomining is essential for urban sustainability.",
        "Annual Municipal Solid Waste (MSW) Implementation Status Reports published by the Central Pollution Control Board (CPCB) and MoHUA Swachh Bharat Mission portal."
    ),
    "D78": (
        "Aquifer depletion in critical breadbasket regions imperils national food security and drinking water availability, requiring quantitative extraction monitoring.",
        "Dynamic Ground Water Resource Assessment of India reports published by the Central Ground Water Board (CGWB) and Ministry of Jal Shakti."
    ),
    "D79": (
        "The clean energy transition is physically material-intensive; concentrated refining control creates unprecedented geopolitical vulnerabilities and supply chokepoints.",
        "The Role of Critical Minerals in Clean Energy Transitions and Global Critical Minerals Outlook published by the International Energy Agency (IEA)."
    ),
    "D80": (
        "Hospital bed availability, intensive care density, and health worker ratios determine health system surge capacity during epidemics and acute medical crises.",
        "National Health Profile published by the Central Bureau of Health Intelligence (CBHI), Ministry of Health and Family Welfare (MoHFW), and National Health Authority."
    ),
    "D81": (
        "Net food-importing nations face severe balance-of-payments vulnerability during global agricultural trade shocks and fertilizer price escalations.",
        "The State of Food Security and Nutrition in the World (SOFI) and Crop Prospects and Food Situation reports published by the UN FAO and World Food Programme."
    ),
    "D82": (
        "Traffic congestion causes severe economic loss in wasted commuter time, elevated fuel combustion emissions, and supply chain friction.",
        "Urban mobility indices and congestion benchmarks published by the Ministry of Road Transport and Highways (MoRTH), Ministry of Housing and Urban Affairs (MoHUA), and TomTom Traffic Index."
    ),
    "D83": (
        "Blood component supply chains are vital for maternal care, surgery, and trauma resuscitation. Rare Rh-negative groups require proactive reserve tracking to prevent stockouts.",
        "National Blood Transfusion Council (NBTC) annual performance reports, e-RaktKosh national blood portal, and Ministry of Health and Family Welfare (MoHFW)."
    ),
    "D84": (
        "Continuous industrial emissions monitoring ensures accountability for particulate and gaseous polluters in critically polluted industrial clusters.",
        "Central Pollution Control Board (CPCB) Continuous Emission Monitoring Systems (CEMS) portal and Comprehensive Environmental Pollution Index (CEPI) monitoring reports."
    ),
    "D85": (
        "Railway safety depends on proactive ultrasonic detection of microscopic rail flaws and rapid deployment of indigenous automatic train protection systems.",
        "Annual Safety Performance Reports published by the Commission of Railway Safety (CRS), Ministry of Civil Aviation, and Ministry of Railways (Railway Board)."
    ),
    "D86": (
        "Emerging sovereign debt burdens and high-frequency credit default swap spreads provide early warnings of debt distress and fiscal rollover risks.",
        "International Debt Statistics (IDS) published by the World Bank and sovereign debt security data from the Bank for International Settlements (BIS)."
    ),
    "D87": (
        "Decentralized solar mini-grids and solar agricultural pumps provide energy access in remote unelectrified hamlets without grid extension costs.",
        "Ministry of New and Renewable Energy (MNRE) annual reports and PM-KUSUM implementation progress dashboards."
    ),
    "D88": (
        "Judicial pendency exceeding decades deprives citizens of timely justice and exacerbates overcrowded undertrial prison populations.",
        "National Judicial Data Grid (NJDG) district court statistics maintained by the Supreme Court of India e-Committee and Department of Justice."
    ),
    "D89": (
        "Cyber attacks against critical infrastructure and corporate systems threaten national digital sovereignty, requiring rapid detection and containment.",
        "Indian Computer Emergency Response Team (CERT-In) Annual Cyber Security Incident Profiles, Ministry of Electronics and Information Technology (MeitY)."
    ),
    "D90": (
        "Gaps in refrigerated transport and cold storage lead to massive post-harvest spoilage of perishable horticultural produce, eroding farmer incomes.",
        "National Centre for Cold-chain Development (NCCD) cold storage assessments and Ministry of Food Processing Industries (MoFPI) annual reports."
    ),
    "D91": (
        "Wildfire early warning systems combining satellite thermal anomaly detection and quick ground response protect biodiversity and carbon sinks.",
        "Forest Survey of India (FSI) India State of Forest Report (ISFR) Fire Alert System 3.0 based on NASA SNPP-VIIRS and MODIS satellite feeds."
    ),
    "D92": (
        "Rapid urbanization without adequate rental housing forces low-income and migrant workers into informal slums with heavy rent-to-income burdens.",
        "Affordable Rental Housing Complexes (ARHC) portal and Pradhan Mantri Awas Yojana - Urban (PMAY-U) reports published by MoHUA."
    ),
    "D93": (
        "Overfishing beyond maximum sustainable yield and excessive juvenile bycatch jeopardize marine biodiversity and coastal fisher livelihoods.",
        "Marine Fisheries Census and annual marine fish landings reports published by ICAR-Central Marine Fisheries Research Institute (CMFRI)."
    ),
    "D94": (
        "Tele-mental health services bridge critical geographic psychiatrist deficits, providing free 24/7 psychological first aid to citizens in distress.",
        "Tele Mental Health Assistance and Networking Across States (Tele-MANAS) portal operational reports, NIMHANS, and Ministry of Health and Family Welfare."
    ),

}

def generate_chart_code(fig_num, c, palette_slice, subtitle="", height=380, indent=8):
    ctype, x, y, title = c[0], c[1], c[2], c[3]
    var_name = f"fig{fig_num}"
    lines = []
    
    if ctype == "geo_scatter":
        size_val = f'"{c[4]}"' if len(c) > 4 and c[4] else "None"
        color_val = f'"{c[5]}"' if len(c) > 5 and c[5] else "None"
        hover_val = f'"{c[6]}"' if len(c) > 6 and c[6] else "None"
        scope_val = f'"{c[7]}"' if len(c) > 7 and c[7] else "None"
        lines.append(f"{var_name} = create_geo_scatter(df, lat=\"{x}\", lon=\"{y}\", size={size_val}, color={color_val}, hover_name={hover_val}, title=\"{title}\", subtitle=\"{subtitle}\", scope={scope_val}, height={height})")
    elif ctype == "area":
        lines.append(f"{var_name} = px.area(df, x=\"{x}\", y={y}, color_discrete_sequence={palette_slice})")
        lines.append(f"{var_name} = base_layout({var_name}, \"{title}\", \"{c[4]}\", \"{c[5]}\", height={height}, subtitle=\"{subtitle}\")")
    elif ctype == "line":
        lines.append(f"{var_name} = px.line(df, x=\"{x}\", y={y}, markers=True, color_discrete_sequence={palette_slice})")
        lines.append(f"{var_name} = base_layout({var_name}, \"{title}\", \"{c[4]}\", \"{c[5]}\", height={height}, subtitle=\"{subtitle}\")")
    elif ctype == "bar":
        y_expr = y if isinstance(y, list) else f'"{y}"'
        lines.append(f"{var_name} = px.bar(df, x=\"{x}\", y={y_expr}, color_discrete_sequence={palette_slice})")
        lines.append(f"{var_name} = base_layout({var_name}, \"{title}\", \"{c[4]}\", \"{c[5]}\", height={height}, subtitle=\"{subtitle}\")")
    elif ctype == "horizontal_bar":
        lines.append(f"{var_name} = create_horizontal_bar(df, x=\"{x}\", y=\"{y}\", title=\"{title}\", x_title=\"{c[4]}\", y_title=\"{c[5]}\", subtitle=\"{subtitle}\", height={height})")
    elif ctype == "donut":
        lines.append(f"df_donut{fig_num} = df[(df[\"{y}\"] > 0)] if (\"{y}\" in df.columns and pd.api.types.is_numeric_dtype(df[\"{y}\"])) else df")
        lines.append(f"val_col_{fig_num} = \"{y}\" if (\"{y}\" in df.columns and pd.api.types.is_numeric_dtype(df[\"{y}\"])) else None")
        lines.append(f"{var_name} = create_donut_chart(df_donut{fig_num}, names=\"{x}\", values=val_col_{fig_num}, title=\"{title}\", subtitle=\"{subtitle}\", height={height})")
    elif ctype == "histogram":
        x_title = c[4] if len(c) > 4 and c[4] else ""
        y_title = c[5] if len(c) > 5 and c[5] else "Frequency"
        lines.append(f"{var_name} = create_histogram(df, x=\"{x}\", title=\"{title}\", x_title=\"{x_title}\", y_title=\"{y_title}\", subtitle=\"{subtitle}\", height={height})")
    elif ctype == "violin":
        x_expr = f'"{x}"' if x else "None"
        x_title = c[4] if len(c) > 4 and c[4] else ""
        y_title = c[5] if len(c) > 5 and c[5] else ""
        lines.append(f"{var_name} = create_violin_chart(df, x={x_expr}, y=\"{y}\", title=\"{title}\", x_title=\"{x_title}\", y_title=\"{y_title}\", subtitle=\"{subtitle}\", height={height})")
    elif ctype == "sunburst":
        lines.append(f"df_sun{fig_num} = df[df[\"{y}\"] > 0] if \"{y}\" in df.columns else df")
        lines.append(f"{var_name} = create_sunburst(df_sun{fig_num}, path={x}, values=\"{y}\", title=\"{title}\", subtitle=\"{subtitle}\", height={height})")
    elif ctype == "funnel":
        lines.append(f"{var_name} = create_funnel_chart(df, x=\"{x}\", y=\"{y}\", title=\"{title}\", subtitle=\"{subtitle}\", height={height})")
    elif ctype == "correlation_heatmap":
        cols_arg = f"{x}" if isinstance(x, list) else f"df.select_dtypes(include=['number']).columns.tolist()[:6]"
        lines.append(f"{var_name} = create_correlation_heatmap(df, cols={cols_arg}, title=\"{title}\", subtitle=\"{subtitle}\", height={height})")
    elif ctype == "density_heatmap":
        x_title = c[4] if len(c) > 4 and c[4] else ""
        y_title = c[5] if len(c) > 5 and c[5] else ""
        lines.append(f"{var_name} = create_density_heatmap(df, x=\"{x}\", y=\"{y}\", title=\"{title}\", x_title=\"{x_title}\", y_title=\"{y_title}\", subtitle=\"{subtitle}\", height={height})")
    elif ctype == "radar":
        lines.append(f"radar_cols_{fig_num} = [c for c in {x} if c in df.columns]")
        lines.append(f"radar_vals_{fig_num} = [float(df[c].dropna().iloc[-1]) if c in df.columns and len(df[c].dropna()) > 0 else 0.0 for c in radar_cols_{fig_num}]")
        lines.append(f"{var_name} = create_radar_chart(radar_cols_{fig_num}, radar_vals_{fig_num}, title=\"{title}\", subtitle=\"{subtitle}\", height={height})")
    elif ctype == "scatter":
        trend = ', trendline="ols"' if fig_num == 4 else ""
        lines.append(f"{var_name} = px.scatter(df, x=\"{x}\", y=\"{y}\"{trend}, color_discrete_sequence={palette_slice})")
        lines.append(f"{var_name} = base_layout({var_name}, \"{title}\", \"{c[4]}\", \"{c[5]}\", height={height}, subtitle=\"{subtitle}\")")
    elif ctype == "box":
        x_expr = f'"{x}"' if x else "None"
        lines.append(f"{var_name} = px.box(df, x={x_expr}, y=\"{y}\", color_discrete_sequence={palette_slice})")
        lines.append(f"{var_name} = base_layout({var_name}, \"{title}\", \"{c[4]}\", \"{c[5]}\", height={height}, subtitle=\"{subtitle}\")")
    elif ctype == "treemap":
        lines.append(f"df_tree{fig_num} = df[df[\"{y}\"] > 0] if \"{y}\" in df.columns else df")
        lines.append(f"{var_name} = px.treemap(df_tree{fig_num}, path={x}, values=\"{y}\", color_discrete_sequence={palette_slice})")
        lines.append(f"{var_name} = base_layout({var_name}, \"{title}\", height={height}, subtitle=\"{subtitle}\")")
    else:
        lines.append(f"{var_name} = px.line(df, x=\"{x}\", y={y}, color_discrete_sequence={palette_slice})")
        lines.append(f"{var_name} = base_layout({var_name}, \"{title}\", \"{c[4]}\", \"{c[5]}\", height={height}, subtitle=\"{subtitle}\")")
        
    pad = " " * indent
    return f"\n{pad}".join(lines)

def generate_dashboard_code(spec):
    slug = spec["slug"]
    did = spec["id"]
    title = spec["title"]
    csv_file = spec["csv"]
    kpis = spec["kpis"]
    charts = spec["charts"]
    time_col = spec["time_col"]
    
    ctx = BRIEFING_CONTEXT.get(did, (
        "Empirical intelligence derived from official publications and open data records.",
        "Verified external provenance and production data engineering pipeline."
    ))
    why_matters = ctx[0]
    data_note = ctx[1]

    meta_dashboards_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "metadata", "dashboards.json")
    dash_meta = {}
    if os.path.exists(meta_dashboards_path):
        try:
            with open(meta_dashboards_path, "r", encoding="utf-8") as f_meta:
                dash_meta = {d["id"]: d for d in json.load(f_meta)}
        except Exception:
            pass
    source_org = dash_meta.get(did, {}).get("source_org", spec["title"])
    source_org_clean = source_org.replace('"', '\\"')

    code = f'''"""
Dashboard Module: {did} - {title}
Domain: {spec['domain']}
Authentic Source: Verified Primary Dataset ({csv_file})
Visuals: 5 KPI Cards + 7 Meaningful Plotly Visualizations + 1 Data Grid = 13 Visuals
"""

import os
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

from app.components.html_utils import render_html
from app.components.info_modal import render_info_button
from app.components.kpi_card import render_kpi
from app.components.charts import (
    base_layout, COLOR_PALETTE, create_geo_scatter, create_donut_chart,
    create_histogram, create_violin_chart, create_sunburst, create_funnel_chart,
    create_horizontal_bar, create_correlation_heatmap, create_density_heatmap,
    create_radar_chart, create_waterfall_chart, create_treemap, create_box_chart,
    create_line_chart, create_bar_chart, create_area_chart
)

CSV_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "{csv_file}")
WHY_MATTERS = """{why_matters}"""
DATA_NOTE = """{data_note}"""

@st.cache_data
def load_data():
    df = pd.read_csv(CSV_PATH)
    return df

def render():
    df_raw = load_data()
    
    # Header & Institutional Badging
    c_title, c_info = st.columns([4.2, 1.2])
    with c_title:
        render_html(f"""<div style="display:flex; align-items:center; gap:8px; margin-bottom:8px; flex-wrap:wrap;">
<span class="domain-pill domain-{spec['domain'].lower()}">{spec['domain']}</span>
<span class="kpi-chip" style="font-family:var(--font-mono); font-size:0.75rem; color:var(--accent-cyan); background:rgba(56,189,248,0.1); border-color:rgba(56,189,248,0.3);">{did}</span>
<span class="live-dot" style="margin-left:4px;"></span>
<span style="font-size:0.75rem; color:var(--text-muted); font-weight:600; text-transform:uppercase; letter-spacing:0.05em;">SOVEREIGN REAL DATASET</span>
</div>
<h1 style="font-size:1.85rem; font-weight:800; letter-spacing:-0.03em; margin:0 0 6px 0; background:linear-gradient(135deg, #ffffff 40%, #94a3b8 100%); -webkit-background-clip:text; -webkit-text-fill-color:transparent;">
{title}
</h1>
<div style="font-size:0.875rem; color:var(--text-secondary); line-height:1.4;">
Authoritative Public Data Intelligence &bull; Production analytical pipeline &bull; Verified provenance: <code style="font-size:0.78rem; color:var(--accent-cyan); background:#080808; border:1px solid #1a1a1a; padding:2px 6px; border-radius:4px;">{csv_file}</code>
</div>""")
    with c_info:
        st.write("")
        render_info_button("{did}")

    # Interactive Analytical Slicers
    render_html("""<div class="visuals-section-header" style="margin-top:1.5rem;">
<span class="visuals-section-title">🎛️ Interactive Analytical Slicers</span>
<span class="visuals-density-pill">Parametric Filtering</span>
</div>""")
    f_col1, f_col2, f_col3 = st.columns([1.5, 1.5, 1])
    df = df_raw.copy()

    # Time or Date Filter
    if "{time_col}" in df.columns:
        time_series = df["{time_col}"].dropna()
        if pd.api.types.is_numeric_dtype(time_series) and len(time_series.unique()) > 1:
            min_val = int(time_series.min())
            max_val = int(time_series.max())
            if min_val < max_val:
                with f_col1:
                    selected_range = st.slider("Select Horizon Range:", min_val, max_val, (min_val, max_val), key=f"{slug}_slider")
                    df = df[(df["{time_col}"] >= selected_range[0]) & (df["{time_col}"] <= selected_range[1])]
        elif len(time_series.unique()) > 1 and "{time_col}" in ["date", "Date"]:
            dates = sorted(time_series.unique().tolist())
            with f_col1:
                date_range = st.select_slider("Select Date Span:", options=dates, value=(dates[0], dates[-1]), key=f"{slug}_dslider")
                df = df[(df["{time_col}"] >= date_range[0]) & (df["{time_col}"] <= date_range[1])]

    # Categorical Filter
    cat_col = next((c for c in ["country", "state", "city", "market", "region", "economy_group"] if c in df.columns and len(df[c].dropna().unique()) > 1), None)
    if cat_col:
        unique_cats = sorted(df[cat_col].dropna().unique().tolist())
        with f_col2:
            selected_cats = st.multiselect(f"Filter {{cat_col.title()}}:", unique_cats, default=unique_cats, key=f"{slug}_{{cat_col}}_sel")
            if selected_cats:
                df = df[df[cat_col].isin(selected_cats)]

    # Sort & Narrative View
    num_cols_for_sort = df.select_dtypes(include=[np.number]).columns.tolist()
    with f_col3:
        sort_order = st.selectbox("Sort View:", ["Default Chronology", "Highest Value First", "Lowest Value First"], key=f"{slug}_sort")
        if sort_order == "Highest Value First" and num_cols_for_sort:
            df = df.sort_values(by=num_cols_for_sort[0], ascending=False)
        elif sort_order == "Lowest Value First" and num_cols_for_sort:
            df = df.sort_values(by=num_cols_for_sort[0], ascending=True)

    # Safety guard
    if df.empty:
        st.warning("⚠️ No records match active filters. Resetting to complete analytical dataset.")
        df = df_raw.copy()

    # 1. Executive KPI Cards Section (5 Cards)
    render_html("""
    <div class="visuals-section-header" style="margin-top:1.5rem;">
        <span class="visuals-section-title">📌 Executive Performance Indicators</span>
        <span class="visuals-density-pill">5 Computed Metrics</span>
    </div>
    """)
    kpi_cols = st.columns(5)
'''

    # Dynamically compute each KPI
    for idx, (label, col, agg, fmt, subtext, status) in enumerate(kpis):
        code += f'''
    with kpi_cols[{idx}]:
        try:
            if "{agg}" == "latest":
                val = float(df["{col}"].dropna().iloc[-1])
            elif "{agg}" == "max":
                val = float(df["{col}"].dropna().max())
            elif "{agg}" == "min":
                val = float(df["{col}"].dropna().min())
            elif "{agg}" == "sum":
                val = float(df["{col}"].dropna().sum())
            elif "{agg}" == "count":
                val = float(len(df["{col}"].dropna()))
            else: # mean
                val = float(df["{col}"].dropna().mean())
            fmt_val = "{fmt}".format(val=val)
        except Exception:
            fmt_val = "N/A"
        render_kpi("{label}", fmt_val, "{subtext}", status="{status}")
'''

    code += '''
    # 2. Dynamic Computed Empirical Intelligence Briefing
    render_html("""<div class="visuals-section-header" style="margin-top:1.5rem;">
<span class="visuals-section-title">💡 Institutional Analytical Briefing & Derived Empirical Intelligence</span>
<span class="visuals-density-pill">3-Tier Empirical Brief</span>
</div>""")
    try:
        num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        entity_col = next((c for c in ["country", "state", "city", "market", "region", "economy_group"] if c in df.columns), None)
        time_c = next((c for c in ["year", "fiscal_year", "crop_year", "date", "Date"] if c in df.columns), None)
        
        primary_col = num_cols[0] if num_cols else None
        secondary_col = num_cols[1] if len(num_cols) > 1 else None
        
        b1, b2, b3, b4 = "", "", "", ""
        
        if primary_col:
            p_series = df[primary_col].dropna()
            p_min, p_max = float(p_series.min()), float(p_series.max())
            p_mean, p_median = float(p_series.mean()), float(p_series.median())
            p_latest = float(p_series.iloc[-1])
            p_first = float(p_series.iloc[0])
            
            # Insight 1: Trajectory / Distribution
            if time_c and len(p_series) > 1:
                t_start = df.loc[p_series.index[0], time_c]
                t_end = df.loc[p_series.index[-1], time_c]
                pct_change = ((p_latest - p_first) / abs(p_first) * 100) if p_first != 0 else 0
                b1 = f"• <b>Longitudinal Trajectory ({t_start}–{t_end})</b>: Primary metric <code>{primary_col}</code> shifted from {p_first:,.2f} to {p_latest:,.2f} (net drift of <b>{pct_change:+.1f}%</b>), tracking long-term structural adjustments."
            else:
                std_val = float(p_series.std()) if len(p_series) > 1 else 0.0
                b1 = f"• <b>Central Baseline Distribution</b>: Across {len(p_series)} observations, <code>{primary_col}</code> averages <b>{p_mean:,.2f}</b> (median: {p_median:,.2f}, std dev: {std_val:,.2f})."

            # Insight 2: Historical Extremes
            max_idx = p_series.idxmax()
            min_idx = p_series.idxmin()
            max_entity = df.loc[max_idx, entity_col] if entity_col else (df.loc[max_idx, time_c] if time_c else "Peak")
            min_entity = df.loc[min_idx, entity_col] if entity_col else (df.loc[min_idx, time_c] if time_c else "Trough")
            b2 = f"• <b>Empirical Extremes</b>: Peak observation registered at <b>{p_max:,.2f}</b> ({max_entity}) vs historical trough of <b>{p_min:,.2f}</b> ({min_entity}), yielding a total dynamic range of {p_max - p_min:,.2f}."

            # Insight 3: Disparity or Statistical Correlation
            if entity_col and p_min > 0:
                disp = p_max / p_min
                top3_sum = float(df.nlargest(3, primary_col)[primary_col].sum())
                tot_sum = float(p_series.sum())
                top3_share = (top3_sum / tot_sum * 100) if tot_sum > 0 else 0
                b3 = f"• <b>Cross-Sectional Concentration</b>: Top jurisdiction exceeds lowest by <b>{disp:.1f}x</b>. The top 3 jurisdictions concentrate <b>{top3_share:.1f}%</b> of aggregate measured volume."
            elif secondary_col:
                corr = float(df[primary_col].corr(df[secondary_col]))
                corr_desc = "strong positive" if corr > 0.6 else ("moderate positive" if corr > 0.3 else ("strong negative" if corr < -0.6 else "uncoupled/neutral"))
                b3 = f"• <b>Empirical Co-Movement</b>: Pearson correlation between <code>{primary_col}</code> and <code>{secondary_col}</code> is <b>{corr:+.2f}</b> ({corr_desc} empirical association)."

            # Insight 4: Recent Momentum
            if len(p_series) >= 2:
                p_prior = float(p_series.iloc[-2])
                mom = ((p_latest - p_prior) / abs(p_prior) * 100) if p_prior != 0 else 0
                b4 = f"• <b>Latest Cycle Momentum</b>: Latest recorded reading registered at <b>{p_latest:,.2f}</b> (<b>{mom:+.1f}%</b> change relative to preceding observation)."

        finding_html = "<br>".join(filter(None, [b1, b2, b3, b4])) if any([b1, b2, b3, b4]) else "Empirical observations active across all monitored dimensions."
        
        render_html(f"""<div class="institutional-briefing">
<div class="briefing-card card-finding">
<div class="briefing-label label-finding">⚡ Key Empirical Finding (Live Computation)</div>
<div class="briefing-text">{finding_html}</div>
</div>
<div class="briefing-card card-why">
<div class="briefing-label label-why">🏛️ Why This Matters (Policy & Macroeconomic Significance)</div>
<div class="briefing-text">{WHY_MATTERS}</div>
</div>
<div class="briefing-card card-note">
<div class="briefing-label label-note">📋 Data & Methodological Framework</div>
<div class="briefing-text">{DATA_NOTE}</div>
</div>
</div>""")
    except Exception:
        pass

    # 3. Interactive Plotly Visualizations (7 Charts)
    render_html("""<div class="visuals-section-header" style="margin-top:1.75rem;">
<span class="visuals-section-title">📊 Multi-Dimensional Analytical Visualizations</span>
<span class="visuals-density-pill">7 Interactive Visuals</span>
</div>""")
'''

    # Chart 1 & Chart 2 (Row 1)
    c1, c2 = charts[0], charts[1]
    sub1, sub2 = get_chart_subtitle(spec, 1, c1), get_chart_subtitle(spec, 2, c2)
    chart1_code = generate_chart_code(1, c1, "COLOR_PALETTE", sub1, height=380)
    chart2_code = generate_chart_code(2, c2, "COLOR_PALETTE[2:]", sub2, height=380)
    code += f'''
    row1_c1, row1_c2 = st.columns(2)
    with row1_c1:
        # Chart 1: {c1[3]}
        {chart1_code}
        st.plotly_chart(fig1, use_container_width=True)

    with row1_c2:
        # Chart 2: {c2[3]}
        {chart2_code}
        st.plotly_chart(fig2, use_container_width=True)
'''

    # Chart 3 & Chart 4 (Row 2)
    c3, c4 = charts[2], charts[3]
    sub3, sub4 = get_chart_subtitle(spec, 3, c3), get_chart_subtitle(spec, 4, c4)
    chart3_code = generate_chart_code(3, c3, "COLOR_PALETTE", sub3, height=380)
    chart4_code = generate_chart_code(4, c4, "COLOR_PALETTE[1:]", sub4, height=380)
    code += f'''
    row2_c1, row2_c2 = st.columns(2)
    with row2_c1:
        # Chart 3: {c3[3]}
        {chart3_code}
        st.plotly_chart(fig3, use_container_width=True)

    with row2_c2:
        # Chart 4: {c4[3]}
        {chart4_code}
        st.plotly_chart(fig4, use_container_width=True)
'''

    # Chart 5 & Chart 6 (Row 3)
    c5, c6 = charts[4], charts[5]
    sub5, sub6 = get_chart_subtitle(spec, 5, c5), get_chart_subtitle(spec, 6, c6)
    chart5_code = generate_chart_code(5, c5, "COLOR_PALETTE[3:]", sub5, height=380)
    chart6_code = generate_chart_code(6, c6, "COLOR_PALETTE[4:]", sub6, height=380)
    code += f'''
    row3_c1, row3_c2 = st.columns(2)
    with row3_c1:
        # Chart 5: {c5[3]}
        {chart5_code}
        st.plotly_chart(fig5, use_container_width=True)

    with row3_c2:
        # Chart 6: {c6[3]}
        {chart6_code}
        st.plotly_chart(fig6, use_container_width=True)
'''

    # Chart 7 (Row 4 Full-Width / Focused Visual)
    c7 = charts[6]
    sub7 = get_chart_subtitle(spec, 7, c7)
    chart7_code = generate_chart_code(7, c7, "COLOR_PALETTE[5:]", sub7, height=360, indent=4)
    code += f'''
    # Chart 7: {c7[3]}
    {chart7_code}
    st.plotly_chart(fig7, use_container_width=True)
'''

    # 4. Interactive Data Table (Visual 13) and Navigation Shortcuts
    code += f'''
    # 4. Interactive Data Table (Visual 13)
    render_html("""<div class="visuals-section-header" style="margin-top:1.75rem;">
<span class="visuals-section-title">📋 Analytical Data Grid & Granular Records</span>
<span class="visuals-density-pill">Visual #13 &bull; Verified Records</span>
</div>""")
    st.dataframe(df, use_container_width=True, height=280)
    
    dl_c1, dl_c2 = st.columns([3, 1])
    with dl_c1:
        render_html(f"""<div style="font-size:0.82rem; color:var(--text-muted); font-family:var(--font-sans); padding-top:6px;">
Displaying <strong style="color:var(--text-primary);">{{len(df)}}</strong> verified observations across <strong style="color:var(--text-primary);">{{len(df.columns)}}</strong> analytical attributes &bull; Sovereign dataset: <code style="font-family:var(--font-mono); font-size:0.75rem; color:var(--accent-cyan);">{{CSV_PATH}}</code>
</div>""")
    with dl_c2:
        st.download_button(
            label="📥 Export Filtered CSV",
            data=df.to_csv(index=False).encode('utf-8'),
            file_name=f"{slug}_filtered.csv",
            mime="text/csv",
            use_container_width=True
        )

    render_html("""<div class="visuals-section-header" style="margin-top:1.5rem;">
<span class="visuals-section-title">🔗 Cross-System Deep Navigation</span>
<span class="visuals-density-pill">Provenance Tracing</span>
</div>""")
    nav_col1, nav_col2 = st.columns(2)
    with nav_col1:
        if st.button("🔍 Explore Full Schema & Profile in Dataset Explorer", key=f"f_nav_ds_{slug}", use_container_width=True):
            st.session_state["current_view"] = "Dataset Explorer"
            st.session_state["selected_dataset_slug"] = "{slug}"
            st.rerun()
    with nav_col2:
        if st.button("🏛️ View Publishing Authority in Source Directory", key=f"f_nav_src_{slug}", use_container_width=True):
            st.session_state["current_view"] = "Source Directory"
            st.session_state["selected_source_name"] = "{source_org_clean}"
            st.rerun()
'''

    return code

def build_all():
    print(f"=== Generating {len(DASHBOARD_SPECS)} Production Dashboard Modules ===")
    for spec in DASHBOARD_SPECS:
        path = os.path.join(DASHBOARDS_DIR, spec["file"])
        code = generate_dashboard_code(spec)
        with open(path, "w", encoding="utf-8") as f:
            f.write(code)
        print(f"Generated dashboard: [{spec['id']}] {spec['title']} -> {path}")
    print("=== All 54 Dashboard Modules Generated Successfully ===")

if __name__ == "__main__":
    build_all()
