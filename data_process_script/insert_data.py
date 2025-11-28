from data_access.read_db import execute_sql, execute_select
from data_access.db_conn import engine
import pandas as pd
import numpy as np
from sqlalchemy import create_engine, MetaData, Table, Column, text, inspect
from sqlalchemy.types import VARCHAR, Integer, Float, DateTime, Boolean, Text
from datetime import datetime

# 读取CSV文件
csv_file_path = 'D:\IDLE\projects\med-data\source-data\data_composition\labels_brset.csv'

# 读取CSV时尝试推断更好的数据类型
df = pd.read_csv(csv_file_path)

# 定义数据库表的名称
table_name = 'brset'

# 首先检查表是否已存在
inspector = inspect(engine)
if inspector.has_table(table_name):
    # 如果表已存在，先删除它
    with engine.connect() as conn:
        conn.execute(text(f"DROP TABLE IF EXISTS `{table_name}`"))
        conn.commit()
    print(f"Existing table '{table_name}' dropped.")


# 创建类型映射函数
def pandas_type_to_sqlalchemy(dtype, max_length=None):
    if pd.api.types.is_integer_dtype(dtype):
        return Integer()
    elif pd.api.types.is_float_dtype(dtype):
        return Float()
    elif pd.api.types.is_datetime64_any_dtype(dtype):
        return DateTime()
    elif pd.api.types.is_bool_dtype(dtype):
        return Boolean()
    else:
        # 对于字符串类型，计算最大长度
        if max_length is not None and max_length > 255:
            return Text() if max_length > 4000 else VARCHAR(max_length)
        else:
            return VARCHAR(255)

column_types = {}
for col in df.columns:
    col_data = df[col]

    # 处理缺失值
    col_data_not_null = col_data.dropna()

    if len(col_data_not_null) == 0:
        # 如果全是空值，默认使用VARCHAR(255)
        column_types[col] = VARCHAR(255)
        continue

    # 计算字符串列的最大长度
    max_length = None
    if col_data.dtype == 'object':
        try:
            max_length = int(col_data_not_null.astype(str).str.len().max())
            # 增加一些缓冲空间
            max_length = min(max_length * 2, 8000)  # 限制最大长度
        except:
            max_length = 255

    # 获取适当的SQL类型
    column_types[col] = pandas_type_to_sqlalchemy(col_data.dtype, max_length)

# 使用pandas直接创建表并插入数据
try:
    df.to_sql(
        name=table_name,
        con=engine,
        index=False,
        dtype=column_types
    )
    print(f"Successfully created table '{table_name}' and inserted {len(df)} records.")

except Exception as e:
    print(f"Error using to_sql: {e}")
    print("Trying alternative approach...")

    # 备用方法：使用SQLAlchemy Core创建表
    metadata = MetaData()

    # 定义表结构
    table = Table(
        table_name,
        metadata,
        *[Column(col, column_types[col]) for col in df.columns]
    )

    # 创建表
    metadata.create_all(engine)
    print(f"Table '{table_name}' created successfully with optimized data types.")

    # 插入数据
    df.to_sql(
        name=table_name,
        con=engine,
        if_exists='append',
        index=False,
        dtype=column_types
    )
    print(f"Successfully inserted {len(df)} records into {table_name}")
