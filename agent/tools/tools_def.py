import json

import pandas as pd
import sqlalchemy

from agent.utils.get_config import config_data
from agent.utils.llm_access.LLM import get_llm
from .copilot.data_explanation import get_llm_data_explanation_func
from .copilot.utils.dsl_search import query_data_func
from .copilot.utils.read_db import execute_select
from .data_trans.download_csv_to_pd import download_csv_to_dataframe, extract_csv_filename_from_url, read_csv_from_local

DATABASE_URL = config_data['mysql']
engine = sqlalchemy.create_engine(DATABASE_URL)

STATIC_URL = config_data['static_path']

llm = get_llm()

from .copilot.sql_code import query_database_func
from .copilot.python_code import draw_graph_func, draw_compare_graph_func


def query_database(question: str, df_cols: str | list = None) -> pd.DataFrame:
    """
    query_database(question: str, df_cols: str | list = None) -> pd.DataFrame:
    Query the database using natural language question. Can not query anything not included in the database content!!!
    Returns the query results in pandas DataFrame.

    Args:
    - question (str): Natural language question, table names can be included in the question.
    - df_cols (str|list): The columns' names of the DataFrame(e.g. "uid, username, stu_num").

    Returns:
    - pd.DataFrame: A DataFrame containing the results of the database query.
        The DataFrame includes the columns provided in df_cols(the second args)
    returns None in case of error

    Example:
    ```python
        ans_df = query_database('Select the grades of Jane Smith, use table stu_grade ,stu_info, class_info', df_cols='lesson_id, lesson_name, grade')
        # Output(pd.DataFrame):
        #        lesson_id lesson_name grade
        # 0        001  Mathematics     99.00
        # 1        002      English     88.50
        # 2        003     Physics    65.00
        # ... and so on(the structure of the output DataFrame id based on df_cols(the second input args))
    ```
    """

    result = query_database_func(question, df_cols, llm, engine)
    return result


def draw_graph(question: str, data: pd.DataFrame, col_explanation: str = None) -> str:
    """
    draw_graph(question: str, data: pd.DataFrame, col_explanation: str = None) -> str:
    Draw graph based on natural language graph description and data provided in a pandas DataFrame.
    Returns an url path string of the graph.

    Args:
    - question (str): Natural language graph type and other requirements.
    - data (pd.DataFrame): A pandas DataFrame for providing drawing data.
    - col_explanation (str, optional): Natural language to describe the meanings of columns.

    Returns:
    - str: url path string of the output graph.(e.g. "http://127.0.0.1:8003/tmp_imgs/mlkjcvep.png").
    returns None in case of error

    Example:
    ```python
        data = pd.DataFrame({
            '月份': ['1月', '2月', '3月', '4月', '5月'],
            '销售额': [200, 220, 250, 210, 230]
        })
        graph_url = draw_graph("draw line graph, use red line", data)
        # Output(str):
        # "http://127.0.0.1:8003/tmp_imgs/ekhidpcl.png"

        data = pd.DataFrame({
            'Gender': [1, 2, 3],
            'Sales Percentage': [35, 45, 20]
        })
        graph_url = draw_graph("draw pie chart", data, "Gender: 1 means male, 2 means female, 3 means not known;")
        # Output(str):
        # "http://127.0.0.1:8003/tmp_imgs/ewcdkdkl.png"

        data = pd.DataFrame({
            'Month': ['January', 'February', 'March', 'April', 'May', 'June'],
            'Sales Revenue (USD)': [12000, 15000, 18000, 13500, 16500, 19500]
        })
        graph_url = draw_graph("draw bar chart, use different color for each bar", data)
        # Output(str):
        # "http://127.0.0.1:8003/tmp_imgs/glddvysc.png"
    ```
    """
    result = draw_graph_func(question, data, llm, col_explanation)
    result = STATIC_URL + result[2:]
    return result


def draw_compare_graph(question: str, data_dict: dict, col_explanation: str = None) -> str:
    """
    draw_compare_graph(question: str, data_dict: dict, col_explanation: str = None) -> str:
    Draw graph to compare something based on natural language graph description and data provided in a dictionary of pandas DataFrames.
    Returns an url path string of the graph.

    Args:
    - question (str): Natural language graph type and other requirements.
    - data_dict (dict): A dictionary with string keys and pandas DataFrame values for providing drawing data. The key can only be a string and the value can only be a pandas DataFrame.
    - col_explanation (str, optional): Natural language to describe the meanings of columns.

    Returns:
    - str: url path string of the output graph.(e.g. "http://127.0.0.1:8003/tmp_imgs/mlkjcvep.png").
    returns None in case of error

    Example:
    ```python
        data_dict = {
            'sales_data': pd.DataFrame({
                '月份': ['1月', '2月', '3月', '4月', '5月'],
                '销售额': [200, 220, 250, 210, 230]
            }),
            'inventory_data': pd.DataFrame({
                '月份': ['1月', '2月', '3月', '4月', '5月'],
                '库存量': [100, 90, 80, 95, 85]
            })
        }
        graph_url = draw_compare_graph("draw line graph", data_dict)
        # Output(str):
        # "http://127.0.0.1:8003/tmp_imgs/ekhidpcl.png"

        data_dict = {
            'group A': pd.DataFrame({
                'Gender': [1, 2, 3],
                'Sales Percentage': [35, 45, 20]
            }),
            'group B': pd.DataFrame({
                'Gender': [1, 2, 3],
                'Sales Percentage': [31, 59, 3]
            })
        }
        graph_url = draw_compare_graph("draw pie chart", data_dict, "use blend bar layers to compare two groups. Gender: 1 means male, 2 means female, 3 means not known;")
        # Output(str):
        # "http://127.0.0.1:8003/tmp_imgs/ewcdkdkl.png"

        data_dict = {
            'monthly_sales': pd.DataFrame({
                'Month': ['January', 'February', 'March', 'April', 'May', 'June'],
                'Sales Revenue (USD)': [12000, 15000, 18000, 13500, 16500, 19500]
            })
        }
        graph_url = draw_compare_graph("draw bar chart, use different color for each bar", data_dict)
        # Output(str):
        # "http://127.0.0.1:8003/tmp_imgs/glddvysc.png"
    ```
    """
    result = draw_compare_graph_func(question, data_dict, llm, col_explanation)
    result = STATIC_URL + result[2:]
    return result


def explain_data(question: str, data: pd.DataFrame, col_explanation: str = None) -> str:
    """
    explain_data(question: str, data: pd.DataFrame, col_explanation: str = None) -> str:
    Explain the data provided in a pandas DataFrame based on a natural language question. This function must be used after important dataframe assigned.
    Returns a str of natural language data analysis.

    Args:
    - question (str): Natural language question.
    - data (pd.DataFrame): A pandas DataFrame for analysis.
    - col_explanation (str, optional): Natural language to describe the meanings of columns.

    Returns:
    - str: Explanation of data

    Example:
    ```python
        data = pd.DataFrame({
            'month': ['1', '2', '3', '4', '5'],
            'sales': [200, 220, 250, 210, 230]
        })
        data_description = explain_data("how is the sales condition?", data, "month: 1 means Jan and so forth")
        # Output(str):
        # "Based on the data..."
    ```
    """
    ans = get_llm_data_explanation_func(question, data, llm, col_explanation)
    return ans


def exe_sql(sql: str) -> pd.DataFrame:
    """
    exe_sql(sql: str) -> pd.DataFrame:
    Execute the sql query string.
    Returns the query results in pandas DataFrame.

    Args:
    - sql (str): query string.

    Returns:
    - pd.DataFrame: A DataFrame containing the results of the database query.
    returns None in case of error

    Example:
    ```python
        ans_df = exe_sql('SELECT lesson_id, lesson_name, grade FROM lessons WHERE grade > 90')
        # Output(pd.DataFrame):
        #        lesson_id lesson_name grade
        # 0        001  Mathematics     99.00
        # 1        002      English     95.50
        # 2        005     Chemistry     92.00
        # ... and so on
        ```
    """
    ans = execute_select(engine, sql)
    return ans


def load_data(url: str) -> pd.DataFrame:
    """
    load_data(url: str) -> pd.DataFrame:
    Load data form a CSV file url
    Returns the result in a pandas DataFrame.

    Args:
    - url (str): url string(e.g. http://127.0.0.1:8009/tmp_imgs/imqtzywu.csv).

    Returns:
    - pd.DataFrame: A DataFrame containing the data in the CSV file.
    returns None in case of error

    Example:
    ```python
        ans_df = load_data("http://127.0.0.1:8009/tmp_imgs/xjfsutvp.csv")
    ```
    """
    file_name = extract_csv_filename_from_url(url)
    df = read_csv_from_local("./tmp_imgs/"+file_name)
    return df


def query_data(json_string: str) -> tuple[pd.DataFrame, int, bool]:
    """
    query_data(json_string: str) -> tuple[pd.DataFrame, int, bool]:
    Query data from Manticore Search (elasticsearch like grammar) with json string
    return results as a pandas DataFrame, total number of search results, and error flag.

    Args:
        json_string (str): JSON string containing the search query parameters

    Returns:
        tuple[pd.DataFrame, int, bool]:
            - DataFrame containing the search results
            - Total number of matches
            - Boolean indicating if an error occurred (True = error, False = success)
            Returns empty DataFrame, 0, and True if error occurs.

    Examples:
        # Example 1: Successful query
        query_json = '''
        {
            "table": "brset",
            "query": {
                "match": {"'_all'": "diabetes"}
            },
            "limit": 3
        }
        '''
        df, total_count, error = query_data(query_json)
        # Output:
        # df (pd.DataFrame):
        #   patient_id diagnosis         patient_age diabetic_retinopathy
        # 0      P001  diabetes               45                   2
        # 1      P003  diabetes type 2         52                   1
        # 2      P007  prediabetes             58                   0
        # total_count: 15
        # error: False

        # Example 2: Range query
        query_json = '''
        {
            "table": "brset",
            "query": {
                "range": {"'patient_age'": {"gte": 40, "lte": 60}}
            },
            "limit": 2
        }
        '''
        df, total_count, error = query_data(query_json)
        # Output:
        # df (pd.DataFrame):
        #   patient_id diagnosis patient_age diabetic_retinopathy
        # 0      P001  diabetes          45                   2
        # 1      P003  hypertension      52                   0
        # total_count: 42
        # error: False

        # Example 3: Error case (invalid table name)
        query_json = '''
        {
            "table": "nonexistent_table",
            "query": {
                "match": {"'diagnosis'": "diabetes"}
            }
        }
        '''
        df, total_count, error = query_data(query_json)
        # Output:
        # df (pd.DataFrame): Empty DataFrame
        # total_count: 0
        # error: True

        # Example 4: Empty result (not an error)
        query_json = '''
        {
            "table": "brset",
            "query": {
                "match": {"'diagnosis'": "nonexistent_condition"}
            }
        }
        '''
        df, total_count, error = query_data(query_json)
        # Output:
        # df (pd.DataFrame): Empty DataFrame
        # total_count: 0
        # error: False

    Important Note:
        When specifying field names in the query, make sure to properly quote field names
        that contain special characters. For example:

        Wrong: {'match': {'diabetic_retinopathy': 1}}
        Correct: {'match': {"'diabetic_retinopathy'": 1}}

        Field names with underscores or other special characters need to be enclosed in quotes.
    """
    ans, count, err_flag = query_data_func(json_string)
    return ans, count, err_flag

