-- Keep a log of any SQL queries you execute as you solve the mystery.
-- Use crime scene report table to get id for month: July day: 28 year: 2021 and street: Humphrey Street
SELECT description FROM crime_scene_reports
WHERE day = 28
AND month = 7
AND year = 2021
AND street = "Humphrey Street";
-- Theft occured at 10:15 AM. Time to check out the three interviews
SELECT name, transcript FROM interviews
WHERE day = 28
AND month = 7
AND year = 2021;
-- Emma (bakery owner), Ruth saw someone get into car, Eugene saw thief at ATM before robbery, Raymond heard
-- phone call after robbery, Lily sons Robert and Patrick are in Paris now
-- Check license plate info with people to get names
SELECT name FROM people
JOIN bakery_security_logs ON people.license_plate = bakery_security_logs.license_plate
WHERE activity = "exit"
AND minute BETWEEN 15 AND 25
AND hour = 10
AND day = 28
AND month = 7
AND year = 2021;
 -- Vanessa, Bruce, Barry, Luca, Sofia, Iman, Diana, Kelsey
-- Account number could be cross referenced with bank_accounts to narrow list
SELECT name FROM people
JOIN bank_accounts ON  people.id = bank_accounts.person_id
JOIN atm_transactions ON bank_accounts.account_number = atm_transactions.account_number
WHERE atm_location = "Leggett Street"
AND transaction_type = "withdraw"
AND day = 28
AND month = 7
AND year = 2021;
-- Bruce, Diana, Iman, Luca left
-- Check flights leaving tomorrow with names
SELECT name, flights.hour FROM people
JOIN passengers ON people.passport_number = passengers.passport_number
JOIN flights ON passengers.flight_id = flights.id
AND day = 29
AND month = 7
AND year = 2021
ORDER BY hour, minute;
-- Bruce, Luca left, use phone call less than minute to find final person
SELECT DISTINCT name FROM people
JOIN phone_calls ON people.phone_number = phone_calls.caller
WHERE duration < 60
AND day = 28
AND month = 7
AND year = 2021;
-- THIEF MUST BE BRUCE
-- Now find city and accomplice
SELECT city FROM airports
WHERE id = (
SELECT destination_airport_id
FROM flights
WHERE day = 29
AND month = 7
AND year = 2021
ORDER BY hour, minute);
-- New York City
-- Use phone call to find who Bruce was chatting with
SELECT name FROM people
JOIN phone_calls ON people.phone_number = phone_calls.receiver
WHERE duration < 60
AND day = 28
AND month = 7
AND year = 2021
AND caller = (
SELECT phone_number FROM people
WHERE name= "Bruce");
-- Accomplice is Robin