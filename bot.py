import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
import os

EMAIL = "your_email@gmail.com"
PASSWORD = "your_app_password"

# -------------------------
# NEWS FETCHING
# -------------------------

def get_et_news():
    url = "https://economictimes.indiatimes.com/markets/stocks/news"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")

    news = []
    for item in soup.select("div.eachStory")[:5]:
        title = item.get_text(strip=True)
        news.append(title)

    return news

def get_mc_news():
    url = "https://www.moneycontrol.com/news/business/stocks/"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")

    news = []
    for item in soup.select("li.clearfix")[:5]:
        title = item.get_text(strip=True)
        news.append(title)

    return news

# -------------------------
# SIMPLE SENTIMENT LOGIC
# -------------------------

def analyze_sentiment(text):
    positive_words = ["gain", "rise", "up", "profit", "growth", "surge"]
    negative_words = ["fall", "down", "loss", "decline", "crash"]

    text = text.lower()

    if any(word in text for word in positive_words):
        return "Positive", "BUY"
    elif any(word in text for word in negative_words):
        return "Negative", "SELL"
    else:
        return "Neutral", "WATCH"

# -------------------------
# CREATE TABLE
# -------------------------

def generate_table(news_list):
    table = """
    <html>
    <body>
    <h2>📊 F&O Stock News - {}</h2>
    <table border="1" cellpadding="8" cellspacing="0">
    <tr>
        <th>News</th>
        <th>Sentiment</th>
        <th>Action</th>
    </tr>
    """.format(datetime.now().strftime("%d-%m-%Y"))

    for news in news_list:
        sentiment, action = analyze_sentiment(news)

        table += f"""
        <tr>
            <td>{news}</td>
            <td>{sentiment}</td>
            <td>{action}</td>
        </tr>
        """

    table += "</table></body></html>"

    return table

# -------------------------
# SEND EMAIL
# -------------------------

def send_email(html_content):
    msg = MIMEText(html_content, "html")
    msg['Subject'] = "📈 Daily F&O Trading Sheet"
    msg['From'] = EMAIL
    msg['To'] = EMAIL

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(EMAIL, PASSWORD)
    server.send_message(msg)
    server.quit()

# -------------------------
# MAIN
# -------------------------
et_news = get_et_news()
mc_news = get_mc_news()

all_news = et_news + mc_news

html_report = generate_table(all_news)
send_email(html_report)