# SQL Table and Dependency Rules for Nuclear Fuel Assembly Data

This document describes the main entities, their relationships, and the dependencies for the SQL schema representing the nuclear fuel assembly dataset. These rules are written in plain English and are intended to guide the SQL table design and constraints.

## Entities

- **FUEL_ASSEMBLY**: Stores information about each fuel assembly, including name, mass, length, manufacturing year, burnup, and introduction year. Each fuel assembly references a reactor core, a reactor site, and a reactor epoch via foreign keys.
- **REACTOR_CORE**: Stores information about reactor cores, including power and type.
- **REACTOR_SITES**: Stores information about reactor sites (site names) and references a reactor location via a foreign key.
- **REACTOR_LOCATIONS**: Stores information about reactor locations (region names).
- **REACTOR_EPOCHS**: Stores information about reactor epochs (epoch labels).

## Relationships and Foreign Keys

- Each **FUEL_ASSEMBLY** references:
  - A **REACTOR_CORE** (`reactor_core_id`)
  - A **REACTOR_SITE** (`reactor_site_id`)
  - A **REACTOR_EPOCH** (`reactor_epoch_id`)
- Each **REACTOR_SITE** references:
  - A **REACTOR_LOCATION** (`reactor_location_id`)
- **FUEL_ASSEMBLY** does not directly reference a location; the location is determined via the associated site.
