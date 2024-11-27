from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
import pandas as pd
from dotenv import load_dotenv
import os
import psycopg

load_dotenv()

options = Options()
options.add_argument("start-maximized")
options.add_argument("disable-infobars")
options.add_argument("--disable-extensions")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")


# Read URLs from Excel
file_path = 'datafile/twitter_links.xlsx'  # Path to your Excel file
urls_df = pd.read_excel(file_path)
urls = urls_df['Links'].tolist() 


email = os.getenv("EMAIL")
password = os.getenv("PASSWORD")

service = Service(executable_path="./drivers/chromedriver")
driver = webdriver.Chrome(service=service, options=options)


def login_to_twitter():
    try:
        driver.get("https://twitter.com/login")

        # Wait for the email input form to become visible
        email_input = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "input[name='text']"))
        )
        email_input.send_keys(email)

        # Wait for the next button to become clickable
        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'body > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > button:nth-child(6)'))
        )
        next_button.click()

        # Wait for the password input form to become visible
        password_input = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "input[name='password']"))
        )
        password_input.send_keys(password)

        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@class='css-175oi2r r-sdzlij r-1phboty r-rs99b7 r-lrvibr r-19yznuf r-64el8z r-1fkl15p r-1loqt21 r-o7ynqc r-6416eg r-1ny4l3l']"))
        )
        login_button.click()
    except Exception as e:
        print(f"Login failed: {e}")


def extract_bio():
    try:
        bio_tag = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "div[data-testid='UserDescription'] span[class='css-1jxf684 r-bcqeeo r-1ttztb7 r-qvutc0 r-poiln3']"))
        )
        return bio_tag.text
    except TimeoutException:
        return None

def extract_following_count():
    try:
        following_tag = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "div[class='css-175oi2r r-1rtiivn'] span[class='css-1jxf684 r-bcqeeo r-1ttztb7 r-qvutc0 r-poiln3 r-1b43r93 r-1cwl3u0 r-b88u0q'] span[class='css-1jxf684 r-bcqeeo r-1ttztb7 r-qvutc0 r-poiln3']"))
        )
        return following_tag.text
    except TimeoutException:
        return None

def extract_followers_count():
    try:
        followers_tag = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "div[class='css-175oi2r r-13awgt0 r-18u37iz r-1w6e6rj'] div[class='css-175oi2r'] span[class='css-1jxf684 r-bcqeeo r-1ttztb7 r-qvutc0 r-poiln3 r-1b43r93 r-1cwl3u0 r-b88u0q'] span[class='css-1jxf684 r-bcqeeo r-1ttztb7 r-qvutc0 r-poiln3']"))
        )
        return followers_tag.text
    except TimeoutException:
        return None

def extract_location():
    try:
        location_tag = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "span[role='presentation'] span[class='css-1jxf684 r-bcqeeo r-1ttztb7 r-qvutc0 r-poiln3'] span[class='css-1jxf684 r-bcqeeo r-1ttztb7 r-qvutc0 r-poiln3']"))
        )
        return location_tag.text
    except TimeoutException:
        return None

def extract_website():
    try:
        website_tag = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "a[role='none'] span[class='css-1jxf684 r-bcqeeo r-1ttztb7 r-qvutc0 r-poiln3']"))
        )
        return website_tag.text
    except TimeoutException:
        return None


def save_to_db(bio, following_count, followers_count, location, website):
    with psycopg.connect(
        dbname="twitter",
        user="postgres",
        password="root",
        host="localhost",
        port="5432"
    ) as conn:
        with conn.cursor() as cur:
            # Check if the data already exists
            cur.execute("""
                SELECT * FROM twitter_data WHERE bio = %s AND following_count = %s AND followers_count = %s AND location = %s AND website = %s
            """, (bio, following_count, followers_count, location, website))
            
            if not cur.fetchone():  # If no existing record is found
                # Insert data into the twitter_data table
                cur.execute("""
                    INSERT INTO twitter_data (bio, following_count, followers_count, location, website)
                    VALUES (%s, %s, %s, %s, %s)
                """, (bio, following_count, followers_count, location, website))
                conn.commit()

def fetch_data():
    with psycopg.connect(
        dbname="twitter",
        user="postgres",
        password="root",
        host="localhost",
        port="5432"
    ) as conn:
        with conn.cursor() as cur:
            # Fetch and print the data to verify the insertion
            cur.execute("SELECT * FROM twitter_data")
            rows = cur.fetchall()
            for row in rows:
                print(row)


if __name__ == "__main__":
    login_to_twitter()
    for url in urls:
        print(f"Processing {url}...")
        driver.get(url)
        bio = extract_bio()
        following_count = extract_following_count()
        followers_count = extract_followers_count()
        location = extract_location()
        website = extract_website()
        save_to_db(bio, following_count, followers_count, location, website)
        fetch_data()
    driver.quit()
