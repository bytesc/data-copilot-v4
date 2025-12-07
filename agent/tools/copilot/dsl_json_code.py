from agent.tools.copilot.utils.read_db import execute_select

def get_data_info_prompt(engine, example=False, tables=None):
    df = execute_select(engine, "SHOW TABLES")
    data_prompt = """
Here is the structure of the data:
"""

    # 获取所有表结构
    table_descriptions = {}
    for table_row in df.to_dict('records'):
        table_name = table_row['Table']
        if tables is None or table_name in tables:
            desc_df = execute_select(engine, f"DESC {table_name}")
            table_descriptions[table_name] = desc_df.to_dict('records')

    # 构建表结构描述（表格格式）
    for table_name, fields in table_descriptions.items():
        data_prompt += f"desc {table_name};\n"
        data_prompt += "| Field | Type | Properties |\n"
        data_prompt += "|-------|------|------------|\n"
        for field in fields:
            field_name = field["Field"]
            field_type = field["Type"]
            properties = field.get("Properties", "")
            data_prompt += f"| {field_name} | {field_type} | {properties} |\n"
        data_prompt += "\n"

    if example:
        data_prompt += """
Here is data samples(just samples, do not mock any data):
"""
        # 添加示例数据
        for table_name in table_descriptions.keys():
            data_prompt += f"\n-- Sample data from {table_name} table:\n"
            sample_df = execute_select(engine, f"SELECT * FROM {table_name} LIMIT 3")

            # 构建表头
            columns = sample_df.columns.tolist()
            data_prompt += "| " + " | ".join(columns) + " |\n"
            data_prompt += "|" + "|".join(["---" for _ in columns]) + "|\n"

            # 构建数据行
            for _, row in sample_df.iterrows():
                data_prompt += "| " + " | ".join(str(cell) for cell in row) + " |\n"
            data_prompt += "\n"

    return data_prompt
