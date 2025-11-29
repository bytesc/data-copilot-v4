import requests
import json


def search_manticore_simple(query_json):
    """
    向Manticore Search发送简单查询请求
    """
    url = "http://localhost:9308/search"

    headers = {
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, json=query_json, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"请求错误: {e}")
        return None


# 示例1: 简单全文搜索
def search_by_keyword(keyword):
    """根据关键词搜索"""
    query = {
        "table": "brset",
        "query": {
            "match": {"_all": keyword}
        },
        "limit": 10
    }

    result = search_manticore_simple(query)
    return result


# 示例2: 按年龄范围搜索
def search_by_age(min_age, max_age):
    """按年龄范围搜索"""
    query = {
        "table": "brset",
        "query": {
            "range": {"patient_age": {"gte": min_age, "lte": max_age}}
        },
        "limit": 10
    }

    result = search_manticore_simple(query)
    return result


# 示例3: 组合条件搜索
def search_combined(age_min, dr_level):
    """组合条件搜索：年龄+糖尿病视网膜病变等级"""
    query = {
        "table": "brset",
        "query": {
            "bool": {
                "must": [
                    {"range": {"patient_age": {"gte": age_min}}},
                    {"equals": {"diabetic_retinopathy": dr_level}}
                ]
            }
        },
        "limit": 10
    }

    result = search_manticore_simple(query)
    return result


# 显示结果
def show_results(result, title):
    """简单显示结果"""
    print(f"\n=== {title} ===")

    if not result or 'hits' not in result:
        print("没有找到结果")
        return

    hits = result['hits']['hits']
    total = result['hits']['total']

    print(f"找到 {total} 条记录")

    for i, hit in enumerate(hits, 1):
        source = hit['_source']
        print(f"{i}. 图像: {source.get('image_id', 'N/A')}, "
              f"年龄: {source.get('patient_age', 'N/A')}, "
              f"糖尿病等级: {source.get('diabetic_retinopathy', 'N/A')}")


def search_test():
    """组合条件搜索：年龄+糖尿病视网膜病变等级"""
    query = {
        'table': 'brset',
        'query': {'match': {"'diabetic_retinopathy'": 0}},
        'fields': ['patient_sex'],
        'limit': 100000,
        'options': {
            'max_matches': 1000000  # 提高最大匹配数
        }
    }
    result = search_manticore_simple(query)
    return result


# 主函数
if __name__ == "__main__":
    print("Manticore Search 简单查询示例")

    # # 1. 关键词搜索
    # result1 = search_by_keyword("diabetes")
    # show_results(result1, "关键词'diabetes'搜索结果")
    #
    # # 2. 年龄范围搜索
    # result2 = search_by_age(40, 60)
    # show_results(result2, "年龄40-60岁患者")
    #
    # # 3. 组合条件搜索
    # result3 = search_combined(50, 2)
    # show_results(result3, "50岁以上且糖尿病视网膜病变等级2")

    result4 = search_test()
    show_results(result4, "last")