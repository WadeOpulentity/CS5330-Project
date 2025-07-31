-- Test data for the space management database

-- Insert test planets
INSERT INTO Planets (name, size, population) VALUES
('Earth', 12742, 7800000000),
('Mars', 6779, 250000),
('Alpha Centauri B', 15000, 1200000000),
('Kepler-442b', 14500, 850000000);

-- Insert test space stations
INSERT INTO SpaceStations (name, orbiting_planet_id, owner_planet_id) VALUES
('Luna Station', 1, 1),
('Phobos Outpost', 2, 2),
('Deep Space Station Alpha', NULL, 1);

-- Insert test spaceports
INSERT INTO Spaceports (name, planet_id, station_id, capacity, fee_per_seat) VALUES
('Kennedy Space Center', 1, NULL, 50, 25.00),
('Luna Port', NULL, 1, 30, 15.00),
('New Shanghai Spaceport', 1, NULL, 75, 20.00),
('Olympus Mons Terminal', 2, NULL, 40, 30.00),
('Phobos Station Port', NULL, 2, 20, 35.00),
('Centauri Prime Hub', 3, NULL, 60, 50.00),
('Kepler Gateway', 4, NULL, 45, 45.00);

-- Insert test spacecraft types
INSERT INTO Spacecraft (type_name, capacity, range_km) VALUES
('Shuttle Class', 150, 500000),
('Cruiser Class', 300, 2000000),
('Explorer Class', 200, 5000000),
('Transport Class', 500, 1000000);

-- Insert test routes
INSERT INTO Routes (origin_spaceport_id, destination_spaceport_id, distance) VALUES
(1, 2, 384400),  -- Earth Kennedy to Luna Port
(1, 3, 12000),   -- Kennedy to New Shanghai  
(3, 4, 78000000), -- New Shanghai to Olympus Mons
(4, 5, 9376),    -- Olympus Mons to Phobos Station
(1, 4, 78000000), -- Kennedy to Olympus Mons
(6, 7, 25000000), -- Centauri Prime to Kepler Gateway
(2, 5, 9400);    -- Luna Port to Phobos Station

-- Insert test flights
INSERT INTO Flights (flight_number, route_id, spacecraft_id, departure_time, flight_time_hours) VALUES
('EL001', 1, 1, '09:00:00', 8.5),
('EL002', 1, 1, '15:30:00', 8.5),
('ES001', 2, 1, '06:00:00', 2.0),
('EM001', 3, 2, '10:00:00', 72.0),
('MP001', 4, 1, '14:00:00', 4.5),
('EM002', 5, 2, '08:30:00', 72.0),
('CK001', 6, 3, '12:00:00', 168.0),
('LP001', 7, 1, '16:00:00', 4.8);

-- Insert test flight schedules
INSERT INTO FlightSchedules (flight_number, day_of_week) VALUES
('EL001', 'Monday'),
('EL001', 'Wednesday'),
('EL001', 'Friday'),
('EL002', 'Tuesday'),
('EL002', 'Thursday'),
('EL002', 'Saturday'),
('ES001', 'Monday'),
('ES001', 'Tuesday'),
('ES001', 'Wednesday'),
('ES001', 'Thursday'),
('ES001', 'Friday'),
('EM001', 'Sunday'),
('MP001', 'Monday'),
('MP001', 'Thursday'),
('EM002', 'Tuesday'),
('CK001', 'Saturday'),
('LP001', 'Wednesday'),
('LP001', 'Sunday');