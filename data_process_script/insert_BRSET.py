
# from data_access.db_conn import engine
import pandas as pd
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import create_engine, text, TEXT

engine = create_engine("mysql+pymysql://root:@localhost:9306/Manticore")

def execute_sql(sql):
    # 使用连接执行SQL语句
    with engine.connect() as connection:
        try:
            # 执行SQL语句
            result = connection.execute(text(sql))
            # 提交事务（对于INSERT、UPDATE、DELETE等操作）
            connection.commit()
            # 返回影响的行数
            return result.rowcount
        except SQLAlchemyError as e:
            # 如果发生错误，回滚事务
            connection.rollback()
            # 打印错误信息
            print(f"An error occurred: {e}")
            return e

# 读取CSV文件
csv_file_path = 'D:\IDLE\projects\med-data\source-data\labels_brset.csv'

"""
CREATE TABLE `brset` (
  `image_id` text,
  `patient_id` int,
  `camera` text,
  `patient_age` float,
  `comorbidities` text,
  `diabetes_time_y` text,
  `insuline` text,
  `patient_sex` int,
  `exam_eye` int,
  `diabetes` text,
  `nationality` text,
  `optic_disc` text,
  `vessels` int,
  `macula` int,
  `DR_SDRG` int,
  `DR_ICDR` int,
  `focus` int,
  `Illuminaton` int,
  `image_field` int,
  `artifacts` int,
  `diabetic_retinopathy` int,
  `macular_edema` int,
  `scar` int,
  `nevus` int,
  `amd` int,
  `vascular_occlusion` int,
  `hypertensive_retinopathy` int,
  `drusens` int,
  `hemorrhage` int,
  `retinal_detachment` int,
  `myopic_fundus` int,
  `increased_cup_disc` int,
  `other` int,
  `quality` text
);
"""

df = pd.read_csv(csv_file_path)

# 定义数值型列（根据你的表结构）
numeric_columns = [
    'patient_id', 'patient_age', 'patient_sex', 'exam_eye', 'vessels',
    'macula', 'DR_SDRG', 'DR_ICDR', 'focus', 'Illuminaton', 'image_field',
    'artifacts', 'diabetic_retinopathy', 'macular_edema', 'scar', 'nevus',
    'amd', 'vascular_occlusion', 'hypertensive_retinopathy', 'drusens',
    'hemorrhage', 'retinal_detachment', 'myopic_fundus', 'increased_cup_disc', 'other'
]

# 处理null值：数值列用0替换，文本列用空字符串替换
for col in df.columns:
    if col in numeric_columns:
        df[col] = df[col].fillna(0)
    else:
        df[col] = df[col].fillna('')

# 构建INSERT语句
table_name = 'brset'
columns = df.columns.tolist()

# 生成INSERT语句
sql = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES\n"

# 构建值部分
values_list = []
for _, row in df.iterrows():
    row_values = []
    for value in row:
        if isinstance(value, (int, float)):
            row_values.append(str(value))
        else:
            # 转义单引号
            escaped_value = str(value).replace("'", "''")
            row_values.append(f"'{escaped_value}'")

    values_list.append("(" + ", ".join(row_values) + ")")

sql += ",\n".join(values_list) + ";"

# 执行SQL
print("开始执行SQL插入...")
row_count = execute_sql(sql)
print(f"插入完成，影响行数: {row_count}")






