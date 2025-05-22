# Amazon Price Tracker with Email Alerts

A Python project that tracks the price of a specific Amazon product and sends an email notification when the price drops below a desired threshold.

## Features

- Scrapes Amazon product page to get the current price.
- Sends email alerts via Gmail SMTP using a secure App Password.
- Configurable product URL, target price, and recipient email.
- Handles Gmail security by using 2FA and App Passwords.
- Basic error handling for network and authentication issues.

## Prerequisites

- Python 3.x
- Required Python packages: `requests`, `beautifulsoup4`, `smtplib` (built-in)
- A Gmail account with 2-Step Verification enabled and an App Password generated for the script.

## Setup

1. Clone this repository:
   ```bash
   git clone https://github.com/MadhuTech2024/Amazon-Price-Tracker-with-Email-Alerts.git
   cd amazon-price-tracker
