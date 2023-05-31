import requests


def get_crypto_data():
    url = 'https://api.coincap.io/v2/assets'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data['data']
    return None


def format_crypto_data(data):
    formatted_data = []
    for item in data:
        vwap_24h = float(item['vwap24Hr']) if item['vwap24Hr'] is not None else None
        formatted_item = {
            'symbol': item['symbol'],
            'name': item['name'],
            'current_price': round(float(item['priceUsd']), 4),
            'change_24h': round(float(item['changePercent24Hr']), 4),
            'trade_volume': round(float(item['volumeUsd24Hr']), 4),
            'vwap_24h': round(vwap_24h, 4) if vwap_24h is not None else None,
        }
        formatted_data.append(formatted_item)
    return formatted_data


def get_crypto_news():
    url = "https://api.coingecko.com/api/v3/news"
    response = requests.get(url)
    data = response.json()
    news = []
    if "data" in data:
        news_data = data["data"]
        for item in news_data:
            title = item.get("title")
            description = item.get("description")
            source = item.get("url")
            if title and description and source:
                news_item = {
                    "title": title,
                    "description": description,
                    "source": source,
                }
                news.append(news_item)
    return news