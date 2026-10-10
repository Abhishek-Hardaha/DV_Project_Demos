"""
Script to append D75 to D94 specifications to scripts/build_dashboards.py
and generate all 20 new dashboard files (d75_*.py to d94_*.py).
"""

import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BUILD_SCRIPT = os.path.join(PROJECT_ROOT, "scripts", "build_dashboards.py")

NEW_SPECS_CODE = '''
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
'''

NEW_BRIEFING_CODE = '''
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
'''

def update_and_build():
    with open(BUILD_SCRIPT, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Update DASHBOARD_SPECS if D75 not yet present
    if '"id": "D75"' not in content:
        target_specs_end = "\ndef get_chart_subtitle"
        idx_specs = content.find(target_specs_end)
        if idx_specs == -1:
            raise ValueError("Could not find get_chart_subtitle in build_dashboards.py")
        
        bracket_pos = content.rfind("]", 0, idx_specs)
        content = content[:bracket_pos] + ",\n" + NEW_SPECS_CODE.strip() + "\n" + content[bracket_pos:]
        print("Inserted D75-D94 specs into DASHBOARD_SPECS.")
    else:
        print("D75 already present in DASHBOARD_SPECS.")

    # 2. Update BRIEFING_CONTEXT if D75 not yet present
    if '"D75":' not in content:
        target_d74 = '"D74": (\n        "Evaluating national well-being beyond GDP reveals that social support networks, institutional trust, and personal freedom are as foundational to human flourishing as income.",\n        "UN Sustainable Development Solutions Network (SDSN) World Happiness Report and Gallup World Poll data."\n    ),'
        idx_d74 = content.find(target_d74)
        if idx_d74 == -1:
            # Try alternate formatting
            target_d74 = '"D74": ('
            idx_d74 = content.find(target_d74)
            # Find the closing parenthesis of D74
            end_d74 = content.find('),', idx_d74)
            insert_pos = end_d74 + 2
        else:
            insert_pos = idx_d74 + len(target_d74)

        content = content[:insert_pos] + "\n" + NEW_BRIEFING_CODE.strip() + content[insert_pos:]
        print("Inserted D75-D94 briefing contexts into BRIEFING_CONTEXT.")
    else:
        print("D75 already present in BRIEFING_CONTEXT.")

    with open(BUILD_SCRIPT, "w", encoding="utf-8") as f:
        f.write(content)
    print("Successfully updated scripts/build_dashboards.py!")

    # 3. Now execute build_all from build_dashboards
    print("Importing build_dashboards and running build_all()...")
    sys.path.insert(0, os.path.join(PROJECT_ROOT, "scripts"))
    import build_dashboards
    importlib_reload = sys.modules.get("importlib", None)
    if importlib_reload:
        import importlib
        importlib.reload(build_dashboards)
    build_dashboards.build_all()
    print("Build complete!")

if __name__ == "__main__":
    update_and_build()
