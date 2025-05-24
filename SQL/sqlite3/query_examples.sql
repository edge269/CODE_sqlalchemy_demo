-- Query 1: Get the name of all FUEL_ASSEMBLY in 900 MWe reactors
SELECT FA_name
FROM FUEL_ASSEMBLY fa
JOIN REACTOR_DESIGN rd ON fa.reactor_design_id = rd.id
WHERE rd.reactor_power = 900;

-- Query 2: Get the BUp of all FUEL_ASSEMBLY implemented in the Auvergne-Rhône-Alpes region and that are in the CPY design
SELECT fa.FA_BUp
FROM FUEL_ASSEMBLY fa
JOIN REACTOR_DESIGN rd ON fa.reactor_design_id = rd.id
JOIN PLANTS p ON fa.plant_id = p.id
JOIN REACTOR_LOCATIONS rl ON p.reactor_location_id = rl.id
WHERE rl.reactor_location = 'Auvergne-Rhône-Alpes'
  AND rd.reactor_type = 'CPY';

-- Query 3: Get the max and min BUp for the above selection
SELECT MAX(fa.FA_BUp) AS max_bup, MIN(fa.FA_BUp) AS min_bup
FROM FUEL_ASSEMBLY fa
JOIN REACTOR_DESIGN rd ON fa.reactor_design_id = rd.id
JOIN PLANTS p ON fa.plant_id = p.id
JOIN REACTOR_LOCATIONS rl ON p.reactor_location_id = rl.id
WHERE rl.reactor_location = 'Auvergne-Rhône-Alpes'
  AND rd.reactor_type = 'CPY';

-- Query 4: Number of FUEL_ASSEMBLY that are in VD3 epoch and on 1450 MWe core designs
SELECT COUNT(*) AS num_fa
FROM FUEL_ASSEMBLY fa
JOIN REACTOR_DESIGN rd ON fa.reactor_design_id = rd.id
JOIN EPOCHS e ON fa.epoch_id = e.id
WHERE e.epoch = 'VD3'
  AND rd.reactor_power = 1450;

-- Query 5: List all 1300 MWe plants in the three/four northernmost French regions
-- (Assuming regions: 'Hauts-de-France', 'Île-de-France', 'Normandy', 'Grand Est')
SELECT DISTINCT p.plant_name, rl.reactor_location
FROM PLANTS p
JOIN REACTOR_LOCATIONS rl ON p.reactor_location_id = rl.id
JOIN FUEL_ASSEMBLY fa ON fa.plant_id = p.id
JOIN REACTOR_DESIGN rd ON fa.reactor_design_id = rd.id
WHERE rd.reactor_power = 1300
  AND rl.reactor_location IN ('Hauts-de-France', 'Île-de-France', 'Normandy', 'Grand Est');
