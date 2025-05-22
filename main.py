import requests
from bs4 import BeautifulSoup
import smtplib
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Email & SMTP configuration
SMTP_ADDRESS = os.getenv("SMTP_ADDRESS")
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

# Amazon product URL and target price
URL = "https://www.amazon.com/Sweetcrispy-Managerial-Executive-Ergonomic-Comfortable/dp/B0D3DVG3HG/"
TARGET_PRICE = 100.00

# Headers to mimic a real browser
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9"
}

# Fetch the Amazon product page
response = requests.get(URL, headers=HEADERS)
soup = BeautifulSoup(response.content, "lxml")

# Extract the product title
title_tag = soup.find(id="productTitle")
product_title = title_tag.get_text().strip() if title_tag else "No Title Found"

# Extract the product price
price_tag = soup.find("span", class_="a-offscreen")
if price_tag:
    raw_price = price_tag.get_text().strip().replace("$", "").replace(",", "")
    price = float(raw_price)
else:
    price = None

print(f"Product: {product_title}")
print(f"Current Price: ${price if price else 'Not Found'}")

# Check price and send email alert if price is below target
if price and price < TARGET_PRICE:
    subject = "Amazon Price Alert!"
    body = f"{product_title} is now ${price}!\nBuy now: {URL}"
    message = f"Subject:{subject}\n\n{body}"

    with smtplib.SMTP(SMTP_ADDRESS, port=587) as connection:
        connection.starttls()
        connection.login(user=EMAIL_ADDRESS, password=EMAIL_PASSWORD)
        connection.sendmail(
            from_addr=EMAIL_ADDRESS,
            to_addrs=EMAIL_ADDRESS,
            msg=message.encode("utf-8")
        )
    print("✅ Email sent!")
    