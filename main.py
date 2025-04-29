import requests
from twilio.rest import Client
import os
from dotenv import load_dotenv

load_dotenv()

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

# STEP 1: Check stock price change
API_URL = "https://www.alphavantage.co/query"
stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": os.getenv("STOCKS_API_KEY"),
}

response = requests.get(url=API_URL, params=stock_params)
response.raise_for_status()
data = response.json()["Time Series (Daily)"]

data_list = [value for (key, value) in data.items()]

# Take the most recent two closing prices
today_close = float(data_list[0]["4. close"])
yesterday_close = float(data_list[1]["4. close"])

# Calculate the percentage change
stock_price_change = ((today_close - yesterday_close) / yesterday_close) * 100
rounded_change = round(stock_price_change, 2)

print(f"Today's close: {today_close}")
print(f"Yesterday's close: {yesterday_close}")
print(f"Stock Change: {rounded_change}%")

# Check if the price movement is significant
if abs(rounded_change) >= 5:
    print("Significant move detected. Fetching news...")

    # STEP 2: Fetch Tesla-related news
    NEWS_API_URL = "https://newsapi.org/v2/everything"
    news_params = {
        "qInTitle": COMPANY_NAME,   # Use Tesla Inc in the title for more accuracy
        "sortBy": "publishedAt",
        "apiKey": os.getenv("NEWS_API_KEY"),
        "language": "en",
        "pageSize": 3,              # Only get top 3
    }

    news_response = requests.get(url=NEWS_API_URL, params=news_params)
    news_response.raise_for_status()
    news_data = news_response.json()["articles"]
    
    # Just in case there are fewer than 3 articles
    top_articles = news_data[:3]

    # Format articles
    formatted_articles = [
        f"Headline: {article['title']}\nBrief: {article['description']}" 
        for article in top_articles
    ]

    # STEP 3: Send WhatsApp message via Twilio
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    client = Client(account_sid, auth_token)

    from_number = os.getenv("TWILIO_FROM_NUMBER")
    to_number = os.getenv("YOUR_WHATSAPP_NUMBER")

    direction_symbol = "🔺" if rounded_change > 0 else "🔻"

    for article in formatted_articles:
        message = client.messages.create(
            from_=f"whatsapp:{from_number}",
            body=f"{STOCK}: {direction_symbol}{abs(rounded_change)}%\n{article}",
            to=f"whatsapp:{to_number}"
        )
        print(f"Sent message: {message.sid}")

else:
    print("No significant movement. No news fetched.")
