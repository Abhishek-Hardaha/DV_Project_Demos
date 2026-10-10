"""
Script to append D55 to D74 specifications to scripts/build_dashboards.py
and generate all 20 new dashboard files (d55_*.py to d74_*.py).
"""

import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BUILD_SCRIPT = os.path.join(PROJECT_ROOT, "scripts", "build_dashboards.py")

NEW_SPECS_CODE = '''
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
'''

NEW_BRIEFING_CODE = '''
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
'''

def update_build_script():
    with open(BUILD_SCRIPT, "r", encoding="utf-8") as f:
        content = f.read()

    if '"id": "D55"' in content:
        print("D55 already exists in build_dashboards.py")
        return

    # 1. Insert NEW_SPECS_CODE right before the end of DASHBOARD_SPECS (before `\ndef get_chart_subtitle`)
    target_specs_end = "\ndef get_chart_subtitle"
    idx_specs = content.find(target_specs_end)
    if idx_specs == -1:
        raise ValueError("Could not find get_chart_subtitle in build_dashboards.py")
    
    # Locate the closing bracket before get_chart_subtitle
    bracket_pos = content.rfind("]", 0, idx_specs)
    content = content[:bracket_pos] + ",\n" + NEW_SPECS_CODE.strip() + "\n" + content[bracket_pos:]
    
    # 2. Insert NEW_BRIEFING_CODE right after D54 in BRIEFING_CONTEXT
    target_d54 = '"D54": (\n        "Inland water transport is an environmentally sustainable and cost-effective freight mode. Development of National Waterways under the Jal Marg Vikas Project connects the hinterland to sea ports.",\n        "Official cargo movement reports published by the Inland Waterways Authority of India (IWAI), Ministry of Ports, Shipping and Waterways."\n    )'
    idx_d54 = content.find(target_d54)
    if idx_d54 == -1:
        raise ValueError("Could not find D54 in BRIEFING_CONTEXT")
    
    insert_pos = idx_d54 + len(target_d54)
    content = content[:insert_pos] + ",\n" + NEW_BRIEFING_CODE.strip() + content[insert_pos:]

    with open(BUILD_SCRIPT, "w", encoding="utf-8") as f:
        f.write(content)
    print("Successfully updated scripts/build_dashboards.py with D55 to D74!")

if __name__ == "__main__":
    update_build_script()
