from .tools.copilot.sql_code import get_db_info_prompt
from .tools.copilot.utils import call_llm_test
from .tools.copilot.utils.parse_output import parse_generated_sql_code
from .tools.copilot.utils.read_db import execute_sql, execute_sql_2
from .tools.tools_def import engine, llm

def get_llm_data_comment_func(txt, table):
    print("##############doc")
    print(txt)
    data_str = get_db_info_prompt(engine, simple=True, example=False, tables=[table])

    pre_prompt = """
Please write sql code to add table and colum comments to the table.
Here is the document:
"""

    data_prompt = """
Here is the table structure: 
""" + data_str

    end_prompt = """
Remind:
1. All code should be completed in a single markdown code block without any comments, explanations or cmds.

"""

    final_prompt = pre_prompt + txt + "\n" + data_prompt + "\n" + end_prompt
    ans = call_llm_test.call_llm(final_prompt, llm)
    print("##############sql")
    print(ans.content)
    result_sql = parse_generated_sql_code(ans.content)
    if result_sql is None:
        error_msg = """
    code should only be in a md code block: 
    ```sql
    # some sql code
    ```
    without any additional comments, explanations or cmds !!!
    """
        print(ans + "No code was generated.")

    return result_sql

def get_llm_data_comment(extracted_text, table_name):
    sql = get_llm_data_comment_func(extracted_text, table_name)
    execute_sql_2(engine, sql)
    return True
