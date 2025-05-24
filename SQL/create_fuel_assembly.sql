-- SQL schema for the nuclear fuel assembly dataset (normalized, with primary keys and foreign keys)

CREATE TABLE PLANTS (
    id SERIAL PRIMARY KEY,
    plant_name VARCHAR(32),
    reactor_location_id INTEGER REFERENCES REACTOR_LOCATIONS(id)
);

CREATE TABLE REACTOR_DESIGN (
    id SERIAL PRIMARY KEY,
    reactor_power INTEGER,
    reactor_type VARCHAR(4)
);

CREATE TABLE EPOCHS (
    id SERIAL PRIMARY KEY,
    epoch VARCHAR(8)
);

CREATE TABLE FUEL_ASSEMBLY (
    id SERIAL PRIMARY KEY,
    FA_name VARCHAR(8),
    FA_mass FLOAT,
    FA_length_ft INTEGER,
    FA_manufacturing_year INTEGER,
    FA_BUp FLOAT,
    reactor_design_id INTEGER REFERENCES REACTOR_DESIGN(id),
    plant_id INTEGER REFERENCES PLANTS(id),
    epoch_id INTEGER REFERENCES EPOCHS(id),
    introduction_year INTEGER
);

CREATE TABLE REACTOR_LOCATIONS (
    id SERIAL PRIMARY KEY,
    reactor_location VARCHAR(32)
);

-- Foreign keys in FUEL_ASSEMBLY reference the primary keys of the other tables, establishing relationships between assemblies, cores, sites, locations, and epochs.
