import json

import requests
from SECRET.KEITARO_KEY import API_TOKEN


def query_for_keitaro(start_date, end_date, buyer_sub_id):
    headers ={
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'Api-Key': API_TOKEN
    }

    json_data = {
        "range": {
            "interval": "custom_date_range",
            "timezone": "Europe/Istanbul",
            "from": f'{start_date}',
            "to": f'{end_date}'
            },
        "columns": [],
        "metrics": [
            "clicks",
            "conversions"
            ],
        "grouping": [],
        "filters": [

            {
                "name": "sub_id_6",
                "operator": "CONTAINS",
                "expression": f"{buyer_sub_id}"
            }
        ],
        "sort": [
            {
                "name": "campaign_unique_clicks",
                "order": "desc"
            }
        ],
        "summary": False,
        "limit": None,
        "offset": 0,
    }
    if buyer_sub_id == '':
        json_data['filters'] = []
    # json_data = json.dumps(json_data)
    response = requests.post('http://136.244.93.168/admin_api/v1/report/build', json=json_data, headers=headers)
    return response.json()




def check_query_results(query_result):
    # check if query results have key "rows"
    if 'rows' in query_result:
        return True
    else:
        return False


def get_clicks_and_conversions(query_result):
    # get clicks and conversions from query result
    if check_query_results(query_result):
        clicks = query_result['rows'][0]['clicks']
        conversions = query_result['rows'][0]['conversions']
        if clicks is None:
            clicks = 0
        if conversions is None:
            conversions = 0
        return clicks, conversions
    else:
        return None, None


def get_result_to_display(query_result):
    # get clicks and conversions from query result
    if check_query_results(query_result):
        clicks, conversions = get_clicks_and_conversions(query_result)
        return f'clicks: {clicks}, conversions: {conversions}'
    else:
        return 'No results'

