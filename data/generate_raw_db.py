import pandas as pd
import numpy as np
import random
import string

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

# Function to generate a random FA mass
def generate_fa_mass():
    return round(np.random.normal(750, 25), 1)

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

# Function to generate a random FA BUp
def generate_fa_bup():
    return round(random.uniform(0, 72), 1)

# Function to determine reactor epoch based on introduction year
def determine_reactor_epoch(introduction_year):
    current_year = 2025  # Assuming the current year is 2025 for this example
    decade_count = (current_year - introduction_year) // 10 + 1
    return f"VD{decade_count}"

# Generate data
data = []
existing_names = set()  # Set to keep track of existing FA names
for _ in range(10000):  # Generate 10,000 rows of data
    fa_name = generate_unique_fa_name(existing_names)
    fa_mass = generate_fa_mass()
    fa_introduction_year = generate_fa_introduction_year()
    reactor_power = determine_reactor_power(fa_introduction_year)
    reactor_type, _ = reactor_power_types[reactor_power]  # Extract only the reactor type
    fuel_type = determine_fuel_type(reactor_power, fa_introduction_year)
    site_code, (reactor_site, reactor_location) = random.choice(list(reactor_sites.items()))
    fa_manufacturing_year = generate_fa_manufacturing_year(fa_introduction_year)
    fa_bup = generate_fa_bup()
    reactor_epoch = determine_reactor_epoch(fa_introduction_year)
    
    data.append([
        fa_name, fa_mass, fa_manufacturing_year, fa_introduction_year,
        reactor_power, reactor_type, fuel_type, site_code,
        reactor_location, fa_bup, reactor_epoch
    ])

# Create a DataFrame
columns = [
    "FA_name", "FA_mass", "FA_manufacturing_year", "FA_introduction_year",
    "reactor_power", "reactor_type", "fuel_type", "reactor_site",
    "reactor_location", "FA_BUp", "reactor_epoch"
]
df = pd.DataFrame(data, columns=columns)

# Save to Excel
df.to_excel("nuclear_data.xlsx", index=False)

print("Excel file 'nuclear_data.xlsx' has been generated successfully.")
