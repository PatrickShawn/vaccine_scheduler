DROP TABLE IF EXISTS Appointments;
DROP TABLE IF EXISTS Availabilities;
DROP TABLE IF EXISTS Caregivers;
DROP TABLE IF EXISTS Patients;
DROP TABLE IF EXISTS Vaccines;



CREATE TABLE Caregivers (
    Username varchar(255),
    Salt BINARY(16),
    Hash BINARY(16),
    PRIMARY KEY (Username)
);

CREATE TABLE Availabilities (
    Time date,
    Username varchar(255) REFERENCES Caregivers,
    PRIMARY KEY (Time, Username)
);

CREATE TABLE Vaccines (
    Name varchar(255),
    Doses int,
    PRIMARY KEY (Name)
);

CREATE TABLE Patients (
    Username varchar(255),
    Salt BINARY(16),
    Hash BINARY(16),
    PRIMARY KEY (Username)
);

CREATE TABLE Appointments (
    Id INT IDENTITY(1,1),
    Time date,
    Caregiver_name varchar(255) REFERENCES Caregivers(Username),
    Patient_name varchar(255) REFERENCES Patients(Username),
    Vaccine_name varchar(255) REFERENCES Vaccines(Name),
    PRIMARY KEY (id)
);




