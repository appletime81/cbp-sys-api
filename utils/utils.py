import pandas as pd
from typing import List, Dict

TIME_FORMAT = "%Y-%m-%d %H:%M:%S"


def convert_time_to_str(datetime_data):
    return datetime_data.strftime(TIME_FORMAT)


def convert_url_condition_to_dict(url_condition):
    dict_condition = {}
    list_ = url_condition.split("&")
    for sub_condition in list_:
        key, value = sub_condition.split("=")
        if "start" in key:
            key = key.replace("start", "range")
            # covert YYYYMMDDHHMMSS to YYYY-MM-DD HH:MM:SS
            value = (
                value[:4]
                + "-"
                + value[4:6]
                + "-"
                + value[6:8]
                + " "
                + value[8:10]
                + ":"
                + value[10:12]
                + ":"
                + value[12:]
            )
            dict_condition[key] = {"gte": value}
        elif "end" in key:
            key = key.replace("end", "range")
            # covert YYYYMMDDHHMMSS to YYYY-MM-DD HH:MM:SS
            value = (
                value[:4]
                + "-"
                + value[4:6]
                + "-"
                + value[6:8]
                + " "
                + value[8:10]
                + ":"
                + value[10:12]
                + ":"
                + value[12:]
            )
            dict_condition[key].update({"lte": value})
        elif "equal" in key:
            # covert YYYYMMDDHHMMSS to YYYY-MM-DD HH:MM:SS
            value = (
                value[:4]
                + "-"
                + value[4:6]
                + "-"
                + value[6:8]
                + " "
                + value[8:10]
                + ":"
                + value[10:12]
                + ":"
                + value[12:]
            )
            dict_condition[key] = value
        else:
            dict_condition[key] = value

    return dict_condition


def convert_dict_to_sql_condition(dict_condition: Dict, table_name: str):
    sql_condition = ""
    for key, value in dict_condition.items():
        if "range" in key:
            date_column_name = key.replace("range", "")
            start_date = value["gte"]
            end_date = value["lte"]
            sql_condition += (
                f" {date_column_name} BETWEEN '{start_date}' AND '{end_date}' AND"
            )
        elif "equal" in key:
            date_column_name = key.replace("equal", "")
            date = value
            sql_condition += f" {date_column_name} = '{date}' AND"
        else:
            sql_condition += f" {key} = '{value}' AND"
    if sql_condition.endswith("AND"):
        sql_condition = sql_condition[1:-4]

    sql_condition = f"SELECT * FROM {table_name} WHERE {sql_condition};"
    return sql_condition


def convert_dict_condition_to_url(dict_condition):
    url_condition = ""
    for key, value in dict_condition.items():
        url_condition += f"{key}={value}&"
    return url_condition[:-1]


def cal_fee_amount_post(ratio: float, fee_amount_pre: float):
    fee_amount_post = float(format(fee_amount_pre * ratio / 100, ".2f"))
    return fee_amount_post


def dflist_to_df(list_data: List[pd.DataFrame]):
    df = pd.concat(list_data, axis=0, ignore_index=True)
    df = df.drop(columns=["_sa_instance_state"])
    return df
