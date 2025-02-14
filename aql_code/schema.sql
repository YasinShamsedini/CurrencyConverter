-- Database
CREATE DATABASE CurrencyConverter;

USE CurrencyConverter;

-- Exchange Rates Table
CREATE TABLE ExchangeRates (
    ID INT PRIMARY KEY IDENTITY(1,1),
    CurrencyCode NVARCHAR(3) NOT NULL,
    Rate DECIMAL(18, 6) NOT NULL,
    LastUpdated DATETIME DEFAULT GETDATE()
);

-- Sample Data
INSERT INTO ExchangeRates (CurrencyCode, Rate) VALUES
('USD', 1.0),
('EUR', 0.94),
('GBP', 0.81),
('JPY', 146.45),
('CAD', 1.35);
