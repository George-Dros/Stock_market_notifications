import requests
import datetime as dt
from twilio.rest import Client

dtime = dt.datetime.now()

STOCK = "Stock in question"
COMPANY_NAME = "Name inc etc."
ALPHA_API_KEY = "Alphavantage api key"
NEWS_API = "news.org api"
account_sid = "twillio account id"
twil_token = "twillio token"


TODAY_DATE = dt.date.today()
DAY_OF_WEEK = dtime.weekday()

YESTERDAY = TODAY_DATE - dt.timedelta(days=1)
PREVIOUS_DAY = TODAY_DATE - dt.timedelta(days=2)

if DAY_OF_WEEK == 0:
    YESTERDAY = TODAY_DATE - dt.timedelta(days=3)
    PREVIOUS_DAY = TODAY_DATE - dt.timedelta(days=4)

need_news = False

response = requests.get(f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={STOCK}&apikey={ALPHA_API_KEY}")
response.raise_for_status()


data = response.json()["Time Series (Daily)"]
yesterday_price = float(data[str(YESTERDAY)]["4. close"])
previous_price = float(data[str(PREVIOUS_DAY)]["4. close"])

percentage_change = ((previous_price - yesterday_price) / previous_price) * 100
if abs(percentage_change) > 5:
    need_news = True

if need_news:
    if percentage_change > 5:
        print(f"increase by {round(percentage_change, 2)}")
    elif percentage_change < - 5:
        print(f"decrease by {round(percentage_change, 2)}")

    url = ('https://newsapi.org/v2/everything?'
           f'q={COMPANY_NAME}&'
           f'from={YESTERDAY}&'
           'sortBy=popularity&'
           'pageSize=3&'
           f'apiKey={NEWS_API}'
           )

    news_response = requests.get(url)
    news_response.raise_for_status()

    news = news_response.json()["articles"]

    for article in news:
        client = Client(account_sid, twil_token)
        if percentage_change > 0:
            message = client.messages \
                .create(
                body=f"TSLA: 🔺{round(percentage_change, 2)}% \nHeadline: {article['title']} \nBrief: {article['description']}",
                from_="twillio free phone",
                to="your phone"
            )
        elif percentage_change < 0:
            message = client.messages \
                .create(
                body=f"TSLA: 🔻{round(percentage_change, 2)}% \nHeadline: {article['title']} \nBrief: {article['description']}",
                from_="twillio free phone",
                to="your phone"
            )
