import pandas as pd
import requests
import json


def search_manticore_simple(query_json):
    """Execute search query against Manticore Search endpoint"""
    url = "http://localhost:9308/search"

    headers = {
        "Content-Type": "application/json"
    }

    print("#####################query######################")
    print(query_json)
    try:
        response = requests.post(url, json=query_json, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return None


def query_data_func(json_string: str):
    error_flag = False
    total_count = 0

    try:
        # Parse the input JSON string
        query_dict = json.loads(json_string)

        # 添加或替换limit和options字段
        query_dict['limit'] = 10000000
        query_dict['options'] = {
            'max_matches': 10000000  # 提高最大匹配数
        }

        result = search_manticore_simple(query_dict)

        if result is None:
            error_flag = True
            return pd.DataFrame(), total_count, error_flag

        # 获取总记录数
        if 'hits' in result and 'total' in result['hits']:
            total_count = result['hits']['total']
            # 处理不同版本的Manticore返回格式
            if isinstance(total_count, dict) and 'value' in total_count:
                total_count = total_count['value']

        if 'hits' in result and 'hits' in result['hits']:
            hits = result['hits']['hits']
            if hits:
                data = [hit['_source'] for hit in hits]
                df = pd.DataFrame(data)
                return df, total_count, error_flag
            else:
                print("No matching results found")
                return pd.DataFrame(), total_count, error_flag
        else:
            print("Unexpected result structure, attempting direct conversion...")
            df = pd.DataFrame(result) if result else pd.DataFrame()
            return df, total_count, error_flag

    except json.JSONDecodeError as e:
        error_flag = True
        error_message = f"JSON decode error: {e}"
        print(error_message)
        return pd.DataFrame(), total_count, error_flag
    except Exception as e:
        error_flag = True
        error_message = f"Error processing data: {e}"
        print(error_message)
        return pd.DataFrame(), total_count, error_flag