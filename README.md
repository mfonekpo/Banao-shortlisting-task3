# Twitter Data Extractor with Selenium and PostgreSQL

This project is a Python-based automation script that scrapes user information from Twitter profiles using Selenium WebDriver, processes the data, and saves it into a PostgreSQL database for further analysis.

---

## Table of Contents

- [Twitter Data Extractor with Selenium and PostgreSQL](#twitter-data-extractor-with-selenium-and-postgresql)
  - [Table of Contents](#table-of-contents)
  - [Features](#features)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Configuration](#configuration)
  - [Usage](#usage)
  - [Project Workflow](#project-workflow)
  - [Database Schema](#database-schema)
    - [Expected Output](#expected-output)
  - [Code Overview](#code-overview)
  - [Limitations](#limitations)
  - [Future Improvements](#future-improvements)
  - [License](#license)

---

## Features

1. **Automated Login**: Logs into Twitter using provided credentials.
2. **Data Extraction**: Scrapes the following data from Twitter profiles:
   - Bio
   - Following count
   - Followers count
   - Location
   - Website
3. **Database Storage**: Saves scraped data to a PostgreSQL database, ensuring no duplicate records are inserted.
4. **Error Handling**: Handles missing elements gracefully by returning `null` for non-existent fields.

---

## Prerequisites

1. **Python**: Version 3.8 or above.
2. **WebDriver**: [ChromeDriver](https://sites.google.com/chromium.org/driver/).
3. **PostgreSQL**: Ensure you have a running PostgreSQL instance.
4. **Browser**: Google Chrome is required for Selenium WebDriver.
5. **Libraries**: The script relies on the following Python libraries:
   - `selenium`
   - `webdriver_manager`
   - `dotenv`
   - `psycopg`
   - `pandas`

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/youruserame/Banao-shortlisting-task3.git
   ```

2. Install the required libraries:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   ```bash
   touch .env
   python3 -m venv venv
   source venv/bin/activate
   ```

4. Run the script:
   ```bash
   python main.py
   ```

---

## Configuration

Before running the script, ensure a ```.env``` file in the root directory and define the following environment variables:


- `EMAIL`: Your Twitter email address.
- `PASSWORD`: Your Twitter password.    
- `DB_NAME`: The name of the PostgreSQL database.
- `DB_USER`: The username for accessing the PostgreSQL database.
- `DB_PASSWORD`: The password for accessing the PostgreSQL database.
- `DB_HOST`: The host address of the PostgreSQL database.
- `DB_PORT`: The port number of the PostgreSQL database.    

---

## Usage

1. Run the script:
   ```bash
    python twitter_scraper.py
   ```
2. The script will:

    - Log in to Twitter.
    - Visit each profile URL from the Excel file.
    - Scrape the required data.
    - Save the data to the PostgreSQL database.
    - Print the database contents to the console.

## Project Workflow

- Initialization:
        Set up Selenium WebDriver with custom Chrome options to avoid detection.
        Load URLs from an Excel file.

- Login:
        Automatically log in to Twitter using provided credentials.

- Data Extraction:
        Navigate to each Twitter profile URL.
        Extract Bio, Following Count, Followers Count, Location, and Website.
        Handle missing elements gracefully by returning null.

- Database Operations:
        Check for duplicate entries.
        Insert new records into the twitter_data table.

- Output:
        Stores all records in the database for verification.


## Database Schema


| Field Name        | Data Type | Description                   |
|-------------------|-----------|-------------------------------|
| `id`              | `SERIAL`  | Auto-incrementing primary key |
| `bio`             | `TEXT`    | User bio                     |
| `following_count` | `TEXT`    | Number of accounts followed   |
| `followers_count` | `TEXT`    | Number of followers           |
| `location`        | `TEXT`    | User's location              |
| `website`         | `TEXT`    | Website link                 |

### Expected Output

Here is an example of the data that will be stored in the database after extraction:

| id  | bio                        | following_count | followers_count | location       | website              |
|-----|----------------------------|-----------------|-----------------|----------------|----------------------|
| 1   | "Tech enthusiast and coder"| 150             | 2000            | "San Francisco"| "www.example.com"    |
| 2   | "Data Scientist @Company"  | 500             | 10000           | "New York, USA"| "www.dataguru.io"    |
| 3   | "Love Python & Automation" | 300             | 5000            | "London, UK"   | "www.automationpro.uk"|



## Code Overview


- login_to_twitter(): Automates the login process using credentials from the .env file.

- extract_bio(): Extracts the user's bio from their profile. Returns null if not found.

- extract_following_count(): Extracts the number of accounts the user follows. Returns null if not found.

- extract_followers_count(): Extracts the user's follower count. Returns null if not found.

- extract_location(): Extracts the user's location. Returns null if not found.

- extract_website(): Extracts the user's website link. Returns null if not found.

- save_to_db(bio, following_count, followers_count, location, website): Saves the extracted data into the PostgreSQL database after checking for duplicates.

- fetch_data(): Fetches and prints all records from the database for verification.


## Limitations

- Dynamic Page Layouts: Twitter's page structure may change, requiring updates to CSS selectors.

- Rate Limiting: Twitter may block requests if too many profiles are visited in a short time.

- Error Handling: While missing elements are handled, network interruptions or unexpected errors may disrupt execution.


## Future Improvements

- Multi-threading: Speed up the scraping process by implementing multi-threading.

- Enhanced Error Handling: Improve exception handling for edge cases like account suspensions or private profiles.


## License

This project is not under any specific license.