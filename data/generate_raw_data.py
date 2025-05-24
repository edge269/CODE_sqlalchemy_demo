import pandas as pd
import numpy as np
import random
import string

# Allow for a random seed to be set by the user
RANDOM_SEED = 42  # Set to 42 for the current demo; user can change as needed
random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)

# Define the list of French nuclear reactors and their locations
reactor_sites = {
    "CHI": ("Chinon", "Centre-Val de Loire"),
    "CIV": ("Civaux", "Nouvelle-Aquitaine"),
    "CRU": ("Cruas", "Auvergne-Rhône-Alpes"),
    "DAM": ("Dampierre", "Centre-Val de Loire"),
    "FES": ("Fessenheim", "Grand Est"),
    "FLA": ("Flamanville", "Normandy"),
    "GOL": ("Golfech", "Occitanie"),
    "GRA": ("Gravelines", "Hauts-de-France"),
    "NOG": ("Nogent", "Île-de-France"),
    "PAL": ("Paluel", "Normandy"),
    "PEN": ("Penly", "Normandy"),
    "SAL": ("Saint-Alban", "Auvergne-Rhône-Alpes"),
    "STL": ("Saint-Laurent", "Centre-Val de Loire"),
    "TRI": ("Tricastin", "Auvergne-Rhône-Alpes"),
}

# Mapping of reactor sites to allowed reactor powers and operation start year
site_reactor_power_map = {
    "CHI": {"powers": {900: 1983}},  # Chinon (CPY)
    "CIV": {"powers": {1450: 1998}},  # Civaux (N4)
    "CRU": {"powers": {900: 1984}},  # Cruas (CPY)
    "DAM": {"powers": {900: 1980}},  # Dampierre (CPY)
    "FES": {"powers": {900: 1977}},  # Fessenheim (CPY, historical)
    "FLA": {"powers": {1300: 1986, 1600: 2025}},  # Flamanville (1300, EPR)
    "GOL": {"powers": {1300: 1993}},  # Golfech (P'4)
    "GRA": {"powers": {900: 1980}},  # Gravelines (CPY)
    "NOG": {"powers": {1300: 1987}},  # Nogent (P'4)
    "PAL": {"powers": {1300: 1984}},  # Paluel (P4)
    "PEN": {"powers": {1300: 1990}},  # Penly (P'4)
    "SAL": {"powers": {1300: 1986}},  # Saint-Alban (P4)
    "STL": {"powers": {900: 1981}},  # Saint-Laurent (CPY)
    "TRI": {"powers": {900: 1980}},  # Tricastin (CPY)
}

# Define reactor power and types with their initial operation years
reactor_power_types = {
    900: ("CPY", 1980),
    1300: ("DPY", 1990),
    1450: ("PQY", 2000),
    1600: ("EPR", 2010)
}

# Function to generate a unique FA name
def generate_unique_fa_name(existing_names):
    while True:
        letter = random.choice(string.ascii_uppercase)
        number = random.randint(1000, 9999)
        fa_name = f"F{letter}{number}"
        if fa_name not in existing_names:
            existing_names.add(fa_name)
            return fa_name

# Function to determine FA length based on reactor power
def determine_fa_length_ft(reactor_power):
    if reactor_power == 900:
        return 12
    else:
        return 14

# Function to generate a random FA mass based on FA length
def generate_fa_mass(fa_length_ft):
    if fa_length_ft == 12:
        mean = 750
        std = 25
    else:  # 14 ft
        mean = 750 * 14 / 12
        std = 25 * 14 / 12
    return round(np.random.normal(mean, std), 1)

# Function to generate a random FA introduction year
def generate_fa_introduction_year():
    return random.randint(1970, 2025)

# Function to determine reactor power based on introduction year
def determine_reactor_power(introduction_year):
    if 1970 <= introduction_year < 1980:
        return 900
    elif 1980 <= introduction_year < 1990:
        return random.choice([900, 1300])
    elif 1990 <= introduction_year < 2010:
        return random.choice([900, 1300, 1450])
    else:
        return random.choice([900, 1300, 1450, 1600])

# Function to determine fuel type based on reactor power and introduction year
def determine_fuel_type(reactor_power, introduction_year):
    if reactor_power == 900 and introduction_year >= 1995:
        return random.choice(["UO2", "MOX"])
    elif reactor_power == 900:
        return "UO2"
    else:
        return "UO2"

# Function to generate a random FA manufacturing year
def generate_fa_manufacturing_year(introduction_year):
    return introduction_year - random.randint(0, 5)

# Function to generate a random FA BUp based on mass, reactor type, and epoch
def generate_fa_bup(fa_mass, reactor_power, reactor_epoch):
    # Base BUp: linear with mass (normalized to 0-72 GWd/tM)
    min_mass = 750  # 12ft mean
    max_mass = 875  # 14ft mean
    base_bup = 72 * (fa_mass - min_mass) / (max_mass - min_mass)
    base_bup += np.random.normal(0, 2)  # add some randomness (std=2)
    base_bup = max(0, min(base_bup, 72))

    # Reactor type factor: 1300, 1450, 1600 MWe allow up to 20% more BUp
    if reactor_power in [1300, 1450, 1600]:
        type_factor = 1.2 + np.random.normal(0, 0.03)  # 20% more, slight randomness
    else:
        type_factor = 1.0 + np.random.normal(0, 0.05)  # more randomness for 900 MWe
    bup_type = base_bup * type_factor
    bup_type = max(0, min(bup_type, 72))

    # Reactor epoch factor: +2% per epoch (VDn), slight randomness
    try:
        epoch_num = int(reactor_epoch[2:])
    except Exception:
        epoch_num = 1
    epoch_factor = 1 + 0.02 * epoch_num + np.random.normal(0, 0.005)
    bup_final = bup_type * epoch_factor
    bup_final = max(0, min(bup_final, 72))
    return round(bup_final, 1)

# Function to determine reactor epoch based on introduction year
def determine_reactor_epoch(introduction_year):
    current_year = 2025  # Assuming the current year is 2025 for this example
    decade_count = (current_year - introduction_year) // 10 + 1
    return f"VD{decade_count}"

# Generate data
data = []
existing_names = set()  # Set to keep track of existing FA names
for _ in range(10000):  # Generate 10,000 rows of data
    site_code, (reactor_site, reactor_location) = random.choice(list(reactor_sites.items()))
    site_info = site_reactor_power_map.get(site_code, {"powers": {900: 1980}})
    allowed_powers = list(site_info["powers"].keys())
    reactor_power = random.choice(allowed_powers)
    # Get the correct start year for the chosen power at this site
    site_start_year = site_info["powers"][reactor_power]
    fa_length_ft = determine_fa_length_ft(reactor_power)
    fa_mass = generate_fa_mass(fa_length_ft)
    fa_name = generate_unique_fa_name(existing_names)
    # Introduction year must be >= site_start_year for the chosen power
    fa_introduction_year = random.randint(site_start_year, 2025)
    reactor_type, _ = reactor_power_types[reactor_power]  # Extract only the reactor type
    fuel_type = determine_fuel_type(reactor_power, fa_introduction_year)
    fa_manufacturing_year = generate_fa_manufacturing_year(fa_introduction_year)
    reactor_epoch = determine_reactor_epoch(fa_introduction_year)
    fa_bup = generate_fa_bup(fa_mass, reactor_power, reactor_epoch)
    
    data.append([
        fa_name, fa_mass, fa_length_ft, fa_manufacturing_year, fa_introduction_year,
        reactor_power, reactor_type, fuel_type, site_code,
        reactor_location, fa_bup, reactor_epoch
    ])

# Create a DataFrame with different (denormalized) columns for the CSV/Excel output
csv_columns = [
    "FA_name", "FA_mass_kg", "FA_length_ft", "FA_year_made", "FA_year_intro", "reactor_power_MWe",
    "reactor_type_code", "fuel_type", "plant_code", "plant_name", "region", "burnup_GWd_tU", "epoch_label",
    # Add a combined field for demo
    "plant_and_region"
]
csv_data = []
for row in data:
    # row: [fa_name, fa_mass, fa_length_ft, fa_manufacturing_year, fa_introduction_year, reactor_power, reactor_type, fuel_type, site_code, reactor_location, fa_bup, reactor_epoch]
    plant_and_region = f"{row[8]} ({row[9]})"
    csv_data.append([
        row[0], row[1], row[2], row[3], row[4], row[5],
        row[6], row[7], row[8], row[8], row[9], row[10], row[11],
        plant_and_region
    ])
df_csv = pd.DataFrame(csv_data, columns=csv_columns)

# Save to Excel
excel_path = "data/plants_data.xlsx"
df_csv.to_excel(excel_path, index=False)

# Optionally save to CSV
csv_path = "data/plants_data.csv"
df_csv.to_csv(csv_path, index=False)

print(f"Excel file '{excel_path}' and CSV file '{csv_path}' have been generated successfully.")
