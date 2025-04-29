# Stock Price Alert System

A Python script that monitors stock prices and sends WhatsApp notifications with relevant news when significant price changes occur.

## Setup

1. Install required packages:
```bash
pip install requests twilio python-dotenv
```

2. Create a `.env` file with:
```
STOCKS_API_KEY=your_alpha_vantage_api_key
NEWS_API_KEY=your_news_api_key
TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_FROM_NUMBER=your_twilio_whatsapp_number
YOUR_WHATSAPP_NUMBER=your_personal_whatsapp_number
```

## Usage

Run the script:
```bash
python stock_alert.py
```

## Customization

Modify these variables in the script:
- `STOCK`: Stock symbol to monitor (default: "TSLA")
- `COMPANY_NAME`: Company name for news searches (default: "Tesla Inc")
- Threshold percentage in `if abs(rounded_change) >= 5:`

## How It Works

1. Fetches recent stock closing prices using API 
2. Calculates percentage change
3. If change exceeds threshold:
   - Fetches related news articles from mewsapi.org
   - Sends WhatsApp alerts via Twilio using twilio API

## Requirements

- Twilio account
- Alpha Vantage API key
- News API key
