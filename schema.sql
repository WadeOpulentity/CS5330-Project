--
-- Table structure for table `Planets`
--
CREATE TABLE Planets (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE, -- Each planet has a unique name
    size INT, -- We want to record its size (an integer)
    population BIGINT -- and its population
);

--
-- Table structure for table `SpaceStations`
--
CREATE TABLE SpaceStations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    -- A station can be in orbit of a planet, so this can be NULL
    orbiting_planet_id INT,
    -- Every station is owned by a planet
    owner_planet_id INT NOT NULL,
    FOREIGN KEY (orbiting_planet_id) REFERENCES Planets(id),
    FOREIGN KEY (owner_planet_id) REFERENCES Planets(id)
);

--
-- Table structure for table `Spaceports`
--
CREATE TABLE Spaceports (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    -- A spaceport can be on a planet or a station
    planet_id INT,
    station_id INT,
    -- The maximum number of flights that can arrive+depart from it on a daily basis
    capacity INT,
    -- A fixed fee for each seat available on the flight
    fee_per_seat DECIMAL(10, 2),
    FOREIGN KEY (planet_id) REFERENCES Planets(id),
    FOREIGN KEY (station_id) REFERENCES SpaceStations(id) ON DELETE CASCADE,
    -- A spaceport name is only unique within the planet it's on
    UNIQUE (planet_id, name)
);

--
-- Table structure for table `Spacecraft`
--
CREATE TABLE Spacecraft (
    id INT AUTO_INCREMENT PRIMARY KEY,
    type_name VARCHAR(255) NOT NULL UNIQUE, -- Each type of spacecraft has a unique type name
    capacity INT, -- We also would record the capacity of the spacecraft
    range_km INT -- and the range (maximum travel distance) of the craft
);

--
-- Table structure for table `Routes`
--
CREATE TABLE Routes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    origin_spaceport_id INT NOT NULL,
    destination_spaceport_id INT NOT NULL,
    distance INT, -- We want to record the distance between the spaceports
    FOREIGN KEY (origin_spaceport_id) REFERENCES Spaceports(id),
    FOREIGN KEY (destination_spaceport_id) REFERENCES Spaceports(id)
);

--
-- Table structure for table `Flights`
--
CREATE TABLE Flights (
    flight_number VARCHAR(50) PRIMARY KEY, -- A flight will have a unique flight number assigned
    route_id INT NOT NULL, -- An actual flight will be specified by the route it serves
    spacecraft_id INT NOT NULL, -- and the type of spacecraft that it uses
    departure_time TIME, -- The time of departure remains the same for each day it runs
    flight_time_hours DECIMAL(5, 2), -- the total flight time (in hours, which can be a decimal number)
    FOREIGN KEY (route_id) REFERENCES Routes(id),
    FOREIGN KEY (spacecraft_id) REFERENCES Spacecraft(id)
);

--
-- Table structure for table `FlightSchedules`
--
CREATE TABLE FlightSchedules (
    flight_number VARCHAR(50) NOT NULL,
    -- We will also need to record on which day of the week (Monday/Tuesday etc.) it departs
    day_of_week ENUM('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday') NOT NULL,
    PRIMARY KEY (flight_number, day_of_week),
    FOREIGN KEY (flight_number) REFERENCES Flights(flight_number)
);