-- SQL schema for the nuclear fuel assembly dataset (Oracle version)

CREATE TABLE LOCATIONS (
    id NUMBER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    location VARCHAR2(32) NOT NULL
);

CREATE TABLE EPOCHS (
    id NUMBER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    epoch VARCHAR2(8) NOT NULL
);

CREATE TABLE REACTOR_DESIGN (
    id NUMBER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    reactor_power NUMBER(6) NOT NULL,
    reactor_type VARCHAR2(4) NOT NULL
);

CREATE TABLE PLANTS (
    id NUMBER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    plant_name VARCHAR2(32) NOT NULL,
    location_id NUMBER NOT NULL,
    CONSTRAINT fk_location FOREIGN KEY (location_id) REFERENCES LOCATIONS(id)
);

CREATE TABLE FUEL_ASSEMBLY (
    id NUMBER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    FA_name VARCHAR2(8) NOT NULL,
    FA_mass FLOAT NOT NULL,
    FA_length_ft NUMBER(2) NOT NULL,
    FA_manufacturing_year NUMBER(4) NOT NULL,
    FA_BUp FLOAT NOT NULL,
    reactor_design_id NUMBER NOT NULL,
    plant_id NUMBER NOT NULL,
    epoch_id NUMBER NOT NULL,
    introduction_year NUMBER(4) NOT NULL,
    CONSTRAINT fk_design FOREIGN KEY (reactor_design_id) REFERENCES REACTOR_DESIGN(id),
    CONSTRAINT fk_plant FOREIGN KEY (plant_id) REFERENCES PLANTS(id),
    CONSTRAINT fk_epoch FOREIGN KEY (epoch_id) REFERENCES EPOCHS(id)
);
