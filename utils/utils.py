import pandas as pd
from typing import List, Dict

TIME_FORMAT = "%Y-%m-%d %H:%M:%S"


def convert_time_to_str(datetime_data):
    return datetime_data.strftime(TIME_FORMAT)


def convert_url_condition_to_dict(url_condition):
    url_condition_dict = {}
    url_condition_list = url_condition.split("&")
    for url_condition in url_condition_list:
        url_condition = url_condition.split("=")
        url_condition_dict.update({url_condition[0]: url_condition[1]})
    return url_condition_dict


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
