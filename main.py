import requests
from bs4 import BeautifulSoup
import smtplib
import os
from dotenv import load_dotenv
import csv
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

# Email & SMTP configuration
SMTP_ADDRESS = os.getenv("SMTP_ADDRESS")
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

# Prompt user for input
URL = input("Enter the Amazon product URL: ")
TARGET_PRICE = float(input("Enter your target price: "))

# Headers to mimic a real browser
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Connection": "keep-alive",
}

# Fetch the Amazon product page
response = requests.get(URL, headers=HEADERS)
soup = BeautifulSoup(response.content, "html.parser")

# Extract the product title
title_tag = soup.find(id="productTitle")
product_title = title_tag.get_text().strip() if title_tag else None

# Extract the product price
price_tag = soup.find("span", class_="a-offscreen")
if price_tag:
    raw_price = price_tag.get_text().strip().replace("$", "").replace(",", "")
    try:
        price = float(raw_price)
    except ValueError:
        price = None
else:
    price = None

if not product_title or price is None:
    print("Could not find product title or price. Printing a snippet of the HTML for debugging:")
    print(response.text[:2000])  # Print the first 2000 characters of the HTML
    product_title = product_title if product_title else "No Title Found"

print(f"Product: {product_title}")
print(f"Current Price: ${price if price is not None else 'Not Found'}")

# --- Price History Logging ---
with open("price_history.csv", mode="a", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow([datetime.now().isoformat(), product_title, price])

# Check price and send email alert if price is below target
if price is not None and price < TARGET_PRICE:
    subject = "Amazon Price Alert!"
    body = f"{product_title} is now ${price}!\nBuy now: {URL}"
    message = f"Subject: {subject}\n\n{body}"

    try:
        with smtplib.SMTP(SMTP_ADDRESS, port=587) as connection:
            connection.starttls()
            connection.login(user=EMAIL_ADDRESS, password=EMAIL_PASSWORD)
            connection.sendmail(
                from_addr=EMAIL_ADDRESS,
                to_addrs=EMAIL_ADDRESS,
                msg=message.encode("utf-8")
            )
        print("Email sent!")
    except Exception as e:
        print(f"Failed to send email: {e}")