import pandas as pd
from typing import List, Dict

TIME_FORMAT = "%Y-%m-%d %H:%M:%S"


def convert_time_to_str(datetime_data):
    return datetime_data.strftime(TIME_FORMAT)


def convert_dict_data_date_to_normal_str(dict_data: Dict):
    for key, value in dict_data.items():
        if "Date" in key:
            dict_data[key] = convert_time_to_str(value)
    return dict_data


def convert_url_condition_to_dict(url_condition):
    dict_condition = {}
    list_ = url_condition.split("&")
    for sub_condition in list_:
        key, value = sub_condition.split("=")
        if "start" in key:
            key = key.replace("start", "range")
            # covert YYYYMMDDHHMMSS to YYYY-MM-DD HH:MM:SS
            value = value[:4] + "-" + value[4:6] + "-" + value[6:8] + " " + "00:00:00"
            dict_condition[key] = {"gte": value}
        elif "end" in key:
            key = key.replace("end", "range")
            # covert YYYYMMDDHHMMSS to YYYY-MM-DD HH:MM:SS
            value = value[:4] + "-" + value[4:6] + "-" + value[6:8] + " " + "00:00:00"
            dict_condition[key].update({"lte": value})
        else:
            dict_condition[key] = value

    return dict_condition


def convert_url_condition_to_dict_ignore_date(url_condition):
    dict_condition = {}
    list_ = url_condition.split("&")
    for sub_condition in list_:
        key, value = sub_condition.split("=")
        dict_condition[key] = value
    return dict_condition


def convert_dict_to_sql_condition(dict_condition: Dict, table_name: str):
    sql_condition = ""
    for key, value in dict_condition.items():
        if "range" in key:
            date_column_name = key.replace("range", "")
            start_date = value["gte"]
            end_date = value["lte"]
            if start_date == end_date:
                end_date = end_date.replace("00:00:00", "23:59:59")
            sql_condition += (
                f" {date_column_name} BETWEEN '{start_date}' AND '{end_date}' AND"
            )
        else:
            sql_condition += f" {key} = '{value}' AND"
    if sql_condition.endswith("AND"):
        sql_condition = sql_condition[1:-4]

    sql_condition = f"SELECT * FROM {table_name} WHERE {sql_condition};"
    return sql_condition


def convert_dict_with_date_to_range_format(dict_condition: Dict):
    new_dict_condition = {}
    for key, value in dict_condition.items():
        if key.startswith("start"):
            newKey = key.replace("start", "range")
            if newKey not in new_dict_condition:
                new_dict_condition[newKey] = {}
            new_dict_condition[newKey]["gte"] = (
                value[:4] + "-" + value[4:6] + "-" + value[6:8] + " " + "00:00:00"
            )
        elif key.startswith("end"):
            newKey = key.replace("end", "range")
            if newKey not in new_dict_condition:
                new_dict_condition[newKey] = {}
            new_dict_condition[newKey]["lte"] = (
                value[:4] + "-" + value[4:6] + "-" + value[6:8] + " " + "00:00:00"
            )
        else:
            new_dict_condition[key] = value
    return new_dict_condition


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
    return df


# if __name__ == "__main__":
#     dict_ = convert_url_condition_to_dict(
#         "SupplierName=供應商&SubmarineCable=海纜名稱&PartyName=會員代號&Status=處理狀態&BillMilestone=計帳段號&startCreateDate=20230101&endCreateDate=20230131"
#     )
#     sql = convert_dict_to_sql_condition(dict_, "TABLE")
#     print(sql)
