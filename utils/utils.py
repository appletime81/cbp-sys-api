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
