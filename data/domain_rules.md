# Work Domain Rules for Nuclear Fuel Assembly Data

This document outlines the business and data integrity rules defined by the data owner for the structure and content of the nuclear fuel assembly dataset used in this project.

---

## 1. Fuel Assembly (FA) Naming

- Each fuel assembly (FA) must have a unique identifier (`FA_name`)
- The FA name follows the pattern: `F` + [A-Z] + [1000-9999]
  - **Example**: `FJ1234`

## 2. Mass and Length

- The mass of a fuel assembly (`FA_mass`) is a real number, typically distributed around a central value depending on the assembly's length
- **900 MWe FAs** are shorter (**12ft**); all other reactor powers use longer (**14ft**) FAs
- The FA length in feet (`FA_length_ft`) must be recorded as **12** or **14** accordingly

## 3. Manufacturing and Introduction Years

- `FA_manufacturing_year` is the year the assembly was manufactured
  - **Constraint**: Must be ≤ `FA_introduction_year`
- `FA_introduction_year` is the year the assembly was introduced into service
  - **Range**: From the start year of the reactor power at the plant to the current year (2025)
  - **Business Rule**: Cannot be before the operation start year of the corresponding reactor power at that plant

## 4. Reactor Power and Type

| Reactor Power (MWe) | Reactor Type | Description |
|---------------------|--------------|-------------|
| 900                 | CPY          | Compact PWR |
| 1300                | DPY          | Standard PWR |
| 1450                | PQY          | Advanced PWR |
| 1600                | EPR          | European PWR |

- Each plant only allows specific reactor powers, and each power at a plant has its own operation start year
- **Example**: Flamanville allows:
  - 1300 MWe from 1986
  - 1600 MWe from 2025

## 5. Fuel Type

| Reactor Power | Year Constraint | Allowed Fuel Types |
|---------------|-----------------|-------------------|
| 900 MWe       | After 1995      | `UO2` or `MOX`    |
| All others    | Any year        | `UO2` only        |
| 900 MWe       | Before 1995     | `UO2` only        |

## 6. Plant and Location

- `plant` is a code (e.g., `CHI`, `CIV`) mapped to a specific French nuclear plant and region
- `location` is the French region of the plant
- Each plant is associated with a set of allowed reactor powers and their respective operation start years

## 7. Burnup (BUp)

- `FA_BUp` is a real number between **0** and **72 GWd/tU**, representing the burnup of the assembly
- **Observed trends** (not strict dependencies):
  - Burnup generally increases with fuel assembly mass
  - Higher for more recent reactor types
  - Tends to rise with later epochs

## 8. Epoch (licensing framework)

- `epoch` is a string (e.g., VD1, VD2, ...) indicating the decade between the plant operation start year and the FA introduction year.
- **Calculation formula**: `VD[n] = (introduction_year - operation_start_year) // 10 + 1`

## 9. Data Integrity Rules

**Required Constraints**:
- All fields must be present and non-null
- No duplicate `FA_name` values are allowed
- All values must conform to the above rules for type and range

## 10. Pedagogical Note: Data File vs. Database Schema

> **Important**: The generated data files (`plants_data.xlsx`, `plants_data.csv`) intentionally use different field names and a denormalized structure compared to the normalized database schema.

### Field Name Mapping

| Data File Column | Database Schema Field | Notes |
|------------------|----------------------|-------|
| `FA_mass_kg` | `FA_mass` | Mass in kilograms |
| `FA_year_made` | `FA_manufacturing_year` | Year manufactured |
| `FA_year_intro` | `FA_introduction_year` | Year introduced |
| `plant_code` | Normalized plant table | Code only in DB |
| `plant_name` | Normalized plant table | Name only in DB |
| `region` | Location table | Normalized in schema |
| `burnup_GWd_tU` | `FA_BUp` | Same field name |
| `epoch_label` | `epoch` | Same field name |
| `plant_and_region` | *Not in schema* | Demo field only |

### Educational Purpose

This distinction is **pedagogical**: it demonstrates the difference between:
- **Flat, denormalized data export** (CSV/Excel files)
- **Normalized relational database design** (SQL schema)

---

## Reference

This document should be referenced for all data modeling, validation, and ORM mapping tasks in this project.

**Project**: French Nuclear Fuel Assembly Data  
**Last Updated**: June 28, 2025  
**Contact**: Hervé LEBAIL, Framatome
