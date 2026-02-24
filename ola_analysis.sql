USE ola;
SELECT * FROM ola_cleaned LIMIT 10;
-- Retrieve all rides that were completed successfully
SELECT *
FROM ola_cleaned
WHERE Booking_Status = 'Success';


-- Calculate the average ride distance for each vehicle type
SELECT
    Vehicle_Type,
    ROUND(AVG(Ride_Distance), 2) AS avg_ride_distance
FROM ola_cleaned
GROUP BY Vehicle_Type;

-- Count total number of rides cancelled by customers
SELECT COUNT(*) AS total_customer_cancellations
FROM ola_cleaned
WHERE Booking_Status = 'Cancelled by Customer';

-- Identify the top 5 customers based on number of rides booked
SELECT
    Customer_ID,
    COUNT(*) AS total_rides
FROM ola_cleaned
GROUP BY Customer_ID
ORDER BY total_rides DESC
LIMIT 5;

-- Count total number of rides cancelled by drivers
SELECT COUNT(*) AS driver_cancellations
FROM ola_cleaned
WHERE Booking_Status = 'Cancelled by Driver';

-- Find highest and lowest driver ratings for Prime Sedan vehicle type
SELECT
    MAX(Driver_Ratings) AS max_driver_rating,
    MIN(Driver_Ratings) AS min_driver_rating
FROM ola_cleaned
WHERE Vehicle_Type = 'Prime Sedan';

-- Retrieve all rides where the payment method was UPI
SELECT *
FROM ola_cleaned
WHERE Payment_Method = 'UPI';

-- Calculate average customer rating for each vehicle type
SELECT
    Vehicle_Type,
    ROUND(AVG(Customer_Rating), 2) AS avg_customer_rating
FROM ola_cleaned
GROUP BY Vehicle_Type;

-- Calculate total revenue generated from completed rides
SELECT
    ROUND(SUM(Booking_Value), 2) AS total_completed_revenue
FROM ola_cleaned
WHERE Booking_Status = 'Success';

-- Retrieve all incomplete rides along with their cancellation reason
SELECT
    Booking_ID,
    Customer_ID,
    Booking_Status AS cancellation_reason
FROM ola_cleaned
WHERE Booking_Status IN (
    'Cancelled by Driver',
    'Cancelled by Customer',
    'Driver Not Found'
);