--
-- Table structure for table `Planets`
--
CREATE TABLE Planets (
    id INT AUTO_INCREMENT PRIMARY KEY,
    [cite_start]name VARCHAR(255) NOT NULL UNIQUE, -- Each planet has a unique name [cite: 9]
    [cite_start]size INT, -- We want to record its size (an integer) [cite: 9]
    [cite_start]population BIGINT -- and its population [cite: 9]
);

--
-- Table structure for table `SpaceStations`
--
CREATE TABLE SpaceStations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    [cite_start]-- A station can be in orbit of a planet, so this can be NULL [cite: 10]
    orbiting_planet_id INT,
    [cite_start]-- Every station is owned by a planet [cite: 11]
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
    [cite_start]-- A spaceport can be on a planet or a station [cite: 15, 16]
    planet_id INT,
    station_id INT,
    [cite_start]-- The maximum number of flights that can arrive+depart from it on a daily basis [cite: 18]
    capacity INT,
    [cite_start]-- A fixed fee for each seat available on the flight [cite: 19]
    fee_per_seat DECIMAL(10, 2),
    FOREIGN KEY (planet_id) REFERENCES Planets(id),
    FOREIGN KEY (station_id) REFERENCES SpaceStations(id) ON DELETE CASCADE,
    [cite_start]-- A spaceport name is only unique within the planet it's on [cite: 17]
    UNIQUE (planet_id, name)
);

--
-- Table structure for table `Spacecraft`
--
CREATE TABLE Spacecraft (
    id INT AUTO_INCREMENT PRIMARY KEY,
    [cite_start]type_name VARCHAR(255) NOT NULL UNIQUE, -- Each type of spacecraft has a unique type name [cite: 23]
    [cite_start]capacity INT, -- We also would record the capacity of the spacecraft [cite: 23]
    [cite_start]range_km INT -- and the range (maximum travel distance) of the craft [cite: 23]
);

--
-- Table structure for table `Routes`
--
CREATE TABLE Routes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    origin_spaceport_id INT NOT NULL,
    destination_spaceport_id INT NOT NULL,
    [cite_start]distance INT, -- We want to record the distance between the spaceports [cite: 21]
    FOREIGN KEY (origin_spaceport_id) REFERENCES Spaceports(id),
    FOREIGN KEY (destination_spaceport_id) REFERENCES Spaceports(id)
);

--
-- Table structure for table `Flights`
--
CREATE TABLE Flights (
    [cite_start]flight_number VARCHAR(50) PRIMARY KEY, -- A flight will have a unique flight number assigned [cite: 25]
    [cite_start]route_id INT NOT NULL, -- An actual flight will be specified by the route it serves [cite: 24]
    [cite_start]spacecraft_id INT NOT NULL, -- and the type of spacecraft that it uses [cite: 24]
    [cite_start]departure_time TIME, -- The time of departure remains the same for each day it runs [cite: 28]
    [cite_start]flight_time_hours DECIMAL(5, 2), -- the total flight time (in hours, which can be a decimal number) [cite: 25]
    FOREIGN KEY (route_id) REFERENCES Routes(id),
    FOREIGN KEY (spacecraft_id) REFERENCES Spacecraft(id)
);

--
-- Table structure for table `FlightSchedules`
--
CREATE TABLE FlightSchedules (
    flight_number VARCHAR(50) NOT NULL,
    [cite_start]-- We will also need to record on which day of the week (Monday/Tuesday etc.) it departs [cite: 25, 28]
    day_of_week ENUM('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday') NOT NULL,
    PRIMARY KEY (flight_number, day_of_week),
    FOREIGN KEY (flight_number) REFERENCES Flights(flight_number)
);