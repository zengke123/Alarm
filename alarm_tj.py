#!/usr/bin/env python
from TxtParse import parseHtml
from collections import Counter

def get_alarm(df):

    '''
    获取当天出现的告警类别
    :return:去重后的告警码与告警标题 类型为字典
    '''

    alarm_codes = list(df["告警码"])
    alarm_titles = list(df["告警标题"])
    alarm_code_map = dict(zip(alarm_codes, alarm_titles))
    return alarm_codes, alarm_code_map

# 今日告警分析
def alarm_analyse(df):
    today_alarm_list, alarm_code_map = get_alarm(df)
    alarm_count = Counter(today_alarm_list)
    num = len(alarm_count.keys())
    data = []
    data.append(["告警码", "告警标题", "告警主机", "累计次数"])
    for k, v in alarm_count.most_common(num):
        hosts = df[df["告警码"].isin([k])]["主机名称"].drop_duplicates()
        host = " | ".join(hosts)
        data.append([str(k), alarm_code_map.get(k), host, str(v)])
    table_html = parseHtml(data, title="今日告警分析")
    return table_html

# 告警同比分析
def alarm_compare(today_df, yesterday_df):
    today_alarm_list, alarm_code_map = get_alarm(today_df)
    yesterday_alarm_list, yes_alarm_code_map = get_alarm(yesterday_df)
    # 减少告警、重复告警、新增告警
    today_alarm_set = set(today_alarm_list)
    yesterday_alarm_set = set(yesterday_alarm_list)
    # 分别找出最近2天相同的告警码，减少、增加的告警
    same_alarm = today_alarm_set & yesterday_alarm_set
    clear_alarm = yesterday_alarm_set - same_alarm
    add_alarm = today_alarm_set - same_alarm
    # 根据减少的告警码生成html表单
    clear_alarm_data = [["告警码", "告警标题", "告警主机", "累计次数"]]
    for i in clear_alarm:
        hosts = yesterday_df[yesterday_df["告警码"].isin([i])]["主机名称"].drop_duplicates()
        host = " | ".join(hosts)
        clear_alarm_data.append([str(i), yes_alarm_code_map.get(i), host, str(Counter(yesterday_alarm_list).get(i))])
    clear_alarm_html = parseHtml(clear_alarm_data, title="与昨天比较，今天减少告警")
    # 根据相同的告警码生成html表单
    same_alarm_data = [["告警码", "告警标题", "告警主机", "累计次数"]]
    for i in same_alarm:
        hosts = today_df[today_df["告警码"].isin([i])]["主机名称"].drop_duplicates()
        host = " | ".join(hosts)
        same_alarm_data.append([str(i), alarm_code_map.get(i), host, str(Counter(today_alarm_list).get(i))])
    same_alarm_html = parseHtml(same_alarm_data, title="与昨天比较，今天仍存在告警")
    # 根据新增的告警码生成html表单
    add_alarm_data = [["告警码", "告警标题", "告警主机", "累计次数"]]
    for i in add_alarm:
        hosts = today_df[today_df["告警码"].isin([i])]["主机名称"].drop_duplicates()
        host = " | ".join(hosts)
        add_alarm_data.append([str(i), alarm_code_map.get(i), host, str(Counter(today_alarm_list).get(i))])
    add_alarm_html = parseHtml(add_alarm_data, title="与昨天比较，今天新增告警")
    return clear_alarm_html, same_alarm_html, add_alarm_html