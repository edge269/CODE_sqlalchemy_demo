-- SQL schema for the nuclear fuel assembly dataset (normalized, with primary keys and foreign keys)

CREATE TABLE FUEL_ASSEMBLY (
    id SERIAL PRIMARY KEY,
    FA_name VARCHAR(8),
    FA_mass FLOAT,
    FA_length_ft INTEGER,
    FA_manufacturing_year INTEGER,
    FA_BUp FLOAT,
    reactor_core_id INTEGER REFERENCES REACTOR_CORE(id), -- FK to REACTOR_CORE
    reactor_site_id INTEGER REFERENCES REACTOR_SITES(id), -- FK to REACTOR_SITES
    reactor_epoch_id INTEGER REFERENCES REACTOR_EPOCHS(id), -- FK to REACTOR_EPOCHS
    introduction_year INTEGER
);

CREATE TABLE REACTOR_CORE (
    id SERIAL PRIMARY KEY,
    reactor_power INTEGER,
    reactor_type VARCHAR(4)
);

CREATE TABLE REACTOR_SITES (
    id SERIAL PRIMARY KEY,
    reactor_site VARCHAR(32),
    reactor_location_id INTEGER REFERENCES REACTOR_LOCATIONS(id) -- FK to REACTOR_LOCATIONS
);

CREATE TABLE REACTOR_LOCATIONS (
    id SERIAL PRIMARY KEY,
    reactor_location VARCHAR(32)
);

CREATE TABLE REACTOR_EPOCHS (
    id SERIAL PRIMARY KEY,
    epoch VARCHAR(8)
);

-- Foreign keys in FUEL_ASSEMBLY reference the primary keys of the other tables, establishing relationships between assemblies, cores, sites, locations, and epochs.
