"""
Script to append D35-D54 specifications and briefings into scripts/build_dashboards.py,
then generate all 54 production dashboard modules.
"""

import os
import sys

NEW_BRIEFINGS = {
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
}

NEW_SPECS = [
    {
        "id": "D35",
        "slug": "d35_india_gst_collections",
        "title": "India Goods & Services Tax (GST) Revenue Collections",
        "domain": "Taxation & Public Revenue",
        "file": "d35_india_gst_collections.py",
        "csv": "data/analytical/d35_india_gst_collections.csv",
        "time_col": "year",
        "kpis": [
            ["Peak Monthly Collection", "total_gst_crore", "max", "₹{val:,.0f} Cr", "All-Time Highest Month", "pos"],
            ["Latest Monthly Collection", "total_gst_crore", "latest", "₹{val:,.0f} Cr", "Most Recent Month", "pos"],
            ["Mean Monthly Collection", "total_gst_crore", "mean", "₹{val:,.0f} Cr", "26-Month Average", "neutral"],
            ["Total CGST Mobilized", "cgst_crore", "sum", "₹{val:,.0f} Cr", "Central GST Component", "pos"],
            ["Compensation Cess Total", "cess_crore", "sum", "₹{val:,.0f} Cr", "Dedicated State Cess", "neutral"],
        ],
        "charts": [
            ["line", "period_str", ["total_gst_crore", "rolling_3m_avg_crore"], "Monthly GST Revenue Trajectory & 3-Month Moving Average", "Month", "Revenue (₹ Crore)"],
            ["bar", "period_str", ["cgst_crore", "sgst_crore", "igst_crore", "cess_crore"], "Monthly Tax Component Deconstruction (CGST, SGST, IGST, Cess)", "Month", "Amount (₹ Crore)"],
            ["scatter", "cgst_sgst_combined", "igst_crore", "Domestic State GST vs Inter-State IGST Collections", "Domestic GST (CGST+SGST) ₹ Cr", "IGST ₹ Cr"],
            ["area", "period_str", ["igst_share_pct", "cess_share_pct"], "IGST and Cess Proportional Share Evolution (%)", "Month", "Share (%)"],
            ["horizontal_bar", "total_gst_crore", "period_str", "Top Revenue Month Rankings (₹ Crore)", "Revenue (₹ Crore)", "Month"],
            ["violin", "year", "total_gst_crore", "Fiscal Year Revenue Density & Variability Comparison", "Fiscal Year", "Revenue (₹ Crore)"],
            ["correlation_heatmap", ["cgst_crore", "sgst_crore", "igst_crore", "cess_crore", "total_gst_crore", "rolling_3m_avg_crore"], None, "Inter-Component Revenue Correlation Matrix", None, None],
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
            ["Total Accounts Opened", "total_beneficiaries_lakh", "sum", "{val:,.1f} Lk", "Total Beneficiaries", "pos"],
            ["Total Deposit Balance", "total_deposits_crore", "sum", "₹{val:,.0f} Cr", "Total Deposits Mobilized", "pos"],
            ["Avg Deposit Per Account", "avg_deposit_per_account_inr", "mean", "₹{val:,.0f}", "National Account Balance Mean", "pos"],
            ["RuPay Debit Card Issuance", "rupay_cards_issued_lakh", "sum", "{val:,.1f} Lk", "Cards Distributed", "pos"],
            ["Average Rural Coverage", "rural_share_pct", "mean", "{val:.1f}%", "Rural/Semi-Urban Penetration", "neutral"],
        ],
        "charts": [
            ["horizontal_bar", "total_beneficiaries_lakh", "state", "PMJDY Beneficiaries by State (Lakh Accounts)", "Beneficiaries (Lakh)", "State"],
            ["scatter", "total_beneficiaries_lakh", "total_deposits_crore", "Account Volume vs Cumulative Deposit Balances (₹ Cr)", "Beneficiaries (Lakh)", "Deposits (₹ Cr)"],
            ["bar", "state", ["rural_beneficiaries_lakh", "urban_beneficiaries_lakh"], "Rural vs Urban Beneficiary Segmentation across States", "State", "Accounts (Lakh)"],
            ["treemap", ["deposit_density_tier", "state"], "total_deposits_crore", "Deposit Volume Distribution across Deposit Density Tiers", None, None],
            ["histogram", "avg_deposit_per_account_inr", None, "Distribution of State Average Account Balance (₹ INR)", "Avg Balance (₹)", "State Count"],
            ["box", "deposit_density_tier", "women_share_pct", "Women Financial Inclusion Share (%) by Density Tier", "Density Tier", "Women Share (%)"],
            ["radar", ["rural_share_pct", "women_share_pct", "rupay_card_penetration_pct"], None, "National Financial Inclusion Structural Ratios Profile", None, None],
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
            ["Total Persondays Generated", "persondays_generated_lakh", "sum", "{val:,.1f} Lk", "Rural Workdays Created", "pos"],
            ["Total Scheme Expenditure", "total_expenditure_crore", "sum", "₹{val:,.0f} Cr", "Wage & Material Capex", "neutral"],
            ["Average Daily Wage", "avg_wage_rate_rs", "mean", "₹{val:.1f}/day", "Notified State Wage Average", "pos"],
            ["Average Women Participation", "women_participation_pct", "mean", "{val:.1f}%", "Women Labor Force Share", "pos"],
            ["Households Supported", "households_worked_lakh", "sum", "{val:,.1f} Lk", "Rural Families Benefited", "pos"],
        ],
        "charts": [
            ["horizontal_bar", "persondays_generated_lakh", "state", "State Rural Employment Creation (Lakh Persondays)", "Persondays (Lakh)", "State"],
            ["scatter", "avg_wage_rate_rs", "women_participation_pct", "Notified Wage Rate vs Female Participation Ratio", "Avg Wage (₹/day)", "Women Participation (%)"],
            ["bar", "state", "total_expenditure_crore", "State-wise Public Outlay on Rural Employment (₹ Crore)", "State", "Expenditure (₹ Cr)"],
            ["treemap", ["women_inclusion_tier", "state"], "persondays_generated_lakh", "Persondays Generated Grouped by Women Inclusion Tier", None, None],
            ["box", "women_inclusion_tier", "persondays_per_household", "Employment Intensity (Days/HH) across Inclusion Tiers", "Inclusion Tier", "Days per Household"],
            ["histogram", "cost_per_personday_rs", None, "Unit Cost per Personday Created (₹ INR) Distribution", "Cost per Day (₹)", "Frequency"],
            ["correlation_heatmap", ["persondays_generated_lakh", "women_participation_pct", "total_expenditure_crore", "avg_wage_rate_rs", "cost_per_personday_rs"], None, "MGNREGS Structural Parameter Inter-Correlation", None, None],
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
            ["Peak Passenger Traffic", "total_passengers_million", "max", "{val:.1f} M", "Highest Annual Passengers", "pos"],
            ["Latest Passenger Volume", "total_passengers_million", "latest", "{val:.1f} M", "Latest Recorded FY", "pos"],
            ["Domestic Passenger Share", "domestic_share_pct", "latest", "{val:.1f}%", "Internal Passenger Dominance", "neutral"],
            ["Total Freight Cargo", "cargo_tonnage_million_mt", "latest", "{val:.2f} M MT", "Annual Air Cargo Handled", "pos"],
            ["Operational Airports", "operating_airports_count", "latest", "{val:.0f} Hubs", "UDAN Regional Expansion", "pos"],
        ],
        "charts": [
            ["line", "year", ["domestic_passengers_million", "intl_passengers_million", "total_passengers_million"], "Annual Passenger Footfall Growth Trajectory (Million Passengers)", "Year", "Passengers (Million)"],
            ["bar", "year", "aircraft_movements_million", "Scheduled Aircraft Movements Capacity (Million Takeoffs/Landings)", "Year", "Movements (Million)"],
            ["area", "year", ["cargo_tonnage_million_mt"], "Air Freight Cargo Throughput Expansion (Million MT)", "Year", "Cargo (Million MT)"],
            ["scatter", "total_passengers_million", "aircraft_movements_million", "Passenger Load Density vs Commercial Flight Movements", "Passengers (Million)", "Movements (Million)"],
            ["horizontal_bar", "operating_airports_count", "year", "Operational Airport Infrastructure Growth Timeline", "Airports Count", "Year"],
            ["line", "year", ["pax_yoy_growth_pct"], "Year-on-Year Commercial Passenger Growth Volatility (%)", "Year", "YoY Growth (%)"],
            ["radar", ["domestic_share_pct", "pax_per_aircraft_movement", "cargo_per_airport_kt"], None, "Aviation Fleet and Operational Efficiency Diagnostic Profile", None, None],
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
            ["Total Cargo Throughput", "total_traffic_mmt", "sum", "{val:,.1f} MMT", "Major Ports Combined", "pos"],
            ["Top Port Volume", "total_traffic_mmt", "max", "{val:.1f} MMT", "Leading Cargo Gateway", "pos"],
            ["Mean Turnaround Time", "avg_turnaround_hours", "mean", "{val:.1f} hrs", "Average Vessel Dwell Time", "neutral"],
            ["Total POL & Liquid Bulk", "pol_oil_mmt", "sum", "{val:.1f} MMT", "Petroleum & Hydrocarbons", "neutral"],
            ["Containerized & Other Cargo", "container_other_mmt", "sum", "{val:.1f} MMT", "High-Value Cargo Handling", "pos"],
        ],
        "charts": [
            ["horizontal_bar", "total_traffic_mmt", "port_name", "Major Ports Total Cargo Handled (MMT)", "Cargo (MMT)", "Port"],
            ["scatter", "total_traffic_mmt", "avg_turnaround_hours", "Throughput Volume vs Vessel Turnaround Time (Hours)", "Traffic (MMT)", "Turnaround (Hours)"],
            ["bar", "port_name", ["pol_oil_mmt", "iron_ore_mmt", "coal_mmt", "container_other_mmt"], "Cargo Commodity Disaggregation Across Major Ports", "Port", "Cargo (MMT)"],
            ["treemap", ["coast", "port_name"], "total_traffic_mmt", "Maritime Traffic Concentration by Coastal Corridor (East vs West)", None, None],
            ["box", "coast", "avg_turnaround_hours", "Vessel Turnaround Efficiency Distribution by Coast", "Coast", "Turnaround Hours"],
            ["donut", "coast", "total_traffic_mmt", "National Coastal Cargo Share: West Coast vs East Coast", None, None],
            ["radar", ["pol_share_pct", "bulk_cargo_share_pct", "container_share_pct"], None, "Aggregate Cargo Commodity Share Distribution (%)", None, None],
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
            ["Total Wireless Base", "total_wireless_sub_million", "latest", "{val:.1f} M", "Total Mobile Subscribers", "pos"],
            ["Broadband Connections", "broadband_sub_million", "latest", "{val:.1f} M", "High-Speed Internet Users", "pos"],
            ["National Teledensity", "overall_teledensity_pct", "latest", "{val:.1f}%", "Per 100 Inhabitants", "pos"],
            ["Rural Subscriber Share", "rural_sub_share_pct", "latest", "{val:.1f}%", "Rural Telephony Penetration", "neutral"],
            ["Urban Teledensity", "urban_teledensity_pct", "latest", "{val:.1f}%", "Metropolitan Saturation", "pos"],
        ],
        "charts": [
            ["line", "time_label", ["total_wireless_sub_million", "broadband_sub_million"], "Mobile Subscribers & Broadband Penetration Timeline", "Period", "Subscribers (Million)"],
            ["bar", "time_label", ["urban_sub_million", "rural_sub_million"], "Urban vs Rural Wireless Connection Composition", "Period", "Subscribers (Million)"],
            ["scatter", "broadband_sub_million", "overall_teledensity_pct", "Broadband Adoption vs Aggregate Teledensity Penetration", "Broadband (Million)", "Teledensity (%)"],
            ["area", "time_label", ["broadband_penetration_pct"], "Broadband Penetration Share of Total Wireless Base (%)", "Period", "Penetration (%)"],
            ["horizontal_bar", "overall_teledensity_pct", "time_label", "Overall Teledensity Progression Across Quarters", "Teledensity (%)", "Period"],
            ["line", "time_label", ["broadband_yoy_growth_pct"], "Broadband Year-on-Year Growth Dynamics (%)", "Period", "YoY Growth (%)"],
            ["radar", ["overall_teledensity_pct", "rural_sub_share_pct", "broadband_penetration_pct"], None, "National Digital Connectivity Equilibrium Profile", None, None],
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
            ["Peak Iron Ore Output", "iron_ore_million_mt", "max", "{val:.1f} MMT", "All-Time High Extraction", "pos"],
            ["Latest Iron Ore Output", "iron_ore_million_mt", "latest", "{val:.1f} MMT", "Most Recent Annual Output", "pos"],
            ["Limestone Extraction", "limestone_million_mt", "latest", "{val:.1f} MMT", "Cement Industry Feedstock", "pos"],
            ["Metallic Minerals Value", "total_metallic_value_billion_inr", "latest", "₹{val:.1f} B", "Gross Pithead Value", "pos"],
            ["Bauxite Production", "bauxite_million_mt", "latest", "{val:.1f} MMT", "Aluminum Feedstock Output", "neutral"],
        ],
        "charts": [
            ["line", "year", ["iron_ore_million_mt", "limestone_million_mt", "bauxite_million_mt"], "Core Industrial Mineral Production Volumes (MMT)", "Year", "Production (MMT)"],
            ["bar", "year", "total_metallic_value_billion_inr", "Gross Value of Metallic Mineral Output (Billion INR)", "Year", "Value (₹ Billion)"],
            ["scatter", "iron_ore_million_mt", "total_metallic_value_billion_inr", "Iron Ore Extraction Volume vs Total Metallic Sector Value", "Iron Ore (MMT)", "Value (₹ Billion)"],
            ["area", "year", ["total_bulk_minerals_mmt"], "Total Non-Fuel Bulk Mineral Output Trajectory (MMT)", "Year", "Total Minerals (MMT)"],
            ["horizontal_bar", "zinc_conc_million_mt", "year", "Zinc Concentrate Production Evolution (MMT)", "Zinc Conc (MMT)", "Year"],
            ["line", "year", ["iron_ore_yoy_growth_pct"], "Iron Ore Production Annual Growth Rate Volatility (%)", "Year", "YoY Growth (%)"],
            ["correlation_heatmap", ["iron_ore_million_mt", "bauxite_million_mt", "limestone_million_mt", "manganese_ore_million_mt", "total_metallic_value_billion_inr"], None, "Mineral Commodity Production Inter-Correlation", None, None],
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
            ["Total Forest Canopy", "total_forest_sqkm", "sum", "{val:,.0f} sq km", "Combined Forest Cover", "pos"],
            ["Largest Forest Estate", "total_forest_sqkm", "max", "{val:,.0f} sq km", "State with Max Forest Cover", "pos"],
            ["Total Forest Carbon Stock", "carbon_stock_million_tonnes", "sum", "{val:,.0f} MT", "Terrestrial Carbon Reservoir", "pos"],
            ["Very Dense Canopy Area", "very_dense_forest_sqkm", "sum", "{val:,.0f} sq km", "Pristine High-Canopy Cover", "pos"],
            ["Mean Forest Cover Ratio", "forest_cover_pct", "mean", "{val:.1f}%", "National Geographical Mean", "neutral"],
        ],
        "charts": [
            ["horizontal_bar", "total_forest_sqkm", "state", "Total Forest Cover by State (sq km)", "Forest Area (sq km)", "State"],
            ["scatter", "total_forest_sqkm", "carbon_stock_million_tonnes", "Forest Area vs Total Carbon Stock (Million Tonnes)", "Forest Area (sq km)", "Carbon Stock (MT)"],
            ["bar", "state", ["very_dense_forest_sqkm", "mod_dense_forest_sqkm", "open_forest_sqkm"], "Canopy Density Classification (VDF, MDF, OF) by State", "State", "Area (sq km)"],
            ["treemap", ["ecological_zone_tier", "state"], "carbon_stock_million_tonnes", "Forest Carbon Stock Concentration by Ecological Tier", None, None],
            ["box", "ecological_zone_tier", "forest_cover_pct", "Forest Cover Density (% Area) by Ecological Zone Tier", "Ecological Tier", "Forest Cover (%)"],
            ["histogram", "carbon_density_tonnes_per_sqkm", None, "Carbon Density (Tonnes Carbon / sq km) Spread", "Carbon Density (T/sq km)", "State Count"],
            ["radar", ["dense_canopy_ratio", "forest_cover_pct", "national_forest_share_pct"], None, "Forest Ecological Health and Canopy Integrity Radar", None, None],
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
            ["Peak POL Consumption", "pol_consumption_mmt", "max", "{val:.1f} MMT", "Record Petroleum Demand", "neg"],
            ["Latest Refinery Throughput", "refinery_throughput_mmt", "latest", "{val:.1f} MMT", "Domestic Refining Activity", "pos"],
            ["Crude Import Dependency", "import_dependency_pct", "latest", "{val:.1f}%", "External Supply Exposure", "neg"],
            ["Diesel Demand Dominance", "diesel_consumption_mmt", "latest", "{val:.1f} MMT", "Transport & Commercial Fuel", "neutral"],
            ["Domestic Crude Output", "crude_production_mmt", "latest", "{val:.1f} MMT", "Upstream Production", "neutral"],
        ],
        "charts": [
            ["line", "year", ["pol_consumption_mmt", "refinery_throughput_mmt", "crude_production_mmt"], "Petroleum Demand vs Refining Throughput and Domestic Crude Output", "Year", "Volume (MMT)"],
            ["bar", "year", ["diesel_consumption_mmt", "petrol_consumption_mmt", "lpg_consumption_mmt"], "Refined Product Consumption Breakdown (Diesel, Petrol, LPG)", "Year", "Consumption (MMT)"],
            ["scatter", "pol_consumption_mmt", "import_dependency_pct", "Aggregate Petroleum Demand vs Crude Import Dependency (%)", "Consumption (MMT)", "Import Dependency (%)"],
            ["area", "year", ["net_crude_deficit_mmt"], "Crude Oil Net Supply Deficit Expansion (MMT)", "Year", "Deficit (MMT)"],
            ["horizontal_bar", "import_dependency_pct", "year", "Evolution of Crude Oil Import Dependency Ratio (%)", "Import Dependency (%)", "Year"],
            ["line", "year", ["consumption_yoy_growth_pct"], "Petroleum Consumption Annual Growth Rate Volatility (%)", "Year", "YoY Growth (%)"],
            ["radar", ["import_dependency_pct", "diesel_share_pct", "cooking_fuel_lpg_share_pct"], None, "Hydrocarbon Fuel Security & Energy Demand Matrix", None, None],
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
            ["Total Registered IPC Crimes", "total_ipc_crimes", "sum", "{val:,.0f} Cases", "Recorded IPC Offenses", "neg"],
            ["Highest Crime Incidence", "total_ipc_crimes", "max", "{val:,.0f} Cases", "Peak State Volume", "neg"],
            ["Average Conviction Rate", "conviction_rate_pct", "mean", "{val:.1f}%", "Judicial Conviction Efficacy", "pos"],
            ["Average Chargesheet Rate", "chargesheet_rate_pct", "mean", "{val:.1f}%", "Police Investigation Rate", "pos"],
            ["Total Crimes Against Women", "crimes_against_women", "sum", "{val:,.0f} Cases", "Women Safety Offenses", "neg"],
        ],
        "charts": [
            ["horizontal_bar", "total_ipc_crimes", "state", "Total Registered IPC Offenses by State", "Cases Count", "State"],
            ["scatter", "chargesheet_rate_pct", "conviction_rate_pct", "Investigation Chargesheet Rate vs Judicial Conviction Rate", "Chargesheet Rate (%)", "Conviction Rate (%)"],
            ["bar", "state", ["crimes_against_women", "cyber_crimes"], "Incidence of Crimes Against Women and Cyber Offenses", "State", "Cases Count"],
            ["treemap", ["crime_severity_tier", "state"], "total_ipc_crimes", "Total IPC Offenses Distribution by Crime Severity Tier", None, None],
            ["box", "crime_severity_tier", "crime_rate_per_lakh", "Crime Rate per Lakh Population across Severity Tiers", "Severity Tier", "Crime Rate / Lakh"],
            ["histogram", "conviction_rate_pct", None, "Judicial Conviction Rate (%) Spread across States", "Conviction Rate (%)", "State Count"],
            ["radar", ["conviction_rate_pct", "chargesheet_rate_pct", "women_crime_share_pct"], None, "Judicial Efficacy and Law Enforcement Composite Profile", None, None],
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
            ["Houses Completed", "houses_completed_thousand", "sum", "{val:,.1f}K", "Delivered Pucca Houses", "pos"],
            ["Houses Sanctioned", "houses_sanctioned_thousand", "sum", "{val:,.1f}K", "Total Sanctioned Dwellings", "pos"],
            ["Mean Completion Rate", "completion_rate_pct", "mean", "{val:.1f}%", "Project Delivery Velocity", "pos"],
            ["Central Assistance Released", "central_assistance_crore", "sum", "₹{val:,.0f} Cr", "Disbursed Central Subsidy", "neutral"],
            ["Women Sole/Joint Ownership", "women_ownership_pct", "mean", "{val:.1f}%", "Gender Empowerment Titling", "pos"],
        ],
        "charts": [
            ["horizontal_bar", "houses_completed_thousand", "state", "PMAY Completed Houses by State (Thousands)", "Completed (Thousand)", "State"],
            ["scatter", "houses_sanctioned_thousand", "houses_completed_thousand", "Houses Sanctioned vs Houses Completed Correlation", "Sanctioned (K)", "Completed (K)"],
            ["bar", "state", ["houses_grounded_thousand", "houses_completed_thousand", "pipeline_houses_thousand"], "PMAY Project Pipeline: Grounded vs Completed vs Ongoing", "State", "Houses (K)"],
            ["treemap", ["state"], "central_assistance_crore", "Central Fiscal Assistance (₹ Cr) Distribution by State", None, None],
            ["box", "state", "women_ownership_pct", "Women Ownership Titling Rate (%) Distribution", "State", "Women Ownership (%)"],
            ["histogram", "completion_rate_pct", None, "PMAY State Completion Rate (%) Frequency Distribution", "Completion Rate (%)", "State Count"],
            ["radar", ["completion_rate_pct", "grounding_rate_pct", "women_ownership_pct"], None, "Social Housing Delivery and Inclusivity Scorecard", None, None],
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
            ["Tap Connections Provided", "fhtc_provided_lakh", "sum", "{val:,.1f} Lk", "Functional Tap Connections", "pos"],
            ["National Coverage Mean", "current_coverage_pct", "mean", "{val:.1f}%", "State Average Tap Coverage", "pos"],
            ["Pre-Mission Baseline", "baseline_2019_pct", "mean", "{val:.1f}%", "2019 Launch Baseline", "neutral"],
            ["Coverage Expansion Added", "coverage_expansion_percentage_points", "mean", "+{val:.1f} pp", "Net Percentage Point Gain", "pos"],
            ["Remaining Unconnected", "unconnected_households_lakh", "sum", "{val:,.1f} Lk", "Target Household Balance", "neutral"],
        ],
        "charts": [
            ["horizontal_bar", "current_coverage_pct", "state", "Rural Tap Water Coverage by State (%)", "Coverage (%)", "State"],
            ["scatter", "baseline_2019_pct", "current_coverage_pct", "2019 Baseline vs Current Tap Water Coverage (%)", "Baseline 2019 (%)", "Current Coverage (%)"],
            ["bar", "state", ["fhtc_provided_lakh", "unconnected_households_lakh"], "Connected vs Remaining Unconnected Rural Households (Lakh)", "State", "Households (Lakh)"],
            ["treemap", ["saturation_status", "state"], "fhtc_provided_lakh", "Tap Connections Grouped by Mission Saturation Tier", None, None],
            ["box", "saturation_status", "coverage_expansion_percentage_points", "Expansion Gain (pp) by Saturation Milestone", "Status", "Gain (pp)"],
            ["histogram", "growth_multiplier", None, "Tap Connection Coverage Growth Multiplier Spread", "Multiplier", "Frequency"],
            ["radar", ["current_coverage_pct", "certified_har_ghar_jal_pct", "coverage_expansion_percentage_points"], None, "Har Ghar Jal Mission Saturation and Momentum Index", None, None],
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
            ["Electricity Coverage", "electricity_avail_pct", "mean", "{val:.1f}%", "Schools with Power", "pos"],
            ["Drinking Water Coverage", "drinking_water_avail_pct", "mean", "{val:.1f}%", "Schools with Piped Water", "pos"],
            ["Girls Toilet Availability", "girls_toilet_avail_pct", "mean", "{val:.1f}%", "Dedicated Sanitation", "pos"],
            ["Digital Computing Access", "computer_facility_pct", "mean", "{val:.1f}%", "Schools with Computers", "neutral"],
            ["Mean Primary PTR", "ptr_primary", "mean", "{val:.1f}:1", "Pupil-Teacher Ratio", "pos"],
        ],
        "charts": [
            ["horizontal_bar", "basic_amenities_composite_pct", "state", "School Basic Amenities Composite Index by State (%)", "Composite Score (%)", "State"],
            ["scatter", "ptr_primary", "digital_readiness_composite_pct", "Pupil-Teacher Ratio vs Digital Infrastructure Readiness (%)", "PTR Primary", "Digital Readiness (%)"],
            ["bar", "state", ["electricity_avail_pct", "drinking_water_avail_pct", "girls_toilet_avail_pct"], "Essential School Amenities Parity across States (%)", "State", "Availability (%)"],
            ["treemap", ["infrastructure_parity_tier", "state"], "ptr_primary", "Primary PTR Distribution Grouped by Infrastructure Parity Tier", None, None],
            ["box", "infrastructure_parity_tier", "digital_readiness_composite_pct", "Digital Facility Availability by Infrastructure Parity Tier", "Parity Tier", "Digital Readiness (%)"],
            ["histogram", "ptr_upper_primary", None, "Upper Primary Pupil-Teacher Ratio (PTR) Distribution", "PTR Ratio", "State Count"],
            ["radar", ["electricity_avail_pct", "drinking_water_avail_pct", "girls_toilet_avail_pct", "computer_facility_pct", "internet_facility_pct"], None, "National School Physical and Digital Infrastructure Profile", None, None],
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
            ["Peak Foreign Arrivals", "foreign_tourist_arrivals_million", "max", "{val:.2f} M", "Highest Recorded Arrivals", "pos"],
            ["Foreign Exchange Earnings", "foreign_exchange_earnings_usd_billion", "latest", "${val:.1f} B", "Annual Services Forex", "pos"],
            ["Domestic Visits Footfall", "domestic_tourist_visits_million", "latest", "{val:,.0f} M", "Internal Tourism Scale", "pos"],
            ["Spend per Foreign Tourist", "fee_per_foreign_tourist_usd", "latest", "${val:,.0f}", "Average Inbound Expenditure", "pos"],
            ["Medical Tourism Share", "medical_tourism_share_pct", "latest", "{val:.1f}%", "High-Value Health Inflow", "pos"],
        ],
        "charts": [
            ["line", "year", ["foreign_tourist_arrivals_million"], "Inbound Foreign Tourist Arrivals (FTA) Trajectory (Million)", "Year", "Arrivals (Million)"],
            ["bar", "year", "foreign_exchange_earnings_usd_billion", "Foreign Exchange Earnings from Tourism (Billion USD)", "Year", "FEE (USD Billion)"],
            ["area", "year", ["domestic_tourist_visits_million"], "Domestic Tourist Visits (DTV) Expansion Over Time (Million)", "Year", "Visits (Million)"],
            ["scatter", "foreign_tourist_arrivals_million", "foreign_exchange_earnings_usd_billion", "Tourist Arrivals vs Inbound Foreign Exchange Earnings", "Arrivals (M)", "Earnings ($B)"],
            ["horizontal_bar", "fee_per_foreign_tourist_usd", "year", "Average Foreign Exchange Earnings per Inbound Tourist (USD)", "Spend ($)", "Year"],
            ["line", "year", ["fta_yoy_growth_pct"], "Annual Foreign Tourist Arrivals Growth Volatility (%)", "Year", "YoY Growth (%)"],
            ["radar", ["top_state_share_pct", "medical_tourism_share_pct"], None, "Tourism Economic Concentration and Specialization Indicators", None, None],
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
            ["Peak Welfare Offtake", "total_offtake_million_mt", "max", "{val:.1f} MMT", "Maximum Annual Distribution", "pos"],
            ["Latest Foodgrain Offtake", "total_offtake_million_mt", "latest", "{val:.1f} MMT", "Public Distribution Vol", "pos"],
            ["Central Buffer Stock", "central_buffer_stock_million_mt", "latest", "{val:.1f} MMT", "Strategic Food Reserve", "pos"],
            ["Annual Food Subsidy", "food_subsidy_thousand_crore", "latest", "₹{val:.1f}K Cr", "Union Budget NFSA Outlay", "neutral"],
            ["Biometric PDS E-PoS", "aadhaar_authenticated_pds_pct", "latest", "{val:.1f}%", "Aadhaar e-PoS Authentication", "pos"],
        ],
        "charts": [
            ["line", "year", ["total_offtake_million_mt", "central_buffer_stock_million_mt"], "Foodgrain PDS Offtake vs Central Pool Buffer Stocks (MMT)", "Year", "Grain (Million MT)"],
            ["bar", "year", ["rice_offtake_million_mt", "wheat_offtake_million_mt"], "PDS Grain Allocation Deconstruction: Rice vs Wheat", "Year", "Grain (Million MT)"],
            ["scatter", "total_offtake_million_mt", "food_subsidy_thousand_crore", "Grain Distributed vs Food Subsidy Budget Expenditure", "Offtake (MMT)", "Subsidy (₹K Cr)"],
            ["area", "year", ["rice_share_pct", "wheat_share_pct"], "Proportional Composition of Grain Distribution (% Rice vs Wheat)", "Year", "Share (%)"],
            ["horizontal_bar", "aadhaar_authenticated_pds_pct", "year", "Aadhaar-Authenticated Fair Price Shop Digitization (%)", "e-PoS Rate (%)", "Year"],
            ["line", "year", ["subsidy_per_mt_inr"], "Implicit Economic Cost / Subsidy Burden per MT Grain (₹ INR)", "Year", "Subsidy / MT (₹)"],
            ["radar", ["rice_share_pct", "wheat_share_pct", "aadhaar_authenticated_pds_pct"], None, "Food Security Strategic Logistics & Integrity Indicators", None, None],
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
            ["Peak Patent Filings", "patents_filed", "max", "{val:,.0f} Filings", "All-Time High Annual Patents", "pos"],
            ["Latest Patents Granted", "patents_granted", "latest", "{val:,.0f} Grants", "Annual Patent Approvals", "pos"],
            ["Domestic Filings Share", "domestic_share_pct", "latest", "{val:.1f}%", "Resident Inventor Dominance", "pos"],
            ["Trademark Filings", "trademark_applications", "latest", "{val:,.0f} Marks", "Annual Commercial Brands", "pos"],
            ["Grant to Filing Efficiency", "grant_to_filing_ratio_pct", "latest", "{val:.1f}%", "Examination & Grant Yield", "pos"],
        ],
        "charts": [
            ["line", "year", ["patents_filed", "patents_granted"], "Patent Applications Filed vs Patents Granted Over Time", "Year", "Number of Patents"],
            ["bar", "year", ["domestic_filed", "foreign_filed"], "Domestic Resident vs Foreign Patent Application Origination", "Year", "Filings Count"],
            ["scatter", "patents_filed", "patents_granted", "Patent Filing Volume vs Institutional Patent Grant Yield", "Filings", "Grants"],
            ["area", "year", ["domestic_share_pct"], "Domestic Resident Inventor Share of Total Filings (%)", "Year", "Resident Share (%)"],
            ["horizontal_bar", "trademark_applications", "year", "Trademark Applications Filed Timeline Comparison", "Trademarks Count", "Year"],
            ["line", "year", ["patent_filings_yoy_growth_pct", "grants_yoy_growth_pct"], "Year-on-Year Growth Rates: Applications vs Grant Decisions (%)", "Year", "YoY Growth (%)"],
            ["radar", ["domestic_share_pct", "grant_to_filing_ratio_pct", "domestic_to_foreign_ratio"], None, "National Innovation and IP Examination Capability Radar", None, None],
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
            ["Beneficiary Farmers", "farmer_beneficiaries_lakh", "sum", "{val:,.1f} Lk", "Enrolled Agrarian Households", "pos"],
            ["Cumulative DBT Disbursed", "cumulative_dbt_crore", "sum", "₹{val:,.0f} Cr", "Total Direct Income Support", "pos"],
            ["Mean eKYC Verification", "ekyc_authenticated_pct", "mean", "{val:.1f}%", "Biometric/OTP Compliance", "pos"],
            ["Aadhaar Bank Seeding", "aadhaar_seeded_pct", "mean", "{val:.1f}%", "APBS DBT Readiness", "pos"],
            ["Women Farmer Beneficiaries", "women_farmers_pct", "mean", "{val:.1f}%", "Female Landholder Inclusion", "pos"],
        ],
        "charts": [
            ["horizontal_bar", "farmer_beneficiaries_lakh", "state", "PM-KISAN Registered Farmers by State (Lakh)", "Farmers (Lakh)", "State"],
            ["scatter", "farmer_beneficiaries_lakh", "cumulative_dbt_crore", "Farmer Beneficiary Scale vs Cumulative Cash Outlay (₹ Cr)", "Farmers (Lakh)", "Disbursal (₹ Cr)"],
            ["bar", "state", "cumulative_dbt_crore", "State-wise Cumulative DBT Cash Disbursed to Farmers (₹ Cr)", "State", "Disbursal (₹ Cr)"],
            ["treemap", ["beneficiary_scale_tier", "state"], "cumulative_dbt_crore", "Direct Benefit Transfers Grouped by State Scale Tier", None, None],
            ["box", "beneficiary_scale_tier", "women_farmers_pct", "Women Farmer Inclusion Share (%) by Beneficiary Scale Tier", "Scale Tier", "Women Share (%)"],
            ["histogram", "digital_compliance_score", None, "State Digital Compliance Composite Index Spread", "Compliance Index", "Frequency"],
            ["radar", ["ekyc_authenticated_pct", "aadhaar_seeded_pct", "women_farmers_pct"], None, "Direct Benefit Transfer Delivery Integrity Framework", None, None],
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
            ["Peak Auto Production", "total_production_million", "max", "{val:.2f} M", "Highest Recorded Output", "pos"],
            ["Latest Auto Production", "total_production_million", "latest", "{val:.2f} M", "Latest Recorded Production", "pos"],
            ["Domestic Vehicle Sales", "domestic_sales_million", "latest", "{val:.2f} M", "Domestic Market Absorption", "pos"],
            ["Automotive Exports", "total_exports_million", "latest", "{val:.2f} M", "Overseas Shipments", "pos"],
            ["Passenger Vehicle Share", "pv_share_of_production_pct", "latest", "{val:.1f}%", "Cars & SUVs of Total Auto", "neutral"],
        ],
        "charts": [
            ["line", "year", ["total_production_million", "domestic_sales_million", "total_exports_million"], "Automotive Production, Domestic Sales & Export Trajectories", "Year", "Vehicles (Million)"],
            ["bar", "year", ["pv_production_million", "cv_production_million", "three_wheeler_million", "two_wheeler_million"], "Vehicle Production Segment Disaggregation (PV, CV, 3W, 2W)", "Year", "Vehicles (Million)"],
            ["scatter", "domestic_sales_million", "total_exports_million", "Domestic Sales Demand vs Global Export Shipments", "Domestic Sales (M)", "Exports (M)"],
            ["area", "year", ["export_intensity_pct"], "Automotive Export Intensity Share of Production (%)", "Year", "Export Intensity (%)"],
            ["horizontal_bar", "total_production_million", "year", "Annual Vehicle Production Volume Timeline Ranking", "Production (M)", "Year"],
            ["line", "year", ["production_yoy_growth_pct"], "Automotive Production Year-on-Year Growth Volatility (%)", "Year", "YoY Growth (%)"],
            ["radar", ["pv_share_of_production_pct", "two_wheeler_share_pct", "export_intensity_pct"], None, "Automotive Manufacturing Segment Concentration Profile", None, None],
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
            ["Peak Raw Coal Output", "total_raw_coal_production_mt", "max", "{val:.1f} MT", "All-Time High Extraction", "pos"],
            ["Power Sector Dispatch", "power_sector_dispatch_mt", "latest", "{val:.1f} MT", "Thermal Power Supply", "pos"],
            ["Coal India Ltd Share", "cil_share_pct", "latest", "{val:.1f}%", "National CIL Monopoly Share", "neutral"],
            ["Coal Import Volume", "coal_imports_mt", "latest", "{val:.1f} MT", "External Coal Inflows", "neg"],
            ["Power Baseload Share", "power_sector_share_pct", "latest", "{val:.1f}%", "Grid Dispatch Allocation", "neutral"],
        ],
        "charts": [
            ["line", "year", ["total_raw_coal_production_mt", "cil_production_mt", "power_sector_dispatch_mt"], "Domestic Coal Production & Power Dispatch Trajectories (MT)", "Year", "Coal (Million Tonnes)"],
            ["bar", "year", ["cil_production_mt", "non_cil_production_mt"], "Coal Production: Coal India Ltd (CIL) vs Captive/Commercial Miners", "Year", "Production (MT)"],
            ["scatter", "total_raw_coal_production_mt", "power_sector_dispatch_mt", "Domestic Coal Output vs Thermal Power Plant Dispatch", "Production (MT)", "Power Dispatch (MT)"],
            ["area", "year", ["coal_imports_mt"], "Coal Import Volumes Inflow Over Time (Million Tonnes)", "Year", "Imports (MT)"],
            ["horizontal_bar", "pithead_stock_mt", "year", "Pithead Coal Inventory Stock Levels Timeline (MT)", "Pithead Stock (MT)", "Year"],
            ["line", "year", ["power_dispatch_yoy_growth_pct"], "Power Sector Coal Supply Annual Growth Rate (%)", "Year", "YoY Growth (%)"],
            ["radar", ["power_sector_share_pct", "cil_share_pct", "import_to_domestic_ratio"], None, "Coal Baseload Energy Security & Domestic Self-Reliance Radar", None, None],
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
            ["Peak Waterway Cargo", "total_waterway_cargo_mmt", "max", "{val:.1f} MMT", "Highest Cargo Volume", "pos"],
            ["Latest Cargo Volume", "total_waterway_cargo_mmt", "latest", "{val:.1f} MMT", "Latest Freight Movement", "pos"],
            ["National Waterway 1 (Ganga)", "nw1_ganga_mmt", "latest", "{val:.2f} MMT", "NW-1 Haldia-Varanasi", "pos"],
            ["NW-2 Brahmaputra Cargo", "nw2_brahmaputra_mmt", "latest", "{val:.2f} MMT", "NW-2 Dhubri-Sadiya", "pos"],
            ["Coastal & Tidal Cargo", "tidal_coastal_cargo_mmt", "latest", "{val:.1f} MMT", "Goa & Maharashtra Waterways", "neutral"],
        ],
        "charts": [
            ["line", "year", ["total_waterway_cargo_mmt"], "Inland Waterways Cargo Traffic Growth Trajectory (MMT)", "Year", "Cargo (Million MT)"],
            ["bar", "year", ["nw1_ganga_mmt", "nw2_brahmaputra_mmt", "nw3_west_coast_mmt"], "Priority National Waterways Cargo Comparison (NW-1, NW-2, NW-3)", "Year", "Cargo (Million MT)"],
            ["scatter", "nw1_ganga_mmt", "total_waterway_cargo_mmt", "NW-1 Ganga Freight Volume vs Aggregate National Waterway Traffic", "NW-1 (MMT)", "Total Cargo (MMT)"],
            ["area", "year", ["goa_waterways_mmt", "maharashtra_waterways_mmt"], "Tidal Waterway Mining & Coastal Freight (Goa & Maharashtra)", "Year", "Cargo (MMT)"],
            ["horizontal_bar", "total_waterway_cargo_mmt", "year", "Annual Waterway Cargo Ranking Timeline (MMT)", "Cargo (MMT)", "Year"],
            ["line", "year", ["cargo_yoy_growth_pct"], "Inland Waterway Freight Annual Growth Rate Volatility (%)", "Year", "YoY Growth (%)"],
            ["radar", ["nw1_ganga_share_pct", "nw2_brahmaputra_share_pct", "nw1_to_nw2_ratio"], None, "National Inland Waterways Freight Utilization Profile", None, None],
        ]
    }
]

def update_build_dashboards_py():
    with open("scripts/build_dashboards.py", "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Update BRIEFING_CONTEXT
    # Find the end of BRIEFING_CONTEXT dictionary
    marker_briefing = '"D34": ('
    if marker_briefing in content and '"D35": (' not in content:
        # Find closing paren and comma for D34
        idx = content.find(marker_briefing)
        end_d34 = content.find(')\n}', idx)
        if end_d34 != -1:
            insertion_briefing = "),\n"
            for did, (why, note) in NEW_BRIEFINGS.items():
                why_escaped = why.replace('"', '\\"')
                note_escaped = note.replace('"', '\\"')
                insertion_briefing += f'    "{did}": (\n        "{why_escaped}",\n        "{note_escaped}"\n    ),\n'
            insertion_briefing = insertion_briefing.rstrip(",\n") + "\n"
            content = content[:end_d34] + insertion_briefing + content[end_d34+1:]
            print("Successfully injected D35-D54 into BRIEFING_CONTEXT")
        else:
            print("Could not find end of D34 in BRIEFING_CONTEXT")
    elif '"D35": (' in content:
        print("D35 already present in BRIEFING_CONTEXT")

    # 2. Update DASHBOARD_SPECS
    marker_specs = "'id': 'D34'"
    if marker_specs in content and "'id': 'D35'" not in content and '"id": "D35"' not in content:
        idx_spec = content.find(marker_specs)
        end_d34_spec = content.find('}]', idx_spec)
        if end_d34_spec != -1:
            import json
            insertion_specs = "},\n"
            for spec in NEW_SPECS:
                formatted_spec = json.dumps(spec, indent=4)
                # Indent by 4 spaces
                indented = "\n".join("    " + line for line in formatted_spec.split("\n"))
                insertion_specs += indented + ",\n"
            insertion_specs = insertion_specs.rstrip(",\n") + "\n"
            # end_d34_spec points to '}]', we replace '}' with '}' + insertion_specs
            content = content[:end_d34_spec+1] + insertion_specs + content[end_d34_spec+1:]
            print("Successfully injected D35-D54 into DASHBOARD_SPECS")
        else:
            print("Could not find end of D34 in DASHBOARD_SPECS")
    elif "'id': 'D35'" in content or '"id": "D35"' in content:
        print("D35 already present in DASHBOARD_SPECS")

    # Update summary message if it says 34
    content = content.replace("All 34 Dashboard Modules Generated Successfully", "All 54 Dashboard Modules Generated Successfully")

    with open("scripts/build_dashboards.py", "w", encoding="utf-8") as f:
        f.write(content)
    print("scripts/build_dashboards.py written successfully.")

if __name__ == "__main__":
    update_build_dashboards_py()
    # Now run build_dashboards
    sys.path.insert(0, os.path.abspath("."))
    import scripts.build_dashboards as bd
    print(f"Total DASHBOARD_SPECS now: {len(bd.DASHBOARD_SPECS)}")
    print(f"Total BRIEFING_CONTEXT now: {len(bd.BRIEFING_CONTEXT)}")
    bd.build_all()
