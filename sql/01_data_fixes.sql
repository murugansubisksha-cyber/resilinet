-- Data Fixes Applied on [TODAY'S DATE]
-- Purpose: Fix missing weather coordinates (NaN values)

-- Fix missing coordinates for 4 weather stations
UPDATE weather 
SET latitude = CASE 
    WHEN location = 'Guwahati' THEN 26.18
    WHEN location = 'Nagaon' THEN 26.15
    WHEN location = 'Lumding' THEN 25.28
    WHEN location = 'Silchar' THEN 24.82
    ELSE latitude
END,
longitude = CASE 
    WHEN location = 'Guwahati' THEN 91.75
    WHEN location = 'Nagaon' THEN 92.72
    WHEN location = 'Lumding' THEN 92.84
    WHEN location = 'Silchar' THEN 92.80
    ELSE longitude
END
WHERE latitude IS NULL OR longitude IS NULL;

-- Verification Query
SELECT COUNT(*) as invalid_coordinates
FROM weather 
WHERE latitude < 24 OR latitude > 27 OR longitude < 90 OR longitude > 94;