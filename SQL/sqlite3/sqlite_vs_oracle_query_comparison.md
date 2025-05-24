# SQLite3 vs Oracle SQL Query Comparison: Nuclear Fuel Assembly Example

This document compares SQL queries for common business and analytical questions in both SQLite3 and Oracle, using the normalized schema for nuclear fuel assemblies. The queries include examples for fuel assemblies, plants, regions, and reactor designs. The queries are functionally equivalent, but may differ in syntax or supported features depending on the database dialect.

---

## Query 1: Get the name of all Fuel Assemblies in 900 MWe Reactors
**Purpose:** List all fuel assembly names (`FA_name`) used in reactors with a power of 900 MWe.

```sql
SELECT FA_name
FROM FUEL_ASSEMBLY fa
JOIN REACTOR_DESIGN rd ON fa.reactor_design_id = rd.id
WHERE rd.reactor_power = 900;
```
- **SQLite3:** Supported as written.
- **Oracle:** Supported as written.

---

## Query 2: Get the Burnup (BUp) of all Fuel Assemblies implemented in the Auvergne-Rhône-Alpes region and that are in the CPY design
**Purpose:** Find the burnup values for all fuel assemblies in a specific region and reactor design.

```sql
SELECT fa.FA_BUp
FROM FUEL_ASSEMBLY fa
JOIN REACTOR_DESIGN rd ON fa.reactor_design_id = rd.id
JOIN PLANTS p ON fa.plant_id = p.id
JOIN REACTOR_LOCATIONS rl ON p.reactor_location_id = rl.id
WHERE rl.reactor_location = 'Auvergne-Rhône-Alpes'
  AND rd.reactor_type = 'CPY';
```
- **SQLite3:** Supported as written.
- **Oracle:** Supported as written.

---

## Query 3: Get the max and min Burnup for the above selection
**Purpose:** Find the maximum and minimum burnup values for the same selection as Query 2.

```sql
SELECT MAX(fa.FA_BUp) AS max_bup, MIN(fa.FA_BUp) AS min_bup
FROM FUEL_ASSEMBLY fa
JOIN REACTOR_DESIGN rd ON fa.reactor_design_id = rd.id
JOIN PLANTS p ON fa.plant_id = p.id
JOIN REACTOR_LOCATIONS rl ON p.reactor_location_id = rl.id
WHERE rl.reactor_location = 'Auvergne-Rhône-Alpes'
  AND rd.reactor_type = 'CPY';
```
- **SQLite3:** Supported as written.
- **Oracle:** Supported as written.

---

## Query 4: Number of Fuel Assemblies that are in VD3 epoch and on 1450 MWe core designs
**Purpose:** Count the number of fuel assemblies in the VD3 epoch and on 1450 MWe reactor designs.

```sql
SELECT COUNT(*) AS num_fa
FROM FUEL_ASSEMBLY fa
JOIN REACTOR_DESIGN rd ON fa.reactor_design_id = rd.id
JOIN EPOCHS e ON fa.epoch_id = e.id
WHERE e.epoch = 'VD3'
  AND rd.reactor_power = 1450;
```
- **SQLite3:** Supported as written.
- **Oracle:** Supported as written.

---

## Query 5: List all 1300 MWe Plants in the Northernmost French Regions
**Purpose:** List all plants (and their regions) with 1300 MWe reactors in the three/four northernmost French regions.

Regions considered: 'Hauts-de-France', 'Île-de-France', 'Normandy', 'Grand Est'.

```sql
SELECT DISTINCT p.plant_name, rl.reactor_location
FROM PLANTS p
JOIN REACTOR_LOCATIONS rl ON p.reactor_location_id = rl.id
JOIN FUEL_ASSEMBLY fa ON fa.plant_id = p.id
JOIN REACTOR_DESIGN rd ON fa.reactor_design_id = rd.id
WHERE rd.reactor_power = 1300
  AND rl.reactor_location IN ('Hauts-de-France', 'Île-de-France', 'Normandy', 'Grand Est');
```
- **SQLite3:** Supported as written.
- **Oracle:** Supported as written.

---

## Notes on Dialect Differences
- For these queries, the SQL is portable between SQLite3 and Oracle because they use standard SQL features (JOINs, WHERE, aggregate functions).
- More complex queries (window functions, CTEs, date/time handling, etc.) may require dialect-specific adjustments.
- Table and column names are case-insensitive in both systems, but best practice is to use uppercase for Oracle.
- In production, always test queries on the target database to ensure compatibility.
