def filter_data(data, search_query):
    filtered_data = []
    for item in data:
        if search_query.lower() in item['symbol'].lower() or search_query.lower() in item['name'].lower():
            formatted_item = {
                'symbol': item['symbol'],
                'name': item['name'],
                'current_price': item['current_price'],
                'change_24h': item['change_24h'],
                'trade_volume': item['trade_volume'],
                'vwap_24h': item['vwap_24h'],
            }
            filtered_data.append(formatted_item)
    return filtered_data