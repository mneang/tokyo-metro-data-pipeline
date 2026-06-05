-- Create Lines table
CREATE TABLE Lines (
    Line_ID TEXT PRIMARY KEY,
    Line_Name_En TEXT NOT NULL,
    Line_Name_Jp TEXT NOT NULL
);

-- Create Stations table
CREATE TABLE Stations (
    Station_ID TEXT PRIMARY KEY,
    English_Name TEXT NOT NULL,
    Japanese_Name TEXT NOT NULL,
    Line_IDs TEXT NOT NULL,
    Line_Names_En TEXT,
    Line_Names_Jp TEXT,
    FOREIGN KEY (Line_IDs) REFERENCES Lines (Line_ID)
);

-- Create Passengers table
CREATE TABLE Passengers (
    Station_ID TEXT NOT NULL,
    English_Name TEXT,
    Daily_Passenger_Avg INTEGER NOT NULL,
    Year_Over_Year_Change REAL NOT NULL,
    PRIMARY KEY (Station_ID, Daily_Passenger_Avg),
    FOREIGN KEY (Station_ID) REFERENCES Stations (Station_ID)
);

-- Create Revenue table
CREATE TABLE Revenue (
    Fiscal_Year INTEGER NOT NULL,
    Fiscal_Month INTEGER NOT NULL,
    Calendar_Year INTEGER NOT NULL,
    Calendar_Month TEXT NOT NULL,
    Commuter_Revenue INTEGER NOT NULL,
    Commuter_YoY_Percentage REAL NOT NULL,
    Non_Commuter_Revenue INTEGER NOT NULL,
    Non_Commuter_YoY_Percentage REAL NOT NULL,
    Total_Revenue INTEGER NOT NULL,
    Total_YoY_Percentage REAL NOT NULL
);
