import pandas as pd

from agent.utils.pd_to_walker import generate_random_string, STATIC_URL


def pd_to_csv(df: pd.DataFrame):
    file_path = "./tmp_imgs/" + generate_random_string(8)+".csv"
    df.to_csv(file_path, index=False)
    return STATIC_URL + file_path[2:]
